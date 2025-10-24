from flask import Flask, jsonify
import os
import time
import redis
import psycopg2
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter('app_requests_total', 'Total HTTP requests')

# Read envs
DB_URL = os.environ.get('DATABASE_URL')
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

# Simple retry for db connection (for lab resilience)
conn = None
for i in range(10):
    try:
        conn = psycopg2.connect(DB_URL)
        break
    except Exception as e:
        print('DB connection failed, retrying...', e)
        time.sleep(1)

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.route('/api')
def index():
    REQUEST_COUNT.inc()
    # increment counter in redis
    try:
        hits = r.incr('hits')
    except Exception:
        hits = None

    db_time = None
    try:
        cur = conn.cursor()
        cur.execute('SELECT NOW()')
        db_time = cur.fetchone()[0].isoformat()
        cur.close()
    except Exception:
        db_time = None

    return jsonify({
        'message': 'Hello from backend',
        'db_time': db_time,
        'hits': hits
    })

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})
