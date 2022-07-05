import os
import logging
from bot_utils.authHandler import AuthHandler
import interactions
from interactions import Intents


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Programm started")
    bot = interactions.Client(token=os.getenv('vvj_token'), intents=Intents.DEFAULT | Intents.GUILD_MESSAGE_CONTENT)

    authHandler = AuthHandler.instance()
    authHandler.addBot(bot)

    current_workdir = os.path.abspath(os.getcwd())
    modules_path = os.path.join(current_workdir, "modules")
    for name in os.listdir(modules_path):
        if os.path.isfile(name):
            logging.error(name)
            bot.load(f"modules.{name}")
            logging.info(f"Bot: Module {name} loaded")

    bot.load("modules.tools")
    bot.start()


if __name__ == '__main__':
    main()