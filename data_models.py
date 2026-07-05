"""
Data models for the Book-Alchemy library.
Defines the database schema for authors and books using SQLAlchemy.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    """
    Model representing an author.
    Attributes:
        id (int): Unique identifier.
        name (str): Author's name.
        birth_date (date): Date of birth.
        date_of_death (date): Date of death.
    """
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    birth_date = db.Column(db.Date)
    date_of_death = db.Column(db.Date)

    def __repr__(self):
        return f"<Author: {self.name}>"

    def __str__(self):
        return f"{self.name}"


class Book(db.Model):
    """
    Model representing a book.
    Attributes:
        id (int): Unique identifier.
        title (str): Book title.
        isbn (str): International Standard Book Number.
        author_id (int): ID of the author who wrote the book.
    """
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120))
    isbn = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    author = db.relationship('Author', backref='books')  # needed to query for author name

    def __repr__(self):
        return f"<Book: {self.title}>"

    def __str__(self):
        return f"{self.title}"
