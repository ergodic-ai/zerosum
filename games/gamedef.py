from pydantic import BaseModel


# class ActionFormat(BaseModel):
#     type: Literal["text", "json"]
#     format: str


class Gamedef(BaseModel):
    name: str
    description: str
    n_players: int
    rules: str
    actions: str
    action_format: str  # change later
    objective: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_system_prompt(self) -> str:

        multiplayer_line = (
            f"You are playing {self.name} with {self.n_players} players."
            if self.n_players > 1
            else "You are playing {self.name}."
        )

        return f"""
        {multiplayer_line}
        {self.description}. 
        
        The rules are as follows:
        {self.rules}.

        The actions you can take are as follows:
        {self.actions}.

        Your objective is:
        {self.objective}.
        Please respond in the following JSON format:
        {self.action_format}.

        At each step you will be given the current state of the game and the actions that have been taken.
        """
