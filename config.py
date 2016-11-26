DEBUG = True

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "hackme"

SHOPIFY_APPLICATION_NAME="Hello World App"
SHOPIFY_APPLICATION_KEY="dd55a795732727073f59ad785b01dcd4"
SHOPIFY_APPLICATION_SECRET="e3508e0583edc55ef779f6ea62c731a8"
SHOPIFY_APPLICATION_SCOPES="read_orders"
