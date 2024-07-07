from datetime import datetime
import unittest
import json
from app import app, db, Product

SECRET = 'TestSecret'
TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBuZ0E0Y1BxeEFxSk9WLVJWLWszTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1pMWdqZ2g1bGtiNHZobW1hLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjY2N2VlMzQ1ZDFlZjI3YjI1Nzk3YzIiLCJhdWQiOiJJbWFnZSIsImlhdCI6MTcyMDMyODIxNCwiZXhwIjoxNzIwNDE0NjE0LCJzY29wZSI6IiIsImF6cCI6IkJmekVJODhiZTFCSGNBTmtDYm43aXBTWEVsd1lzTWl0IiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnByb2R1Y3RzIiwiZ2V0OnByb2R1Y3RzLWRldGFpbCIsInBhdGNoOnByb2R1Y3RzIiwicG9zdDpwcm9kdWN0cyIsInBvc3Q6c2VyaWFsIl19.r4D9XG42k7SlHaT5KKVJPCFmw6KH_NaShCj5BWhsI7GIjNQdCAr5VsIyZ_W0jZt63QpYcn1nQGS0MZPGrxxsTvcy1WTlwiwNQZoPKOlfIWY1dXUzt-o-gNOKQKxRY5DFOQTr236JExQ9JWge6rqzgL5zcw5JhW58gRdd33ErsBirjTu-33fxFAC-Ovyrf6Iztwsvi5yp80SSdotKs82zRgjn5SyBuM76r5QQ4cNWS3RbQHf1MqmykOkB7arlgn7IRx-nvXJ3S5QTgjyG-rLiF7IibYEl_hZSe2PfCT7iBt1yFHC79Q1Rgu5kB2GkRw0UaFtsIiZpzfV0wGe-ucqj8w'
TOKEN_USER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBuZ0E0Y1BxeEFxSk9WLVJWLWszTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1pMWdqZ2g1bGtiNHZobW1hLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2Njg5YWViMTY3MWM0MDdlOGE4ZjRhMWQiLCJhdWQiOiJJbWFnZSIsImlhdCI6MTcyMDMyODE4MiwiZXhwIjoxNzIwNDE0NTgyLCJzY29wZSI6IiIsImF6cCI6IkJmekVJODhiZTFCSGNBTmtDYm43aXBTWEVsd1lzTWl0IiwicGVybWlzc2lvbnMiOltdfQ.lGJmz0rp0CyYg7Kvs-27Hd36sBw654N9Wz4HK7Y0kUPFUOQceSQ81kExXq84se11bflTWD_FBSWtV75qDdRJNxb7ZUKk0jzsAvcIpIlhOsnTgb6D6NUuLz0H4JHquPcKH7lQ1z9Hu649kBCfOrIoSr-CS5XYsav1HA2Cje_RtnSRugsy9F7lQq3xWeFz-HzSRfUT4FF5vBf2mSXarR3ozmL-B3qqWv2wpX0PmqI7bkG0JKksXHAJ3HhmHbJjmIAL1NgZeHnmzQVQ882WN0GTaM5DbQef0JRWbqjW6shr636er3D9CtLO6AgvJaU8uXnWHG1PYfX_d9u7KNFKH21c4g'
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
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123qwe@localhost:5432/storePhone' 
        app.config['JWT_SECRET'] = 'TestSecret'
        self.app = app.test_client()
        self.test_product = {"name": "Sản phẩm kiểm thử " + str(datetime.now())}
        self.test_serial = {"name": "Sản phẩm kiểm thử", "imeis": ["123456789012345", "098765432109876"]}

        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()
        pass

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

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(isinstance(data['products'], list))

    # # RBAC for GET /products
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
        token = generate_token('User')
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.post('/products', json=self.test_product, headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission Not found')

    # GET /products/<int:id>
    def test_get_product_detail_success(self):
        product = Product(name="Sản phẩm chi tiết")
        db.session.add(product)
        db.session.commit()
        
        token = generate_token('Admin')  
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.get(f'/products/1', headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['product']['id'], 1)

    def test_get_product_detail_not_found(self):
        token = generate_token('Admin') 
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.get('/products/9999', headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_get_product_detail_unauthorized(self):
        token = generate_token('User')
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.get('/products/1', json=self.test_product, headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission Not found')

    # PATCH /products/<int:id>
    def test_update_product_success(self):
        product = Product(name="Sản phẩm cũ")
        db.session.add(product)
        db.session.commit()

        new_product_data = {"name": "Sản phẩm mới" + str(datetime.now())}
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

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission Not found')
    
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
        self.assertEqual(data['delete'], product.id)

    def test_delete_product_unauthorized(self):
        product = Product(name="Sản phẩm cần xóa")
        db.session.add(product)
        db.session.commit()

        token = generate_token('User')
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.delete(f'/products/{product.id}', headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission Not found')

    # POST /CreateProducts
    def test_create_product_and_serial_success(self):
        token = generate_token('Admin')
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.post('/CreateProducts', json=self.test_serial, headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['product']['name'], self.test_serial['name'])
        self.assertEqual(len(data['created_serials']), len(self.test_serial['imeis']))

    def test_create_product_and_serial_unauthorized(self):
        token = generate_token('User') 
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.post('/CreateProducts', json=self.test_serial, headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission Not found')