import inspect
import logging
import re

from bot_utils.authHandler import AuthHandler
from bot_utils.db import DataBase
import interactions

class Planet(interactions.Extension):
    def __init__(self, bot: interactions.Client):
        self.bot: interactions.Client = bot
        self._planetData: dict = {}
        self._db = DataBase()

    @interactions.extension_command(
        name="add_planet",
        description="Speichert einen neuen Planeten",
        options = [
            interactions.Option(
                name="username",
                description="username des Spielers",
                type=interactions.OptionType.STRING,
                required=True,
            ),
            interactions.Option(
                name="position",
                description="position im format <g>:<s>:<p>",
                type=interactions.OptionType.STRING,
                required=True,
            ),
        ],
    )
    async def add_planet(self, ctx: interactions.CommandContext, *, username, position):
        
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
        await ctx.defer()
        id = self._db.get_id(username)
        if self._db.check_planets(galaxy, system, location):
            await ctx.send('Planet bereits gespeichert')
            return
        else:
            self._db.add_planet(galaxy, system, location, id)
            #todo check for failure

        await ctx.send('Planet gespeichert')

    @interactions.extension_command(
        name="del_planet",
        description="Löscht einen Planeten",
        options = [
            interactions.Option(
                name="username",
                description="username des Spielers",
                type=interactions.OptionType.STRING,
                required=True,
            ),
            interactions.Option(
                name="position",
                description="position im format <g>:<s>:<p>",
                type=interactions.OptionType.STRING,
                required=True,
            ),
        ],
    )
    async def del_planet(self, ctx: interactions.CommandContext, *, username, position):
        
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
        await ctx.defer()
        id = self._db.get_id(username)
        if not self._db.check_planets(galaxy, system, location):
            await ctx.send('Planet nicht vorhanden')
            return
        else:
            self._db.del_planet(galaxy, system, location)
            #todo: check for failure
        
        await ctx.send('Planet gelöscht')

    @interactions.extension_command(
        name="add_moon",
        description="Speichert einen neuen Mond",
        options = [
            interactions.Option(
                name="username",
                description="username des Spielers",
                type=interactions.OptionType.STRING,
                required=True,
            ),
            interactions.Option(
                name="position",
                description="position im format <g>:<s>:<p>",
                type=interactions.OptionType.STRING,
                required=True,
            ),
        ],
    )
    async def add_moon(self, ctx: interactions.CommandContext, *, username, position):

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
        await ctx.defer()
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
    
    @interactions.extension_command(
        name="del_moon",
        description="Löscht einen Mond",
        options = [
            interactions.Option(
                name="username",
                description="username des Spielers",
                type=interactions.OptionType.STRING,
                required=True,
            ),
            interactions.Option(
                name="position",
                description="position im format <g>:<s>:<p>",
                type=interactions.OptionType.STRING,
                required=True,
            ),
        ],
    )
    async def del_moon(self, ctx: interactions.CommandContext, *, username, position):

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
        await ctx.defer()
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


    #@addPlanet.error
    async def addPlanet_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Fehlende Argumente!\nBsp.: !addPlanet 1:1:1,Sc0t')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    #@delPlanet.error
    async def delPlanet_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Fehlende Argumente!\nBsp.: !delPlanet 1:1:1,Sc0t')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    #@addMoon.error
    async def addMoon_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Fehlende Argumente!\nBsp.: !addMoon 1:1:1,Sc0t')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    #@delMoon.error
    async def delMoon_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Fehlende Argumente!\nBsp.: !delMoon 1:1:1,Sc0t')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')

def setup(bot: interactions.Client):
    Planet(bot)
