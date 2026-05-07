"""Tests for discovery module (EPIC-03).

Covers:
- PortFinding model
- Discovery service functions (scan_ip_range, scan_ports, get_port_findings_by_asset)
- Discovery API endpoints (RBAC, scan triggers, port listing)
- XML parsing from nmap
- Security: network validation, nmap availability
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Generator
import subprocess
from unittest.mock import patch, MagicMock

from app.models.port_finding import PortFinding
from app.models.asset import Asset
from app.discovery.service import (
    scan_ip_range,
    scan_ports,
    get_port_findings_by_asset,
    _parse_nmap_xml,
    _is_lab_network,
)
from app.schemas.port_finding import PortFindingCreate, PortFindingResponse


# ── Nmap XML Fixtures ───────────────────────────────────────────────────

NMAP_PING_XML = """<?xml version="1.0"?>
<nmaprun scanner="nmap" args="nmap -sn -oX - 192.168.1.0/24" start="1234567890">
  <host>
    <status state="up" reason="arp-response"/>
    <addresses>
      <address addr="192.168.1.1" addrtype="ipv4"/>
    </addresses>
    <hostnames>
      <hostname name="gateway"/>
    </hostnames>
  </host>
  <host>
    <status state="up" reason="arp-response"/>
    <addresses>
      <address addr="192.168.1.100" addrtype="ipv4"/>
    </addresses>
    <hostnames>
      <hostname name="web-server"/>
    </hostnames>
    <os>
      <osmatch name="Linux 5.15" accuracy="95"/>
    </os>
  </host>
  <host>
    <status state="down" reason="no-response"/>
    <addresses>
      <address addr="192.168.1.200" addrtype="ipv4"/>
    </addresses>
  </host>
</nmaprun>"""

NMAP_PORT_XML = """<?xml version="1.0"?>
<nmaprun scanner="nmap" args="nmap -sT -p 22,80,443 -oX - 192.168.1.100">
  <host>
    <status state="up" reason="syn-ack"/>
    <addresses>
      <address addr="192.168.1.100" addrtype="ipv4"/>
    </addresses>
    <ports>
      <port protocol="tcp" portid="22">
        <state state="open" reason="syn-ack"/>
        <service name="ssh" product="OpenSSH" version="8.9" extrainfo="Ubuntu"/>
      </port>
      <port protocol="tcp" portid="80">
        <state state="open" reason="syn-ack"/>
        <service name="http" product="nginx" version="1.24.0"/>
      </port>
      <port protocol="tcp" portid="443">
        <state state="closed" reason="reset"/>
        <service name="https"/>
      </port>
    </ports>
  </host>
</nmaprun>"""

NMAP_EMPTY_XML = """<?xml version="1.0"?>
<nmaprun scanner="nmap" args="nmap -sn -oX - 192.168.1.0/30" start="1234567890">
  <host>
    <status state="down" reason="no-response"/>
    <addresses>
      <address addr="192.168.1.1" addrtype="ipv4"/>
    </addresses>
  </host>
