#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

# GET /bakeries → all bakeries
@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    response = [bakery.to_dict() for bakery in bakeries]
    return make_response(jsonify(response), 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    response = bakery.to_dict()  
    # SerializerMixin automatically handles nested baked_goods 
    return make_response(jsonify(response), 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    response = [bg.to_dict() for bg in baked_goods]
    return make_response(jsonify(response), 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    response = baked_good.to_dict()
    return make_response(jsonify(response), 200)