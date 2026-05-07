#!/bin/bash
# =============================================================================
# DAR-Cyber - Nmap Lab Test Script
# =============================================================================
# This script tests nmap installation and performs safe scans in the lab network.
# Only scan private ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
# =============================================================================

set -euo pipefail

echo "=========================================="
echo "DAR-Cyber - Nmap Lab Test Script"
echo "=========================================="
echo ""

# Check nmap installation
echo "Checking nmap installation..."
if ! command -v nmap &> /dev/null; then
    echo "ERROR: nmap is not installed or not in PATH"
    exit 1
fi

nmap --version
echo ""

# Test ping scan on lab network (safe, no port scan)
echo "Scanning lab network 172.16.0.0/16 (ping only, safe for lab)..."
echo "Command: nmap -sn 172.16.0.0/16 --max-retries 1 --host-timeout 1s"
echo ""

# Run nmap with safe parameters
# -sn: Ping scan only (no port scan)
# --max-retries 1: Limit retries
# --host-timeout 1s: Timeout per host
nmap -sn 172.16.0.0/16 --max-retries 1 --host-timeout 1s 2>&1 || {
    echo ""
    echo "Note: Scan completed with warnings (expected in some lab configurations)"
}

echo ""
echo "=========================================="
echo "Nmap test completed."
echo "=========================================="
