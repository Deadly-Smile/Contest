import sqlite3
import json

from flask import Flask, request

app = Flask(__name__)


def create_user(user_id, user_name, balance):
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (user_id, user_name, balance) VALUES (?, ?, ?)', (user_id, user_name, balance))
    conn.commit()
    conn.close()

@app.route('/api/users', methods=['POST'])
def create_user():
    user_data = request.json
    user_id = user_data.get('user_id')
    user_name = user_data.get('user_name')
    balance = user_data.get('balance')
    
    # Validate user data
    if not isinstance(user_id, int):
        return jsonify({'error': 'user_id must be an integer'}), 400
    if not isinstance(user_name, str):
        return jsonify({'error': 'user_name must be a string'}), 400
    if not isinstance(balance, int):
        return jsonify({'error': 'balance must be an integer'}), 400
    
    # Check if user_id already exists
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    if cursor.fetchone() is not None:
        conn.close()
        return jsonify({'error': 'user_id already exists'}), 400
    
    # Create the user
    create_user(user_id, user_name, balance)
    
    return jsonify({'message': 'User created successfully'}), 201



@app.route("/api/stations", methods=["POST"])
def route_create_station():
    """Simple API for creating station"""

    data = request.get_json()

    db = sqlite3.connect("sqlite.db")
    db.cursor().execute("INSERT INTO station (station_id, station_name, longitude, latitude) VALUES (?, ?, ?, ?)", (data["station_id"], data["station_name"], data["longitude"], data["latitude"]))
    db.commit()
    db.close()

    return data, 201


@app.route("/api/stations", methods=["GET"])
def route_fetch_all_stations():
    """Simple API for fetching all stations info"""

    db = sqlite3.connect("sqlite.db")
    db.row_factory = sqlite3.Row

    result = db.cursor().execute("SELECT * FROM station",).fetchall()
    
    db.commit()
    db.close()

    stations = [dict(row) for row in result]

    return {"stations" : stations}, 200

@app.route("/api/trains", methods=["POST"])
def route_create_train():
    """Simple API for Creating train info"""
    data = request.get_json()
    db = sqlite3.connect("sqlite.db")
    cnt = 0
    ser_st = ""
    ser_end = ""
    for stops in data["stops"]:
        cnt+=1
        if cnt == 1:
            ser_st = stops["departure_time"]
        ser_end =  stops["arrival_time"]
        db.cursor().execute("INSERT INTO train_stop (train_id, station_id, arrival_time, departure_time, fare) VALUES (?, ?, ?, ?, ?)", (data["train_id"], stops["station_id"], stops["arrival_time"], stops["departure_time"], stops["fare"]))
   
    db.cursor().execute("INSERT INTO train (train_id, train_name, capacity, service_start, service_ends) VALUES (?, ?, ?, ?, ?)", (data["train_id"], data["train_name"], data["capacity"], ser_st, ser_end))
    
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
