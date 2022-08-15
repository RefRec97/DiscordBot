import os
import logging
from bot_utils.authHandler import AuthHandler
import interactions
from interactions import Intents
from bot_utils import bot_password_token_file as config
#import subprocess
#subprocess.run('python install_packages.py')

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Programm started")

    bot = interactions.Client(token=str(config.token), intents=Intents.DEFAULT | Intents.GUILD_MESSAGE_CONTENT)

    #authHandler = AuthHandler.instance()
    #authHandler.addBot(bot)

    current_workdir = os.path.abspath(os.getcwd())
    modules_path = os.path.join(current_workdir, "modules")

    for name in os.listdir(modules_path):
        search = os.path.join(modules_path, name)
        if os.path.isfile(search):
            module_name = os.path.splitext(name)[0]
            bot.load(f"modules.{module_name}")
            logging.info(f"Bot: Module {module_name} loaded")

    bot.start()


if __name__ == '__main__':
    main()