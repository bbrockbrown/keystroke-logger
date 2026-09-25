#!/usr/bin/env python3
"""Push a snapshot of keystrokes.db to the portfolio's /api/keystrokes endpoint.

Run periodically by the com.keystroke.sync launch agent. Sends absolute totals
(overall + per local day), so a retried or skipped run never double-counts.
"""
import os
import sqlite3
import sys
from datetime import datetime

import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'keystrokes.db')

load_dotenv(os.path.join(BASE_DIR, '.env'))


def log(message):
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S} - {message}", flush=True)


def build_snapshot():
    # Read-only so a sync can never interfere with the tracker's writes
    conn = sqlite3.connect(f'file:{DB_PATH}?mode=ro', uri=True)
    try:
        total = conn.execute('SELECT COALESCE(SUM(count), 0) FROM keystrokes').fetchone()[0]
        # Timestamps are naive local time, so DATE() already gives the local day
        rows = conn.execute(
            'SELECT DATE(timestamp), SUM(count) FROM keystrokes GROUP BY DATE(timestamp)'
        ).fetchall()
    finally:
        conn.close()
    return {'total': total, 'days': {date: count for date, count in rows if date}}


def main():
    url = os.getenv('KEYSTROKE_SYNC_URL')
    token = os.getenv('KEYSTROKE_SYNC_TOKEN')
    if not url or not token:
        log('KEYSTROKE_SYNC_URL and KEYSTROKE_SYNC_TOKEN must be set in .env')
        return 1

    snapshot = build_snapshot()
    try:
        response = requests.post(
            url,
            json=snapshot,
            headers={'Authorization': f'Bearer {token}'},
            timeout=30,
        )
    except requests.exceptions.RequestException as e:
        log(f'Sync failed: {e}')
        return 1

    if not response.ok:
        log(f'Sync failed: HTTP {response.status_code} {response.text[:200]}')
        return 1

    log(f"Synced total={snapshot['total']} days={len(snapshot['days'])}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
