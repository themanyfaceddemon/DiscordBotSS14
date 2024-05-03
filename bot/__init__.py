import discord
import toml
from discord.ext import commands

from classes.lang import LanguageManager

with open("config.toml", "r") as file:
    config = toml.load(file)
    command_prefix = config["bot"]["command_prefix"]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=command_prefix, intents=intents, help_command=None)
lang = LanguageManager()
