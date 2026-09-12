import os
from flask import Flask, jsonify
app = Flask(__name__)
ITEMS = [{"name": "web-01", "environment": "dev", "owner": "platform", "status": "active", "os": "Ubuntu", "version": os.getenv("APP_VERSION", "dev")}]
@app.get('/health')
def health(): return jsonify(status='ok'), 200
@app.get('/api/systems')
def systems(): return jsonify(ITEMS), 200
