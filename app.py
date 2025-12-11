from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = "your_secret_key_here"   
def get_db():
    conn = sqlite3.connect("notes.db")
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



@app.route("/")
@login_required
def index():
    conn = get_db()
    notes = conn.execute("SELECT * FROM notes WHERE user_id=?", (session["user_id"],)).fetchall()
    conn.close()
    return render_template("index.html", notes=notes)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        conn = get_db()
        conn.execute("INSERT INTO notes (title, content, user_id) VALUES (?, ?, ?)",
                     (title, content, session["user_id"]))
        conn.commit()
        conn.close()

        return redirect("/")
    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    conn = get_db()
    note = conn.execute("SELECT * FROM notes WHERE id=? AND user_id=?", (id, session["user_id"])).fetchone()

    if not note:
        return "Unauthorized access", 403

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        conn.execute("UPDATE notes SET title=?, content=? WHERE id=? AND user_id=?",
                     (title, content, id, session["user_id"]))
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("edit.html", note=note)

@app.route("/delete/<int:id>")
@login_required
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM notes WHERE id=? AND user_id=?", (id, session["user_id"]))
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_pw = generate_password_hash(password)

        conn = get_db()
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                         (username, hashed_pw))
            conn.commit()
            conn.close()
            return redirect("/login")
        except:
            return "Username already exists!"

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            return redirect("/")
        else:
            return "Invalid username or password!"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    conn = get_db()

  
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            user_id INTEGER
        )
    """)

    conn.commit()
    conn.close()

    app.run(debug=True)
