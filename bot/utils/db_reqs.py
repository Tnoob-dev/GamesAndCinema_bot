from db.create_db import engine, Game
from sqlmodel import Session, select
from typing import List

def insert(query: Game) -> None: # No estoy pa retornar el str del print xd
    try:
        with Session(engine) as session:
            session.add(query)
            session.commit()
        print("Juego annadido")
    except Exception as e:
        raise Exception(f"Error al annadir a la db -> {e}")

def get_game(name: str) -> List[int]:
    try:
        with Session(engine) as session:
            statement = select(Game).where(Game.name == name)
            result = session.exec(statement).first()

            return result.file_ids

    except Exception as e:
        raise Exception(f"Error al obtener desde la db -> {e}")


#### IMPLEMENTAR LUEGO

# def delete(id: int):
#     try:
#         with Session(engine) as session:
#             statement = select(Game).where(Game.id == id)
#         print("Juego annadido")
#     except Exception as e:
#         raise Exception(f"Error eliminar de la db -> {e}")