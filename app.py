#!/usr/bin/env python3
"""
Flask backend for resurrexi.io
Serves static site + handles compute interest form submissions
"""

from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
import json
import datetime
import re
import html

app = Flask(__name__)

# Simple in-memory rate limiting (per IP, resets on restart)
RATE_LIMIT = {}
RATE_LIMIT_MAX = 5  # max submissions per IP
RATE_LIMIT_WINDOW = 3600  # per hour

def check_rate_limit(ip):
    """Returns True if allowed, False if rate limited"""
    now = datetime.datetime.now()
    if ip not in RATE_LIMIT:
        RATE_LIMIT[ip] = []

    # Remove old entries outside window
    RATE_LIMIT[ip] = [t for t in RATE_LIMIT[ip] if (now - t).seconds < RATE_LIMIT_WINDOW]

    if len(RATE_LIMIT[ip]) >= RATE_LIMIT_MAX:
        return False

    RATE_LIMIT[ip].append(now)
    return True

# Allowed values for dropdown fields
ALLOWED_RESEARCH_AREAS = {'ai-ml', 'political-economy', 'psychology', 'finance', 'security', 'interdisciplinary', 'other'}
ALLOWED_TIMELINES = {'asap', '1-3months', '3-6months', '6months+', 'flexible', ''}

def sanitize_string(s, max_length=1000):
    """Sanitize user input - escape HTML, limit length, strip whitespace"""
    if not isinstance(s, str):
        return ''
    # Strip, limit length, escape HTML entities
    s = s.strip()[:max_length]
    s = html.escape(s)
    # Remove any null bytes or control characters (except newlines/tabs)
    s = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', s)
    return s

def validate_email(email):
    """Basic email validation"""
    if not isinstance(email, str):
        return False
    # Simple regex - not perfect but catches obvious garbage
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip())) and len(email) < 255

# Paths
import os
BASE_DIR = Path(__file__).parent
PUBLIC_DIR = BASE_DIR / "public"
SUBMISSIONS_DIR = Path(os.environ.get('SUBMISSIONS_DIR', BASE_DIR / "submissions"))
SUBMISSIONS_DIR.mkdir(exist_ok=True)

@app.route('/api/compute-interest', methods=['POST'])
def compute_interest():
    """Handle compute interest form submissions with sanitization"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        # Rate limiting
        client_ip = request.headers.get('CF-Connecting-IP', request.remote_addr)
        if not check_rate_limit(client_ip):
            return jsonify({'success': False, 'error': 'Too many submissions. Try again later.'}), 429

        # Validate and sanitize email (required)
        email = data.get('email', '')
        if not validate_email(email):
            return jsonify({'success': False, 'error': 'Invalid email address'}), 400

        # Validate research area (required, must be from allowed list)
        research_area = data.get('research_area', '')
        if research_area not in ALLOWED_RESEARCH_AREAS:
            return jsonify({'success': False, 'error': 'Invalid research area'}), 400

        # Validate timeline (optional, must be from allowed list)
        timeline = data.get('timeline', '')
        if timeline and timeline not in ALLOWED_TIMELINES:
            timeline = ''

        # Sanitize all string fields
        sanitized = {
            'name': sanitize_string(data.get('name', ''), max_length=200),
            'email': sanitize_string(email, max_length=255),
            'institution': sanitize_string(data.get('institution', ''), max_length=300),
            'research_area': research_area,  # Already validated against allowlist
            'project_description': sanitize_string(data.get('project_description', ''), max_length=5000),
            'timeline': timeline,  # Already validated against allowlist
            'open_access': bool(data.get('open_access', False)),
            'reproducible': bool(data.get('reproducible', False)),
            'submitted_at': datetime.datetime.now().isoformat(),
            'ip_address': request.headers.get('CF-Connecting-IP', request.remote_addr)  # Real IP via Cloudflare
        }

        # Generate safe filename (no user input in filename)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        filename = f"compute_interest_{timestamp}.json"
        filepath = SUBMISSIONS_DIR / filename

        with open(filepath, 'w') as f:
            json.dump(sanitized, f, indent=2)

        print(f"[SUBMISSION] Saved: {filename}")
        print(f"  Email: {sanitized['email']}")
        print(f"  Research Area: {sanitized['research_area']}")

        return jsonify({
            'success': True,
            'message': 'Interest recorded successfully'
        }), 200

    except Exception as e:
        print(f"[ERROR] Form submission failed: {e}")
        return jsonify({
            'success': False,
            'error': 'Submission failed'  # Don't leak internal errors
        }), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Serve static files from public directory"""
    if path == '':
        path = 'index.html'
    elif not path.endswith('.html') and not path.startswith('static/'):
        # Try adding .html extension
        html_path = PUBLIC_DIR / f"{path}.html"
        if html_path.exists():
            return send_from_directory(PUBLIC_DIR, f"{path}.html")

    return send_from_directory(PUBLIC_DIR, path)

if __name__ == '__main__':
    # Development server
    app.run(host='0.0.0.0', port=5000, debug=False)
