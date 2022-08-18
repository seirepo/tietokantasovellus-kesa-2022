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
            flash("Log in to create a new set")
            return redirect("/login")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        name = request.form["name"]
        description = request.form["description"]
        words = request.form["words"]
        term = request.form["term"]
        definition = request.form["definition"]
        private = request.form["private"]

        result = sets.validate_new_set_info(name, description, words, term, definition, private)
        if not result["success"]:
            flash(result["msg"])
            return redirect(request.url)

        sets.default_if_empty(term, definition)

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

        #TODO: refactor the following
        if request.form["submit_button"] == "Continue":
            answer_with = request.form["answer_with"]
            if answer_with not in ("word1", "word2"):
                flash("You must answer with either the term of definition")
                return redirect(request.url)

            game_id = request.form["game_id"]
            plays.update_answer_with(game_id, answer_with)
            card = plays.get_random_card(game_id)

            return render_template("play.html", set_id=set_id, game_id=game_id, card=card, answer_with=answer_with)

        elif request.form["submit_button"] == "Start a new game":
            answer_with = request.form["answer_with"]
            if answer_with not in ("word1", "word2"):
                flash("You must answer with either the term of definition")
                return redirect(request.url)

            new_game_id = plays.setup_new_game(current_user_id, set_id, answer_with)
            card = plays.get_random_card(new_game_id)

            return render_template("play.html", set_id=set_id, game_id=new_game_id, card=card, answer_with=answer_with)

        else:
            flash("Unknown submit value")
            return redirect(request.url)

@app.route("/play/<int:set_id>", methods=["GET", "POST"])
def play(set_id):
    if request.method == "GET":
        current_user_id = users.current_user_id()
        if not current_user_id:
            flash("Log in to play")
            return redirect("/login")

        game_id = plays.get_latest_game_id(current_user_id, set_id)
        if not game_id:
            return redirect("/set/" + str(set_id))

        next_card = plays.get_random_card(game_id)
        if not next_card:
            results = plays.get_card_results_ordered(game_id)
            set_info = sets.get_set_info(set_id)
            plays.delete_game(game_id)
            #TODO: update stats
            return render_template("finish.html", results=results, card_count=len(results), set=set_info, game_id=game_id)

        answer_with = plays.get_answer_with(game_id)[0]
        return render_template("play.html", set_id=set_id, game_id=game_id, card=next_card, answer_with=answer_with)

    if request.method == "POST":
        current_user_id = users.current_user_id()
        if not current_user_id:
            flash("Log in to play")
            return redirect("/login")

        response = request.form["response"]
        card_id = request.form["card_id"]
        game_id = request.form["game_id"]
        answer_with = request.form["answer_with"]

        correct = plays.check_result(response, card_id, game_id, answer_with)
        card = sets.get_card(card_id)
        if answer_with == "word1":
            word_to_guess = card.word2
            correct_answer = card.word1
        else:
            word_to_guess = card.word1
            correct_answer = card.word2

        return render_template("card-result.html", set_id=set_id, word=word_to_guess, correct=correct, response=response, correct_answer=correct_answer)

@app.route("/edit-set/<int:set_id>", methods=["GET", "POST"])
def edit_set(set_id):
    if request.method == "GET":
        if users.current_user():
            set = sets.get_set_info(set_id)
            cards = sets.get_cards(set_id)
            return render_template("edit-set.html", set=set, cards=cards, set_id=set_id)
        else:
            flash("Log in to create sets")
            return redirect("/login")

    if request.method == "POST":
        if users.current_user_id() != sets.get_set_creator_id(set_id):
            return render_template("error.html")

        name = request.form["name"]
        description = request.form["description"]
        words = request.form["words"]
        term = request.form["term"]
        definition = request.form["definition"]
        private = request.form["private"]
        
        result = sets.validate_set_info(name, description, words, term, definition, private)
        if not result["success"]:
            flash(result["msg"])
            return redirect(request.url)

        sets.default_if_empty(term, definition)

        word1 = request.form.getlist("word1")
        word2 = request.form.getlist("word2")
        card_ids = request.form.getlist("card id")
        remove_ids = request.form.getlist("remove card")
        cards_to_update = dict(zip(card_ids, zip(word1, word2)))

        for card_id in remove_ids:
            del cards_to_update[card_id]

        if len(cards_to_update) == 0:
            flash("You can't remove all cards")
            return redirect(request.url)

        #sets.update_cards(cards)
        sets.update_set(set_id, name, description, term, definition, private, cards_to_update)
        word_pairs = sets.parse_words(words)
        sets.add_cards_to_set(set_id, word_pairs)
        sets.remove_cards(remove_ids)
        plays.clear_games_by_set(set_id)

    return redirect("/" + str(users.current_user_id()))
