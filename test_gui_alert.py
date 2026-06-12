"""
test_gui_alert.py

Launches the GUI with a simulated ARP spoofing result pre-loaded,
so you can see what the Alerts tab looks like during an attack.
This is for thesis screenshots — not a real attack.
"""
import threading
import tkinter as tk
from datetime import datetime

from core.models import Alert, AlertLevel, Host, Port, ScanResult
from ui.gui import NetworkScannerGUI


def main():
    # Create the GUI
    app = NetworkScannerGUI()

    # Build a fake scan result that contains ARP spoofing
    fake_result = ScanResult(
        target_range="192.168.1.0/24",
        started_at=datetime.now().isoformat(),
        finished_at=datetime.now().isoformat(),
        duration_seconds=9.4,
        hosts=[
            Host(
                ip="192.168.1.1",
                mac="aa:bb:cc:11:22:33",
                vendor="TP-Link Technologies",
                hostname="router.local",
                is_gateway=True,
                ports=[
                    Port(number=80, service="http", banner="HTTP/1.1 200 OK"),
                    Port(number=443, service="https"),
                ],
            ),
            Host(
                ip="192.168.1.15",
                mac="dd:ee:ff:44:55:66",
                vendor="Apple, Inc.",
                hostname="iPhone-Ahmed",
                ports=[],
            ),
            Host(
                ip="192.168.1.22",
                mac="11:22:33:aa:bb:cc",
                vendor="Samsung Electronics",
                hostname="Galaxy-S24",
                ports=[
                    Port(number=8080, service="http-proxy"),
                ],
            ),
            Host(
                ip="192.168.1.99",
                mac="aa:bb:cc:11:22:33",  # SAME MAC as the gateway!
                vendor="Unknown",
                hostname="",
                ports=[
                    Port(number=80, service="http"),
                    Port(number=4444, service="unknown",
                         banner="Metasploit reverse shell"),
                ],
            ),
        ],
        alerts=[
            Alert(
                level=AlertLevel.CRITICAL,
                title="Possible ARP Spoofing Detected",
                message=(
                    "MAC address aa:bb:cc:11:22:33 is claimed by multiple IPs: "
                    "192.168.1.1, 192.168.1.99. This is a strong indicator of "
                    "an ARP spoofing / MITM attack."
                ),
            ),
            Alert(
                level=AlertLevel.CRITICAL,
                title="Gateway MAC Collision",
                message=(
                    "Gateway 192.168.1.1 (aa:bb:cc:11:22:33) shares its MAC "
                    "with: 192.168.1.99. Gateway impersonation suspected. "
                    "An attacker may be intercepting all network traffic."
                ),
            ),
        ],
    )

    # Load the fake result into the GUI after it starts
    def load_fake():
        app.root.after(500, lambda: app._display_results(fake_result, 99))

    load_fake()
    app.run()


if __name__ == "__main__":
    main()