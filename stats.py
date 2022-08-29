from db import db
from datetime import datetime
import plays

def add_stats(game_id):
    finish_time = datetime.now()
    game_info = plays.get_game_info(game_id)
    time = finish_time - game_info.start_time

    sql = """SELECT """