#!/usr/bin/env python
import os
import logging
import datetime
import functools
from flask_migrate import Migrate
import jwt
from dotenv import load_dotenv

# pylint: disable=import-error
from flask import Flask, jsonify, request, abort

from model import setup_db, db

load_dotenv()
JWT_SECRET = os.environ.get('JWT_SECRET', 'abc123abc1234')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
DATABASE_URI = os.environ.get('DATABASE_URI', 'postgresql://postgres:123qwe@localhost:5432/BlogSite')

app = Flask(__name__)
setup_db(app, DATABASE_URI) 
migrate = Migrate(app, db)


@app.route('/', methods=['POST', 'GET'])
def health():
    return jsonify("Hello world!")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
