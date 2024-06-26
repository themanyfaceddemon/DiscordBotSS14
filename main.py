import logging

import discord
import toml
from colorlog import ColoredFormatter

from bot import bot
from bot.commands import login
from bot.events import on_ready


def main() -> None:
    with open("config.toml", "r") as file:
        config = toml.load(file)
    try:
        bot.run(config["bot"]["token"])
    except discord.errors.LoginFailure as err:
        logging.fatal(f"Bot login fatal error: {err}")

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    console_handler = logging.StreamHandler()
    formatter = ColoredFormatter(
        "[%(asctime)s] [%(log_color)s%(levelname)s%(reset)s] - %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'purple',
        },
        secondary_log_colors={},
        style='%'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    main()
