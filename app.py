from flask import Flask, request, jsonify, json, make_response
from mongoengine import connect, Document, StringField, IntField

app = Flask(__name__)


connect( db='Book', username='Admin', password='admin', host='mongodb+srv://Admin:admin@cluster0.joaaq.mongodb.net/Book?retryWrites=true&w=majority')

class Book(Document):
    _id = IntField()
    name = StringField()
    author = StringField()

    def to_json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "author": self.author
        }

@app.route("/", methods=['GET'])
def ok():
    return {
        "message": "The API is working fine."
    }

@app.route("/book", methods=['GET'])
def read_Book():
    results = Book.objects()
    allBooks = []
    for result in results:
        # result._id = str(result._id)
        bookObject = {
            "_id": result._id,
            "name": result.name,
            "author": result.author
        }
        allBooks.append(bookObject)
    
    resp = make_response(jsonify(allBooks))
    return resp

@app.route("/book/createBook", methods=['POST'])
def create_Book():
    
    book_id = request.form["id"]
    book_name = request.form['name']
    book_author = request.form['author']
    
    book = Book (
        _id = str(book_id),
        name = book_name,
        author = book_author
    )
    book.save()

    resp = make_response({
        "message": book.name +" added to database"
    })

    return resp

@app.route("/book/deleteBook/<bookID>", methods=["DELETE"])
def delete_Book(bookID):
    toDelete = Book.objects.get(_id=str(bookID))
    Book.objects(_id=str(bookID)).delete()

    resp = make_response({
        "message": toDelete.name + " Deleted from Database"
    })

    return resp

@app.route("/book/updateBook/<bookID>", methods=["PUT"])
def update_Book(bookID):
    book = Book.objects.get(_id=str(bookID))
    book_name = request.form['name']
    book_author = request.form['author']
    Book.objects(_id=str(bookID)).update(name=book_name, author=book_author)


    resp = make_response({
        "message": book.name + " Updated"
    })
    
    return resp


if (__name__ == "__main__"):
    app.run(debug=True)
