from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://localhost:5173', os.getenv('FLASK_WEBSITE')]) 

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
    origin = request.headers.get('Origin', 'No origin')
    print(f"[KEYSTROKES] Request from origin: {origin}")
    return jsonify({'total_keystrokes': get_total_keystrokes()})

@app.route('/api/portfolio-stats')
def get_portfolio_stats():
    origin = request.headers.get('Origin', 'No origin')
    print(f"[PORTFOLIO] Request from origin: {origin}")
    return jsonify({
        'total_keystrokes': get_total_keystrokes(),
        'today_keystrokes': get_today_keystrokes(),
        'recent_activity': get_recent_activity(),
        'last_updated': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Start the Flask server
    port = int(os.getenv('PORT', 5010))
    app.run(debug=os.getenv('FLASK_ENV') == 'development', host='0.0.0.0', port=port) 