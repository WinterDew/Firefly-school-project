from flask import Flask, render_template, url_for, request
from flask import redirect, session, flash
from bcrypt import hashpw,checkpw,gensalt
import sqlite3 as db
import os
from datetime import datetime

def db_setup():
    conn = db.connect(f"{os.path.dirname(__file__)}/firefly.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT, date_joined DATETIME);""")
    conn.commit()
    cur.close()
    conn.close()
db_setup()


app = Flask(__name__)
app.config['SECRET_KEY'] = '#tr5988fhdskghlkoifayfgghakf'

@app.route("/")
def index():
    if len(session) == 0:
        return redirect(url_for("login"))
    else:
        return f"Hello {session['username']}"
    
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login/auth",methods=["POST"])
def auth():
    conn = db.connect(f"{os.path.dirname(__file__)}/firefly.db")
    cur = conn.cursor()
    username = request.json["username"]
    password = request.json["password"]
    if cur.execute("SELECT username FROM users WHERE username= ?;",(username,)).fetchall() == None:
        flash("User Does Not Exist, Try Signing In.")
        cur.close()
        conn.close()
        return redirect(url_for("login"))
    else:
        session["username"] = username
        return redirect(url_for("index"))
    

@app.route("/login/signup",methods=["POST"])
def signup():
    # connect to database
    # get json username and password and hash
    # Put new user into db
    # or redirect to login.

    conn = db.connect(f"{os.path.dirname(__file__)}/firefly.db")
    cur = conn.cursor()
    print(request.json)
    username = request.json["username"]
    password = hashpw(request.json["password"].encode("UTF-8"),gensalt())
    if cur.execute("SELECT username FROM users WHERE username= ?;",(username,)).fetchall() == None: 
        cur.execute("INSERT INTO users VALUES (?,?,?);",(username,password,datetime.timestamp()))
        conn.commit()
        cur.close()
        conn.close()
        flash("User successfully added, Please login.")
        return redirect(url_for("login"))
    else:
        flash("User already exists, Please login instead.")
        cur.close()
        conn.close()
        return(redirect(url_for("login")))

if __name__ == "__main__":
    app.run("127.0.0.1",9800,True)