import discord
import discord.ext
import discord.ext.commands
from discord import Option

from bot import bot, config, db_manager, lang
from classes.ss14login import SS14Login


@bot.slash_command(name="loggin", description=lang.loc('loggin', 'com_desc'), guild_ids=list[discord.Guild](config["bot"]["servers"]))
async def loggin(
    ctx:           discord.ApplicationContext,
    login:         Option(str, description=lang.loc('loggin', 'arg_desc_login'), required=True),   # type: ignore
    password:      Option(str, description=lang.loc('loggin', 'arg_desc_password'), required=True) # type: ignore
    ):
    ss14login = SS14Login()

    if ss14login.login(login, password):
        resp = lang.loc('loggin', 'correct')
        db_manager.add_or_update_member(ctx.author.id, login, None) # There may be a problem if a person enters email
    else:
        resp = lang.loc('loggin', 'error')

    await ctx.respond(resp, ephemeral=True)
