import unittest
import json
from app import app, db

SECRET = 'TestSecret'
TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBuZ0E0Y1BxeEFxSk9WLVJWLWszTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1pMWdqZ2g1bGtiNHZobW1hLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjY2N2VlMzQ1ZDFlZjI3YjI1Nzk3YzIiLCJhdWQiOiJJbWFnZSIsImlhdCI6MTcyMDI5MTgxOCwiZXhwIjoxNzIwMjk5MDE4LCJzY29wZSI6IiIsImF6cCI6IkJmekVJODhiZTFCSGNBTmtDYm43aXBTWEVsd1lzTWl0IiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnByb2R1Y3RzIiwiZ2V0OnByb2R1Y3RzLWRldGFpbCIsInBhdGNoOnByb2R1Y3RzIiwicG9zdDpwcm9kdWN0cyIsInBvc3Q6c2VyaWFsIl19.BgMq1tMeu6hNE5b5ZKRkNGDk87sMCehbhYLAXga9NUfCb5vmA2GDZ2U9U4jpnPbRrlIalNcRB2DqcSj5XyrL2xwRu2gLsWklKZOHQqPnGunS0PuchKlxc6dlDz_XoLCFpfBD1bfkZ5KNqgs-__QE-HZ5O-3rNek4ovKDj1e3KYoPGfaLSUx1ChEZxJqTctHwtLquvor1c0JF7bdrd89OEF8ft4-5J9Gt3RXXTFju59U29PhR57uXvcXJsnMjIHJ-XB9JwAYQxtcDD3V3ca6oD4QXYzMwAYKi13xudmpV0e-c415AzPg8Y6ElQa8VwHPW_5ZzKJCalN1wDIzOj789sw'
EMAIL = 'admin@dev.com'
PASSWORD = 'Xopru6-xesquj-kaqgef'

class ProductTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Sử dụng cơ sở dữ liệu tạm thời
        app.config['JWT_SECRET'] = 'TestSecret'
        self.app = app.test_client()
        db.init_app(app)
        db.create_all()

        self.test_product = {"name": "Sản phẩm kiểm thử"}
        self.test_serial = {"name": "Sản phẩm kiểm thử", "imeis": ["123456789012345", "098765432109876"]}

        self.headers = {
            'Authorization': f'Bearer {TOKEN}'
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_products(self):
        response = self.app.get('/products')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(isinstance(data['products'], list))

    def test_create_product(self):
        response = self.app.post('/products', json=self.test_product, headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_create_product_and_serial(self):
        response = self.app.post('/CreateProducts', json=self.test_serial, headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['product']['name'], self.test_serial['name'])

    def test_404_product_not_found(self):
        response = self.app.get('/products/9999')  
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')
