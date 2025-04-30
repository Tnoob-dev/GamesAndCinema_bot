from pyrogram.client import Client
from pyrogram.types import Message
from pyrogram.filters import private, channel, command
from pyrogram.errors import FloodWait
from typing import List
from pathlib import Path
from utils.db_reqs import insert, get_game
from db.create_db import Game
import dotenv as dt
import os
import asyncio

dt.load_dotenv(dotenv_path=Path.cwd() / Path("bot") / Path("core") / ".env")

bot: Client = Client(os.getenv("NAME"))


@bot.on_message(command("start") & private)
async def hello(client: Client, message: Message):
    admins: List[str] = os.getenv("ADMINS").split(",")

    if len(message.command) >= 2:
        # await message.reply("juegazo xd")
        file_ids: List[int] = get_game(message.command[1])

        for id in file_ids:
            success = False
            while not success:
                try:
                    await client.copy_message(
                        message.chat.id, os.getenv("CHANNEL_ID"), id
                    )
                    success = True
                except FloodWait as f:
                    await asyncio.sleep(f.value)

    else:
        if str(message.from_user.id) in admins:
            await message.reply(f"Hola Administrador: {message.from_user.first_name}")
        else:
            await message.reply(
                f"Hola {message.from_user.mention}, Busca el juego en el grupo y toca el enlace para obtenerlo aqui"
            )


@bot.on_message(command("add_game") & private)
async def add_game(client: Client, message: Message):
    admins: List[str] = os.getenv("ADMINS").split(",")

    if str(message.from_user.id) in admins:
        insert(
            Game(
                name=message.command[1],
                file_ids=[
                    i
                    for i in range(
                        int(message.command[2].split("-")[0]),
                        int(message.command[2].split("-")[1]) + 1,
                    )
                ],
            )
        )
        await message.reply(
            f"Juego Añadido -> https://t.me/GL_game_server_bot?start={message.command[1]}"
        )
    else:
        await message.reply("No tienes permiso para usar este comando")


if __name__ == "__main__":
    print("starting bot")
    bot.start()
    print("bot started")
    bot.loop.run_forever()
