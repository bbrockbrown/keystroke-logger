# Keystroke Counter

A background service that tracks your keystrokes and provides real-time statistics through a web interface and API.

## Features

- Background keystroke tracking (printable characters only)
- SQLite database storage with timestamps
- Flask web interface with real-time updates
- CORS-enabled for cross-origin requests (so you can pull data from elsewhere)
- Daemon mode for continuous tracking

## Quick Start

### Prerequisites
- Python 3.8+
- macOS/Linux (for keyboard access permissions)

### Installation

1. **Clone and setup:**
   ```bash
   git clone git remote add origin https://github.com/bbrockbrown/keystroke-logger.git
   cd keystroke-logger
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   # See .env.example and edit own .env:
   FLASK_WEBSITE=https://yourportfolio.com
   FLASK_ENV=development
   ```

### Usage

**Option 1: Quick Test**
```bash
python app.py
# Visit http://localhost:5010
```

**Option 2: Background Service (Recommended)**
```bash
# Start keystroke tracking daemon
python keystroke_daemon.py &

# Start web server separately
python app.py
```

### macOS Permissions
Grant accessibility permissions: `System Preferences > Security & Privacy > Privacy > Accessibility`

## API Endpoints

### GET `/api/keystrokes`
```json
{"total_keystrokes": 12345}
```

### GET `/api/portfolio-stats`
```json
{
  "total_keystrokes": 12345,
  "today_keystrokes": 567,
  "recent_activity": [
    {"date": "2024-03-21", "count": 1200},
    {"date": "2024-03-20", "count": 800}
  ],
  "last_updated": "2024-03-21T10:30:00"
}
```

## File Structure
```
keystroke-counter/
├── app.py                 # Flask web server & API
├── keystroke_tracker.py   # Core tracking logic
├── keystroke_daemon.py    # Background service wrapper
├── api_client.py          # Example API client
├── test_keystrokes.py     # Basic integration test
├── templates/             # Web interface HTML
├── keystrokes.db          # SQLite database (generated)
└── requirements.txt       # Dependencies
```

## Troubleshooting

**Permission denied errors:**
- Grant accessibility permissions to your terminal/IDE

**CORS errors:**
- Update origins list in `app.py` line 8
- Check your portfolio domain is correct

**Database locked:**
- Only one tracker instance should run at a time

**Port conflicts:**
- Change port in `app.py` line 76

## Funsies

feel free to use this for your own portfolio! 