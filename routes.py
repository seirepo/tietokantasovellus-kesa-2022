from queue import Empty
from flask import flash, redirect, render_template, request, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from db import db
import users
import sets
import plays

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
    #TODO: refactor function
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        #TODO: checks to a separate validate function
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
        user_sets = sets.get_sets(id, 0)
    else:
        user_sets = sets.get_sets(id, 1)
    return render_template("user.html", count=len(user_sets), username=username, sets=user_sets, creator=id)

@app.route("/add-new-set", methods=["GET", "POST"])
def add_new_set():
    #TODO: refactor function
    if request.method == "GET":
        if users.current_user():
            return render_template("add-new-set.html")
        else:
            #TODO: add an error message "log in to create a new set" or sth
            return redirect("/login")
    if request.method == "POST":
        #TODO: move check to separate function
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        
        #TODO: make sure that empty set cannot be saved
        #TODO: move validation to a separate method
        name = request.form["name"]
        if len(name) < 1 or len(name) > 100:
            flash("Name length must be between 1-100")
            return redirect("/add-new-set")

        description = request.form["description"]
        if len(description) > 100:
            flash("Description too long: " + len(description) + "> 100")
            return redirect("/add-new-set")

        words = request.form["words"]
        if len(words) > 10000:
            flash("Word list too long: " + len(words) + " > 10000")
            return redirect("/add-new-set")

        term = request.form["term"]
        if len(term) > 100:
            flash("Term too long: " + len(term) + " > 100")
            return redirect("/add-new-set")
        if len(term) == 0:
            term = "term"

        definition = request.form["definition"]
        if len(definition) > 100:
            flash("Definition too long: " + len(term) + " > 100")
            return redirect("/add-new-set")
        if len(definition) == 0:
            definition = "definition"

        private = request.form["private"]
        if private not in ("0", "1"):
            flash("Unsupported visibility selection")
            return redirect("/add-new-set")

        creator_id = users.current_user_id()
        sets.add_new_set(name, description, words, term, definition, private, creator_id)

        return redirect("/" + str(creator_id))

@app.route("/remove-sets", methods=["GET", "POST"])
def remove():
    if request.method == "GET":
        if users.current_user():
            user_sets = sets.get_sets(users.current_user_id(), 0)
            return render_template("remove-sets.html", sets=user_sets)
        else:
            #TODO: add an error message "log in to create and remove sets" or sth
            return redirect("/login")

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        set_ids = request.form.getlist("selection")
        sets.remove_sets(set_ids)

        return redirect("/" + str(users.current_user_id()))

@app.route("/set/<int:set_id>", methods=["GET", "POST"])
def set(set_id):
    current_user_id = users.current_user_id()
    if request.method == "GET":
        set = sets.get_set_info(set_id)
        cards = sets.get_cards(set_id)

        if not current_user_id:
            return render_template("set.html", set=set, card_count=len(cards), cards=cards)
        game_id = plays.get_latest_game_id(current_user_id, set_id)

        return render_template("set.html", set=set, card_count=len(cards), cards=cards, game_id=game_id)
    if request.method == "POST":
        if not current_user_id:
            flash("Log in to play")
            return redirect("/login")

        if request.form["submit_button"] == "Continue":
            game_id = request.form["game_id"]
            print("####got game id", game_id)
            card = plays.get_random_card(game_id)
            return render_template("play.html", set_id=set_id, card=card)
        elif request.form["submit_button"] == "Start a new game":
            new_game_id = plays.setup_new_game(current_user_id, set_id)
            card = plays.get_random_card(new_game_id)
            return render_template("play.html", set_id=set_id, card=card)
        else:
            flash("Unknown submit value")
            return redirect(request.url)

@app.route("/play/<int:set_id>", methods=["GET", "POST"])
def play(set_id):
    if request.method == "GET":
        return redirect("/set/" + str(set_id))
    if request.method == "POST":
        current_user_id = users.current_user_id()
        if not current_user_id:
            flash("Log in to play")
            return redirect("/login")


@app.route("/edit-set/<int:id>", methods=["GET", "POST"])
def edit_set(id):
    #TODO: finish implementation
    if request.method == "GET":
        if users.current_user():
            #TODO: render edit-set.html
            set = sets.get_set_info(id)
            cards = sets.get_cards(id)
            return render_template("edit-set.html", set=set, cards=cards, set_id=id)
        else:
            #TODO: add an error message "log in to create and remove sets" or sth
            return redirect("/login")

    if request.method == "POST":
        #TODO: implement edit
        word1 = request.form.getlist("word1")
        word2 = request.form.getlist("word2")
        card_ids = request.form.getlist("card id")
        remove_ids = request.form.getlist("remove card")
        cards = dict(zip(card_ids, zip(word1, word2)))
        print("####cards:", cards)
        print("####card ids to be removed:", remove_ids)

        for id in remove_ids:
            del cards[id]

        #TODO: check that user can't remove all words from set

        sets.update_cards(cards)
        sets.remove_cards(remove_ids)
    return redirect("/" + str(users.current_user_id()))
