from flask import Flask, render_template, url_for, request
from flask import redirect, session, flash
from bcrypt import hashpw,checkpw,gensalt
import sqlite3 as sql
from datetime import datetime
import uuid

app = Flask(__name__)
# app.config['SECRET_KEY'] = '#tr5988fhdskghlkoifayfgghakf'
app.config["SECRET_KEY"] = str(uuid.uuid4())
database_address = "firefly.db"

def setup_db():
    conn = sql.connect(database_address)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("PRAGMA auto_vacuum = 1;")
    cur.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT NOT NULL, date_joined DATETIME NOT NULL);")
    cur.execute("CREATE TABLE IF NOT EXISTS posts(author TEXT NOT NULL, content TEXT NOT NULL, date_created DATETIME NOT NULL,id INTEGER PRIMARY KEY AUTOINCREMENT, FOREIGN KEY(author) REFERENCES users(username));")
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
        conn = sql.connect(database_address)
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
            return redirect(url_for("login"))

    else:
        toast = session["toast"]
        session["toast"] = ""
        return render_template("login.html", toast = toast)


@app.route("/signup", methods = ["GET","POST"])
def signup():
    
    if request.method == "POST":
        print("signup request recieved")
        username = request.form["username"]
        password = hashpw(request.form["password"].encode(),gensalt()).decode()
        print(username, password)
        try:
            conn = sql.connect(database_address)
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
        toast = session["toast"]
        session["toast"] = ""
        return render_template("signup.html", toast = toast)

@app.route("/home", methods=["GET","POST"])
def home():
    if "username" in session:
        conn = sql.connect(database_address)
        cur = conn.cursor()
        if request.method == "POST":
            username = session["username"]
            content = request.form['content']
            cur.execute("INSERT INTO posts (author,content,date_created) VALUES (?,?,?)",(username,content,datetime.timestamp(datetime.now())))
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
                posts.append([data[0],data[1],datetime.fromtimestamp(data[2]).ctime(),data[3]])
            toast = session["toast"]
            session["toast"] = ""
            return render_template("home.html",posts = posts,toast = toast)
    else:
        return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("username")
    session["toast"] = "Logout Successful"
    return redirect(url_for("login"))

@app.route("/post/delete",methods=["GET"])
def delete_post():
    try:
        username = request.args['user']
        if username == session["username"]:
            conn = sql.connect(database_address)
            cur = conn.cursor()
            cur.execute("DELETE FROM posts WHERE author=? AND id=?",(username,request.args['id']))
            conn.commit()
            cur.close()
            conn.close()
            session["toast"] = "Post deleted successfully"
        else:
            session["toast"] = "Post can only be deleted by the author"
    except:
        session["toast"] = "An internal error occurred, Please try again."
    return redirect(url_for("home"))



@app.route("/user/delete",methods=["GET","POST"])
def delete_user():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if "username" in session:
            if username == session["username"]:
                conn = sql.connect(database_address)
                cur = conn.cursor()
                password_db = cur.execute("SELECT password FROM users WHERE username = ?",(username,)).fetchone()
                if checkpw(password.encode(),password_db[0].encode()):
                    
                    cur.execute("DELETE FROM posts WHERE author=?",(session["username"],))
                    cur.execute("DELETE FROM users WHERE username=?",(session["username"],))
                    session.pop("username")
                    conn.commit()
                    cur.close()
                    conn.close()
                    session["toast"] = "Account and all associated posts have been deleted."
                    return redirect(url_for('login'))
                else:
                    session["toast"] = "Incorrect password, Please try again"
                    conn.commit()
                    cur.close()
                    conn.close()
                    return redirect(url_for("delete_user"))
            else:
                session["toast"] = "User must be logged in to delete the account."
                return redirect(url_for("home"))
        else:
            session["toast"] = "User must be logged in to delete the account."
            return redirect(url_for("login"))
    else:
        return render_template("delete_user.html", toast = session["toast"])

if __name__ == "__main__":
    app.run("127.0.0.1",9800,True)