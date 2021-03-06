from flask import Flask, render_template, request, redirect, url_for, abort, flash, session
from models import Shop, db
from shopify import Shop
import requests
import json
import hashlib
import hmac

app = Flask(__name__)
app.config.from_object('config')

@app.route('/login', methods=['GET'])
def login():
    shop = request.args.get('shop')
    if shop:
        return redirect("https://{0}/admin/oauth/authorize?client_id={1}&scope={2}&redirect_uri={3}".format(shop, app.config['SHOPIFY_APPLICATION_KEY'], app.config['SHOPIFY_APPLICATION_SCOPES'], url_for("callback", _external=True)))
    else:
        return render_template("login.html")

@app.route('/auth/shopify/callback', methods=['GET'])
def callback():
    shop = request.args.get('shop')
    code = request.args.get('code')
    given_hmac = request.args.get('hmac')

    #validate the hmac, to make sure we're not being screwed around with
    h = dict([(key,value) for key, value in request.args.items() if key not in ['hmac','signature']])

    # now sort lexicographically and turn into querystring
    query = '&'.join(["{0}={1}".format(key, h[key]) for key in sorted(h)])

    # generate the digest
    digest = hmac.new(app.config['SHOPIFY_APPLICATION_SECRET'], msg=query, digestmod=hashlib.sha256).hexdigest()

    if given_hmac != digest:
        abort(403, "Authentication failed. Digest provided was: {0}".format(digest))
    else:
        # we're in! get an access token
        payload = {'client_id': app.config['SHOPIFY_APPLICATION_KEY'],'client_secret': app.config['SHOPIFY_APPLICATION_SECRET'],'code': code}

        result = requests.post("https://{}/admin/oauth/access_token".format(shop), data=payload)

        current_shop = Shop.query.filter(Shop.shopify_domain == shop).first()

        if current_shop is None:
            access_token = json.loads(result.text)['access_token']
            current_shop = Shop(shop, access_token)
            current_shop.Save()

        if current_shop is not None:
            session["shop_id"] = current_shop.id
            session["shopify_domain"] = current_shop.shopify_domain

        return redirect("/")

@app.route('/logout', methods=['GET'])
def logout():
    del session["shop_id"]
    del session["shopify_domain"]

# actual app logic here
@app.route('/', methods=['GET'])
def index():
    if session.get("shop_id"):
        current_shop = Shop.query.filter(Shop.id == session.get("shop_id")).first()
        with current_shop:
            flash("Hello {}".format(Shop.current().shop_owner))

        return render_template("embedded/index.html")
    else:
        return redirect("/login")

