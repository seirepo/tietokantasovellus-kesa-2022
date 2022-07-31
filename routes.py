from flask import flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from db import db
import users
import sets

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
            flash("Welcome " + username)
            return redirect("/")
        else:
            flash("Invalid username or password")
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
            flash("Length of username must be between 3 and 20")
            return redirect("/register")

        if len(password1) < 5:
            flash("Length of password must be at least 5")
            return redirect("/register")

        if users.user_exists(username):
            flash("Username already taken")
            return redirect("/register")
        else:
            if password1 != password2:
                flash("Passwords don't match")
                return redirect("/register")

        if users.register(username, password1, role):
            flash("Welcome " + username)
            return redirect("/")
        else:
            #TODO: return error page
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

@app.route("/add-new-set", methods=["GET", "POST"])
def add_new_set():
    if request.method == "GET":
        if users.current_user():
            #TODO: actual implementation
            return render_template("add-new-set.html")
        else:
            #TODO: add an error message "log in to create a new set" or sth
            return redirect("/login")
    if request.method == "POST":
        #TODO: users.check_csrf()
        name = request.form["name"]
        if len(name) < 1 or len(name) > 20:
            flash("Name length must be between 1-20")

        description = request.form["description"]
        if len(description) > 100:
            flash("Description too long: " + len(description) + "> 100")

        words = request.form["words"]
        if len(words) > 1000:
            flash("Word list too long: " + len(words) + " > 1000")

        term = request.form["term"]
        if len(term) > 20:
            flash("Term too long: " + len(term) + " > 20")

        definition = request.form["definition"]
        if len(definition) > 20:
            flash("Definition too long: " + len(term) + " > 20")

        #TODO: validate private
        private = request.form["private"]

        #TODO: handle request form parameters
        sets.add_new_set(name, description, words, term, definition, private, users.current_user_id())

        #TODO: return to user's page
        return redirect("/")

@app.route("/play/<int:id>")
def play(id):
    #TODO: actual implementation
    return render_template("play.html")

@app.route("/edit-set/<int:id>")
def edit_set(id):
    #TODO: actual implementation
    return render_template("edit-set.html")