"""
test_arpdetect.py

Validates the ARP spoofing detection logic by feeding it a crafted
host list containing simulated MITM scenarios. This is how you prove
the detection works without needing an actual attacker on the network.
"""
from core.scanner_engine import ScannerEngine
from core.models import Host


def run_test(label: str, hosts: list):
    print(f"\n{'=' * 60}")
    print(f"  TEST: {label}")
    print(f"{'=' * 60}")
    for h in hosts:
        gw = " [GATEWAY]" if h.is_gateway else ""
        print(f"  {h.ip:<16} {h.mac}{gw}")

    engine = ScannerEngine()
    alerts = engine._detect_arp_spoofing(hosts)

    if not alerts:
        print("\n  → No alerts raised.")
    else:
        for a in alerts:
            print(f"\n  [{a.level.value.upper()}] {a.title}")
            print(f"  {a.message}")


def main():
    # ─────────────────────────────────────────────────────────────
    # Scenario 1: Clean network — should raise ZERO alerts
    # ─────────────────────────────────────────────────────────────
    clean = [
        Host(ip="192.168.1.1",  mac="aa:aa:aa:11:11:11", is_gateway=True),
        Host(ip="192.168.1.10", mac="bb:bb:bb:22:22:22"),
        Host(ip="192.168.1.15", mac="cc:cc:cc:33:33:33"),
    ]
    run_test("Clean network (no anomalies expected)", clean)

    # ─────────────────────────────────────────────────────────────
    # Scenario 2: Duplicate MAC — two IPs share one MAC address
    # Classic ARP poisoning: the attacker's MAC answers for a victim IP
    # ─────────────────────────────────────────────────────────────
    spoof = [
        Host(ip="192.168.1.1",  mac="aa:aa:aa:11:11:11", is_gateway=True),
        Host(ip="192.168.1.10", mac="ee:ee:ee:99:99:99"),
        Host(ip="192.168.1.15", mac="ee:ee:ee:99:99:99"),   # duplicate!
    ]
    run_test("Duplicate MAC address (spoofing expected)", spoof)

    # ─────────────────────────────────────────────────────────────
    # Scenario 3: Gateway impersonation — attacker claims the router's MAC
    # This is the textbook MITM attack
    # ─────────────────────────────────────────────────────────────
    mitm = [
        Host(ip="192.168.1.1",  mac="aa:aa:aa:11:11:11", is_gateway=True),
        Host(ip="192.168.1.10", mac="bb:bb:bb:22:22:22"),
        Host(ip="192.168.1.66", mac="aa:aa:aa:11:11:11"),   # gateway MAC on different IP
    ]
    run_test("Gateway MAC collision (MITM expected)", mitm)


if __name__ == "__main__":
    main()