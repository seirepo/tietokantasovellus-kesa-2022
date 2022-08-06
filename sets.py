from db import db

def add_new_set(name, description, words, term, definition, private, creator_id):
    sql = """INSERT INTO sets (creator_id, name, description, term, definition, private)
             VALUES (:creator_id, :name, :description, :term, :definition, :private)
             RETURNING id"""
    set_id = db.session.execute(sql,
             {"creator_id":creator_id, "name":name, "description":description,
             "term":term, "definition":definition, "private":private}).fetchone()[0]

    for row in words.split("\n"):
        pair = row.strip().split(";")
        if len(pair) != 2:
            continue
        sql = """INSERT INTO cards (set_id, word1, word2)
                 VALUES (:set_id, :word1, :word2)"""
        db.session.execute(sql, {"set_id":set_id, "word1":pair[0], "word2":pair[1]})
    db.session.commit()

def all_sets(creator_id):
    sql = """SELECT id, name, description FROM sets WHERE creator_id=:creator_id"""
    result = db.session.execute(sql, {"creator_id":creator_id})
    sets = result.fetchall()
    return sets
