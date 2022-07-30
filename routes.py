from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from db import db
import users

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

        #TODO: check the length of both
        if len(username) < 3 or len(password1) < 5:
            print("####length of username must be at least 3 and password 5")
            return redirect("/register")

        #TODO: check that username is not taken
        sql = "SELECT id, password FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()

        if user:
            print("####username already taken")
            return redirect("/register")
        else:
            #TODO: check that passwords match
            if password1 != password2:
                print("####passwords don't match")
                return redirect("/register")

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
