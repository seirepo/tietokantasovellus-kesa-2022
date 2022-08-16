from db import db
import sets

def get_latest_game_id(user_id, set_id):
    sql = """SELECT id FROM latest_games WHERE user_id=:user_id AND set_id=:set_id"""
    result = db.session.execute(sql, {"user_id":user_id, "set_id":set_id})
    id = result.fetchone()[0]
    return id

def setup_new_game(user_id, set_id):
    print("####set up new game", set_id, "for", user_id)
    clear_latest(user_id, set_id)
    print("####previous game cleared")
    sql = """INSERT INTO latest_games (user_id, set_id)
    VALUES (:user_id, :set_id) RETURNING id"""
    game_id = db.session.execute(sql, {"user_id":user_id, "set_id":set_id}).fetchone()[0]
    db.session.commit()
    
    cards = sets.get_cards(set_id)
    for card in cards:
        sql = """INSERT INTO card_results (latest_game_id, card_id)
        VALUES (:latest_game_id, :card_id)"""
        result = db.session.execute(sql, {"latest_game_id":game_id,"card_id":card.id})
        db.session.commit()
        if not result:
            return False
    print("####new game setup done")
    return game_id

def get_random_card(latest_game_id):
    #print("####got game id", game_id, "(", type(game_id), ")")
    sql = """SELECT cards.id, cards.word1, cards.word2
             FROM cards, card_results AS results
             WHERE  cards.id = results.card_id AND results.latest_game_id=:latest_game_id
             AND results.result=0
             ORDER BY random()
             LIMIT 1
             """
    #sql = """SELECT card_id FROM card_results WHERE latest_game_id=:latest_game_id LIMIT 1"""
    result = db.session.execute(sql, {"latest_game_id":latest_game_id})
    card = result.fetchone()
    return card

def clear_latest(user_id, set_id):
    sql = """DELETE FROM latest_games WHERE user_id=:user_id AND set_id=:set_id"""
    db.session.execute(sql, {"user_id":user_id, "set_id":set_id})
    db.session.commit()

