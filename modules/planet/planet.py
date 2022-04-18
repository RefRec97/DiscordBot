import logging
import re
from discord.ext import commands

from utils.playerData import PlayerData
from utils.authHandler import AuthHandler

class Planet(commands.Cog):
    def __init__(self, bot: commands.bot):
        self._bot: commands.bot = bot
        self._PlayerData: PlayerData = PlayerData.instance()
        self._userNames: list = []

        self.setup()

    @commands.command(usage="<g>:<s>:<p> <username>",
                      brief="Speichert einen neuen Planeten",
                      help="Speichert den Planet an position <g>:<s>:<p> zu dem spieler <username> ab")
    @commands.check(AuthHandler.instance().check)
    async def planet(self, ctx: commands.context, position: str, username: str):
        position = position.lower()
        username = username.lower()

        if not username in self._userNames:
            await ctx.send('Spieler nicht gefunden')
            return
        try:
            result = re.search("^(\d):(\d{1,3}):(\d{1,3})$",position)
            position = "{}:{}:{}".format(result.group(1),result.group(2),result.group(3))
        except:
            await ctx.send('Poisiton konnte nicht geparst werden\nz.B.: !planet 1:1:1 Name')
            return
        
        returnMsg: str
        if self._addPlanet(position, username):
            returnMsg = "Planet gespeichert"
        else:
            returnMsg = "Fehler beim Speichern des Planeten"

        await ctx.send(returnMsg)

    @commands.check(AuthHandler.instance().check)
    @commands.command(usage="<g>:<s>:<p> <username>",
                      brief="Löscht einen Planeten",
                      help="Löscht den Planet an position <g>:<s>:<p> von dem spieler <username>")
    async def boom(self, ctx: commands.context, position: str, username: str):
        position = position.lower()
        username = username.lower()
        if not username in self._userNames:
            await ctx.send('Spieler nicht gefunden')
            return
        try:
            result = re.search("^(\d):(\d{1,3}):(\d{1,3})$",position)
            position = "{}:{}:{}".format(result.group(1),result.group(2),result.group(3))
        except:
            await ctx.send('Poisiton konnte nicht geparst werden\nz.B.: !boom 1:1:1 Name')
            return
        
        returnMsg: str
        if self._delPlanet(position, username):
            returnMsg = "Planet gelöscht"
        else:
            returnMsg = "Fehler beim Löschen des Planeten"
        
        await ctx.send(returnMsg)

    @planet.error
    async def planet_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Fehlende Argumente!\nBsp.: !planet 1:1:1 sc0t')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    @boom.error
    async def boom_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Fehlende Argumente!\nBsp.: !boom 1:1:1 sc0t')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')

    def setup(self):
        logging.info("Planet: Get Data references")
        self._userNames = self._PlayerData.getUserNamesReference(self.updateCallback)

    def updateCallback(self):
        logging.info("Planet: Updated Data references")
        self._userNames = self._PlayerData.getUserNamesReference()

    def _addPlanet(self, position, user):
        return self._PlayerData.addPlanet(position, user)
    
    def _delPlanet(self, position, user):
        return self._PlayerData.delPlanet(position, user)

def setup(bot: commands.Bot):
    bot.add_cog(Planet(bot))
