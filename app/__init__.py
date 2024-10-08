from flask import Flask, g
from .app_factory import create_app
from .db_connect import close_db, get_db
import os

app = create_app()
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret')  # Use an environment variable for the secret key

# Register Blueprints
from app.blueprints.books import books
from app.blueprints.authors import authors

app.register_blueprint(books)
app.register_blueprint(authors)

from . import routes

@app.before_request
def before_request():
    g.db = get_db()

# Setup database connection teardown
@app.teardown_appcontext
def teardown_db(exception=None):
    close_db(exception)