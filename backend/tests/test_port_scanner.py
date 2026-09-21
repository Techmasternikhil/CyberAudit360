import pytest
from app.scanners.port_scanner import PortScanner

def test_scan_port_closed():
    # Test a port that is almost certainly closed locally (e.g. 54321)
    result = PortScanner.scan_port('127.0.0.1', 54321, timeout=0.1)
    assert result["port"] == 54321
    assert result["state"] == "CLOSED"

def test_scan_target():
    # Test scanning target with specific ports, expecting an empty or partial list of open ports
    results = PortScanner.scan_target('127.0.0.1', ports=[54321, 54322])
    assert isinstance(results, list)
    # We expect 0 open ports for these random high ports
    assert len(results) == 0
