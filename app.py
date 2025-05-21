from flask import Flask, render_template, request, flash, redirect, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book 
import os
from datetime import datetime
from sqlalchemy import func

app = Flask(__name__)

# Update the database URI to use an absolute path
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "data", "library.sqlite")}'

db.init_app(app)


@app.route('/')
def home():
    """
    Home page route. Queries all books from the database and renders the home.html template with the books data.
    Allows sorting by title or author name based on query parameters.
    Also supports keyword search in book titles.
    Displays success messages for actions like book deletion.
    """
    sort_by = request.args.get('sort_by', 'title')
    search_query = request.args.get('search', '')

    query = Book.query

    if search_query:
        query = query.filter(Book.title.ilike(f"%{search_query}%"))

    if sort_by == 'author':
        books = query.join(Author).order_by(Author.name).all()
    else:
        books = query.order_by(func.lower(Book.title)).all()

    no_results = not books and search_query

    # Explicitly handle flashed messages
    messages = get_flashed_messages(with_categories=True)

    return render_template('home.html', books=books, sort_by=sort_by, search_query=search_query, no_results=no_results, messages=messages)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Handle the form for adding a new author to the database. Accepts GET and POST requests.
    On POST, validates and processes the form data, adds the author if valid, and flashes a message.
    Renders the add_author.html template.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        birth_date_str = request.form.get('birthdate')
        date_of_death_str = request.form.get('date_of_death')

        try:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None
            date_of_death = datetime.strptime(date_of_death_str, '%Y-%m-%d').date() if date_of_death_str else None

            if name:
                new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
                db.session.add(new_author)
                db.session.commit()
                flash('Author added successfully!', 'success')
            else:
                flash('Name is required!', 'error')
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'error')

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Handle the form for adding a new book to the database. Accepts GET and POST requests.
    On POST, validates and processes the form data, adds the book if valid, and flashes a message.
    Renders the add_book.html template with the list of authors.
    """
    if request.method == 'POST':
        title = request.form.get('title')
        author_id = request.form.get('author_id')
        publication_year = request.form.get('publication_year')
        isbn = request.form.get('isbn')

        if title and author_id and isbn:
            new_book = Book(title=title, author_id=author_id, publication_year=publication_year, isbn=isbn)
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully!', 'success')
        else:
            flash('Title, Author, and ISBN are required!', 'error')

    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    """
    Deletes a specific book from the database. If the book's author has no other books, deletes the author as well.
    Redirects to the homepage with a success message after deletion.
    """
    book = Book.query.get_or_404(book_id)
    author = book.author

    db.session.delete(book)
    db.session.commit()

    # Check if the author has any other books
    if not author.books:
        db.session.delete(author)
        db.session.commit()

    flash(f"Book '{book.title}' deleted successfully!", 'success')
    return redirect('/')


def main():
    print(f"Using database file: {os.path.join(base_dir, 'data', 'library.sqlite')}")
    app.secret_key = 'your_secret_key_here'  # Replace with a secure key
    app.run(debug=True)

if __name__ == "__main__":
    main()


""" run one time to create the database tables """
# with app.app_context():
#     db.create_all