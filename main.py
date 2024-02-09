import sqlite3
import json

from flask import Flask, request

app = Flask(__name__)


@app.route("/api/books", methods=["POST"])
def route_create_book():
    """Simple API for storing book info"""

    data = request.get_json()

    db = sqlite3.connect("sqlite.db")
    db.cursor().execute("INSERT INTO books (id, title, author, genre, price) VALUES (?, ?, ?, ?, ?)", (data["id"], data["title"], data["author"], data["genre"], data["price"]))
    db.commit()
    db.close()

    return data, 201

@app.route("/api/books/<int:id>", methods=["PUT"])
def route_update_book(id):
    """Simple API for updating book info"""

    data = request.get_json()

    db = sqlite3.connect("sqlite.db")

    result = db.cursor().execute("SELECT id FROM books WHERE id = ?", (id,)).fetchone()

    if result is None:
        return {"message" : "book with id: "+str(id)+" was not found"}, 404
   
    db = sqlite3.connect("sqlite.db")
    db.cursor().execute("UPDATE books SET title = ?, author = ?, genre = ?, price = ? WHERE id = ?", ( data["title"], data["author"], data["genre"], data["price"], id))
    db.commit()
    db.close()

    data["id"] = id

    return data, 200

    
# @app.route("/api/books", methods=["GET"])
def route_fetch_all_books():
    """Simple API for fetching all books info"""

    db = sqlite3.connect("sqlite.db")
    db.row_factory = sqlite3.Row

    result = db.cursor().execute("SELECT * FROM books",).fetchall()
    
    db.commit()
    db.close()

    books = [dict(row) for row in result]

    return {"books" : books}, 200


@app.route("/api/books", methods=["GET"])
def route_search_books():
    """Simple API for fetching all books info by searching"""

    search_field = ''
    # Get query parameters
    value = request.args.get('title', None)
    if value :
        search_field = 'title'
    else : 
        value = request.args.get('author', None)
        if value:
            search_field = 'author'
        else:
            value = request.args.get('genre', None)
            if value:
                search_field = 'genre'
            else:
                return route_fetch_all_books()
    
    sort_field = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')

    db = sqlite3.connect("sqlite.db")
    db.row_factory = sqlite3.Row  # Set row factory to use row objects

    # Build the SQL query
    query = "SELECT * FROM books"

    # Add filtering if search_field and value are provided
    if search_field and value:
        query += f" WHERE {search_field} = ?"

    # Add sorting
    query += f" ORDER BY {sort_field} {'DESC' if order.lower() == 'desc' else 'ASC'}"

    # Execute the query with parameters
    if search_field and value:
        result = db.cursor().execute(query, (value,)).fetchall()
    else:
        result = db.cursor().execute(query).fetchall()

    # Convert each row to a dictionary (JSON object)
    books = [dict(row) for row in result]

    return {"books" : books}, 200


if __name__ == "__main__":
    app.run()
