from quickchart import QuickChart

from bot_utils.db import DataBase
import options.trading_options as trading_options
import interactions
from bot_utils.authHandler import AuthHandler


class Trading(interactions.Extension):
    def __init__(self, bot: interactions.Client):
        self.bot: interactions.Client = bot
        self.db = DataBase()

def setup(bot: interactions.Client):
    Trading(bot)