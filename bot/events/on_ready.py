import logging

import discord
import discord.ext

from bot import bot


@bot.event
async def on_ready():
    logging.info(f"{bot.user} is ready and online!")
