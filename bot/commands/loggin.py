import discord
import discord.ext
import discord.ext.commands
from discord import Option
import toml

from bot import bot, lang
from classes.ss14login import SS14Login
from classes.lang import LanguageManager



@bot.slash_command(name="loggin", description=lang.loc('loggin', 'com_desc'))
async def loggin(
    ctx:           discord.ApplicationContext,
    name_or_emain: Option(str, description=lang.loc('loggin', 'arg_desc_name_or_emain'), required=True), # type: ignore
    password:      Option(str, description=lang.loc('loggin', 'arg_desc_password'), required=True)       # type: ignore
    ):
    ss14login = SS14Login()

    if ss14login.login(name_or_emain, password):
        resp = lang.loc('loggin', 'correct')
    else:
        resp = lang.loc('loggin', 'error')

    await ctx.respond(resp, ephemeral=True)
