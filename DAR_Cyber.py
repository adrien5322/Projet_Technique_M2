"""
Project name: DAR_Cyber
Version: 1.0
Copyright© 10/04/2026, Damien_ROCABOIS & Adrien_CAUDAL & LE NOUY_Ryan 

"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socket
from ipaddress import ip_network

app = FastAPI()

# Autoriser le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# Scan des ports
# ------------------------
def scan_ports(ip):
    open_ports = []
    for port in range(20, 1024):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports


# ------------------------
# Scan réseau
# ------------------------
@app.get("/scan")
def scan_network():
    network = "192.168.1.0/24"  # à adapter
    results = []

    for ip in ip_network(network, strict=False):
        ip = str(ip)
        ports = scan_ports(ip)

        if ports:
            results.append({
                "ip": ip,
                "open_ports": ports
            })

    return results

