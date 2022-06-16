from discord.ext import commands
import logging

from h11 import Data
import utils.db as Database
from utils.authHandler import AuthHandler

class Notify(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot: commands.bot = bot
        self._channels = {}
        self._db = Database.db()
    
    @commands.check(AuthHandler.instance().check)
    @commands.command(usage="<channelId>",
                      brief="Fügt channel zu Updatenachrichten hinzu",
                      help="Fügt channel mit der id <channelId> zu Updatenachrichten hinzu")
    async def addUpdate(self, ctx: commands.context, channelID: int):
        if self._db.check_updatechannel(channelID):
            await ctx.send(returnMsg)
            return

        self._db.add_updatechannel(channelID)
        if self._db.check_updatechannel(channelID):
            returnMsg = "Channel hinzugefügt"
        else:
            returnMsg = "Fehler beim Channel hinzufügen"
        
        await ctx.send(returnMsg)
    
    @addUpdate.error
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
                channel = self.bot.get_channel(int(channelId))
                await channel.send(msg)
            except:
                logging.error("Notify: Failed to send Update Channel")   

def setup(bot: commands.Bot):
    bot.add_cog(Notify(bot))
