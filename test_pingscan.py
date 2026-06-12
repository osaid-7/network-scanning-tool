"""
test_pingscan.py

Host discovery only — no port scanning. Tests the ARP sweep in isolation.
Good for measuring pure discovery speed and accuracy.
"""
import time
from core.scanner_engine import ScannerEngine
from core.network_utils import get_local_network


def main():
    target = get_local_network()
    if not target:
        print("Couldn't detect network. Set target manually.")
        return

    print(f"Ping-scanning {target} (ARP sweep only)...\n")

    engine = ScannerEngine(arp_timeout=2.0)

    t0 = time.perf_counter()
    hosts = engine._discover_hosts(target)
    elapsed = time.perf_counter() - t0

    print(f"{'=' * 55}")
    print(f"  DISCOVERED {len(hosts)} HOSTS in {elapsed:.2f}s")
    print(f"{'=' * 55}\n")

    print(f"{'IP':<16} {'MAC':<20} Vendor / Hostname")
    print("-" * 55)
    for h in hosts:
        tag = " [GATEWAY]" if h.is_gateway else ""
        label = h.hostname if h.hostname else h.vendor
        print(f"{h.ip:<16} {h.mac:<20} {label}{tag}")


if __name__ == "__main__":
    main()