"""
test_database.py

Tests the database module by running a real scan, saving the results,
then reading them back to verify persistence works correctly.
"""
from core.scanner_engine import ScannerEngine
from core.network_utils import get_local_network
from storage.database import ScanDatabase


def main():
    target = get_local_network()
    if not target:
        print("Couldn't detect network.")
        return

    # 1. Run a scan
    print(f"Running scan on {target}...\n")
    engine = ScannerEngine()
    result = engine.scan(target)

    # 2. Save to database
    db = ScanDatabase()
    scan_id = db.save_scan(result)
    print(f"Scan saved to database with ID: {scan_id}")

    # 3. Read it back
    print(f"\nReading scan #{scan_id} from database...\n")
    loaded = db.get_scan_by_id(scan_id)

    print(f"{'=' * 55}")
    print(f"  LOADED FROM DATABASE")
    print(f"{'=' * 55}")
    print(f"Target:   {loaded.target_range}")
    print(f"Duration: {loaded.duration_seconds}s")
    print(f"Hosts:    {len(loaded.hosts)}")
    print(f"Alerts:   {len(loaded.alerts)}\n")

    for h in loaded.hosts:
        gw = " [GATEWAY]" if h.is_gateway else ""
        print(f"  {h.ip:<16} {h.mac}  {h.vendor}{gw}")
        for p in h.ports:
            print(f"      port {p.number:>5}/tcp  {p.service}")

    # 4. Show scan history
    print(f"\n{'=' * 55}")
    print(f"  SCAN HISTORY")
    print(f"{'=' * 55}")
    scans = db.get_scans()
    for s in scans:
        print(f"  #{s['id']}  {s['target']}  {s['host_count']} hosts  "
              f"{s['duration']:.1f}s  {s['started_at'][:19]}")

    # 5. Show stats
    print(f"\n{'=' * 55}")
    print(f"  DATABASE STATS")
    print(f"{'=' * 55}")
    stats = db.get_stats()
    for key, value in stats.items():
        label = key.replace("_", " ").title()
        print(f"  {label}: {value}")

    print(f"\nDatabase file: {db.db_path}")


if __name__ == "__main__":
    main()