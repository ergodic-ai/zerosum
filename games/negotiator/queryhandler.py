from games.queryhandler import QueryHandler
from games.negotiator.playeraction import PlayerAction


class NegotiatorQueryHandler(QueryHandler):
    def __init__(self, model: str, system_query: str):
        super().__init__(PlayerAction, system_query, model)
