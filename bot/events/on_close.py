import logging

import discord
import discord.ext

from bot import bot
from bot.events.read_role import read_role


async def on_close() -> None:
    logging.info(f"Stop read_role loop")
    read_role.stop()

    logging.info(f"Shutdown {bot.user}")
    bot.close()
