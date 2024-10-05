from pydantic import BaseModel


class Gamedef(BaseModel):
    name: str
    description: str
