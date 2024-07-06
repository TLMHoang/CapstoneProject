import os
import json
import pytest

import app as app

SECRET = 'TestSecret'
TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBuZ0E0Y1BxeEFxSk9WLVJWLWszTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1pMWdqZ2g1bGtiNHZobW1hLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjY2N2VlMzQ1ZDFlZjI3YjI1Nzk3YzIiLCJhdWQiOiJJbWFnZSIsImlhdCI6MTcyMDI5MTgxOCwiZXhwIjoxNzIwMjk5MDE4LCJzY29wZSI6IiIsImF6cCI6IkJmekVJODhiZTFCSGNBTmtDYm43aXBTWEVsd1lzTWl0IiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnByb2R1Y3RzIiwiZ2V0OnByb2R1Y3RzLWRldGFpbCIsInBhdGNoOnByb2R1Y3RzIiwicG9zdDpwcm9kdWN0cyIsInBvc3Q6c2VyaWFsIl19.BgMq1tMeu6hNE5b5ZKRkNGDk87sMCehbhYLAXga9NUfCb5vmA2GDZ2U9U4jpnPbRrlIalNcRB2DqcSj5XyrL2xwRu2gLsWklKZOHQqPnGunS0PuchKlxc6dlDz_XoLCFpfBD1bfkZ5KNqgs-__QE-HZ5O-3rNek4ovKDj1e3KYoPGfaLSUx1ChEZxJqTctHwtLquvor1c0JF7bdrd89OEF8ft4-5J9Gt3RXXTFju59U29PhR57uXvcXJsnMjIHJ-XB9JwAYQxtcDD3V3ca6oD4QXYzMwAYKi13xudmpV0e-c415AzPg8Y6ElQa8VwHPW_5ZzKJCalN1wDIzOj789sw'
EMAIL = 'admin@dev.com'
PASSWORD = 'Xopru6-xesquj-kaqgef'


@pytest.fixture
def client():
    try:
        os.environ['JWT_SECRET'] = SECRET
        app.APP.config['TESTING'] = True
        client = app.APP.test_client()

        yield client
    except:
        assert False


def test_health(client):
    try:
        response = client.get('/')
        assert response.status_code == 200
        assert response.json == 'Healthy'
    except:
        assert False


def test_auth(client):
    body = {'email': EMAIL,
            'password': PASSWORD}
    response = client.post('/auth',
                           data=json.dumps(body),
                           content_type='application/json')

    assert response.status_code == 200
    token = response.json['token']
    assert token is not None


