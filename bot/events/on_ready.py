import logging

import discord
import discord.ext

from bot import bot
from bot.events.read_role import read_role


@bot.event
async def on_ready():
    logging.info(f"Start read_role loop")
    read_role.start()

    logging.info(f"{bot.user} is ready and online!")
