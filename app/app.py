import os, time
from flask import Flask, jsonify, request
import psycopg
app=Flask(__name__)
DB=os.environ['DATABASE_URL']
def conn(retries=12):
    for n in range(retries):
        try: return psycopg.connect(DB)
        except psycopg.OperationalError:
            if n == retries-1: raise
            time.sleep(2)
def init_db():
    with conn() as c:
        c.execute('CREATE TABLE IF NOT EXISTS systems (id serial primary key, name text unique not null, environment text not null, owner_name text not null, status text not null, os text not null, app_version text not null)')
@app.get('/health')
def health():
    try:
        with conn(1) as c: c.execute('SELECT 1')
        return jsonify(status='ok'),200
    except Exception: return jsonify(status='degraded'),503
@app.get('/api/systems')
def list_systems():
    init_db()
    with conn() as c:
        rows=c.execute('SELECT id,name,environment,owner_name,status,os,app_version FROM systems ORDER BY id').fetchall()
    return jsonify([dict(zip(['id','name','environment','owner','status','os','version'],r)) for r in rows])
@app.post('/api/systems')
def add_system():
    init_db(); d=request.get_json()
    with conn() as c:
        c.execute('INSERT INTO systems(name,environment,owner_name,status,os,app_version) VALUES (%s,%s,%s,%s,%s,%s)',(d['name'],d['environment'],d['owner'],d['status'],d['os'],d['version']))
    return jsonify(created=d['name']),201
