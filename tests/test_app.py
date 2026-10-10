import os
os.environ.setdefault('DATABASE_URL', 'postgresql://x:x@127.0.0.1:5432/x')
import app.app as m

class Fake:
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def execute(self, *a): return self
    def fetchall(self): return []

def down(retries=12): raise RuntimeError('db down')

def test_health(monkeypatch):
    monkeypatch.setattr(m, 'conn', lambda retries=12: Fake())
    r = m.app.test_client().get('/health')
    assert r.status_code == 200 and r.get_json()['status'] == 'ok'

def test_health_degraded(monkeypatch):
    monkeypatch.setattr(m, 'conn', down)
    assert m.app.test_client().get('/health').status_code == 503

def test_systems(monkeypatch):
    monkeypatch.setattr(m, 'conn', lambda retries=12: Fake())
    assert m.app.test_client().get('/api/systems').status_code == 200
