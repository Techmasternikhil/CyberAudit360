import platform
import psutil
import socket
from typing import Dict, Any

class LocalInventoryScanner:
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Safely gather local system information without invasive commands."""
        info = {
            "hostname": socket.gethostname(),
            "os_name": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "cpu_cores": psutil.cpu_count(logical=True),
            "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "ip_addresses": LocalInventoryScanner._get_local_ips()
        }
        return info

    @staticmethod
    def _get_local_ips() -> list[str]:
        ips = []
        try:
            for interface_name, interface_addresses in psutil.net_if_addrs().items():
                for address in interface_addresses:
                    if address.family == socket.AF_INET:
                        ips.append(address.address)
        except Exception:
            pass
        return ips

    @staticmethod
    def get_running_processes() -> list[Dict[str, Any]]:
        """Safely get a list of running processes (limited data to avoid permission errors)."""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return processes
