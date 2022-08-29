from db import db
import sets

def get_latest_game_id(user_id, set_id):
    sql = """SELECT id FROM latest_games WHERE user_id=:user_id AND set_id=:set_id"""
    result = db.session.execute(sql, {"user_id":user_id, "set_id":set_id})
    id = result.fetchone()
    if id:
        return id[0]
    else:
        return id

def setup_new_game(user_id, set_id, answer_with):
    clear_latest(user_id, set_id)
    sql = """INSERT INTO latest_games (user_id, set_id, answer_with, start_time)
    VALUES (:user_id, :set_id, :answer_with, NOW()) RETURNING id"""
    game_id = db.session.execute(sql, {"user_id":user_id, "set_id":set_id, "answer_with":answer_with}).fetchone()[0]
    db.session.commit()
    
    cards = sets.get_cards(set_id)
    for card in cards:
        sql = """INSERT INTO card_results (latest_game_id, card_id)
        VALUES (:latest_game_id, :card_id)"""
        result = db.session.execute(sql, {"latest_game_id":game_id,"card_id":card.id})
        db.session.commit()
        if not result:
            return False
    return game_id

def get_random_card(latest_game_id):
    sql = """SELECT cards.id, cards.word1, cards.word2
             FROM cards, card_results AS results
             WHERE  cards.id = results.card_id AND results.latest_game_id=:latest_game_id
             AND results.result=0
             ORDER BY random()
             LIMIT 1
             """
    result = db.session.execute(sql, {"latest_game_id":latest_game_id})
    card = result.fetchone()
    return card

def update_answer_with(game_id, answer_with):
    sql = """UPDATE latest_games SET answer_with=:answer_with WHERE id=:game_id"""
    db.session.execute(sql, {"answer_with":answer_with, "game_id":game_id})
    db.session.commit()

def clear_latest(user_id, set_id):
    sql = """DELETE FROM latest_games WHERE user_id=:user_id AND set_id=:set_id"""
    db.session.execute(sql, {"user_id":user_id, "set_id":set_id})
    db.session.commit()

def check_result(response, card_id, game_id, answer_with):
    card = sets.get_card(card_id)
    if answer_with == "word1":
        correct = card.word1
    else:
        correct = card.word2

    if response.lower() == correct.lower():
        sql = """UPDATE card_results SET result=1, time_guessed=NOW()
                 WHERE latest_game_id=:latest_game_id AND card_id=:card_id"""
        result = True
    else:
        sql = """UPDATE card_results SET times_guessed_wrong=times_guessed_wrong + 1
                 WHERE latest_game_id=:latest_game_id AND card_id=:card_id"""
        result = False
    db.session.execute(sql, {"latest_game_id":game_id, "card_id":card_id})
    db.session.commit()
    return result

def get_answer_with(game_id):
    sql = """SELECT answer_with FROM latest_games WHERE id=:game_id"""
    result = db.session.execute(sql, {"game_id":game_id}).fetchone()
    return result

def get_card_results_ordered(game_id):
    sql = """SELECT cards.word1, cards.word2, results.times_guessed_wrong,
             results.time_guessed
             FROM cards, card_results AS results
             WHERE cards.id=results.card_id AND results.latest_game_id=:game_id
             ORDER BY results.times_guessed_wrong DESC, results.time_guessed DESC;"""
    results = db.session.execute(sql, {"game_id":game_id}).fetchall()
    return results

def delete_game(game_id):
    sql = """DELETE FROM latest_games WHERE id=:game_id"""
    db.session.execute(sql, {"game_id":game_id})
    db.session.commit()

def clear_games_by_set(set_id):
    sql = """DELETE FROM latest_games WHERE set_id=:set_id"""
    db.session.execute(sql, {"set_id":set_id})
    db.session.commit()
