# BookAlchemy

BookAlchemy is a Flask-based web application for managing a library of books and authors. Users can add, search, sort, and delete books and authors.

## Features
- Add new books and authors.
- Search for books by title.
- Sort books by title or author name.
- Delete books and their authors (if the author has no other books).

## Prerequisites
- Python 3.7 or higher
- Flask
- Flask-SQLAlchemy

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd BookAlchemy
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```bash
   python
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

## Running the App
1. Start the Flask development server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## File Structure
- `app.py`: Main application file containing routes and logic.
- `data_models.py`: Database models for books and authors.
- `templates/`: HTML templates for the web interface.
- `data/library.sqlite`: SQLite database file.

## License
This project is licensed under the MIT License.
