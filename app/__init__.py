# Import flask and template operators
from flask import Flask, render_template

# Define the WSGI application object
app = Flask(__name__)


# todo turn this into a blueprint
from app.controllers import app
