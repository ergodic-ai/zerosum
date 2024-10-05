from datetime import datetime

import psycopg2
from psycopg2 import sql

class Database:
    def __init__(self, dbname, user, password, host="localhost"):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.conn = None

    def create_user_table(self):
        create_table_sql = '''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                player_name VARCHAR(100),
                elo_score INTEGER
            )
            '''
        self.execute_command(create_table_sql)

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host
            )
            return self.conn
        except Exception as e:
            print(f"Unable to connect to the database: {e}")
            return None

    def close(self):
        if self.conn:
            self.conn.close()

    def insert_game(self, game_name, score):
        query = '''INSERT INTO games (name, score, date_played) VALUES ({}, {}, {})'''.format(game_name, score, datetime.now())
        self.execute_command(query)

    def upsert_player(self, player_name, score):
        query = '''INSERT INTO players (player_name, elo_score) VALUES ({}, {}) ON CONFLICT (player_name) DO UPDATE SET elo_score = players.elo_score + {}'''.format(player_name, score, score)
        self.execute_command(query)

    def execute_command(self, sql_string):
        if not self.conn:
            self.connect()

        try:
            cur = self.conn.cursor()
            query = sql.SQL(sql_string)
            cur.execute(query)
            self.conn.commit()
            cur.close()
            print("Command executed successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
