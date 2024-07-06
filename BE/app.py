#!/usr/bin/env python
import os
import logging
import datetime
import functools
from flask_migrate import Migrate
import jwt
from dotenv import load_dotenv
from auth import AuthError, requires_auth


# pylint: disable=import-error
from flask import Flask, jsonify, request, abort

from model import setup_db, db, Product, Serial
from flask_cors import CORS, cross_origin

load_dotenv()
JWT_SECRET = os.environ.get('JWT_SECRET', 'abc123abc1234')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
DATABASE_URI = os.environ.get('DATABASE_URI', 'postgresql://postgres:123qwe@localhost:5432/BlogSite')
URL_CLIENT = os.environ.get('URL_CLIENT', 'http://localhost:4200')

app = Flask(__name__)
setup_db(app, DATABASE_URI)
migrate = Migrate(app, db)
cors = CORS(app, resources={r"/*": {"origins": URL_CLIENT}})

@app.route('/products', methods=['GET'])
@cross_origin()
def get_products():
    products = Product.query.all()

    product_list = []
    for product in products:
        num_serials = Serial.query.filter_by(product_id=product.id).count()
        product_list.append({
            'id': product.id,
            'name': product.name,
            'countSerial': num_serials
        })

    return jsonify({
        'success': True,
        'products': product_list
    }), 200


@app.route('/products/<int:id>', methods=['GET'])
# @requires_auth('get:products-detail')
def get_product_detail(id):
    product = Product.query.get(id)
    if not product:
        abort(404)
    serials = Serial.query.filter(Serial.product_id == id).all()
    return jsonify({
        'success': True,
        'product': product.format(),
        'serials': [s.imei for s in serials]
    }), 200


@app.route('/products', methods=['POST'])
@requires_auth('post:products')
def create_product(payload):
    req = request.get_json()
    try:
        new_product = Product(name=req.get('name'))
        new_product.insert()
        return jsonify({
            'success': True,
            'product': new_product.format()
        }), 201
    except Exception as e:
        logging.error(f"Error creating product: {e}")
        abort(422)


@app.route('/products/<int:id>', methods=['PATCH'])
@requires_auth('patch:products')
def update_product(payload, id):
    req = request.get_json()
    product = Product.query.get(id)
    if not product:
        abort(404)
    try:
        if 'name' in req:
            product.name = req.get('name')
        product.update()
        return jsonify({
            'success': True,
            'product': product.format()
        }), 200
    except Exception as e:
        logging.error(f"Error updating product: {e}")
        abort(422)


@app.route('/products/<int:id>', methods=['DELETE'])
@requires_auth('delete:products')
def delete_product(payload, id):
    product = Product.query.get(id)
    if not product:
        abort(404)
    try:
        product.delete()
        return jsonify({
            'success': True,
            'delete': id
        }), 200
    except Exception as e:
        logging.error(f"Error deleting product: {e}")
        abort(422)

@app.route('/CreateProducts', methods=['POST'])
@requires_auth('post:products')
def create_product_and_serial(payload):
    try:
        data = request.get_json()
        logging.error(data)
        product_name = data.get('name')
        imeis = data.get('imeis')
        if not product_name:
            abort(
                400, description="Data invalid.Should have productname")
        
        

        product = Product.query.filter_by(name=product_name).first()
        if not product:
            product = Product(name=product_name)
            product.insert()

        created_serials = []
        if imeis or isinstance(imeis, list):
            for imei in imeis:
                if Serial.query.filter_by(imei=imei).first():
                    continue
                new_serial = Serial(imei=imei, product_id=product.id)
                new_serial.insert()
                created_serials.append(new_serial.format())

        return jsonify({
            'success': True,
            'product': product.format(),
            'created_serials': created_serials
        }), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Lỗi khi tạo serial: {e}")
        abort(500)


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'Unathorized'
    }), 401


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Internal Server Error'
    }), 500


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": 'Bad Request'
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": 'Method Not Allowed'
    }), 405


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
