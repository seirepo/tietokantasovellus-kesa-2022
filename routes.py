from flask import flash, redirect, render_template, request, session, abort
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

        role = request.form["role"]
        if role not in ("0", "1"):
            flash("Unsupported role")
            return redirect("/register")

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
            return render_template("add-new-set.html")
        else:
            #TODO: add an error message "log in to create a new set" or sth
            return redirect("/login")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        name = request.form["name"]
        if len(name) < 1 or len(name) > 20:
            flash("Name length must be between 1-20")
            redirect("/add-new-set")

        description = request.form["description"]
        if len(description) > 100:
            flash("Description too long: " + len(description) + "> 100")
            redirect("/add-new-set")

        words = request.form["words"]
        if len(words) > 1000:
            flash("Word list too long: " + len(words) + " > 1000")
            redirect("/add-new-set")

        term = request.form["term"]
        if len(term) > 20:
            flash("Term too long: " + len(term) + " > 20")
            redirect("/add-new-set")

        definition = request.form["definition"]
        if len(definition) > 20:
            flash("Definition too long: " + len(term) + " > 20")
            redirect("/add-new-set")

        private = request.form["private"]
        if private not in ("0", "1"):
            flash("Unsupported visibility selection")
            redirect("/add-new-set")

        creator_id = users.current_user_id()
        sets.add_new_set(name, description, words, term, definition, private, creator_id)

        return redirect("/" + str(creator_id))

@app.route("/remove-sets", methods=["GET", "POST"])
def remove():
    if request.method == "GET":
        print("####GET remove-sets")
        if users.current_user():
            user_sets = sets.all_sets(users.current_user_id())
            return render_template("remove-sets.html", sets=user_sets)

    if request.method == "POST":
        print("####POST remove-sets")
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        set_ids = request.form.getlist("selection")
        print("####poistettavat: ", set_ids)

        #TODO: remove sets and cards in them from db
        return redirect("/" + str(users.current_user_id()))

@app.route("/play/<int:id>")
def play(id):
    #TODO: actual implementation
    return render_template("play.html")

@app.route("/edit-set/<int:id>")
def edit_set(id):
    #TODO: actual implementation
    return render_template("edit-set.html")