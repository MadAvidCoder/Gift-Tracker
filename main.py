import flask
import sqlite3
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = flask.Flask(
    __name__,
    static_folder="static",
    static_url_path="/"
)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day"],
    storage_uri="memory://",
)

conn = sqlite3.connect('gifts.db') 
cursor = conn.cursor()  
cursor.execute('''
    CREATE TABLE IF NOT EXISTS gifts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        gift TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

@app.errorhandler(404)
def not_found(e):
    return flask.send_from_directory("static", "404.html")

@app.get("/")
@limiter.exempt
def index():
    return flask.send_from_directory("static", "index.html")

@app.get("/dashboard")
@limiter.exempt
def dashboard():
    return flask.send_from_directory("static", "dashboard.html")

@app.post("/gifts")
@limiter.limit("50 per day")
def add_gift():
    data = flask.request.get_json()
    name = data.get("name")
    gift = data.get("gift")
    
    if not name or not gift:
        return "Name and gift are required", 400

    conn = sqlite3.connect('gifts.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO gifts (name, gift) VALUES (?, ?)', (name, gift))
    conn.commit()
    conn.close()
    
    return "Gift Added", 201

@app.get("/gifts")
@limiter.limit("1 per second")
def get_gifts():
    conn = sqlite3.connect('gifts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, gift FROM gifts")
    res = cursor.fetchall()
    conn.close()

    gifts = [{'id': row[0], 'name': row[1], 'gift': row[2]} for row in res]
    return flask.jsonify(gifts)

if __name__ == "__main__":
    app.run()