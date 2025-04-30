from sqlmodel import SQLModel, Field, create_engine, Column, JSON
from typing import Optional, List
from os.path import exists

class Game(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    file_ids: List[int] = Field(sa_column=Column(JSON))


engine = create_engine("sqlite:///./bot/core/games.db")

if not exists("./bot/core/games.db"):
    SQLModel.metadata.create_all(engine)
else:
    print("already exists db")