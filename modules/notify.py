
import logging
import interactions
from h11 import Data
import utils.db as Database
from utils.authHandler import AuthHandler
from interactions.ext.get import get

class Notify(interactions.Extension):
    def __init__(self, bot: interactions.Client):
        self.bot: interactions.Client = bot
        self._channels = {}
        self._db = Database.db()
    
    @interactions.extension_command(
        name="add_update",
        description="Fügt channel zu Updatenachrichten hinzu",
        options = [
            interactions.Option(
                name="channel_id",
                description="channel_id des Channels",
                type=interactions.OptionType.STRING,
                required=True,
            ),
        ],
    )
    async def add_update(self, ctx: interactions.CommandContext, channel_id: int):
        if self._db.check_updatechannel(channel_id):
            returnMsg = "Channel bereits vorhanden"
            await ctx.send(returnMsg)
            return

        self._db.add_updatechannel(channel_id)
        if self._db.check_updatechannel(channel_id):
            returnMsg = "Channel hinzugefügt"
        else:
            returnMsg = "Fehler beim Channel hinzufügen"
        
        await ctx.send(returnMsg)
    
    #@addUpdate.error
    async def addUpdate_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Fehlende Argumente!\nBsp.: !addUpdate 123456789')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    async def sendUpdates(self, msg):
        channeltosend = self._db.get_updatechannel()
        for channelId in channeltosend:
            try:
                channel = await get(self.bot, interactions.Channel, channel_id=channelId)
                await channel.send(msg)
            except:
                logging.error("Notify: Failed to send Update Channel")   

def setup(bot: interactions.Client):
    Notify(bot)