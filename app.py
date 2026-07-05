from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from data_models import db, Author, Book
from utils import parse_date

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)

@app.route('/')
def index():
    sort_by = request.args.get('sort_by', 'title')
    q = request.args.get('q', '').strip()

    query = Book.query.join(Author)

    if q:
        query = query.filter(
            db.or_(
                Book.title.ilike(f"%{q}%"),
                Author.name.ilike(f"%{q}%")
            )
        ) # db.or_ builds SQL like WHERE title LIKE '%q%' OR name LIKE '%q%'

    if sort_by == 'author':
        query = query.order_by(Author.name, Book.title)
    else:
        sort_by = 'title'
        query = query.order_by(Book.title)

    all_books = query.all()
    return render_template('home.html', books=all_books, sort_by=sort_by, q=q)


@app.route('/add_author', methods=['GET','POST'])
def add_author():
    message = None
    error = False
    if request.method == "POST":

        new_author = Author(
            name=request.form.get('name'),
            birth_date=parse_date(request.form.get('birth_date')),
            date_of_death=parse_date(request.form.get('date_of_death'))
        )

        try:
            db.session.add(new_author)
            db.session.commit()
            message = f"Author {new_author.name} has been added to the database."
        except Exception as e:
            db.session.rollback() # needed here to take new_author out of staging (add()) when commit() fails
            message = f"An error occurred when tyring to add the author: {e}"
            error = True
        return render_template('add_author.html', author=new_author, message=message, error=error)

    else:
        return render_template('add_author.html')

@app.route('/add_book', methods=['GET','POST'])
def add_book():
    all_authors = Author.query.all()

    message = None
    error = False
    if request.method == "POST":

        new_book = Book(
            author_id=request.form.get('author'),
            title=request.form.get('title'),
            isbn= request.form.get('isbn')
        )

        try:
            db.session.add(new_book)
            db.session.commit()
            message = f"Book {new_book.title} has been added to the database."
        except Exception as e:
            db.session.rollback() # needed here to take new_book out of staging (add()) when commit() fails
            message = f"An error occurred when tyring to add the book: {e}"
            error = True
        return render_template('add_book.html', authors=all_authors, message=message, error=error)
    else:
        return render_template('add_book.html', authors=all_authors)



if __name__ == "__main__":
    app.run(debug=True, port=5001)




# with app.app_context():
#     db.create_all()