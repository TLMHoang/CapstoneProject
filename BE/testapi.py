from datetime import datetime
import unittest
import json
from app import app, db, Product

SECRET = 'TestSecret'
TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBuZ0E0Y1BxeEFxSk9WLVJWLWszTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1pMWdqZ2g1bGtiNHZobW1hLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjY2N2VlMzQ1ZDFlZjI3YjI1Nzk3YzIiLCJhdWQiOiJJbWFnZSIsImlhdCI6MTcyMDI5OTA5MiwiZXhwIjoxNzIwMzA2MjkyLCJzY29wZSI6IiIsImF6cCI6IkJmekVJODhiZTFCSGNBTmtDYm43aXBTWEVsd1lzTWl0IiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnByb2R1Y3RzIiwiZ2V0OnByb2R1Y3RzLWRldGFpbCIsInBhdGNoOnByb2R1Y3RzIiwicG9zdDpwcm9kdWN0cyIsInBvc3Q6c2VyaWFsIl19.nG_e-UimIsjB9u3mRpjqQUnpIcFtgB-MBXE7Atq6mDZaajm8vXNqyqySV_RmUAR4o1OVHl7yvg76ntUg3w0wEp7k_QZc4MX3iMVlKqUjsOmyvkTtGSM_zAiMNZ1a4yktll_urGQgmj9E0H99kUL05vDfd9K04tGXgyTblkFjxGIJi9YjOnqt0jAbujppjod1y63sUEozFs_eNu2NijdgdBT9p5QZDRn36oDWOLbc3wSnVQ47qYu1iwotLMo-lFsxjoBMyqRrcuvxbYgjrqO9pak-P_QYHTKevXomic4h_wQtIylV0rRpUv8N1JYs5CyxWdnj562pXSvlrZiNY87acg'
TOKEN_USER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBuZ0E0Y1BxeEFxSk9WLVJWLWszTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1pMWdqZ2g1bGtiNHZobW1hLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2Njg5YWViMTY3MWM0MDdlOGE4ZjRhMWQiLCJhdWQiOiJJbWFnZSIsImlhdCI6MTcyMDI5OTIzNywiZXhwIjoxNzIwMzA2NDM3LCJzY29wZSI6IiIsImF6cCI6IkJmekVJODhiZTFCSGNBTmtDYm43aXBTWEVsd1lzTWl0IiwicGVybWlzc2lvbnMiOltdfQ.VYgNNM8HPK8JElAjftlWdcMS4XVqAtSKMz29Hw5BQY3WJ5ig5tIk1WV5nfeQ4QdSKJ8TAf9fC2tjBBfUnITPBQjbcPu0fLbkupcuLBa_VX6uuRSsjTE6GQ7gizigEMZcDoOvzopKlZkmzMRYB_PyZPthOGbehLQ7YAA-mVrnon1YBlAUMOXL747Z_RgWMaie9mDi5onSbcIBNyUgZursxQtqOMARjuwRVgZGmKSG8gZHPFZGLdDtJj7Fwg3dt2q1Z7hPFaPLJJLDmzb4yD74F2TcKfaEpVCZNWZKKTg4FigN6-VJMjTfn_cMW_Vq8RHBtHtVXZ5dGOgDRTUKAOi7qQ'
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
        # db.init_app(app)
        # db.create_all()
        self.test_product = {"name": "Sản phẩm kiểm thử " + str(datetime.now())}
        self.test_serial = {"name": "Sản phẩm kiểm thử", "imeis": ["123456789012345", "098765432109876"]}

    def tearDown(self):
        pass
        # db.session.remove()
        # db.drop_all()

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

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission Not found')

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

    # # GET /products/<int:id>
    # def test_get_product_detail_success(self):
    #     token = generate_token('Admin')  
    #     headers = {'Authorization': f'Bearer {token}'}
    #     response = self.app.get(f'/products/1', headers=headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['product']['id'], 1)
    #     # self.assertEqual(data['product']['name'], product.name)

    # def test_get_product_detail_not_found(self):
    #     token = generate_token('Admin') 
    #     headers = {'Authorization': f'Bearer {token}'}
    #     response = self.app.get('/products/9999', headers=headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'Resource not found')

    # # PATCH /products/<int:id>
    # def test_update_product_success(self):
    #     product = Product(name="Sản phẩm cũ")
    #     db.session.add(product)
    #     db.session.commit()

    #     new_product_data = {"name": "Sản phẩm mới" + + str(datetime.now())}
    #     token = generate_token('Admin')
    #     headers = {'Authorization': f'Bearer {token}'}
    #     response = self.app.patch(f'/products/{product.id}', json=new_product_data, headers=headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['product']['name'], new_product_data['name'])

    # def test_update_product_unauthorized(self):
    #     product = Product(name="Sản phẩm cũ")
    #     db.session.add(product)
    #     db.session.commit()

    #     new_product_data = {"name": "Sản phẩm mới"}
    #     token = generate_token('User')  # User không có quyền sửa
    #     headers = {'Authorization': f'Bearer {token}'}
    #     response = self.app.patch(f'/products/{product.id}', json=new_product_data, headers=headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 403)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'Permission not found.')
    
    # # DELETE /products/<int:id>
    # def test_delete_product_success(self):
    #     product = Product(name="Sản phẩm cần xóa")
    #     db.session.add(product)
    #     db.session.commit()

    #     token = generate_token('Admin')
    #     headers = {'Authorization': f'Bearer {token}'}
    #     response = self.app.delete(f'/products/{product.id}', headers=headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], product.id)

    # def test_delete_product_unauthorized(self):
    #     product = Product(name="Sản phẩm cần xóa")
    #     db.session.add(product)
    #     db.session.commit()

    #     token = generate_token('User')  # User không có quyền xóa
    #     headers = {'Authorization': f'Bearer {token}'}
    #     response = self.app.delete(f'/products/{product.id}', headers=headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 403)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'Permission not found.')