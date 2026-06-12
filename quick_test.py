"""
quick_test.py

A minimal test harness for the scanner engine.
Run this to verify everything works before building the GUI.
"""
from core.scanner_engine import ScannerEngine
from core.network_utils import get_local_network


def progress(current: int, total: int, message: str) -> None:
    """Simple progress printer — the engine calls this during the scan."""
    print(f"  [{current:3}%] {message}")


def main() -> None:
    # Auto-detect the local network. Falls back to manual entry if needed.
    target = get_local_network()
    if not target:
        print("Couldn't detect your network automatically.")
        print("Edit this script and set target manually, e.g.:")
        print("    target = '192.168.1.0/24'")
        return

    print(f"Scanning {target} ...\n")

    engine = ScannerEngine()
    result = engine.scan(target, on_progress=progress)

    # ---- Summary header ----
    print(f"\n{'=' * 60}")
    print(f"  SCAN RESULTS")
    print(f"{'=' * 60}")
    print(f"Target:   {result.target_range}")
    print(f"Duration: {result.duration_seconds} seconds")
    print(f"Hosts:    {len(result.hosts)} discovered")
    print(f"Alerts:   {len(result.alerts)}\n")

    # ---- Host list ----
    for h in result.hosts:
        gateway_tag = "  [GATEWAY]" if h.is_gateway else ""
        hostname_tag = f"  ({h.hostname})" if h.hostname else ""
        print(f"{h.ip:16} {h.mac}  {h.vendor}{gateway_tag}{hostname_tag}")
        for p in h.ports:
            banner_preview = f" — {p.banner[:50]}" if p.banner else ""
            print(f"    port {p.number:>5}/tcp  {p.service:<12}{banner_preview}")

    # ---- Security alerts ----
    if result.alerts:
        print(f"\n{'=' * 60}")
        print(f"  SECURITY ALERTS")
        print(f"{'=' * 60}")
        for a in result.alerts:
            print(f"\n[{a.level.value.upper()}] {a.title}")
            print(f"  {a.message}")
    else:
        print("\nNo security alerts — network looks clean.")


if __name__ == "__main__":
    main()