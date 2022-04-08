from this import d
from discord.ext import commands

from utils.fileHandler import FileHandler
from utils.myData import MyData

class Stats(commands.Cog):
    def __init__(self, bot: commands.bot):
        self._bot = bot
        self._fileHandler = FileHandler.instance()
        self._fields = ["platz", "username", "allianz", "heimatplanet", "gesamt", "flotte", "defensive", "gebäude", "forschung"]
        self._userData = None
        self._historyData = None
        self.updateData()
    
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

    def updateData(self):
        self._updateUserData()
        self._updateHistoryData()

    def _updateHistoryData(self):
        self._historyData = self._fileHandler.getHistoryData()
        self._insertDiffDataToUser()
    
    def _insertDiffDataToUser(self):
        for user in self._historyData:
            userData = self._historyData[user][0]
            for element in userData:
                data = str(userData[element]).replace(".","")
                if data.isnumeric():
                    try:
                        currentData = str(self._historyData[user][-1][element]).replace(".","")
                        lastData = str(self._historyData[user][-2][element]).replace(".","")
                        self._userData[user]["diff_"+element] = "{:+g}".format(int(currentData) - int(lastData))
                    except:
                        if user in self._userData:
                            self._userData[user]["diff_"+ element] = "N/A"
    
    def _updateUserData(self):
        myData = self._fileHandler.getCurrentData()
        if(myData.valid):
            self._userData = myData.data

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
