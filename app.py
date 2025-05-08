from flask import Flask, render_template, request, flash
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

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form.get('name')
        birth_date = request.form.get('birthdate')
        date_of_death = request.form.get('date_of_death')

        if name:
            new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
            db.session.add(new_author)
            db.session.commit()
            flash('Author added successfully!', 'success')
        else:
            flash('Name is required!', 'error')

    return render_template('add_author.html')



