import requests
import time
from datetime import datetime

class KeystrokeAPIClient:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url

    def get_total_keystrokes(self):
        """Fetch the total number of keystrokes from the API."""
        try:
            response = requests.get(f"{self.base_url}/api/keystrokes")
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()['total_keystrokes']
        except requests.exceptions.RequestException as e:
            print(f"Error fetching keystrokes: {e}")
            return None

    def monitor_keystrokes(self, interval=1):
        """Continuously monitor keystrokes with a specified update interval."""
        print(f"Starting keystroke monitoring at {datetime.now()}")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                count = self.get_total_keystrokes()
                if count is not None:
                    print(f"Total keystrokes: {count:,} | Time: {datetime.now().strftime('%H:%M:%S')}")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped")

def main():
    # Example usage
    client = KeystrokeAPIClient()
    
    # Get a single reading
    count = client.get_total_keystrokes()
    if count is not None:
        print(f"Current total keystrokes: {count:,}")
    
    # Or monitor continuously
    print("\nStarting continuous monitoring...")
    client.monitor_keystrokes(interval=1)

if __name__ == "__main__":
    main() 