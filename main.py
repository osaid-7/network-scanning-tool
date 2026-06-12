"""
main.py

Entry point for the Network Scanner application.
Sets up logging and launches the GUI.
"""
import logging
import os
import sys


def setup_logging():
    """Configure logging to both file and console."""
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(log_dir, "scanner.log")),
            logging.StreamHandler(sys.stdout),
        ],
    )


def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Network Scanner")

    try:
        from ui.gui import NetworkScannerGUI
        app = NetworkScannerGUI()
        app.run()
    except Exception as e:
        logger.critical(f"Application failed to start: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()