from db import db
import sets

def get_latest_game_id(user_id, set_id):
    sql = """SELECT id FROM latest_games WHERE user_id=:user_id AND set_id=:set_id"""
    result = db.session.execute(sql, {"user_id":user_id, "set_id":set_id})
    id = result.fetchone()
    return id

def setup_new_game(user_id, set_id):
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

def get_random_card(game_id):
    #sql = """SELECT card_id FROM card_results WHERE game_id=:game_id
    #  AND correctly_guessed=0"""
    """
    SELECT cards.word1, cards.word2
    FROM cards, card_results AS results
    WHERE  cards.id = results.card_id AND results.latest_game_id=game_id
    AND results.correctly_guessed=0
    ORDER BY random()
    LIMIT 1
    """

def clear_latest(user_id):
    sql = """DELETE FROM latest_games WHERE user_id=:user_id"""
    db.session.execute(sql, {"user_id":user_id})
    db.session.commit()

