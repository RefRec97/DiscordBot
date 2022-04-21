import inspect
import logging
import re
from discord.ext import commands

from utils.fileHandler import FileHandler
from utils.playerData import PlayerData
from utils.authHandler import AuthHandler

class Planet(commands.Cog):
    def __init__(self, bot: commands.bot):
        self._bot: commands.bot = bot
        self._FileHandler: FileHandler = FileHandler.instance()
        self._PlayerData: PlayerData = PlayerData.instance()
        self._planetData: dict = {}

        self.setup()

    @commands.command(usage="<g>:<s>:<p>,<username>",
                      brief="Speichert einen neuen Planeten",
                      help="Speichert den Planet an position <g>:<s>:<p> zu dem spieler <username> ab")
    @commands.check(AuthHandler.instance().check)
    async def addPlanet(self, ctx: commands.context, *, argumente):
        argumente = argumente.lower()
        if "," in argumente:
            position = argumente.split(',')[0]
            username = argumente.split(',')[1]
        else:
            raise commands.MissingRequiredArgument(param=inspect.Parameter("username",inspect._ParameterKind.VAR_POSITIONAL))

        try:
            result = re.search("^(\d):(\d{1,3}):(\d{1,3})$",position)
            position = "{}:{}:{}".format(result.group(1),result.group(2),result.group(3))
        except:
            await ctx.send('Poisiton konnte nicht geparst werden\nz.B.: !addPlanet 1:1:1,Name')
            return
        if not username in self._planetData:
            await ctx.send('Spieler nicht gefunden')
            return
        

        if position in self._planetData[username]:
            await ctx.send('Planet bereits gespeichert')
            return
        else:
            planet = {"moon": False}
            self._planetData[username][position] = planet
            if not self._FileHandler.setPlanetData(self._planetData):
                await ctx.send('Fehler beim Speichern des Planeten')
                return

        await ctx.send('Planet gespeichert')

    @commands.check(AuthHandler.instance().check)
    @commands.command(usage="<g>:<s>:<p>,<username>",
                      brief="Löscht einen Planeten",
                      help="Löscht den Planet an position <g>:<s>:<p> von dem spieler <username>")
    async def delPlanet(self, ctx: commands.context, *, argumente):
        argumente = argumente.lower()
        if "," in argumente:
            position = argumente.split(',')[0]
            username = argumente.split(',')[1]
        else:
            raise commands.MissingRequiredArgument(param=inspect.Parameter("username",inspect._ParameterKind.VAR_POSITIONAL))

        if not username in self._planetData:
            await ctx.send('Spieler nicht gefunden')
            return
        try:
            result = re.search("^(\d):(\d{1,3}):(\d{1,3})$",position)
            position = "{}:{}:{}".format(result.group(1),result.group(2),result.group(3))
        except:
            await ctx.send('Poisiton konnte nicht geparst werden\nz.B.: !delPlanet 1:1:1,Sc0t')
            return
        
        if not position in self._planetData[username]:
            await ctx.send('Planet nicht vorhanden')
            return
        else:
            self._planetData[username].pop(position,None)
            if not self._FileHandler.setPlanetData(self._planetData):
                await ctx.send('Fehler beim Löschen des Planeten')
                return
        
        await ctx.send('Planet gelöscht')

    @commands.command(usage="<g>:<s>:<p>,<username>",
                      brief="Speichert einen neuen Mond",
                      help="Speichert den Mond an position <g>:<s>:<p> zu dem spieler <username> ab")
    @commands.check(AuthHandler.instance().check)
    async def addMoon(self, ctx: commands.context, *, argumente):
        argumente = argumente.lower()
        if "," in argumente:
            position = argumente.split(',')[0]
            username = argumente.split(',')[1]
        else:
            raise commands.MissingRequiredArgument(param=inspect.Parameter("username",inspect._ParameterKind.VAR_POSITIONAL))

        try:
            result = re.search("^(\d):(\d{1,3}):(\d{1,3})$",position)
            position = "{}:{}:{}".format(result.group(1),result.group(2),result.group(3))
        except:
            await ctx.send('Poisiton konnte nicht geparst werden\nz.B.: !addMoon 1:1:1,Name')
            return
        if not username in self._planetData:
            await ctx.send('Spieler nicht gefunden')
            return
        

        if not position in self._planetData[username]:
            await ctx.send('Kein Planet auf der Position')
            return
        elif self._planetData[username][position]["moon"] == True:
            await ctx.send('Mond bereits gespeichert')
            return
        else:
            self._planetData[username][position]["moon"] = True
            if not self._FileHandler.setPlanetData(self._planetData):
                await ctx.send('Fehler beim Speichern des Mondes')
                return

        await ctx.send('Mond gespeichert')
    
    @commands.command(usage="<g>:<s>:<p>,<username>",
                      brief="Löscht einen Mond",
                      help="Löscht den Mond an position <g>:<s>:<p> von dem spieler <username>")
    @commands.check(AuthHandler.instance().check)
    async def delMoon(self, ctx: commands.context, *, argumente):
        argumente = argumente.lower()
        if "," in argumente:
            position = argumente.split(',')[0]
            username = argumente.split(',')[1]
        else:
            raise commands.MissingRequiredArgument(param=inspect.Parameter("username",inspect._ParameterKind.VAR_POSITIONAL))

        try:
            result = re.search("^(\d):(\d{1,3}):(\d{1,3})$",position)
            position = "{}:{}:{}".format(result.group(1),result.group(2),result.group(3))
        except:
            await ctx.send('Poisiton konnte nicht geparst werden\nz.B.: !delMoon 1:1:1,Name')
            return
        if not username in self._planetData:
            await ctx.send('Spieler nicht gefunden')
            return
        
        if not position in self._planetData[username]:
            await ctx.send('Kein Planet auf der Position')
            return
        elif self._planetData[username][position]["moon"] == False:
            await ctx.send('Mond bereits gelöscht')
            return
        else:
            self._planetData[username][position]["moon"] = False
            if not self._FileHandler.setPlanetData(self._planetData):
                await ctx.send('Fehler beim Löschen des Mondes')
                return

        await ctx.send('Mond gelöscht')


    @addPlanet.error
    async def addPlanet_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Fehlende Argumente!\nBsp.: !addPlanet 1:1:1,Sc0t')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    @delPlanet.error
    async def delPlanet_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Fehlende Argumente!\nBsp.: !delPlanet 1:1:1,Sc0t')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    @addMoon.error
    async def addMoon_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Fehlende Argumente!\nBsp.: !addMoon 1:1:1,Sc0t')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    @delMoon.error
    async def delMoon_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Fehlende Argumente!\nBsp.: !delMoon 1:1:1,Sc0t')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')

    def setup(self):
        logging.info("Planet: Get Data references")
        self._planetData = self._PlayerData.getPlanetDataReference(self.updateCallback)

    def updateCallback(self):
        logging.info("Planet: Updated PlanetData references")
        self._planetData = self._PlayerData.getPlanetDataReference()

def setup(bot: commands.Bot):
    bot.add_cog(Planet(bot))
