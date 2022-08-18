from db import db

def add_new_set(name, description, words, term, definition, private, creator_id):
    sql = """INSERT INTO sets (creator_id, name, description, term, definition, private)
             VALUES (:creator_id, :name, :description, :term, :definition, :private)
             RETURNING id"""
    set_id = db.session.execute(sql,
             {"creator_id":creator_id, "name":name, "description":description,
             "term":term, "definition":definition, "private":private}).fetchone()[0]

    word_pairs = parse_words(words)
    add_cards_to_set(set_id, word_pairs)

def get_sets(creator_id, only_public):
    if only_public:
        sql = """SELECT id, name, description FROM sets WHERE creator_id=:creator_id AND private=0"""
    else:
        sql = """SELECT id, name, description FROM sets WHERE creator_id=:creator_id"""
    result = db.session.execute(sql, {"creator_id":creator_id})
    sets = result.fetchall()
    return sets

def remove_sets(set_ids):
    for set_id in set_ids:
        try:
            sql = """DELETE FROM sets WHERE id=:id"""
            db.session.execute(sql, {"id":set_id})
            db.session.commit()
        except:
            print("####Removing set ", set_id, " failed!")
            return False

def get_set_info(set_id):
    sql = """SELECT id, name, description, term, definition, private
             FROM sets WHERE id=:id"""
    result = db.session.execute(sql, {"id":set_id})
    info = result.fetchone()
    return info

def get_cards(set_id):
    sql = """SELECT id, word1, word2 FROM cards WHERE set_id=:set_id"""
    cards = db.session.execute(sql, {"set_id":set_id}).fetchall()
    return cards

def get_card(id):
    sql = """SELECT word1, word2 FROM cards WHERE id=:id"""
    card = db.session.execute(sql, {"id":id}).fetchone()
    return card

def update_set(set_id, name, description, term, definition, private, cards_to_update):
    #TODO: update set
    sql = """UPDATE sets
             SET name=:name, description=:description, term=:term,
                 definition=:definition, private=:private
             WHERE id=:set_id"""
    db.session.execute(sql,
            {"name":name, "description":description, "term":term, "definition":definition,
            "private":private, "set_id":set_id})
    db.session.commit()

    for card_id in cards_to_update:
        word1 = cards_to_update[card_id][0]
        word2 = cards_to_update[card_id][1]
        sql = """UPDATE cards
                 SET word1=:word1, word2=:word2
                 WHERE id=:card_id"""
        db.session.execute(sql, {"word1":word1, "word2":word2, "card_id":card_id})
    db.session.commit()

def remove_cards(ids):
    for id in ids:
        try:
            sql = """DELETE FROM cards WHERE id=:id"""
            db.session.execute(sql, {"id":id})
            db.session.commit()
        except:
            print("####Removing card with id", id, "failed")

def validate_set_info(name, description, words, term, definition, private):
    success = True
    msg = ""

    if len(name) < 1 or len(name) > 100:
        msg += "Name length must be between 1-100\n"
        success = False

    if len(description) > 100:
        msg += "Description too long: " + len(description) + "> 100\n"
        success = False

    if len(words) > 10000:
        msg +=  "Word list too long: " + len(words) + " > 10000\n"
        success = False

    if len(term) > 100:
        msg +=  "Term too long: " + len(term) + " > 100\n"
        success = False

    if len(definition) > 100:
        msg +=  "Definition too long: " + len(term) + " > 100\n"
        success = False

    if private not in ("0", "1"):
        msg +=  "Unsupported visibility selection\n"
        success = False

    if not success:
        return {"success":False, "msg":msg}
    else:
        return {"success":True, "msg":""}

def default_if_empty(term, definition):
    if len(term) == 0:
        term = "term"

    if len(definition) == 0:
        definition = "definition"

def parse_words(words):
    word_pairs = []
    for row in words.split("\n"):
        pair = row.strip().split(";")
        if len(pair) != 2:
            continue
        word_pairs.append((pair[0], pair[1]))
    return word_pairs

def add_cards_to_set(set_id, cards):
    for pair in cards:
        sql = """INSERT INTO cards (set_id, word1, word2)
                 VALUES (:set_id, :word1, :word2)"""
        db.session.execute(sql, {"set_id":set_id, "word1":pair[0], "word2":pair[1]})
    db.session.commit()
