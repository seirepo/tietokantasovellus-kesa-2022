from db import db
from datetime import datetime, timezone
import plays

def add_stats(game_id):
    finish_time = datetime.now()
    game_info = plays.get_game_info(game_id)[0]
    time = finish_time - game_info["start_time"]
    print(str(time))

    print(time, type(time))
    sql = """SELECT COUNT(*) FROM card_results
             WHERE latest_game_id=:game_id
             AND times_guessed_wrong=0"""
    guessed_on_first = db.session.execute(sql, {"game_id":game_id}).fetchone()[0]

    sql = """INSERT INTO stats (user_id, set_id, play_time, guessed_on_first)
             VALUES (:user_id, :set_id, :play_time, :guessed_on_first)"""

    db.session.execute(sql, {"user_id":game_info["user_id"], "set_id":game_info["set_id"],
                            "guessed_on_first":guessed_on_first, "play_time":time})
    db.session.commit()

def reset_stats(set_id):
    sql = """DELETE FROM stats WHERE set_id=:set_id"""
    db.session.execute(sql, {"set_id":set_id})
    db.session.commit()

def get_recently_played(user_id):
    sql = """SELECT DISTINCT S.id, S.name, S.description FROM sets S
             LEFT JOIN latest_games A ON s.id=A.set_id
             WHERE A.user_id=:user_id;"""

    latest = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return latest

def get_recently_finished(user_id):
    sql = """SELECT DISTINCT S.id, S.name, S.description FROM sets S
             LEFT JOIN stats A ON s.id=A.set_id
             WHERE A.user_id=:user_id
             LIMIT 5;"""
    finished = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return finished