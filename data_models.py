from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """
    Represents an author in the library database, including name, birth date, and date of death.
    """
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    def __repr__(self):
        """
        Return a string representation of the Author instance for debugging.
        """
        return f"<Author(id={self.id}, name='{self.name}')>"

    def __str__(self):
        """
        Return a user-friendly string representation of the Author instance.
        """
        return f"Author: {self.name}"


class Book(db.Model):
    """
    Represents a book in the library database, including ISBN, title, publication year, and author.
    """
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), nullable=False, unique=True)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)

    def __repr__(self):
        """
        Return a string representation of the Book instance for debugging.
        """
        return f"<Book(id={self.id}, title='{self.title}', isbn='{self.isbn}')>"

    def __str__(self):
        """
        Return a user-friendly string representation of the Book instance.
        """
        return f"Book: {self.title} (ISBN: {self.isbn})"


