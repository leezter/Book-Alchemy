from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book 
import os

app = Flask(__name__)

# Update the database URI to use an absolute path
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "data", "library.sqlite")}'

db.init_app(app)


""" run one time to create the database tables """
# with app.app_context():
#     db.create_all()



