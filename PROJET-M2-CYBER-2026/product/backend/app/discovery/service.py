"""Discovery service for network scanning using nmap."""

import subprocess
import xml.etree.ElementTree as ET
import ipaddress
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.port_finding import PortFinding
from app.config import settings

# Ports courants pour le scan
COMMON_PORTS = "22,80,443,3306,5432,8080,8443,21,25,53,110,143,993,995,3389,5900"


def _is_lab_network(ip_range: str) -> bool:
    """Vérifier que l'IP range est dans le réseau lab autorisé."""
    # Réseaux lab Docker typiques
    lab_networks = [
        ipaddress.ip_network("172.16.0.0/12"),
        ipaddress.ip_network("192.168.0.0/16"),
        ipaddress.ip_network("10.0.0.0/8"),
    ]
    try:
        network = ipaddress.ip_network(ip_range, strict=False)
    except ValueError:
        return False
    
    # Vérifier que le réseau est un sous-réseau d'un réseau lab
    return any(network.subnet_of(lab) for lab in lab_networks)


def _parse_nmap_xml(xml_output: str) -> list[dict]:
    """Parser la sortie XML de nmap pour extraire les hosts et ports."""
    hosts = []
    try:
        root = ET.fromstring(xml_output)
    except ET.ParseError:
        return hosts
    
    for host_elem in root.findall("host"):
        # IP address
        addr_elem = host_elem.find("addresses/address")
        if addr_elem is None or addr_elem.get("addrtype") != "ipv4":
            continue
        ip = addr_elem.get("addr", "unknown")
        
        # Hostname
        hostname_elem = host_elem.find("hostnames/hostname")
        hostname = hostname_elem.get("name", f"host-{ip.replace('.', '-')}") if hostname_elem is not None else f"host-{ip.replace('.', '-')}"
        
        # OS detection
        os_match = host_elem.find("os/osmatch")
        os_name = os_match.get("name", "Unknown") if os_match is not None else "Unknown"
        
        # Status
        status_elem = host_elem.find("status")
        host_status = status_elem.get("state", "unknown") if status_elem is not None else "unknown"
        
        if host_status != "up":
            continue
        
        # Ports
        ports = []
        ports_elem = host_elem.find("ports")
        if ports_elem is not None:
            for port_elem in ports_elem.findall("port"):
                state_elem = port_elem.find("state")
                if state_elem is None or state_elem.get("state") != "open":
                    continue
                
                port_id = port_elem.get("portid")
                protocol = port_elem.get("protocol", "tcp")
                service_elem = port_elem.find("service")
                service_name = service_elem.get("name", "unknown") if service_elem is not None else "unknown"
                service_version = ""
                if service_elem is not None:
                    ver = service_elem.get("version", "")
                    prod = service_elem.get("product", "")
                    service_version = f"{prod} {ver}".strip()
                
                ports.append({
                    "port": int(port_id),
                    "protocol": protocol,
                    "service_name": service_name,
                    "service_version": service_version,
                    "state": "open",
                })
        
        hosts.append({
            "ip": ip,
            "hostname": hostname,
            "os_name": os_name,
            "ports": ports,
        })
    
    return hosts


