from future.backports.datetime import datetime
from psycopg2 import sql
from pydantic.dataclasses import dataclass

from games.queryhandler import QueryHandler
from games.structs.GameDefinition import GameDefinition
from games.structs.GameEnv import GameEnvironment
from games.tetris.playeraction import PlayerAction
from database.pgresDB import Database


class Game(GameDefinition):
    # todo should players be a dictionary of name, handler type?
    database: Database

    def __init__(self, gameEnv: GameEnvironment, players: list[str], parallel: bool = False):
        super().__init__(
            gameEnv=gameEnv,
            description="You are in a maze. You can move left, right, up, or down.",
            n_players=1,
            rules="You can only move left, right, up, or down.",
            actions="You can move left, right, up, or down.",
            action_format=PlayerAction,  # change later
            players=players,
            parallel=parallel
        )
        self.database = Database("yourdatabase","yourusername","yourpassword")

    def get_players_handlers(self) -> dict[str, QueryHandler]:
        self.gameEnv.get_role("")
        # todo system prompt needs to be set per handler and be role specific
        pass

    def get_step_string(self, state, previous_actions, previous_rewards) -> str:
        pass

    def run(self):
        table_name = ""
        game_instance = 0
        self.create_tables(table_name)# todo insert relevant info
        self.gameEnv.make(self.players)
        self.gameEnv.reset()
        done = False
        handlers = self.get_players_handlers()

        while not done:
            actions: dict[str, any] = {} # any could be passed into
            for player_id in self.players:
                state = self.gameEnv.get_state
                query = self.gameEnv.build_query(state)
                response = handlers[player_id].query_player(query)
                actions[player_id] = response
                if not self.parallel:
                    observation, reward, done, info = self.gameEnv.step_individual(response)
                    self.update_table(table_name, game_instance, observation, reward)
            if self.parallel:
                observation, reward, done, info = self.gameEnv.step_all(actions)
                self.update_table(table_name, game_instance, observation, reward)

    def score(self) -> dict[str, int]:
        pass

    def create_tables(self, tableName:str):
        query = '''CREATE TABLE {} (state VARCHAR(100),timestamp VARCHAR(100)  PRIMARY KEY, gameInstance INTEGER, score VARCHAR(100) );'''.format(tableName)
        self.database.execute_command(query)

    def update_table(self, tableName:str, gameInstance: int, state:str, score: str):
        curTime = datetime.now().strftime('%H:%M:%S')
        query = '''INSERT INTO {} (state, timestamp, gameInstance, score) VALUES ({}, {},{},{});'''.format(tableName, state, "\'"+curTime+"\'", gameInstance, score)
        self.database.execute_command(query)

