import logging
from discord.ext import commands

from utils.playerData import PlayerData

class Allianz(commands.Cog):
    def __init__(self, bot: commands.bot):
        self._bot: commands.bot = bot
        self._PlayerData: PlayerData = PlayerData.instance()
        self._allianzData: dict = {}

        self.setup()
    
    @commands.command()
    async def allianz(self, ctx: commands.context, *,allianzName):
        """Zeigt die Top 10 Spieler der Allianz <allianzname> an"""
        allianzName = allianzName.lower()

        if not allianzName in self._allianzData:
            await ctx.send('Allianzname nicht gefunden')
            return

        await ctx.send(self._getAllianzString(allianzName))

    @allianz.error
    async def allianz_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Allianzname fehlt!\nBsp.: !allianz Allianz mit Poll')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')

    def setup(self):
        logging.info("Allianz: Get Data references")
        self._allianzData = self._PlayerData.getAllianzDataReference()

    def _getAllianzString(self, allianzName):
        returnMsg = f"```Top 10 von Allianz {allianzName}\n"
        returnMsg +="{:1} {:4} {:20} {:<10} {:10} \n\n".format("","","Name", "Punkte", "Flotte")

        for userData in self._allianzData[allianzName]:           
            arrow = "-" #equal
            try:
                diff = int(userData["diff_platz"])
            except:
                arrow = "" # no history data
            
            if diff > 0:
                arrow = "\u2193" #down
            elif diff < 0:
                arrow = "\u2191" #up
            
            returnMsg +="{:1} {:4} {:20} {:<10} {:10}\n".format(arrow, 
                                                                userData["platz"],
                                                                userData["username"],
                                                                userData["gesamt"],
                                                                userData["flotte"])
        return returnMsg + "```"

def setup(bot: commands.Bot):
    bot.add_cog(Allianz(bot))
