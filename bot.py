from discord.ext import commands
import os
import logging
import interactions
from interactions import Intents


import utils.config as config
from modules import *
from utils.authHandler import AuthHandler
#from utils.playerData import PlayerData

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Programm started")

    client = commands.Bot(command_prefix="!", case_insensitive=True)
    bot = interactions.Client(token=config.token, intents=Intents.DEFAULT | Intents.GUILD_MESSAGE_CONTENT)
    autHandler = AuthHandler.instance()
    autHandler.addBot(bot)

    for name in os.listdir(os.path.join(os.path.abspath(os.getcwd()),"modules")):
        if os.path.exists(os.path.join("modules", name)):
            bot.load(f"modules.{name}.{name}")
            logging.info(f"Bot: Module {name} loaded")

    #client.run()
    bot.load("modules.utils.utils")
    bot.start()

if __name__ == '__main__':
    main()