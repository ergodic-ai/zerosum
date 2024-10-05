from pydantic import BaseModel


class Gamedef(BaseModel):
    name: str
    description: str
    rules: str
    instructions: str
    examples: str
    input_format: str
    output_format: str
