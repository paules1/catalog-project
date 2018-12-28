#!/usr/bin/python

from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import jsonify
from flask import abort
from flask import redirect
from flask import url_for
from flask import session as login_session
from flask import make_response

import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import hmac
import hashlib
from core.datahelper import DataHelper

app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.debug = True


@app.route('/', methods=['GET'])
def home():
    dh = DataHelper()
    categories = dh.get_categories()
    return render_template('home.html', categories=categories)


@app.route('/<category_name>/list')
def by_category():
    return 'By Category..'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
