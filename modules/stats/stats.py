import logging
from discord.ext import commands
from quickchart import QuickChart

from utils.playerData import PlayerData
from utils.authHandler import AuthHandler

class Stats(commands.Cog):
    def __init__(self, bot: commands.bot):
        self._bot: commands.bot = bot
        self._PlayerData: PlayerData = PlayerData.instance()
        self._fields = ["platz", "username", "allianz", "heimatplanet", "gesamt", "flotte", "defensive", "gebäude", "forschung"]
        self._userData: dict = {}
        self._historyData: dict = {}

        
        self.setup()
    
    @commands.check(AuthHandler.instance().check)
    @commands.command()
    async def stats(self, ctx: commands.context, username: str):
        """Zeigt die Werte des Spielers <username> an"""
        username = username.lower()
        await ctx.send(self._getStatsString(username))

    @commands.check(AuthHandler.instance().check)
    @commands.command()
    async def history(self, ctx: commands.context, username: str):
        """Zeigt die Historie des Spielers <username> an"""
        username = username.lower()
        await ctx.send(self._getHistoryString(username))

    @commands.check(AuthHandler.instance().check)
    @commands.command(usage="<username> [size]",
                      brief="Zeigt eine Diagramm an",
                      help="Zeigt ein Diagramm für den User <username> an. Die größe wird über den optionalen " +
                           "parameter [size] angepasst. Mögliche größen sind: S, M, L, XL (default: M)")
    async def chart(self, ctx: commands.context, username: str, size: str = None):
        username = username.lower()
        if isinstance(size,str):
            size = size.lower()
        
        if not username in self._historyData:
            return "Nutzer nicht gefunden"

        chartData = self._setupChartData(self._historyData[username])
       
        await ctx.send(self._getChartURL(chartData, size))

    @stats.error
    async def stats_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Spielername fehlt!\nBsp.: !stats Sc0t')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    @history.error
    async def history_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Spielername fehlt!\nBsp.: !history Sc0t')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    @chart.error
    async def chart_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Spielername fehlt!\nBsp.: !chart Sc0t')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')

    def setup(self):
        logging.info("Stats: Get Data references")
        self._userData = self._PlayerData.getUserDataReference()
        self._historyData = self._PlayerData.getHistoryDataReference()

    def _getChartURL(self, chartData: dict, size: str):
        qc = QuickChart()

        match size:
            case 's':
                qc.width = 500
                qc.height = 300
            case 'm':
                qc.width = 720
                qc.height = 480
            case 'l':
                qc.width = 1280
                qc.height = 720
            case 'xl':
                qc.width = 1980
                qc.height = 1080
            case _: #m
                qc.width = 720
                qc.height = 480
           
        qc.device_pixel_ratio = 2.0
        qc.config = {
            "type": "line",
            "data": {
                "labels": chartData["labels"],
                "datasets": [{
                    "yAxisID": "rankAxis",
                    "label": "Platz",
                    "data": chartData["platz"],
                    "fill": False,
                },{
                    "yAxisID": "pointAxis",
                    "label": "Gesamtpunkte",
                    "data": chartData["gesamt"],
                    "fill": False,
                },{
                    "yAxisID": "pointAxis",
                    "label": "Gebäude",
                    "data": chartData["gebäude"],
                    "fill": False,
                },{
                    "yAxisID": "pointAxis",
                    "label": "Forschung",
                    "data": chartData["forschung"],
                    "fill": False,
                },{
                    "yAxisID": "pointAxis",
                    "label": "Flotte",
                    "data": chartData["flotte"],
                    "fill": False,
                },{
                    "yAxisID": "pointAxis",
                    "label": "Defensive",
                    "data": chartData["defensive"],
                    "fill": False,
                }]
            },
            "options": {
                "scales": {
                "xAxes": [{
                    "stacked": True
                }],
                "yAxes": [{
                    "id": "rankAxis",
                    "display": True,
                    "position": "left",
                    "stacked": True,
                    },{
                    "id": "pointAxis",
                    "display": True,
                    "position": "right",
                    "gridLines": {
                        "drawOnChartArea": False
                    },
                    "ticks": {
                        "beginAtZero": True}
                    }]
                }
            }
        }
        return qc.get_short_url()

    def _setupChartData(self, historyData: dict):
        chartData= {
            "labels": [],
            "gesamt": [],
            "platz": [],
            "flotte": [],
            "gebäude": [],
            "defensive": [],
            "forschung": []
        }

        for day in historyData:
            chartData["labels"].append(day["timestamp"].rsplit("_",1)[0].replace("_","."))
            chartData["gesamt"].append(day["gesamt"].replace(".",""))
            chartData["platz"].append(day["platz"])
            chartData["flotte"].append(day["flotte"].replace(".",""))
            chartData["gebäude"].append(day["gebäude"].replace(".",""))
            chartData["defensive"].append(day["defensive"].replace(".",""))
            chartData["forschung"].append(day["forschung"].replace(".",""))

        return chartData

    def _getHistoryString(self, username):
        if not username in self._historyData:
            return "Nutzer nicht gefunden"
        
        #only use last 7 entrys
        data = self._historyData[username][-7:]

        returnMsg = f"```Spieler {username}\n\n"
        returnMsg +="{0:7} {1:5} {2:10} {3:10} {4:10}\n".format("Datum", "P.", "Gesamt", "Flotte", "Gebäude")
        for entry in data:
            returnMsg += "{0:7} {1:5} {2:10} {3:10} {4:10}\n".format(entry["timestamp"].rsplit("_",1)[0].replace("_","."), str(entry["platz"]),
                                                                     entry["gesamt"] ,entry["flotte"], entry["gebäude"])
        returnMsg += "{0:7} {1:5} {2:10} {3:10} {4:10}\n".format("Diff.", 
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
