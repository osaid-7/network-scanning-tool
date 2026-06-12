"""
demo_mitm.py

Demonstrates MITM detection in the GUI by running a real scan,
then injecting a simulated attacker into the results. The detection
logic runs against the combined real + fake data, triggering actual
CRITICAL alerts in the GUI.

No real ARP spoofing occurs. This is a safe, controlled simulation
for educational demonstration and thesis defense.
"""
from datetime import datetime
from core.scanner_engine import ScannerEngine
from core.network_utils import get_local_network
from core.models import Host, Port, Alert, AlertLevel, ScanResult
from storage.database import ScanDatabase
from ui.gui import NetworkScannerGUI
import time


def main():
    # 1. Detect the network
    target = get_local_network()
    if not target:
        print("Couldn't detect network.")
        return

    print(f"Running real scan on {target}...")

    # 2. Run a real scan to get actual hosts
    engine = ScannerEngine()
    result = engine.scan(target)

    print(f"Found {len(result.hosts)} real hosts.")

    # 3. Find the gateway
    gateway = None
    for h in result.hosts:
        if h.is_gateway:
            gateway = h
            break

    # If no gateway found, use the first host
    if not gateway and result.hosts:
        gateway = result.hosts[0]

    if not gateway:
        print("No hosts found. Cannot simulate attack.")
        return

    print(f"Gateway: {gateway.ip} ({gateway.mac})")
    print(f"Injecting fake attacker with gateway's MAC...")

    # 4. Create a fake attacker host that copies the gateway's MAC
    #    This is the textbook MITM setup: attacker claims to be the gateway
    attacker = Host(
        ip="10.114.254.66",          # Fake IP (not real on your network)
        mac=gateway.mac,              # SAME MAC as the gateway — this triggers detection
        vendor="Unknown",
        hostname="ATTACKER-PC",
        os_guess="Linux/macOS/Android",
        is_gateway=False,
        ports=[
            Port(number=80, service="http", banner="Apache/2.4.52 (Ubuntu)"),
            Port(number=4444, service="unknown", banner="Metasploit reverse TCP handler"),
            Port(number=8080, service="http-proxy", banner="Burp Suite Proxy"),
        ],
    )

    # 5. Add the attacker to the real results
    result.hosts.append(attacker)

    # 6. Re-run MITM detection on the modified host list
    result.alerts = engine._detect_arp_spoofing(result.hosts)

    print(f"Alerts generated: {len(result.alerts)}")
    for a in result.alerts:
        print(f"  [{a.level.value.upper()}] {a.title}")

    # 7. Launch the GUI with the attack results pre-loaded
    print("\nLaunching GUI with attack simulation...")

    app = NetworkScannerGUI()

    # Load the fake attack results after the GUI starts
    def load_attack():
        app._clear_results()
        app._display_results(result, 999)
        # Switch to alerts tab to show the detection
        app.notebook.select(1)

    app.root.after(500, load_attack)
    app.run()


if __name__ == "__main__":
    main()