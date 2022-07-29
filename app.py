from flask import Flask, flash, session
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute("SELECT username FROM users")
    users = result.fetchall()
    return render_template("index.html", count=len(users), users=users)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        #TODO: check username and password
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()

        if not user:
            print("####invalid username")
            return redirect("/login")
        else:
            hash_value = user.password
            if check_password_hash(hash_value, password):
                session["username"] = username
                return redirect("/")
            else:
                print("####invalid password")
                return redirect("/login")
                



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        #TODO: check that username is not taken
        #TODO: check that passwords match
        #TODO: check the length of both

        hash_value = generate_password_hash(password1)

        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        print("####uusi käyttäjä ", username, " lisätty")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        return redirect("/")
    
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/result")
def result():
    query = request.args["query"]
    sql = "SELECT id, username FROM users WHERE username LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    users = result.fetchall()
    return render_template("result.html", users=users, count=len(users))
