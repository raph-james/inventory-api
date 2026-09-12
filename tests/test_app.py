from app.app import app
def test_health():
    r=app.test_client().get('/health')
    assert r.status_code == 200 and r.get_json()['status']=='ok'
def test_systems():
    assert app.test_client().get('/api/systems').status_code == 200
