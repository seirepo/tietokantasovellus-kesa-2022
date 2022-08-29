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

def get_sets(creator_id, show_all, sort_by):
    if sort_by == "name":
        order_by = "ORDER BY name ASC"
    elif sort_by == "newest":
        order_by = "ORDER BY creation_time DESC"
    elif sort_by == "oldest":
        order_by = "ORDER BY creation_time ASC"
    else:
        order_by = "ORDER BY name ASC"

    if show_all:
        sql = """SELECT id, name, description FROM sets WHERE creator_id=:creator_id """ + order_by
    else:
        sql = """SELECT id, name, description FROM sets WHERE creator_id=:creator_id AND private=0 """ + order_by
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
            return False

def validate_new_set_info(name, description, words, term, definition, private):
    result = validate_set_info(name, description, words, term, definition, private)

    if len(words) == 0 or len(parse_words(words)) == 0:
        if not result["success"]:
            result["msg"] += ", "
        result["msg"] += "Set must contain at least 1 word pair"
        result["success"] = False

    return result

def validate_set_info(name, description, words, term, definition, private):
    success = True
    msg = []

    if len(name) < 1 or len(name) > 100:
        msg.append("Name length must be between 1-100")
        success = False

    if len(description) > 100:
        msg.append("Description too long: " + len(description) + "> 100")
        success = False

    if len(words) > 10000:
        msg.append("Word list too long: " + len(words) + " > 10000")
        success = False

    if len(term) > 100:
        msg.append("Term too long: " + len(term) + " > 100")
        success = False

    if len(definition) > 100:
        msg.append("Definition too long: " + len(term) + " > 100")
        success = False

    if private not in ("0", "1"):
        msg.append("Unsupported visibility selection")
        success = False

    if not success:
        return {"success":False, "msg":", ".join(msg)}
    else:
        return {"success":True, "msg":""}

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

def get_set_creator_id(set_id):
    sql = """SELECT creator_id FROM sets WHERE id=:set_id"""
    creator_id = db.session.execute(sql, {"set_id":set_id}).fetchone()
    if creator_id:
        return creator_id[0]

def get_set_creator_info(set_id):
    sql = """SELECT U.id, U.username
             FROM users U LEFT JOIN sets S
             ON S.creator_id=U.id
             WHERE S.id=:id"""
    creator_info = db.session.execute(sql, {"id":set_id}).fetchone()
    return creator_info

def get_all_public_sets():
    sql = """SELECT id, name, description, term, definition, private
             FROM sets
             WHERE private=0"""
    sets = db.session.execute(sql).fetchall()
    return sets

def search_from_sets(query):
    sql = """SELECT id, name, description FROM sets
             WHERE name LIKE :query AND private=0 OR description LIKE :query AND private=0"""
    result = db.session.execute(sql, {"query":"%"+query+"%"}).fetchall()
    return result