</nmaprun>"""

NMAP_INVALID_XML = """This is not valid XML <<<>>>"""


# ── Mock Fixtures for subprocess.run ───────────────────────────────────

@pytest.fixture
def mock_nmap_ping():
    """Mock nmap ping scan to return 2 hosts up."""
    with patch("app.discovery.service.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout=NMAP_PING_XML,
            stderr="",
            returncode=0
        )
        yield mock_run


@pytest.fixture
def mock_nmap_port():
    """Mock nmap port scan to return 2 open ports."""
    with patch("app.discovery.service.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout=NMAP_PORT_XML,
            stderr="",
            returncode=0
        )
        yield mock_run


@pytest.fixture
def mock_nmap_empty():
    """Mock nmap ping scan with no hosts up."""
    with patch("app.discovery.service.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout=NMAP_EMPTY_XML,
            stderr="",
            returncode=0
        )
        yield mock_run


@pytest.fixture
def mock_nmap_not_installed():
    """Mock nmap not installed (FileNotFoundError)."""
    with patch("app.discovery.service.subprocess.run", side_effect=FileNotFoundError("nmap not found")):
        yield


@pytest.fixture
def mock_nmap_timeout():
    """Mock nmap timeout."""
    with patch("app.discovery.service.subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="nmap", timeout=30)):
        yield


# ── Helpers ──────────────────────────────────────────────────────────────

def _create_asset(db_session: Session, ip_address: str = "192.168.1.10", hostname: str = "test-server") -> Asset:
    """Helper to create an asset in the database."""
    asset = Asset(
        hostname=hostname,
        ip_address=ip_address,
        asset_type="server",
        status="active",
    )
    db_session.add(asset)
    db_session.commit()
    db_session.refresh(asset)
    return asset


def _create_port_finding(db_session: Session, asset_id: int, port: int = 80, protocol: str = "tcp") -> PortFinding:
    """Helper to create a port finding in the database."""
    finding = PortFinding(
        asset_id=asset_id,
        port=port,
        protocol=protocol,
        service_name="http",
        service_version="nginx 1.24.0",
        state="open",
        discovered_at=datetime.now(),
    )
    db_session.add(finding)
    db_session.commit()
    db_session.refresh(finding)
    return finding


# ── Tests du modèle PortFinding ──────────────────────────────────────────

class TestPortFindingModel:
    """Tests for PortFinding model."""

    def test_create_port_finding_valid(self, db_session: Session):
        """Test creating a valid PortFinding instance."""
        asset = _create_asset(db_session)
        
        finding = PortFinding(
            asset_id=asset.id,
            port=80,
            protocol="tcp",
            service_name="http",
            service_version="nginx 1.24.0",
            state="open",
        )
        db_session.add(finding)
        db_session.commit()
        db_session.refresh(finding)
        
        assert finding.id is not None
        assert finding.asset_id == asset.id
        assert finding.port == 80
        assert finding.protocol == "tcp"
        assert finding.service_name == "http"
        assert finding.service_version == "nginx 1.24.0"
        assert finding.state == "open"
        assert finding.discovered_at is not None

    def test_port_finding_repr(self, db_session: Session):
        """Test PortFinding __repr__ method."""
        asset = _create_asset(db_session)
        
        finding = PortFinding(
            asset_id=asset.id,
            port=443,
            protocol="tcp",
            service_name="https",
            state="open",
        )
        db_session.add(finding)
        db_session.commit()
        db_session.refresh(finding)
        
        repr_str = repr(finding)
        assert f"id={finding.id}" in repr_str
        assert f"asset_id={asset.id}" in repr_str
        assert "port=443/tcp" in repr_str
        assert "service=https" in repr_str
        assert "state=open" in repr_str

    def test_port_finding_with_nullable_fields(self, db_session: Session):
        """Test creating PortFinding with minimal required fields."""
        asset = _create_asset(db_session)
        
        finding = PortFinding(
            asset_id=asset.id,
            port=22,
            protocol="tcp",
            service_name="ssh",
            state="open",
        )
        db_session.add(finding)
        db_session.commit()
        db_session.refresh(finding)
        
        assert finding.id is not None
        assert finding.service_version is None

    def test_port_finding_relationship_with_asset(self, db_session: Session):
        """Test PortFinding relationship back to Asset."""
        asset = _create_asset(db_session, ip_address="10.0.0.5")
        
        finding = PortFinding(
            asset_id=asset.id,
            port=3306,
            protocol="tcp",
            service_name="mysql",
            state="open",
        )
        db_session.add(finding)
        db_session.commit()
        db_session.refresh(finding)
        
        # Test relationship
        assert finding.asset is not None
        assert finding.asset.id == asset.id
        assert finding.asset.ip_address == "10.0.0.5"

    def test_port_finding_different_states(self, db_session: Session):
        """Test PortFinding with different port states."""
        asset = _create_asset(db_session)
        
        for state in ["open", "closed", "filtered"]:
            finding = PortFinding(
                asset_id=asset.id,
                port=8080,
                protocol="tcp",
                service_name="http-proxy",
                state=state,
            )
            db_session.add(finding)
        
        db_session.commit()
        
        findings = db_session.query(PortFinding).filter(PortFinding.asset_id == asset.id).all()
        states = [f.state for f in findings]
        assert "open" in states
        assert "closed" in states
        assert "filtered" in states


# ── Tests des schemas PortFinding ────────────────────────────────────────

class TestPortFindingSchemas:
    """Tests for PortFinding Pydantic schemas."""

    def test_valid_port_finding_create(self):
        """Test valid PortFindingCreate schema."""
        data = {
            "asset_id": 1,
            "port": 443,
            "protocol": "tcp",
            "service_name": "https",
            "state": "open",
        }
        schema = PortFindingCreate(**data)
        
        assert schema.asset_id == 1
        assert schema.port == 443
        assert schema.protocol.value == "tcp"
        assert schema.service_name == "https"
        assert schema.state.value == "open"

    def test_port_finding_create_invalid_port_range(self):
        """Test PortFindingCreate with invalid port number."""
        # Port too low
        with pytest.raises(ValueError):
            PortFindingCreate(
                asset_id=1,
                port=0,
                protocol="tcp",
                service_name="test",
            )
        
        # Port too high
        with pytest.raises(ValueError):
            PortFindingCreate(
                asset_id=1,
                port=70000,
                protocol="tcp",
                service_name="test",
            )

    def test_port_finding_create_valid_port_boundaries(self):
        """Test PortFindingCreate with valid port boundaries."""
        # Minimum valid port
        schema_min = PortFindingCreate(
            asset_id=1,
            port=1,
            protocol="tcp",
            service_name="test",
        )
        assert schema_min.port == 1
        
        # Maximum valid port
        schema_max = PortFindingCreate(
            asset_id=1,
            port=65535,
            protocol="tcp",
            service_name="test",
        )
        assert schema_max.port == 65535

    def test_port_finding_create_udp_protocol(self):
        """Test PortFindingCreate with UDP protocol."""
        schema = PortFindingCreate(
            asset_id=1,
            port=53,
            protocol="udp",
            service_name="dns",
        )
        assert schema.protocol.value == "udp"

    def test_port_finding_create_missing_required_fields(self):
        """Test that required fields are enforced."""
        with pytest.raises(ValueError) as exc_info:
            PortFindingCreate()
        
        assert "field required" in str(exc_info.value).lower() or "missing" in str(exc_info.value).lower()


# ── Tests du service discovery avec mocks subprocess ────────────────────

class TestScanIpRange:
    """Tests for scan_ip_range service function."""

    def test_scan_ip_range_creates_assets(self, db_session: Session, mock_nmap_ping):
        """Test that scan_ip_range creates new assets from nmap output."""
        assets = scan_ip_range("192.168.1.0/24", db_session)
        
        assert len(assets) == 2  # 2 hosts up in mock XML
        assert all(isinstance(a, Asset) for a in assets)
        # Check that assets were actually saved to DB
        for asset in assets:
            assert asset.id is not None
            assert asset.ip_address is not None
        
        # Verify specific assets from mock XML
        ip_addresses = [a.ip_address for a in assets]
        assert "192.168.1.1" in ip_addresses
        assert "192.168.1.100" in ip_addresses

    def test_scan_ip_range_avoid_duplicates(self, db_session: Session, mock_nmap_ping):
        """Test that scan_ip_range avoids creating duplicate assets."""
        # First scan
        assets1 = scan_ip_range("192.168.1.0/24", db_session)
        count1 = len(assets1)
        
        # Second scan of same range
        assets2 = scan_ip_range("192.168.1.0/24", db_session)
        
        # Should return same assets, not create duplicates
        assert len(assets2) == count1
        
        # Verify no duplicate IPs in DB
        all_assets = db_session.query(Asset).filter(Asset.ip_address.like("192.168.1.%")).all()
        ip_addresses = [a.ip_address for a in all_assets]
        assert len(ip_addresses) == len(set(ip_addresses))  # No duplicates

    def test_scan_ip_range_invalid_range(self, db_session: Session):
        """Test scan_ip_range with invalid IP range format."""
        with pytest.raises(ValueError) as exc_info:
            scan_ip_range("invalid_range", db_session)
        
        # The error message is about lab network, but invalid format is caught first
        assert "Invalid IP range format" in str(exc_info.value)

    def test_scan_ip_range_non_lab_network(self, db_session: Session):
        """Test scan_ip_range rejects non-lab network."""
        with pytest.raises(ValueError) as exc_info:
            scan_ip_range("8.8.8.0/24", db_session)
        
        assert "outside allowed lab networks" in str(exc_info.value)

    def test_scan_ip_range_empty_result(self, db_session: Session, mock_nmap_empty):
        """Test scan_ip_range with no hosts up."""
        assets = scan_ip_range("192.168.1.0/30", db_session)
        assert len(assets) == 0

    def test_scan_ip_range_nmap_not_installed(self, db_session: Session, mock_nmap_not_installed):
        """Test scan_ip_range when nmap is not installed."""
        with pytest.raises(ValueError) as exc_info:
            scan_ip_range("192.168.1.0/24", db_session)
        
        assert "nmap is not installed" in str(exc_info.value)

    def test_scan_ip_range_nmap_timeout(self, db_session: Session, mock_nmap_timeout):
        """Test scan_ip_range when nmap times out."""
        with pytest.raises(ValueError) as exc_info:
            scan_ip_range("192.168.1.0/24", db_session)
        
        assert "timed out" in str(exc_info.value).lower()


class TestScanPorts:
    """Tests for scan_ports service function."""

    def test_scan_ports_creates_findings(self, db_session: Session, mock_nmap_port):
        """Test that scan_ports creates PortFinding records."""
        asset = _create_asset(db_session, ip_address="192.168.1.100")
        
        findings = scan_ports(asset.id, db_session)
        
        assert len(findings) == 2  # 2 open ports in mock XML (22 and 80)
        assert all(isinstance(f, PortFinding) for f in findings)
        assert all(f.asset_id == asset.id for f in findings)
        
        # Check specific ports from mock XML
        ports = [f.port for f in findings]
        assert 22 in ports
        assert 80 in ports
        
        # Check services detected
        for finding in findings:
            if finding.port == 22:
                assert finding.service_name == "ssh"
                assert "OpenSSH" in finding.service_version
            elif finding.port == 80:
                assert finding.service_name == "http"
                assert "nginx" in finding.service_version

    def test_scan_ports_asset_not_found(self, db_session: Session):
        """Test scan_ports with non-existent asset."""
        with pytest.raises(ValueError) as exc_info:
            scan_ports(99999, db_session)
        
        assert "not found" in str(exc_info.value).lower()

    def test_scan_ports_refreshes_previous_findings(self, db_session: Session, mock_nmap_port):
        """Test that scan_ports removes previous findings before new scan."""
        asset = _create_asset(db_session, ip_address="192.168.1.100")
        
        # First scan
        findings1 = scan_ports(asset.id, db_session)
        count1 = len(findings1)
        
        # Second scan
        findings2 = scan_ports(asset.id, db_session)
        
        # Should have fresh findings (old ones deleted)
        assert len(findings2) > 0
        
        # Total in DB should be equal to latest scan count (not cumulative)
        total_in_db = db_session.query(PortFinding).filter(PortFinding.asset_id == asset.id).count()
        assert total_in_db == len(findings2)

    def test_scan_ports_nmap_not_installed(self, db_session: Session, mock_nmap_not_installed):
        """Test scan_ports when nmap is not installed."""
        asset = _create_asset(db_session, ip_address="192.168.1.100")
        
        with pytest.raises(ValueError) as exc_info:
            scan_ports(asset.id, db_session)
        
        assert "nmap is not installed" in str(exc_info.value)


# ── Tests de sécurité pour le scan réseau ───────────────────────────────

class TestDiscoverySecurity:
    """Security tests for network scanning."""

    def test_is_lab_network_valid_192(self):
        """Test _is_lab_network with valid 192.168.x.x network."""
        assert _is_lab_network("192.168.1.0/24") is True
        assert _is_lab_network("192.168.0.0/16") is True

    def test_is_lab_network_valid_10(self):
        """Test _is_lab_network with valid 10.x.x.x network."""
        assert _is_lab_network("10.0.0.0/24") is True
        assert _is_lab_network("10.1.2.0/24") is True

    def test_is_lab_network_valid_172(self):
        """Test _is_lab_network with valid 172.16-31.x.x network."""
        assert _is_lab_network("172.16.0.0/24") is True
        assert _is_lab_network("172.31.255.0/24") is True

    def test_is_lab_network_invalid_172(self):
        """Test _is_lab_network rejects 172.32+ networks."""
        assert _is_lab_network("172.32.0.0/24") is False
        assert _is_lab_network("172.0.0.0/24") is False

    def test_is_lab_network_rejects_public_8_8_8_0(self):
        """Test that scanning external network 8.8.8.0/24 is rejected."""
        assert _is_lab_network("8.8.8.0/24") is False

    def test_is_lab_network_rejects_public_1_1_1_0(self):
        """Test that scanning Cloudflare DNS 1.1.1.0/24 is rejected."""
        assert _is_lab_network("1.1.1.0/24") is False

    def test_scan_rejects_non_lab_network_8_8_8_0(self, db_session: Session):
        """Test that scanning external network 8.8.8.0/24 is rejected."""
        with pytest.raises(ValueError) as exc_info:
            scan_ip_range("8.8.8.0/24", db_session)
        
        assert "not allowed" in str(exc_info.value).lower() or "outside allowed" in str(exc_info.value).lower()

    def test_scan_rejects_non_lab_network_public(self, db_session: Session):
        """Test that scanning public IP ranges is rejected."""
        with pytest.raises(ValueError) as exc_info:
            scan_ip_range("1.2.3.0/24", db_session)
        
        assert "not allowed" in str(exc_info.value).lower() or "outside allowed" in str(exc_info.value).lower()

    def test_scan_rejects_too_wide_network_8(self, db_session: Session):
        """Test that scanning too wide network (e.g. /8) is rejected."""
        with pytest.raises(ValueError) as exc_info:
            scan_ip_range("10.0.0.0/8", db_session)
        
        assert "too large" in str(exc_info.value).lower() or "maximum" in str(exc_info.value).lower()

    def test_scan_rejects_wide_network_16(self, db_session: Session):
        """Test that scanning /16 network is rejected."""
        with pytest.raises(ValueError) as exc_info:
            scan_ip_range("172.16.0.0/16", db_session)
        
        assert "too large" in str(exc_info.value).lower() or "maximum" in str(exc_info.value).lower()


# ── Tests du parsing XML nmap ───────────────────────────────────────────

class TestParseNmapXml:
    """Tests for _parse_nmap_xml function."""

    def test_parse_ping_scan_hosts_up(self):
        """Test parsing nmap ping scan XML with hosts up/down."""
        hosts = _parse_nmap_xml(NMAP_PING_XML)
        
        assert len(hosts) == 2  # Only up hosts
        assert all(h["ip"] for h in hosts)
        
        # Check first host (gateway)
        gateway = next(h for h in hosts if h["ip"] == "192.168.1.1")
        assert gateway["hostname"] == "gateway"
        assert "ports" in gateway
        assert len(gateway["ports"]) == 0  # No ports in ping scan
        
        # Check second host (web-server with OS)
        web_server = next(h for h in hosts if h["ip"] == "192.168.1.100")
        assert web_server["hostname"] == "web-server"
        assert web_server["os_name"] == "Linux 5.15"

    def test_parse_port_scan_open_closed_ports(self):
        """Test parsing nmap port scan XML with open/closed ports."""
        hosts = _parse_nmap_xml(NMAP_PORT_XML)
        
        assert len(hosts) == 1  # One host
        host = hosts[0]
        ports = host["ports"]
        
        # Should only return open ports
        assert len(ports) == 2
        
        # Check SSH port
        ssh = next(p for p in ports if p["port"] == 22)
        assert ssh["state"] == "open"
        assert ssh["service_name"] == "ssh"
        assert "OpenSSH" in ssh["service_version"]
        
        # Check HTTP port
        http = next(p for p in ports if p["port"] == 80)
        assert http["state"] == "open"
        assert http["service_name"] == "http"
        assert "nginx" in http["service_version"]
        
        # Port 443 is closed, should not be in results
        port_ids = [p["port"] for p in ports]
        assert 443 not in port_ids

    def test_parse_invalid_xml(self):
        """Test parsing invalid XML returns empty list."""
        result = _parse_nmap_xml(NMAP_INVALID_XML)
        assert isinstance(result, list)
        assert len(result) == 0

    def test_parse_empty_xml(self):
        """Test parsing empty or minimal XML."""
        empty_xml = '<?xml version="1.0"?><nmaprun></nmaprun>'
        result = _parse_nmap_xml(empty_xml)
        assert isinstance(result, list)
        assert len(result) == 0

    def test_parse_no_hosts(self):
        """Test parsing XML with no hosts element."""
        xml_no_hosts = '<?xml version="1.0"?><nmaprun scanner="nmap"></nmaprun>'
        result = _parse_nmap_xml(xml_no_hosts)
        assert isinstance(result, list)
        assert len(result) == 0

    def test_parse_host_down_filtered(self):
        """Test that down hosts are filtered out."""
        xml_with_down = """<?xml version="1.0"?>
