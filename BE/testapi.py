import unittest
import json
from app import app, db, Product

SECRET = 'TestSecret'
TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBuZ0E0Y1BxeEFxSk9WLVJWLWszTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1pMWdqZ2g1bGtiNHZobW1hLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjY2N2VlMzQ1ZDFlZjI3YjI1Nzk3YzIiLCJhdWQiOiJJbWFnZSIsImlhdCI6MTcyMDI5MTgxOCwiZXhwIjoxNzIwMjk5MDE4LCJzY29wZSI6IiIsImF6cCI6IkJmekVJODhiZTFCSGNBTmtDYm43aXBTWEVsd1lzTWl0IiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnByb2R1Y3RzIiwiZ2V0OnByb2R1Y3RzLWRldGFpbCIsInBhdGNoOnByb2R1Y3RzIiwicG9zdDpwcm9kdWN0cyIsInBvc3Q6c2VyaWFsIl19.BgMq1tMeu6hNE5b5ZKRkNGDk87sMCehbhYLAXga9NUfCb5vmA2GDZ2U9U4jpnPbRrlIalNcRB2DqcSj5XyrL2xwRu2gLsWklKZOHQqPnGunS0PuchKlxc6dlDz_XoLCFpfBD1bfkZ5KNqgs-__QE-HZ5O-3rNek4ovKDj1e3KYoPGfaLSUx1ChEZxJqTctHwtLquvor1c0JF7bdrd89OEF8ft4-5J9Gt3RXXTFju59U29PhR57uXvcXJsnMjIHJ-XB9JwAYQxtcDD3V3ca6oD4QXYzMwAYKi13xudmpV0e-c415AzPg8Y6ElQa8VwHPW_5ZzKJCalN1wDIzOj789sw'
TOKEN_USER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBuZ0E0Y1BxeEFxSk9WLVJWLWszTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1pMWdqZ2g1bGtiNHZobW1hLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjY2N2VlMzQ1ZDFlZjI3YjI1Nzk3YzIiLCJhdWQiOiJJbWFnZSIsImlhdCI6MTcyMDI5MTgxOCwiZXhwIjoxNzIwMjk5MDE4LCJzY29wZSI6IiIsImF6cCI6IkJmekVJODhiZTFCSGNBTmtDYm43aXBTWEVsd1lzTWl0IiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnByb2R1Y3RzIiwiZ2V0OnByb2R1Y3RzLWRldGFpbCIsInBhdGNoOnByb2R1Y3RzIiwicG9zdDpwcm9kdWN0cyIsInBvc3Q6c2VyaWFsIl19.BgMq1tMeu6hNE5b5ZKRkNGDk87sMCehbhYLAXga9NUfCb5vmA2GDZ2U9U4jpnPbRrlIalNcRB2DqcSj5XyrL2xwRu2gLsWklKZOHQqPnGunS0PuchKlxc6dlDz_XoLCFpfBD1bfkZ5KNqgs-__QE-HZ5O-3rNek4ovKDj1e3KYoPGfaLSUx1ChEZxJqTctHwtLquvor1c0JF7bdrd89OEF8ft4-5J9Gt3RXXTFju59U29PhR57uXvcXJsnMjIHJ-XB9JwAYQxtcDD3V3ca6oD4QXYzMwAYKi13xudmpV0e-c415AzPg8Y6ElQa8VwHPW_5ZzKJCalN1wDIzOj789sw'
EMAIL = 'admin@dev.com'
PASSWORD = 'Xopru6-xesquj-kaqgef'


def generate_token(role):
    if role == 'Admin':
        return TOKEN  
    elif role == 'User':
        return TOKEN_USER
    else:
        raise ValueError("Invalid role")
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # GET /products
    def test_get_products_success(self):
        token = generate_token('Admin')  # Hoặc 'User', cả hai đều có quyền
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.get('/products', headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(isinstance(data['products'], list))

    def test_get_products_unauthorized(self):
        response = self.app.get('/products')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # POST /products
    def test_create_product_success(self):
        token = generate_token('Admin')
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.post('/products', json=self.test_product, headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['product']['name'], self.test_product['name'])

    def test_create_product_unauthorized(self):
        token = generate_token('User')  # User không có quyền tạo sản phẩm
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.post('/products', json=self.test_product, headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    # RBAC for GET /products
    def test_get_products_rbac_admin(self):
        token = generate_token('Admin')
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.get('/products', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_get_products_rbac_user(self):
        token = generate_token('User')
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.get('/products', headers=headers)
        self.assertEqual(response.status_code, 200)
    # GET /products/<int:id>
    def test_get_product_detail_success(self):
        product = Product(name="Sản phẩm chi tiết")
        db.session.add(product)
        db.session.commit()

        token = generate_token('Admin')  # Hoặc 'User', cả hai đều có quyền
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.get(f'/products/{product.id}', headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['product']['id'], product.id)
        self.assertEqual(data['product']['name'], product.name)

    def test_get_product_detail_not_found(self):
        token = generate_token('Admin')  # Hoặc 'User', cả hai đều có quyền
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.get('/products/9999', headers=headers)  # ID không tồn tại
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # PATCH /products/<int:id>
    def test_update_product_success(self):
        product = Product(name="Sản phẩm cũ")
        db.session.add(product)
        db.session.commit()

        new_product_data = {"name": "Sản phẩm mới"}
        token = generate_token('Admin')
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.patch(f'/products/{product.id}', json=new_product_data, headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['product']['name'], new_product_data['name'])

    def test_update_product_unauthorized(self):
        product = Product(name="Sản phẩm cũ")
        db.session.add(product)
        db.session.commit()

        new_product_data = {"name": "Sản phẩm mới"}
        token = generate_token('User')  # User không có quyền sửa
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.patch(f'/products/{product.id}', json=new_product_data, headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')
        # DELETE /products/<int:id>
    def test_delete_product_success(self):
        product = Product(name="Sản phẩm cần xóa")
        db.session.add(product)
        db.session.commit()

        token = generate_token('Admin')
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.delete(f'/products/{product.id}', headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], product.id)

    def test_delete_product_unauthorized(self):
        product = Product(name="Sản phẩm cần xóa")
        db.session.add(product)
        db.session.commit()

        token = generate_token('User')  # User không có quyền xóa
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.delete(f'/products/{product.id}', headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    # POST /CreateProducts
    def test_create_product_and_serial_success(self):
        token = generate_token('Admin')
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.post('/CreateProducts', json=self.test_serial, headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['product']['name'], self.test_serial['name'])
        self.assertEqual(len(data['product']['serials']), len(self.test_serial['imeis']))

    def test_create_product_and_serial_unauthorized(self):
        token = generate_token('User')  # User không có quyền tạo sản phẩm và serial
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.post('/CreateProducts', json=self.test_serial, headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')