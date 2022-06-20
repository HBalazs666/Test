import json
import api
from main import app

def test_get_pet():
    url = '/pets/'
    client = app.app.test_client()
    resp = client.get(url)
    # data = json.loads(resp.data)
    assert resp.status_code == 200