<nmaprun>
  <host>
    <status state="down"/>
    <addresses><address addr="10.0.0.1" addrtype="ipv4"/></addresses>
  </host>
  <host>
    <status state="up"/>
    <addresses><address addr="10.0.0.2" addrtype="ipv4"/></addresses>
  </host>
</nmaprun>"""
        hosts = _parse_nmap_xml(xml_with_down)
        assert len(hosts) == 1
        assert hosts[0]["ip"] == "10.0.0.2"


# ── Tests de get_port_findings_by_asset ─────────────────────────────────

class TestGetPortFindingsByAsset:
    """Tests for get_port_findings_by_asset service function."""

    def test_get_port_findings_with_data(self, db_session: Session):
        """Test get_port_findings_by_asset with existing findings."""
        asset = _create_asset(db_session)
        
        # Create multiple findings
        for port in [22, 80, 443, 3306]:
            _create_port_finding(db_session, asset.id, port)
        
        findings, total = get_port_findings_by_asset(db_session, asset.id)
        
        assert total == 4
        assert len(findings) == 4
        assert all(f.asset_id == asset.id for f in findings)

    def test_get_port_findings_empty(self, db_session: Session):
        """Test get_port_findings_by_asset with no findings."""
        asset = _create_asset(db_session)
        
        findings, total = get_port_findings_by_asset(db_session, asset.id)
        
        assert total == 0
        assert len(findings) == 0
        assert isinstance(findings, list)

    def test_get_port_findings_pagination(self, db_session: Session):
        """Test get_port_findings_by_asset with pagination."""
        asset = _create_asset(db_session)
        
        # Create 10 findings
        for i in range(10):
            _create_port_finding(db_session, asset.id, 8000 + i)
        
        # Get first 3
        findings, total = get_port_findings_by_asset(db_session, asset.id, skip=0, limit=3)
        
        assert total == 10
        assert len(findings) == 3
        
        # Get next 3
        findings2, total2 = get_port_findings_by_asset(db_session, asset.id, skip=3, limit=3)
        
        assert total2 == 10
        assert len(findings2) == 3

    def test_get_port_findings_ordered_by_port(self, db_session: Session):
        """Test that findings are ordered by port number."""
        asset = _create_asset(db_session)
        
        # Create findings in random order
        ports = [443, 22, 8080, 80]
        for port in ports:
            _create_port_finding(db_session, asset.id, port)
        
        findings, _ = get_port_findings_by_asset(db_session, asset.id)
        
        # Should be ordered by port
        port_numbers = [f.port for f in findings]
        assert port_numbers == sorted(port_numbers)

    def test_get_port_findings_different_assets(self, db_session: Session):
        """Test that findings are filtered by asset_id."""
        asset1 = _create_asset(db_session, ip_address="10.0.0.1", hostname="server1")
        asset2 = _create_asset(db_session, ip_address="10.0.0.2", hostname="server2")
        
        _create_port_finding(db_session, asset1.id, 22)
        _create_port_finding(db_session, asset1.id, 80)
        _create_port_finding(db_session, asset2.id, 443)
        
        findings1, total1 = get_port_findings_by_asset(db_session, asset1.id)
        findings2, total2 = get_port_findings_by_asset(db_session, asset2.id)
        
        assert total1 == 2
        assert total2 == 1
        assert all(f.asset_id == asset1.id for f in findings1)
        assert all(f.asset_id == asset2.id for f in findings2)


# ── Tests des routes discovery ──────────────────────────────────────────

class TestTriggerIpScanRoute:
    """Tests for POST /api/v1/discovery/scan endpoint."""

    def test_scan_as_admin(self, client: TestClient, auth_headers_admin: dict, db_session: Session, mock_nmap_ping):
        """Test triggering IP scan as admin."""
        payload = {"ip_range": "192.168.1.0/24"}
        response = client.post(
            "/api/v1/discovery/scan",
            json=payload,
            headers=auth_headers_admin
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "assets_found" in data
        assert "assets" in data
        assert isinstance(data["assets"], list)

    def test_scan_rejects_analyst(self, client: TestClient, auth_headers_analyst: dict):
        """Test that analyst cannot trigger IP scan."""
        payload = {"ip_range": "192.168.1.0/24"}
        response = client.post(
            "/api/v1/discovery/scan",
            json=payload,
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 403

    def test_scan_rejects_unauthenticated(self, client: TestClient):
        """Test that unauthenticated user cannot trigger scan."""
        payload = {"ip_range": "192.168.1.0/24"}
        response = client.post(
            "/api/v1/discovery/scan",
            json=payload
        )
        
        assert response.status_code == 401

    def test_scan_missing_ip_range(self, client: TestClient, auth_headers_admin: dict):
        """Test scan with missing ip_range in body."""
        payload = {}
        response = client.post(
            "/api/v1/discovery/scan",
            json=payload,
            headers=auth_headers_admin
        )
        
        # Pydantic validation returns 422 for missing required fields
        assert response.status_code == 422

    def test_scan_invalid_ip_range(self, client: TestClient, auth_headers_admin: dict):
        """Test scan with invalid IP range format."""
        payload = {"ip_range": "not_a_valid_range"}
        response = client.post(
            "/api/v1/discovery/scan",
            json=payload,
            headers=auth_headers_admin
        )
        
        # Pydantic validation returns 422 for invalid field values
        assert response.status_code == 422

    def test_scan_rejects_non_lab_network_in_api(self, client: TestClient, auth_headers_admin: dict):
        """Test that API rejects scan of non-lab network."""
        payload = {"ip_range": "8.8.8.0/24"}
        response = client.post(
            "/api/v1/discovery/scan",
            json=payload,
            headers=auth_headers_admin
        )
        
        # Should return 422 (validation error) or 400 depending on implementation
        assert response.status_code in [400, 422]

    def test_scan_returns_asset_list(self, client: TestClient, auth_headers_admin: dict, db_session: Session, mock_nmap_ping):
        """Test that scan returns proper asset information."""
        payload = {"ip_range": "192.168.1.0/24"}
        response = client.post(
            "/api/v1/discovery/scan",
            json=payload,
            headers=auth_headers_admin
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["assets"]) > 0
        
        asset = data["assets"][0]
        assert "id" in asset
        assert "hostname" in asset
        assert "ip_address" in asset


class TestTriggerPortScanRoute:
    """Tests for POST /api/v1/discovery/ports/{asset_id} endpoint."""

    def test_port_scan_as_admin(self, client: TestClient, auth_headers_admin: dict, db_session: Session, mock_nmap_port):
        """Test triggering port scan as admin."""
        asset = _create_asset(db_session, ip_address="192.168.1.100")
        
        response = client.post(
            f"/api/v1/discovery/ports/{asset.id}",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Check structure of first finding
        finding = data[0]
        assert "id" in finding
        assert "port" in finding
        assert "protocol" in finding
        assert "service_name" in finding
        assert "state" in finding

    def test_port_scan_rejects_analyst(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test that analyst cannot trigger port scan."""
        asset = _create_asset(db_session)
        
        response = client.post(
            f"/api/v1/discovery/ports/{asset.id}",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 403

    def test_port_scan_rejects_unauthenticated(self, client: TestClient, db_session: Session):
        """Test that unauthenticated user cannot trigger port scan."""
        asset = _create_asset(db_session)
        
        response = client.post(
            f"/api/v1/discovery/ports/{asset.id}"
        )
        
        assert response.status_code == 401

    def test_port_scan_asset_not_found(self, client: TestClient, auth_headers_admin: dict):
        """Test port scan with non-existent asset."""
        response = client.post(
            "/api/v1/discovery/ports/99999",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_port_scan_creates_findings_in_db(self, client: TestClient, auth_headers_admin: dict, db_session: Session, mock_nmap_port):
        """Test that port scan actually creates findings in database."""
        asset = _create_asset(db_session, ip_address="192.168.1.100")
        
        response = client.post(
            f"/api/v1/discovery/ports/{asset.id}",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 200
        
        # Verify findings were created in DB
        findings = db_session.query(PortFinding).filter(PortFinding.asset_id == asset.id).all()
        assert len(findings) > 0


class TestListPortFindingsRoute:
    """Tests for GET /api/v1/discovery/ports/{asset_id} endpoint."""

    def test_list_ports_as_analyst(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test listing port findings as analyst."""
        asset = _create_asset(db_session, ip_address="10.0.0.70")
        
        # Create some findings
        for port in [22, 80, 443]:
            _create_port_finding(db_session, asset.id, port)
        
        response = client.get(
            f"/api/v1/discovery/ports/{asset.id}",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] == 3
        assert len(data["items"]) == 3

    def test_list_ports_as_admin(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        """Test listing port findings as admin."""
        asset = _create_asset(db_session, ip_address="10.0.0.80")
        _create_port_finding(db_session, asset.id, 3306)
        
        response = client.get(
            f"/api/v1/discovery/ports/{asset.id}",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1

    def test_list_ports_rejects_unauthenticated(self, client: TestClient, db_session: Session):
        """Test that unauthenticated user cannot list port findings."""
        asset = _create_asset(db_session)
        
        response = client.get(
            f"/api/v1/discovery/ports/{asset.id}"
        )
        
        assert response.status_code == 401

    def test_list_ports_pagination(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test listing port findings with pagination."""
        asset = _create_asset(db_session, ip_address="10.0.0.90")
        
        # Create 10 findings
        for i in range(10):
            _create_port_finding(db_session, asset.id, 9000 + i)
        
        # Get first 3
        response = client.get(
            f"/api/v1/discovery/ports/{asset.id}?skip=0&limit=3",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 10
        assert len(data["items"]) == 3
        assert data["skip"] == 0
        assert data["limit"] == 3

    def test_list_ports_empty(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test listing port findings when none exist."""
        asset = _create_asset(db_session, ip_address="10.0.0.100")
        
        response = client.get(
            f"/api/v1/discovery/ports/{asset.id}",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert len(data["items"]) == 0

    def test_list_ports_response_structure(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test that port findings response has correct structure."""
        asset = _create_asset(db_session, ip_address="10.0.0.110")
        _create_port_finding(db_session, asset.id, 8080)
        
        response = client.get(
            f"/api/v1/discovery/ports/{asset.id}",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check paginated response structure
        assert "items" in data
        assert "total" in data
        assert "skip" in data
        assert "limit" in data
        
        # Check individual finding structure
        if len(data["items"]) > 0:
            finding = data["items"][0]
            assert "id" in finding
            assert "asset_id" in finding
            assert "port" in finding
            assert "protocol" in finding
            assert "service_name" in finding
            assert "state" in finding
            assert "discovered_at" in finding


# ── Tests RBAC (Restent inchangés) ──────────────────────────────────────

class TestDiscoveryRBAC:
    """Comprehensive RBAC tests for discovery endpoints."""

    def test_analyst_cannot_scan_ip_range(self, client: TestClient, auth_headers_analyst: dict):
        """Test RBAC: analyst cannot access POST /scan."""
        payload = {"ip_range": "192.168.1.0/24"}
        response = client.post(
            "/api/v1/discovery/scan",
            json=payload,
            headers=auth_headers_analyst
        )
        assert response.status_code == 403

    def test_analyst_cannot_scan_ports(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test RBAC: analyst cannot access POST /ports/{asset_id}."""
        asset = _create_asset(db_session)
        response = client.post(
            f"/api/v1/discovery/ports/{asset.id}",
            headers=auth_headers_analyst
        )
        assert response.status_code == 403

    def test_analyst_can_list_ports(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test RBAC: analyst can access GET /ports/{asset_id}."""
        asset = _create_asset(db_session)
        response = client.get(
            f"/api/v1/discovery/ports/{asset.id}",
            headers=auth_headers_analyst
        )
        assert response.status_code == 200

    def test_admin_can_scan_ip_range(self, client: TestClient, auth_headers_admin: dict, mock_nmap_empty):
        """Test RBAC: admin can access POST /scan."""
        payload = {"ip_range": "192.168.1.0/30"}
        response = client.post(
            "/api/v1/discovery/scan",
            json=payload,
            headers=auth_headers_admin
        )
        assert response.status_code == 200

    def test_admin_can_scan_ports(self, client: TestClient, auth_headers_admin: dict, db_session: Session, mock_nmap_port):
        """Test RBAC: admin can access POST /ports/{asset_id}."""
        asset = _create_asset(db_session)
        response = client.post(
            f"/api/v1/discovery/ports/{asset.id}",
            headers=auth_headers_admin
        )
        assert response.status_code == 200

    def test_unauthenticated_cannot_access_any_endpoint(self, client: TestClient, db_session: Session):
        """Test RBAC: unauthenticated user cannot access any discovery endpoint."""
        asset = _create_asset(db_session)
        
        # POST /scan
        response1 = client.post("/api/v1/discovery/scan", json={"ip_range": "192.168.1.0/24"})
        assert response1.status_code == 401
        
        # POST /ports/{asset_id}
        response2 = client.post(f"/api/v1/discovery/ports/{asset.id}")
        assert response2.status_code == 401
        
        # GET /ports/{asset_id}
        response3 = client.get(f"/api/v1/discovery/ports/{asset.id}")
        assert response3.status_code == 401
