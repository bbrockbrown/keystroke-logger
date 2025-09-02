#!/usr/bin/env python3
from keystroke_tracker import KeystrokeTracker
import signal
import sys
import os
import logging

# Setup logging
logging.basicConfig(
    filename='keystroke_daemon.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def signal_handler(sig, frame):
    logging.info("Shutting down keystroke tracker daemon...")
    sys.exit(0)

def run_daemon():
    # Log daemon start
    logging.info("Starting keystroke tracker daemon...")
    
    try:
        # Create and start the tracker
        tracker = KeystrokeTracker()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Start tracking
        logging.info("Keystroke tracking active...")
        tracker.start()
        
    except Exception as e:
        logging.error(f"Error in keystroke tracker daemon: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_daemon() 