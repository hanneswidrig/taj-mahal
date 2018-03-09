# Pip Dependencies
from flask import Flask, render_template, request, flash, redirect, url_for
import sys

# Imported Project Files
import db
import secrets

app = Flask('Gardener\'s Exchange')
app.config['SECRET_KEY'] = secrets.secret_flask_key()

@app.before_request
def before_request():
  pass # db.open_db()

def after_request():
  pass # db.close_db()

@app.route('/')
def index():
  return render_template('index.html')

app.run(host='0.0.0.0', port=8080, debug=True)