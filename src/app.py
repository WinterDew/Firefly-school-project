from flask import Flask, render_template, url_for, request
from flask import redirect, session, flash
from bcrypt import hashpw,checkpw,gensalt
import sqlite3 as sql
import os
from datetime import datetime
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = '#tr5988fhdskghlkoifayfgghakf'


def setup_db():
    conn = sql.connect("firefly.db")
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("PRAGMA auto_vacuum = 1;")
    cur.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT NOT NULL, date_joined DATETIME NOT NULL);")
    cur.execute("CREATE TABLE IF NOT EXISTS posts(author TEXT NOT NULL, content TEXT NOT NULL, date_created DATETIME NOT NULL, FOREIGN KEY(author) REFERENCES users(username));")
    conn.commit()
    cur.close()
    conn.close()
setup_db()


@app.route("/")
def index():
    session['toast'] = ""
    if "username" in session:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))
    

@app.route("/login", methods = ["GET","POST"])
def login():
    
    if request.method == "POST":
        print("login request recieved")
        username = request.form["username"]
        password = request.form["password"]
        conn = sql.connect("firefly.db")
        cur = conn.cursor()
        if cur.execute("SELECT username FROM users WHERE username = ?",(username,)).fetchone() == None:
            session["toast"] = "The user does not exist, Please signup."
            print(session["toast"])
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
            session["toast"] = "Incorrect password, Please try again"
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for(login))

    else:
        return render_template("login.html", toast = session["toast"])


@app.route("/signup", methods = ["GET","POST"])
def signup():
    
    if request.method == "POST":
        print("signup request recieved")
        username = request.form["username"]
        password = hashpw(request.form["password"].encode(),gensalt()).decode()
        print(username, password)
        try:
            conn = sql.connect("firefly.db")
            cur = conn.cursor()
            if cur.execute("SELECT username FROM users WHERE username = ?",(username,)).fetchone() != None:
                session["toast"] = "User already exists, Please login."
                print(session["toast"])
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
            print(session["toast"], e)
            session["toast"] = "An error occurred, Please try again."
        
        session["toast"] = "Signup successful, Please login."
        print(session["toast"])
        return redirect(url_for('login'))
    else:
        return render_template("signup.html", toast = session["toast"])

@app.route("/home", methods=["GET","POST"])
def home():
    
    conn = sql.connect("firefly.db")
    cur = conn.cursor()
    if request.method == "POST":
        username = session["username"]
        content = request.form['content']
        cur.execute("INSERT INTO posts VALUES (?,?,?)",(username,content,datetime.timestamp(datetime.now())))
        conn.commit()
        cur.close()
        conn.close()
        session["toast"] = "Posted successfully!"
        return redirect(url_for('home'))
    else:
        dataset = cur.execute("SELECT * FROM posts ORDER BY date_created DESC").fetchall()
        conn.commit()
        cur.close()
        conn.close()
        posts = []
        for data in dataset:
            posts.append([data[0],data[1],datetime.fromtimestamp(data[2]).ctime()])

        return render_template("home.html",posts = posts,toast = session["toast"])
    

if __name__ == "__main__":
    app.run("127.0.0.1",9800,True)