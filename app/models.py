from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopify_app.db'
db = SQLAlchemy(app)

class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shopify_domain = db.Column(db.String(256), unique=True)
    shopify_token = db.Column(db.String(128), unique=True)

    def __init__(self, shopify_domain, shopify_token):
        self.shopify_domain = shopify_domain
        self.shopify_token = shopify_token
        
    def __repr__(self):
        return '<Shop %r>' % self.shopify_domain

    def Save(self):
        db.session.add(self)
        db.session.commit()

