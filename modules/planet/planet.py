import inspect
import logging
import re
from discord.ext import commands

from utils.authHandler import AuthHandler
import utils.db as Database

class Planet(commands.Cog):
    def __init__(self, bot: commands.bot):
        self._bot: commands.bot = bot
        self._planetData: dict = {}
        self._db = Database.db()

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
            galaxy = result.group(1)
            system = result.group(2)
            location = result.group(3)
        except:
            await ctx.send('Poisiton konnte nicht geparst werden\nz.B.: !addPlanet 1:1:1,Name')
            return
        if not self._db.check_player(username):
            await ctx.send('Spieler nicht gefunden')
            return
        
        id = self._db.get_id(username)
        if self._db.check_planets(galaxy, system, location):
            await ctx.send('Planet bereits gespeichert')
            return
        else:
            self._db.add_planet(galaxy, system, location, id)
            #todo check for failure

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

        if not self._db.check_player(username):
            await ctx.send('Spieler nicht gefunden')
            return
        try:
            result = re.search("^(\d):(\d{1,3}):(\d{1,3})$",position)
            galaxy = result.group(1)
            system = result.group(2)
            location = result.group(3)
        except:
            await ctx.send('Poisiton konnte nicht geparst werden\nz.B.: !delPlanet 1:1:1,Sc0t')
            return

        id = self._db.get_id(username)
        if not self._db.check_planets(galaxy, system, location):
            await ctx.send('Planet nicht vorhanden')
            return
        else:
            self._db.del_planet(galaxy, system, location)
            #todo: check for failure
        
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
            galaxy = result.group(1)
            system = result.group(2)
            location = result.group(3)
        except:
            await ctx.send('Position konnte nicht geparst werden\nz.B.: !addMoon 1:1:1,Name')
            return
        if not self._db.check_player(username):
            await ctx.send('Spieler nicht gefunden')
            return
        
        id = self._db.get_id(username)
        if not self._db.check_planets(galaxy, system, location):
            await ctx.send('Kein Planet auf der Position')
            return
        elif self._db.check_moon(galaxy, system, location):
            await ctx.send('Mond bereits gespeichert')
            return
        else:
            self._db.add_moon(galaxy, system, location, id)
            #todo: check for failure

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
            galaxy = result.group(1)
            system = result.group(2)
            location = result.group(3)
        except:
            await ctx.send('Poisiton konnte nicht geparst werden\nz.B.: !delMoon 1:1:1,Name')
            return
        if not self._db.check_player(username):
            await ctx.send('Spieler nicht gefunden')
            return
        
        id = self._db.get_id(username)
        if not self._db.check_planets(galaxy, system, location):
            await ctx.send('Kein Planet auf der Position')
            return
        elif not self._db.check_moon(galaxy, system, location):
            await ctx.send('Mond bereits gelöscht')
            return
        else:
            self._db.del_moon(galaxy, system, location)
            #todo: check failure

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

def setup(bot: commands.Bot):
    bot.add_cog(Planet(bot))
