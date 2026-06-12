"""
test_monitor.py

Runs the network monitor for 3 scan cycles so you can see it detect
changes in real-time. Try connecting/disconnecting a device from your
hotspot while this is running to trigger alerts.

Usage (admin terminal):
    python test_monitor.py
"""
import time
from core.monitor import NetworkMonitor, NetworkEvent
from core.scanner_engine import ScannerEngine
from core.network_utils import get_local_network
from core.models import ScanResult
from typing import List


def on_event(events: List[NetworkEvent], result: ScanResult) -> None:
    """Called by the monitor after every scan. Prints events to terminal."""
    timestamp = time.strftime("%H:%M:%S")
    host_count = len(result.hosts) if result else 0

    print(f"\n{'─' * 60}")
    print(f"  [{timestamp}]  Scan complete — {host_count} hosts online")
    print(f"{'─' * 60}")

    for e in events:
        icon = "🔴" if e.level == "critical" else "🟡" if e.level == "warning" else "🟢"
        # Fallback for terminals that don't support emoji
        label = f"[{e.level.upper()}]"
        print(f"\n  {label} {e.title}")
        print(f"    {e.message}")

    if not events:
        print("\n  No changes detected since last scan.")


def main():
    target = get_local_network()
    if not target:
        print("Couldn't detect network. Set target manually.")
        return

    print(f"{'=' * 60}")
    print(f"  NETWORK MONITOR")
    print(f"{'=' * 60}")
    print(f"  Target:   {target}")
    print(f"  Interval: 15 seconds between scans")
    print(f"  Duration: 3 scan cycles")
    print(f"")
    print(f"  TIP: While this runs, try one of these to trigger alerts:")
    print(f"    - Connect another device to your hotspot")
    print(f"    - Disconnect a device from your hotspot")
    print(f"    - Start or stop a service on your laptop")
    print(f"")
    print(f"  Press Ctrl+C at any time to stop.")
    print(f"{'=' * 60}")

    monitor = NetworkMonitor(
        target=target,
        interval=15,    # 15 seconds between scans (short for testing)
    )

    monitor.start(on_event=on_event)

    try:
        # Let it run for 3 cycles (15s × 3 = ~45 seconds + scan time)
        # Or until user presses Ctrl+C
        cycles = 0
        while cycles < 3 and monitor.is_running():
            time.sleep(1)
            cycles += 1 / 15   # roughly count cycles
    except KeyboardInterrupt:
        print("\n\nStopping monitor (Ctrl+C received)...")

    monitor.stop()
    print(f"\nMonitor stopped. Total scans: {monitor._scan_count}")


if __name__ == "__main__":
    main()