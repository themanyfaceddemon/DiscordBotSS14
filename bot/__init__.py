import discord
import toml
from discord.ext import commands

from classes.db_manager import DBManager
from classes.lang import LanguageManager

with open("config.toml", "r") as file:
    config = toml.load(file)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config["bot"]["prefix"], intents=intents, help_command=None)
lang = LanguageManager(config["lang"]["code"])
db_manager = DBManager(config["db"]["name"])
