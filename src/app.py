from flask import Flask, render_template, url_for, request
from flask import redirect, session, flash
from bcrypt import hashpw,checkpw,gensalt
import sqlite3 as sql
import os
from datetime import datetime
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = '#tr5988fhdskghlkoifayfgghakf'

toast = ""

def setup_db():
    conn = sql.connect("firefly.db")
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("PRAGMA auto_vacuum = 1;")
    cur.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT NOT NULL, date_joined DATETIME NOT NULL);")
    cur.execute("CREATE TABLE IF NOT EXISTS posts(author TEXT NOT NULL, post TEXT NOT NULL, date_created DATETIME NOT NULL, FOREIGN KEY(author) REFERENCES users(username));")
    conn.commit()
    cur.close()
    conn.close()
setup_db()


@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))
    

@app.route("/login", methods = ["GET","POST"])
def login():
    global toast
    if request.method == "POST":
        print("login request recieved")
        username = request.form["username"]
        password = request.form["password"]
        conn = sql.connect("firefly.db")
        cur = conn.cursor()
        if cur.execute("SELECT username FROM users WHERE username = ?",(username,)).fetchone() == None:
            toast = "The user does not exist, Please signup."
            print(toast)
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("signup"))
        password_db = cur.execute("SELECT password FROM users WHERE username = ?",(username,)).fetchone()
        if checkpw(password.encode(),password_db[0].encode()):
            session['username'] = username
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('index'))
        else:
            toast = "Incorrect password, Please try again"
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for(login))

    else:
        return render_template("login.html", toast = toast)


@app.route("/signup", methods = ["GET","POST"])
def signup():
    global toast
    if request.method == "POST":
        print("signup request recieved")
        username = request.form["username"]
        password = hashpw(request.form["password"].encode(),gensalt()).decode()
        print(username, password)
        try:
            conn = sql.connect("firefly.db")
            cur = conn.cursor()
            if cur.execute("SELECT username FROM users WHERE username = ?",(username,)).fetchone() != None:
                toast = "User already exists, Please login."
                print(toast)
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for('login'))
            else:
                cur.execute("INSERT INTO users VALUES (?,?,?)",(username,password,datetime.timestamp(datetime.now())))
                conn.commit()
                cur.close()
                conn.close()
        except Exception as e:
            print(toast, e)
            toast = "An error occurred, Please try again."
        
        toast = "Signup successful, Please login."
        print(toast)
        return redirect(url_for('login'))
    else:
        return render_template("signup.html", toast = toast)

@app.route("/home")
def home():
    return f"Welcome to your home page {session['username']}"

if __name__ == "__main__":
    app.run("127.0.0.1",9800,True)