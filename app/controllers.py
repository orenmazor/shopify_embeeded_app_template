from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
app.config.from_object('config')

@app.route('/login', methods=['GET'])
def login():
    shop = request.args.get('shop')
    if shop:
        return redirect("https://{0}/admin/oauth/authorize?client_id={1}&scope={2}&redirect_uri={3}".format(shop, app.config['SHOPIFY_APPLICATION_KEY'], app.config['SHOPIFY_APPLICATION_SCOPES'], url_for("callback", _external=True)))
    else:
        return render_template("login.html")

@app.route('/login', methods=['POST'])
def authenticate():
    pass


@app.route('/auth/shopify/callback', methods=['GET'])
def callback():
    pass

@app.route('/logout', methods=['GET'])
def logout():
    pass

