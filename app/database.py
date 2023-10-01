import psycopg2
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(current_app.config['SQLALCHEMY_DATABASE_URI'])
    return g.db
