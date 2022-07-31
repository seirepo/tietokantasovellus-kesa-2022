from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from db import db
import users

@app.route("/")
def index():
    result = db.session.execute("SELECT username, role FROM users")
    users = result.fetchall()
    return render_template("index.html", count=len(users), users=users)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.login(username, password):
            print("####welcome", username)
            return redirect("/")
        else:
            print("####invalid username or password")
            return redirect("/login")
                
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        #TODO: validate role
        role = request.form["role"]

        if len(username) < 3 or len(username) > 20:
            print("####length of username must be between 3 and 20")
            return redirect("/register")

        if len(password1) < 5:
            print("####length of password must be at least 5")
            return redirect("/register")

        if users.user_exists(username):
            print("####username already taken")
            return redirect("/register")
        else:
            if password1 != password2:
                print("####passwords don't match")
                return redirect("/register")

        if users.register(username, password1, role):
            print("####welcome", username, "!")
            return redirect("/")
        else:
            print("####something went wrong :-(")
    
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/result")
def result():
    query = request.args["query"]
    sql = "SELECT id, username FROM users WHERE username LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    users = result.fetchall()
    return render_template("result.html", users=users, count=len(users))

@app.route("/<int:id>")
def show_user(id):
    username = users.get_username(id)
    if id == session["user_id"]:
        sql = "SELECT name, description, id FROM sets WHERE creator_id=:id"
    else:
        sql = "SELECT name, description, id FROM sets WHERE creator_id=:id AND private=0"
    result = db.session.execute(sql, {"id":id})
    sets = result.fetchall()
    return render_template("user.html", count=len(sets), username=username, sets=sets, creator=id)

@app.route("/add-new-set")
def create():
    if session.get("username"):
        #TODO: actual implementation
        return render_template("add-new-set.html")
    else:
        #TODO: add an error message "log in to create a new set" or sth
        return redirect("/login")
