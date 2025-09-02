import requests
import time
from datetime import datetime

def test_keystroke_tracking():
    print("Starting keystroke tracking test...")
    print("Type some text in any application to test.")
    print("Press Ctrl+C to stop the test.")
    
    try:
        while True:
            # Get current keystroke count
            response = requests.get("http://localhost:5004/api/keystrokes")
            count = response.json()['total_keystrokes']
            
            # Print current count with timestamp
            print(f"Keystrokes: {count:,} | Time: {datetime.now().strftime('%H:%M:%S')}")
            
            # Wait 1 second before next check
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nTest stopped.")
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the keystroke tracker service.")
        print("Make sure app.py is running on port 5004.")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    test_keystroke_tracking() 