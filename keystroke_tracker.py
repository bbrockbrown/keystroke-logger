from pynput import keyboard
from datetime import datetime
import sqlite3
import os
import time
import string

class KeystrokeTracker:
    def __init__(self):
        self.db_path = 'keystrokes.db'
        self.setup_database()
        self.total_keystrokes = 0
        self.last_save = time.time()
        self.save_interval = 5  # Save to database every 5 seconds
        self.printable_chars = set(string.printable)  # Set of printable characters

    def setup_database(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS keystrokes
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             timestamp DATETIME,
             count INTEGER)
        ''')
        conn.commit()
        conn.close()

    def save_to_database(self):
        if self.total_keystrokes > 0:  # Only save if there are new keystrokes
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('INSERT INTO keystrokes (timestamp, count) VALUES (?, ?)',
                     (datetime.now(), self.total_keystrokes))
            conn.commit()
            conn.close()
            self.total_keystrokes = 0
        self.last_save = time.time()

    def on_press(self, key):
        try:
            # Only count printable characters
            if hasattr(key, 'char') and key.char in self.printable_chars:
                self.total_keystrokes += 1
                if time.time() - self.last_save >= self.save_interval:
                    self.save_to_database()
        except AttributeError:
            pass

    def get_total_keystrokes(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT SUM(count) FROM keystrokes')
        total = c.fetchone()[0] or 0
        conn.close()
        return total + self.total_keystrokes  # Include unsaved keystrokes

    def start(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == "__main__":
    tracker = KeystrokeTracker()
    tracker.start() 