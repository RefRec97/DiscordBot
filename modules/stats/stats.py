import logging
from discord.ext import commands

from utils.playerData import PlayerData

class Stats(commands.Cog):
    def __init__(self, bot: commands.bot):
        self._bot: commands.bot = bot
        self._PlayerData: PlayerData = PlayerData.instance()
        self._fields = ["platz", "username", "allianz", "heimatplanet", "gesamt", "flotte", "defensive", "gebäude", "forschung"]
        self._userData: dict = {}
        self._historyData: dict = {}

        
        self.setup()
    
    @commands.command()
    async def stats(self, ctx: commands.context, username: str):
        """Zeigt die Werte des Spielers <username> an"""
        username = username.lower()
        await ctx.send(self._getStatsString(username))

    @commands.command()
    async def history(self, ctx: commands.context, username: str):
        """Zeigt die Historie des Spielers <username> an"""
        username = username.lower()
        await ctx.send(self._getHistoryString(username))

    @stats.error
    async def stats_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Spielername fehlt!\nBsp.: !stats Sc0t')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    @history.error
    async def history_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Spielername fehlt!\nBsp.: !history Sc0t')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')

    def setup(self):
        logging.info("Stats: Get Data references")
        self._userData = self._PlayerData.getUserDataReference()
        self._historyData = self._PlayerData.getHistoryDataReference()

    def _getHistoryString(self, username):
        if not username in self._historyData:
            return "Nutzer nicht gefunden"
        
        #only use last 7 entrys
        data = self._historyData[username][-7:]

        returnMsg = f"```Spieler {username}\n"
        returnMsg +="{0:11} {1:10} {2:10} {3:10} {4:10}\n".format("Timestamp", "Platz", "Gesamt", "Flotte", "Gebäude")
        for entry in data:
            returnMsg += "{0:11} {1:10} {2:10} {3:10} {4:10}\n".format(entry["timestamp"], str(entry["platz"]),
                                                                       entry["gesamt"] ,entry["flotte"], entry["gebäude"])
        returnMsg += "{0:11} {1:10} {2:10} {3:10} {4:10}\n".format("Differenz", 
                                                                   self._userData[username]["diff_platz"],
                                                                   self._userData[username]["diff_gesamt"],
                                                                   self._userData[username]["diff_flotte"],
                                                                   self._userData[username]["diff_gebäude"])
        return returnMsg + "```"

    def _getStatsString(self, username):
        if not username in self._userData:
            return "Nutzer nicht gefunden"
        userData = self._userData[username]

        returnMsg = "```"
        for field in self._fields:
            if f"diff_{field}" in userData:
                returnMsg += "{0:30}{1:10} ({2})\n".format(field.capitalize(),str(userData[field]), userData["diff_" +field])
            elif userData[field] == "sc0t":
                returnMsg += "{0:30}{1:10} {2}\n".format(field.capitalize(),userData[field], "<- Noob")
            else:
                returnMsg += "{0:30}{1}\n".format(field.capitalize(),userData[field])
        
        #addPlanetData
        returnMsg += "\n{0:30}\n".format("Bekannte Planeten")
        for planetPos in userData["planets"]:
            returnMsg += "[{}]\n".format(planetPos)
        
        return returnMsg + "```"

def setup(bot: commands.Bot):
    bot.add_cog(Stats(bot))
