import socket
import concurrent.futures
from typing import List, Dict, Any

class PortScanner:
    # Common safe ports for a local check (no aggressive scanning)
    COMMON_PORTS = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        135: "RPC",
        139: "NetBIOS",
        143: "IMAP",
        443: "HTTPS",
        445: "SMB",
        1433: "MSSQL",
        3306: "MySQL",
        3389: "RDP",
        5173: "Vite Dev Server",
        5432: "PostgreSQL",
        8000: "Uvicorn API Server",
        8080: "HTTP-Alt"
    }

    PORT_SEVERITY_RULES = {
        21: "HIGH",      # Plaintext Telnet/FTP
        23: "HIGH",      # Plaintext Telnet/FTP
        22: "MEDIUM",    # SSH exposure
        445: "MEDIUM",   # SMB exposure
        1433: "MEDIUM",  # Database exposure
        3306: "MEDIUM",  # Database exposure
        3389: "MEDIUM",  # RDP exposure
        5432: "MEDIUM",  # Database exposure
        80: "LOW",       # Web port
        443: "LOW",      # HTTPS port
        5173: "LOW",     # Dev frontend
        8000: "LOW",     # Dev backend API
        8080: "LOW",     # Alt web
    }

    @staticmethod
    def get_port_severity(port: int) -> str:
        """Determines standard severity level for an identified open port."""
        return PortScanner.PORT_SEVERITY_RULES.get(port, "INFORMATIONAL")

    @staticmethod
    def get_default_ports() -> List[int]:
        """Returns sorted list of standard ports to audit."""
        return sorted(list(PortScanner.COMMON_PORTS.keys()))

    @staticmethod
    def scan_port(ip: str, port: int, timeout: float = 0.5) -> Dict[str, Any]:
        """Safely check if a single port is open on the given IP."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                result = s.connect_ex((ip, port))
                if result == 0:
                    return {
                        "port": port,
                        "state": "OPEN",
                        "service": PortScanner.COMMON_PORTS.get(port, "Unknown")
                    }
        except Exception:
            pass
        return {"port": port, "state": "CLOSED", "service": "Unknown"}

    @staticmethod
    def scan_target(ip: str, ports: List[int] = None) -> List[Dict[str, Any]]:
        """Safely scan a target for a predefined list of common ports."""
        if ports is None:
            ports = list(PortScanner.COMMON_PORTS.keys())
            
        open_ports = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(PortScanner.scan_port, ip, port) for port in ports]
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res["state"] == "OPEN":
                    open_ports.append(res)
        return open_ports
