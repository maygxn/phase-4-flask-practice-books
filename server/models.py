from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# write your models here!
class Book(db.Model, SerializerMixin):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    page_count = db.Column(db.Integer, nullable=False)

    # foreign keys
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'))

    # relationships
    authors = db.relationship('Author', back_populates = 'books')
    publishers = db.relationship('Publisher', back_populates = 'books')

    # serialization rules
    # make tuple
    serialize_rules = ('-authors.books', '-publishers.books')

class Publisher(db.Model, SerializerMixin):
    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    founding_year = db.Column(db.Integer, nullable=False)

    # relationships
    books = db.relationship('Book', back_populates = 'publishers')

    # serialization rules
    # make tuple
    serialize_rules = ('-books.publishers', )


class Author(db.Model, SerializerMixin):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    pen_name = db.Column(db.String)

    # relationships
    books = db.relationship('Book', back_populates = 'authors')

    # serialization rules
    # make tuple
    serialize_rules = ('books.authors', )