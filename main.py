import sqlite3
import json

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()

    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (user_id, user_name, balance) VALUES (?, ?, ?)', (data["user_id"], data["user_name"], data["balance"]))
    conn.commit()
    conn.close()

    return {"user_id": data["user_id"], "user_name": data["user_name"], "balance": data["balance"]}, 201


@app.route('/api/wallets/<int:wallet_id>', methods=['PUT'])
def add_wallet(wallet_id=None):
    data = request.get_json()

    if data['recharge'] < 100 or data['recharge'] > 10000:
        return {
            "message": f"invalid amount: {data['recharge']}"
        }, 400

    conn = sqlite3.connect('sqlite.db')
    result = conn.cursor().execute("SELECT * FROM users WHERE user_id = ?", (wallet_id,)).fetchone()
    if result is None:
        return {
            "message": f"wallet with id: {wallet_id} was not found"
        }, 404

    db = sqlite3.connect("sqlite.db")
    db.cursor().execute("UPDATE users SET balance = ? WHERE user_id = ?", (data["recharge"] + result[2], wallet_id))
    db.commit()
    db.close()
    result = conn.cursor().execute("SELECT * FROM users WHERE user_id = ?", (wallet_id,)).fetchone()

    response = {
        "wallet_id": wallet_id,
        "balance": result[2],
        "wallet_user": {
            "user_id": result[0],
            "user_name": result[1]
        }
    }
    response = jsonify(response)
    return response, 200

@app.route('/api/wallets/<int:wallet_id>', methods=['GET'])
def get_wallet(wallet_id=None):
    # data = request.get_json()
    conn = sqlite3.connect('sqlite.db')
    result = conn.cursor().execute("SELECT * FROM users WHERE user_id = ?", (wallet_id,)).fetchone()
    if result is None:
        return {
            "message": f"wallet with id: {wallet_id} was not found"
        }, 404
    response = {
        "wallet_id": wallet_id,
        "balance": result[2],
        "wallet_user": {
            "user_id": result[0],
            "user_name": result[1]
        }
    }
    response = jsonify(response)
    return response, 200


@app.route("/api/stations", methods=["POST"])
def route_create_station():
    """Simple API for creating station"""

    data = request.get_json()

    db = sqlite3.connect("sqlite.db")
    db.cursor().execute("INSERT INTO station (station_id, station_name, longitude, latitude) VALUES (?, ?, ?, ?)",
                        (data["station_id"], data["station_name"], data["longitude"], data["latitude"]))
    db.commit()
    db.close()

    return data, 201


@app.route("/api/stations", methods=["GET"])
def route_fetch_all_stations():
    """Simple API for fetching all stations info"""

    db = sqlite3.connect("sqlite.db")
    db.row_factory = sqlite3.Row

    result = db.cursor().execute("SELECT * FROM station", ).fetchall()

    db.commit()
    db.close()

    stations = [dict(row) for row in result]

    return {"stations": stations}, 200


@app.route("/api/trains", methods=["POST"])
def route_create_train():
    """Simple API for Creating train info"""
    data = request.get_json()
    db = sqlite3.connect("sqlite.db")
    cnt = 0
    ser_st = ""
    ser_end = ""
    for stops in data["stops"]:
        cnt += 1
        if cnt == 1:
            ser_st = stops["departure_time"]
        ser_end = stops["arrival_time"]
        db.cursor().execute(
            "INSERT INTO train_stop (train_id, station_id, arrival_time, departure_time, fare) VALUES (?, ?, ?, ?, ?)",
            (data["train_id"], stops["station_id"], stops["arrival_time"], stops["departure_time"], stops["fare"]))

    db.cursor().execute(
        "INSERT INTO train (train_id, train_name, capacity, service_start, service_ends) VALUES (?, ?, ?, ?, ?)",
        (data["train_id"], data["train_name"], data["capacity"], ser_st, ser_end))

    db.commit()
    db.close()

    return {
        "train_id": data["train_id"],
        "train_name": data["train_name"],
        "capacity": data["capacity"],
        "service_start": ser_st,
        "service_ends": ser_end,
        "num_stations": cnt
    }, 201


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
        return {"message": "book with id: "+str(id)+" was not found"}, 404

    db = sqlite3.connect("sqlite.db")
    db.cursor().execute("UPDATE books SET title = ?, author = ?, genre = ?, price = ? WHERE id = ?", ( data["title"], data["author"], data["genre"], data["price"], id))
    db.commit()
    db.close()

    data["id"] = id

    return data, 200




# @app.route("/api/books", methods=["GET"])
# def route_fetch_all_books():
#     """Simple API for fetching all books info"""
#
#     db = sqlite3.connect("sqlite.db")
#     db.row_factory = sqlite3.Row
#
#     result = db.cursor().execute("SELECT * FROM books",).fetchall()
#
#     db.commit()
#     db.close()
#
#     books = [dict(row) for row in result]
#
#     return {"books": books}, 200
#
#
# # @app.route("/api/books", methods=["GET"])
# # def route_search_books():
#     """Simple API for fetching all books info by searching"""

#     search_field = ''
#     # Get query parameters
#     value = request.args.get('title', None)
#     if value :
#         search_field = 'title'
#     else :
#         value = request.args.get('author', None)
#         if value:
#             search_field = 'author'
#         else:
#             value = request.args.get('genre', None)
#             if value:
#                 search_field = 'genre'
#             else:
#                 return route_fetch_all_books()

#     sort_field = request.args.get('sort', 'id')
#     order = request.args.get('order', 'asc')

#     db = sqlite3.connect("sqlite.db")
#     db.row_factory = sqlite3.Row  # Set row factory to use row objects

#     # Build the SQL query
#     query = "SELECT * FROM books"

#     # Add filtering if search_field and value are provided
#     if search_field and value:
#         query += f" WHERE {search_field} = ?"

#     # Add sorting
#     query += f" ORDER BY {sort_field} {'DESC' if order.lower() == 'desc' else 'ASC'}"

#     # Execute the query with parameters
#     if search_field and value:
#         result = db.cursor().execute(query, (value,)).fetchall()
#     else:
#         result = db.cursor().execute(query).fetchall()

#     # Convert each row to a dictionary (JSON object)
#     books = [dict(row) for row in result]

#     return {"books" : books}, 200


if __name__ == "__main__":
    app.run()