def scan_ip_range(ip_range: str, db: Session, timeout: int = None) -> list[Asset]:
    """
    Scan an IP range using nmap ping scan and discover assets.
    
    Uses: nmap -sn -oX - <ip_range>
    
    Args:
        ip_range: CIDR notation (e.g. "192.168.1.0/24")
        db: Database session
        timeout: Max seconds for nmap to run (uses settings.NMAP_TIMEOUT if None)
    
    Returns:
        List of discovered Asset instances
    
    Raises:
        ValueError: If the IP range is not in the lab network
    """
    if timeout is None:
        timeout = settings.NMAP_TIMEOUT
    
    # First validate IP range format
    try:
        network = ipaddress.ip_network(ip_range, strict=False)
    except ValueError as exc:
        raise ValueError(f"Invalid IP range format: {ip_range}") from exc
    
    # Security: only allow lab networks (check after format validation)
    if not _is_lab_network(ip_range):
        raise ValueError(
            f"IP range {ip_range} is outside allowed lab networks. "
            "Only private networks (10.x, 172.16-31.x, 192.168.x) are allowed."
        )
    
    # Cap to /24 max for safety (use config value)
    if network.prefixlen < settings.NMAP_MAX_NETWORK_SIZE:
        raise ValueError(f"IP range too large. Maximum /{settings.NMAP_MAX_NETWORK_SIZE} network allowed.")
    
    # Run nmap ping scan
    try:
        result = subprocess.run(
            ["nmap", "-sn", "-oX", "-", ip_range],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        xml_output = result.stdout
    except subprocess.TimeoutExpired:
        raise ValueError(f"Scan timed out after {timeout} seconds")
    except FileNotFoundError:
        raise ValueError("nmap is not installed. Install it: apt-get install nmap")
    except Exception as exc:
        raise ValueError(f"nmap scan failed: {exc}")
    
    # Parse results
    hosts = _parse_nmap_xml(xml_output)
    
    discovered_assets: list[Asset] = []
    
    for host in hosts:
        ip_str = host["ip"]
        
        # Skip if already exists
        existing = db.query(Asset).filter(Asset.ip_address == ip_str).first()
        if existing:
            discovered_assets.append(existing)
            continue
        
        # Determine asset type from OS
        os_name = host["os_name"].lower()
        if "windows" in os_name:
            asset_type = "server"
            os_type = "Windows"
        elif "linux" in os_name:
            asset_type = "server"
            os_type = "Linux"
        else:
            asset_type = "network_device"
            os_type = "Unknown"
        
        asset = Asset(
            hostname=host["hostname"],
            ip_address=ip_str,
            asset_type=asset_type,
            os_type=os_type,
            os_version=host["os_name"],
            status="active",
        )
        db.add(asset)
        db.flush()
        discovered_assets.append(asset)
    
    db.commit()
    
    for asset in discovered_assets:
        db.refresh(asset)
    
    return discovered_assets


def scan_ports(asset_id: int, db: Session, timeout: int = None) -> list[PortFinding]:
    """
    Scan ports on a specific asset using nmap.
    
    Uses: nmap -sT -p <ports> -oX - <ip>
    
    Args:
        asset_id: ID of the asset to scan
        db: Database session
        timeout: Max seconds for nmap to run (uses settings.NMAP_TIMEOUT if None)
    
    Returns:
        List of PortFinding instances
    
    Raises:
        ValueError: If the asset does not exist
    """
    if timeout is None:
        timeout = settings.NMAP_TIMEOUT
    
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise ValueError(f"Asset with ID {asset_id} not found")
    
    # Delete previous findings
    db.query(PortFinding).filter(PortFinding.asset_id == asset_id).delete()
    db.flush()
    
    # Run nmap port scan
    try:
        result = subprocess.run(
            ["nmap", "-sT", "-p", COMMON_PORTS, "-oX", "-", asset.ip_address],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        xml_output = result.stdout
    except subprocess.TimeoutExpired:
        raise ValueError(f"Port scan timed out after {timeout} seconds")
    except FileNotFoundError:
        raise ValueError("nmap is not installed. Install it: apt-get install nmap")
    except Exception as exc:
        raise ValueError(f"Port scan failed: {exc}")
    
    # Parse results
    hosts = _parse_nmap_xml(xml_output)
    
    findings: list[PortFinding] = []
    
    if hosts:
        host = hosts[0]
        for port_data in host["ports"]:
            finding = PortFinding(
                asset_id=asset_id,
                port=port_data["port"],
                protocol=port_data["protocol"],
                service_name=port_data["service_name"],
                service_version=port_data["service_version"],
                state=port_data["state"],
                discovered_at=datetime.now(timezone.utc),
            )
            db.add(finding)
            findings.append(finding)
    
    db.commit()
    
    for finding in findings:
        db.refresh(finding)
    
    return findings


def get_port_findings_by_asset(
    db: Session,
    asset_id: int,
    skip: int = 0,
    limit: int = 100,
) -> tuple[list[PortFinding], int]:
    """Get port findings for a specific asset with pagination."""
    query = db.query(PortFinding).filter(PortFinding.asset_id == asset_id)
    total = query.count()
    findings = query.order_by(PortFinding.port).offset(skip).limit(limit).all()
    return findings, total
