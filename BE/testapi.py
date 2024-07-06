import unittest
import json
from app import app, db, Product, Serial

class ProductTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Sử dụng cơ sở dữ liệu tạm thời
        self.app = app.test_client()
        db.init_app(app)
        db.create_all()

        self.test_product = {"name": "Sản phẩm kiểm thử"}
        self.test_serial = {"name": "Sản phẩm kiểm thử", "imeis": ["123456789012345", "098765432109876"]}

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
        response = self.app.post('/products', json=self.test_product)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)  # Chưa xác thực nên sẽ trả về 401
        self.assertEqual(data['success'], False)

    def test_create_product_and_serial(self):
        response = self.app.post('/CreateProducts', json=self.test_serial)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)  # Chưa xác thực nên sẽ trả về 401
        self.assertEqual(data['success'], False)

    def test_404_product_not_found(self):
        response = self.app.get('/products/9999')  # ID không tồn tại
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')