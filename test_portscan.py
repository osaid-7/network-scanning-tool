"""
test_portscan.py

Focused port scan against a single target IP.
Scans a broader port list than the default engine uses.
"""
import time
from core.scanner_engine import ScannerEngine


# ⚠️  EDIT THIS LINE — put the IP you want to scan.
# Your own laptop is always safe to scan (127.0.0.1 or your LAN IP).
TARGET_IP = "10.114.254.177"   # Change to any IP you have permission to scan

# Expanded port list — top 40 most-common ports
PORTS = [
    20, 21, 22, 23, 25, 53, 67, 68, 69, 80,
    110, 123, 135, 137, 138, 139, 143, 161, 162, 389,
    443, 445, 465, 587, 636, 993, 995, 1433, 1521, 3306,
    3389, 5432, 5900, 5985, 5986, 6379, 8000, 8080, 8443, 9090,
]


def main():
    print(f"Scanning ports on {TARGET_IP}...\n")

    engine = ScannerEngine(port_timeout=1.5)

    t0 = time.perf_counter()
    ports = engine._scan_host_ports(
        host=type("H", (), {"ip": TARGET_IP})(),  # lightweight mock Host
        ports=PORTS,
    )
    elapsed = time.perf_counter() - t0

    print(f"{'=' * 60}")
    print(f"  {TARGET_IP}: {len(ports)} open ports in {elapsed:.2f}s")
    print(f"  (scanned {len(PORTS)} total ports)")
    print(f"{'=' * 60}\n")

    if not ports:
        print("No open ports found in the scanned range.")
        return

    print(f"{'PORT':<8} {'SERVICE':<12} BANNER")
    print("-" * 60)
    for p in ports:
        banner = p.banner[:60] if p.banner else "(no banner)"
        print(f"{p.number:<8} {p.service:<12} {banner}")


if __name__ == "__main__":
    main()