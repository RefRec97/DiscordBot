import logging
import inspect
from discord.ext import commands
import utils.db as Database
from utils.authHandler import AuthHandler

class Allianz(commands.Cog):
    def __init__(self, bot: commands.bot):
        self._bot: commands.bot = bot
        self._allianzData: dict = {}
        self._topAllianzData: dict = {}
        self._db = Database.db()

        self.setup()
    
    @commands.check(AuthHandler.instance().check)
    @commands.command()
    async def allianz(self, ctx: commands.context, *,allianzName):
        """Zeigt die Top 10 Spieler der Allianz <allianzname> an"""
        allianzName = allianzName.lower()

        if not self._db.check_ally(allianzName):
            await ctx.send('Allianzname nicht gefunden')
            return

        await ctx.send(self._getAllianzString(allianzName))

    @commands.check(AuthHandler.instance().check)
    @commands.command(usage="<allianzname>,<galaxy>",
                      brief="Zeigt alle Planeten der Allianz in einer Galaxy an",
                      help="Zeigt alle Planeten der Allianz <allianzname> in einer Galaxy <galaxy> an.")
    async def allianzPosition(self, ctx: commands.context, *,argumente):
        argumente = argumente.lower()
        if "," in argumente:
            allianzName = argumente.split(',')[0]
            galaxy = argumente.split(',')[1]
        else:
            raise commands.MissingRequiredArgument(param=inspect.Parameter("galaxy",inspect._ParameterKind.VAR_POSITIONAL))
        
        if not self._db.check_ally(allianzName):
            await ctx.send('Allianzname nicht gefunden')
            return
        

        await ctx.send(self._getAllianzPosString(allianzName, galaxy))

    @allianz.error
    async def allianz_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Allianzname fehlt!\nBsp.: !allianz Allianz mit Poll')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    @allianzPosition.error
    async def allianzPosition_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Fehlende Argumente!\nBsp.: !allianzPosition Allianz mit Poll,3')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')

    def setup(self):
        logging.info("Allianz: Get Data references")

    def updateCallback(self):
        logging.info("Allianz: Updated Data references")
        self._allianzData = self._PlayerData.getAllianzDataReference()
        self._topAllianzData = self._getAllTopAllianzMembers(self._allianzData)

    def _getAllianzPosString(self, allianzName, galaxy):
        allianzPlanetsinGalaxy = self._db.get_allypos_gal(allianzName, galaxy)
        return self._getStringFromPlanets(allianzPlanetsinGalaxy, galaxy)
    
    def _getStringFromPlanets(self, planets: list, gal: str):
        if len(planets) == 0:
            return f"``` Keine bekannte Planeten in galaxy {gal} ```"
        
        returnStr = "```"
        for idx,pos in enumerate(planets):
            if (idx%5==0):
                returnStr += "\n"
            returnStr += "{:10}".format(pos)

        return returnStr + "```"

    def _getAllianzString(self, allianzName):
        returnMsg = f"```Top 10 von Allianz {allianzName}\n"
        returnMsg +="{:1} {:4} {:20} {:<10} {:10} \n\n".format("","","Name", "Punkte", "Flotte")
        topally = self._db.get_top_ally(allianzName)
        for i in range(10):
            arrow = "-" #equal
            try:
                diff =0
                #todo calc diff
                # diff = int(userData["diff_platz"])
            except:
                arrow = "" # no history data
            
            if diff > 0:
                arrow = "\u2193" #down
            elif diff < 0:
                arrow = "\u2191" #up
            
            returnMsg +="{:1} {:4} {:20} {:<10} {:10}\n".format(arrow, 
                                                                topally['p'+str(i)]["generalRank"],
                                                                topally['p'+str(i)]["name"],
                                                                topally['p'+str(i)]["generalScore"],
                                                                topally['p'+str(i)]["fleetScore"])
        return returnMsg + "```"

def setup(bot: commands.Bot):
    bot.add_cog(Allianz(bot))
