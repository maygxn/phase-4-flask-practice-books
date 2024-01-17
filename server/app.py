#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_restful import Api, Resource
from flask_migrate import Migrate

from models import db, Author, Publisher, Book # import your models here!

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.get('/')
def index():
    return "Hello world"

# write your routes here!
# route for author routes
@app.route('/authors/<int:id>', methods=['GET', 'DELETE'])
def author_by_id(id):
    author = Author.query.filter(Author.id == id).first()

    if request.method == 'GET':
        try:
            response = make_response(
                author.to_dict(),
                200
            )
        except:
            response = make_response(
                {"Error": "Author_ID does not exist"},
                404
            )
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(author)
            db.session.commit()
            response = make_response(
                {},
                204
            )
        except:
            response = make_response(
                {'Error': "Author not found"},
                404
            )
    return response

@app.route('/books', methods=['GET', 'POST'])
def get_books():
    books = [book.to_dict() for book in Book.query.all()]

    if request.method == 'GET':
        response = make_response(
            books,
            200
        )
    
    elif request.method ==  'POST':
        try:
            form_data = request.get_json()

            new_book = Book(
                title = form_data["title"],
                page_count = form_data["page_count"],
                author_id = form_data["author_id"],
                publisher_id = form_data["publisher_id"]
            )

            db.session.add(new_book)
            db.session.commit()

            response = make_response(
                new_book.to_dict(),
                201
            )
        except ValueError:
            response = make_response(
                {"Errors": ["Validation errors"]},
                400
            )
        
    return response

@app.route('/publishers/<int:id>', methods=['GET'])
def publisher_by_id(id):
    publisher = Publisher.query.filter(Publisher.id == id).first()

    if request.method == 'GET':
        try:
            response = make_response(
                publisher.to_dict(),
                200
            )
        except:
            response = make_response(
                {"Error": "Publisher_ID does not exist"},
                404
            )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
