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

from model import setup_db, db
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

@app.route('/', methods=['POST', 'GET'])
def health():
    return jsonify("Hello world!!!!!")




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
    app.run(host='127.0.0.1', port=8080, debug=True)
