import logging
import datetime
from bot_utils.authHandler import AuthHandler
from bot_utils.db import DataBase
import interactions

class Status(interactions.Extension):
    def __init__(self, bot: interactions.Client):
        self.bot: interactions.Client = bot
        self.lastUpdate = "N/A"
        self._db = DataBase()
    
    @interactions.extension_command(
        name="test",
        description="Pingt den Bot"
    )
    async def test(self, ctx: interactions.CommandContext):
        """Antwortet mit \"Test Bestanden\" (Verbindungstest)"""
        await ctx.send('Test bestanden')

    @interactions.extension_command(
        name="status",
        description="Stand des Datensatzes"
    )
    async def status(self, ctx: interactions.CommandContext):
        if datetime.datetime.now().hour >= 12 and datetime.datetime.now().minute > 32:
            lastUpdate = self._db.check_time(datetime.date.today())
        elif datetime.datetime.now().hour >= 13:
            lastUpdate = self._db.check_time(datetime.date.today())
        else:
            lastUpdate = self._db.check_time(datetime.date.today() - datetime.timedelta(days=1))

        """Stand des Datensatzes"""
        await ctx.send(f"Letztes Update: {lastUpdate}")

    #@test.error
    async def test_error(self, ctx, error):
        if isinstance(error, interactions.CommandContext):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    #@status.error
    async def status_error(self, ctx, error):
        if isinstance(error, interactions.CommandContext):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    


def setup(bot: interactions.Client):
    Status(bot)
