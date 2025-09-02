from flask import Flask, render_template, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://localhost:5173', os.getenv('FLASK_WEBSITE')])  # Add your portfolio domain

# The keystroke daemon should now be running automatically (you can check with launchctl list | grep keystroke)

def get_total_keystrokes():
    try:
        conn = sqlite3.connect('keystrokes.db')
        c = conn.cursor()
        c.execute('SELECT SUM(count) FROM keystrokes')
        total = c.fetchone()[0] or 0
        conn.close()
        return total
    except Exception as e:
        print(f"Error reading from database: {e}")
        return 0

@app.route('/')
def index():
    return render_template('index.html')

def get_recent_activity():
    try:
        conn = sqlite3.connect('keystrokes.db')
        c = conn.cursor()
        c.execute('''
            SELECT DATE(timestamp) as date, SUM(count) as daily_count 
            FROM keystrokes 
            WHERE timestamp >= datetime('now', '-30 days')
            GROUP BY DATE(timestamp)
            ORDER BY date DESC
        ''')
        results = c.fetchall()
        conn.close()
        return [{'date': row[0], 'count': row[1]} for row in results]
    except Exception as e:
        print(f"Error getting recent activity: {e}")
        return []

def get_today_keystrokes():
    try:
        conn = sqlite3.connect('keystrokes.db')
        c = conn.cursor()
        c.execute('''
            SELECT SUM(count) FROM keystrokes 
            WHERE DATE(timestamp) = DATE('now')
        ''')
        today = c.fetchone()[0] or 0
        conn.close()
        return today
    except Exception as e:
        print(f"Error getting today's keystrokes: {e}")
        return 0

@app.route('/api/keystrokes')
def get_keystrokes():
    return jsonify({'total_keystrokes': get_total_keystrokes()})

@app.route('/api/portfolio-stats')
def get_portfolio_stats():
    return jsonify({
        'total_keystrokes': get_total_keystrokes(),
        'today_keystrokes': get_today_keystrokes(),
        'recent_activity': get_recent_activity(),
        'last_updated': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Start the Flask server
    app.run(debug=os.getenv('FLASK_ENV') == 'development', port=5010) 