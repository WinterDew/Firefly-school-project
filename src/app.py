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
    cur.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT, date_joined DATETIME);")
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
        return ""
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
        return render_template("signup.html")

@app.route("/home")
def home():
    return f"Welcome to your home page {session['username']}"

if __name__ == "__main__":
    app.run("127.0.0.1",9800,True)