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
        name="planet_add",
        description="Speichert einen neuen Planeten",
        options = [
            interactions.Option(
                name="username",
                description="username des Spielers",
                type=interactions.OptionType.STRING,
                required=True,
            ),
            interactions.Option(
                name="galaxy",
                description="Galaxie des Mondes",
                type=interactions.OptionType.INTEGER,
                required=True,
            ),
            interactions.Option(
                name="system",
                description="System in der Galaxie",
                type=interactions.OptionType.INTEGER,
                required=True,
            ),
            interactions.Option(
                name="position",
                description="Position im System",
                type=interactions.OptionType.INTEGER,
                required=True,
            ),
        ],
    )
    async def planet_add(self, ctx: interactions.CommandContext, *, username, galaxy:int, system:int, position:int):
        if not self._db.check_player(username):
            await ctx.send('Spieler nicht gefunden')
            return
        await ctx.defer()
        id = self._db.get_id(username)
        if self._db.check_planets(galaxy, system, position):
            await ctx.send('Planet bereits gespeichert')
            return
        else:
            if(AuthHandler.instance().check(ctx)):
                self._db.add_planet(galaxy, system, position, id)
                await ctx.send('Planet gespeichert')
            else:
                await ctx.send("Keine Rechte diesen Befehl zu nutzen")
            
            #todo check for failure

    @interactions.extension_command(
        name="planet_delete",
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
    async def planet_delete(self, ctx: interactions.CommandContext, *, username, position):
        
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
            if(AuthHandler.instance().check(ctx)):
                self._db.del_planet(galaxy, system, location)
                await ctx.send('Planet gelöscht')
            else:
                await ctx.send("Keine Rechte diesen Befehl zu nutzen")
            
            #todo: check for failure

    @interactions.extension_command(
        name="moon_add",
        description="Speichert einen neuen Mond",
        options = [
            interactions.Option(
                name="username",
                description="username des Spielers",
                type=interactions.OptionType.STRING,
                required=True,
            ),
            interactions.Option(
                name="galaxy",
                description="Galaxie des Mondes",
                type=interactions.OptionType.INTEGER,
                required=True,
            ),
            interactions.Option(
                name="system",
                description="System in der Galaxie",
                type=interactions.OptionType.INTEGER,
                required=True,
            ),
            interactions.Option(
                name="position",
                description="Position im System",
                type=interactions.OptionType.INTEGER,
                required=True,
            ),
            interactions.Option(
                name="phalanx",
                description="Level der Phalanx, standardmäßig 0",
                type=interactions.OptionType.STRING,
                required=False,
            ),
            interactions.Option(
                name="basis",
                description="Level der Mondbasis, standardmäßig 0",
                type=interactions.OptionType.STRING,
                required=False,
            ),
            interactions.Option(
                name="robo",
                description="Level der Roboterfabrik, standardmäßig 0",
                type=interactions.OptionType.STRING,
                required=False,
            ),
            interactions.Option(
                name="sprungtor",
                description="Level des Sprungtores, standardmäßig 0",
                type=interactions.OptionType.STRING,
                required=False,
            ),
        ],
    )
    async def moon_add(self, ctx: interactions.CommandContext, *, username, galaxy, system, position, phalanx=0, basis=0, robo=0, sprungtor=0):
        if(AuthHandler.instance().check(ctx)):
            if not self._db.check_player(username):
                await ctx.send('Spieler nicht gefunden')
                return
            await ctx.defer()
            id = self._db.get_id(username)
            status = ''
            if not self._db.check_planets(galaxy, system, position):
                self._db.add_planet(galaxy, system, position, id)
                status = 'Planet gespeichert\n'
            
            if self._db.check_moon(galaxy, system, position):
                await ctx.send('Mond bereits gespeichert')
                return
            else:
                self._db.add_moon(galaxy, system, position, id, phalanx, basis, robo, sprungtor)
                status = status + 'Mond gespeichert'
                await ctx.send(status)
        else:
            await ctx.send("Keine Rechte diesen Befehl zu nutzen")
            
            #todo: check for failure
    
    @interactions.extension_command(
        name="moon_update",
        description="Updatet einen existierenden Mond",
        options = [
            interactions.Option(
                name="position",
                description="position im format <g>:<s>:<p>",
                type=interactions.OptionType.STRING,
                required=True,
            ),
            interactions.Option(
                name="phalanx",
                description="Level der Phalanx, standardmäßig 0",
                type=interactions.OptionType.STRING,
                required=True,
            ),
            interactions.Option(
                name="basis",
                description="Level der Mondbasis, standardmäßig 0",
                type=interactions.OptionType.STRING,
                required=True,
            ),
            interactions.Option(
                name="robo",
                description="Level der Roboterfabrik, standardmäßig 0",
                type=interactions.OptionType.STRING,
                required=True,
            ),
            interactions.Option(
                name="sprungtor",
                description="Level des Sprungtores, standardmäßig 0",
                type=interactions.OptionType.STRING,
                required=True,
            ),
        ],
    )
    async def moon_update(self, ctx: interactions.CommandContext, *, position, phalanx, basis, robo, sprungtor):

        try:
            result = re.search("^(\d):(\d{1,3}):(\d{1,3})$",position)
            galaxy = result.group(1)
            system = result.group(2)
            location = result.group(3)
        except:
            await ctx.send('Position konnte nicht geparst werden\nz.B.: !addMoon 1:1:1,Name')
            return
        await ctx.defer()
        if not self._db.check_moon(galaxy, system, location):
            await ctx.send('Kein Mond vorhanden')
            return
        else:
            if(AuthHandler.instance().check(ctx)):
                self._db.update_moon(galaxy, system, location, phalanx, basis, robo, sprungtor)
                await ctx.send('Mond gespeichert')
            else:
                await ctx.send("Keine Rechte diesen Befehl zu nutzen")
            
            #todo: check for failure

    @interactions.extension_command(
        name="moone_delete",
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
    async def moon_delete(self, ctx: interactions.CommandContext, *, username, position):

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
            if(AuthHandler.instance().check(ctx)):
                self._db.del_moon(galaxy, system, location)
                await ctx.send('Mond gelöscht')
            else:
                await ctx.send("Keine Rechte diesen Befehl zu nutzen")
            
            #todo: check failure

    ##@addPlanet.error
    #async def addPlanet_error(self, ctx, error):
    #    if isinstance(error, commands.MissingRequiredArgument):
    #        await ctx.send('Fehlende Argumente!\nBsp.: !addPlanet 1:1:1,Sc0t')
    #    elif isinstance(error, commands.CheckFailure):
    #        await ctx.send('Keine rechte diesen Befehl zu nutzen')
    #    else:
    #        logging.error(error)
    #        await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    ##@delPlanet.error
    #async def delPlanet_error(self, ctx, error):
    #    if isinstance(error, commands.MissingRequiredArgument):
    #        await ctx.send('Fehlende Argumente!\nBsp.: !delPlanet 1:1:1,Sc0t')
    #    elif isinstance(error, commands.CheckFailure):
    #        await ctx.send('Keine rechte diesen Befehl zu nutzen')
    #    else:
    #        logging.error(error)
    #        await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    ##@addMoon.error
    #async def addMoon_error(self, ctx, error):
    #    if isinstance(error, commands.MissingRequiredArgument):
    #        await ctx.send('Fehlende Argumente!\nBsp.: !addMoon 1:1:1,Sc0t')
    #    elif isinstance(error, commands.CheckFailure):
    #        await ctx.send('Keine rechte diesen Befehl zu nutzen')
    #    else:
    #        logging.error(error)
    #        await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    ##@delMoon.error
    #async def delMoon_error(self, ctx, error):
    #    if isinstance(error, commands.MissingRequiredArgument):
    #        await ctx.send('Fehlende Argumente!\nBsp.: !delMoon 1:1:1,Sc0t')
    #    elif isinstance(error, commands.CheckFailure):
    #        await ctx.send('Keine rechte diesen Befehl zu nutzen')
    #    else:
    #        logging.error(error)
    #        await ctx.send('ZOMFG ¯\_(ツ)_/¯')

def setup(bot: interactions.Client):
    Planet(bot)
