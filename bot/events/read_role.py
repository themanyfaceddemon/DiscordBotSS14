import logging

import discord
import discord.ext
import discord.ext.tasks

from bot import bot, config, db_manager


@discord.ext.tasks.loop(seconds=config["time"]["update_local_db"])
async def read_role() -> None:
    if config["roles"]["not_set"]:
        logging.critical("Donation roles have not been detected. Please set them and change 'not_set' to 'false'!")
        return
    
    roles_config = config['roles']
    roles_list = [(role_id, role_level) for role_id, role_level in roles_config.items() if role_id != 'not_set']

    for guild in bot.guilds:
        for member in guild.members:
            max_level = 0
            for role in member.roles:
                for role_id, role_level in roles_list:
                    if role.id == int(role_id) and role_level > max_level:
                        max_level = role_level
            db_manager.add_or_update_member(member.id, None, max_level)
