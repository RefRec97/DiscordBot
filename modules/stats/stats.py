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
        await ctx.send(self._getOutputString(self._userData[username]))

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

    def _getOutputString(self,userdata):
        returnMsg = "```"
        for field in self._fields:
            if f"diff_{field}" in userdata:
                returnMsg += "{0:30}{1:10} ({2})\n".format(field.capitalize(),str(userdata[field]), userdata["diff_" +field])
            elif userdata[field] == "sc0t":
                returnMsg += "{0:30}{1:10} {2}\n".format(field.capitalize(),userdata[field], "<- Noob")
            else:
                returnMsg += "{0:30}{1}\n".format(field.capitalize(),userdata[field])
        
        #addPlanetData
        returnMsg += "\n{0:30}\n".format("Bekannte Planeten")
        for planetPos in userdata["planets"]:
            returnMsg += "[{}]\n".format(planetPos)
        
        print(returnMsg)
        return returnMsg + "```"

def setup(bot: commands.Bot):
    bot.add_cog(Stats(bot))
