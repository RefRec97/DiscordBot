from ast import arg
import datetime
from email.policy import default
import logging
from tokenize import String
from h11 import Data
from quickchart import QuickChart
from bot_utils import authHandler
from bot_utils.db import DataBase
from bot_utils.authHandler import AuthHandler
from bot_utils.playerData import PlayerData
import interactions
import options.stats_options as stats_options


class Stats(interactions.Extension):
    def __init__(self, bot: interactions.Client):
        self.bot: interactions.Client = bot
        self._fields = ["username", "platz", "allianz", "gesamt", "flotte", "defensive", "gebäude", "forschung"]
        self._db = DataBase()
        self._playerData = PlayerData.instance()
        logging.basicConfig(level=logging.INFO)
        
        
        self.setup()
    
    @interactions.extension_command(
        name="stats",
        description="zeigt die statistiken des spielers an",
        options = [
            interactions.Option(
                name="username",
                description="username des Spielers",
                type=interactions.OptionType.STRING,
                required=True,
            ),
        ],
    )
    async def stats(self, ctx: interactions.CommandContext, *,username):
        username = username.lower()
        await ctx.defer()
        if(AuthHandler.instance().check(ctx)):
            await ctx.send(self._getStatsString(username))
        else:
            await ctx.send("Keine Rechte diesen Befehl zu nutzen")

    @interactions.extension_command(
        name="history",
        description="zeigt die history des spielers an",
        options = [
            interactions.Option(
                name="username",
                description="username des Spielers",
                type=interactions.OptionType.STRING,
                required=True,
            ),
        ],
    )
    async def history(self, ctx: interactions.CommandContext, *,username):
        username = username.lower()
        await ctx.defer()
        if(AuthHandler.instance().check(ctx)):
            await ctx.send(self._getHistoryString(username))
        else:
            await ctx.send("Keine Rechte diesen Befehl zu nutzen")
        

    @interactions.extension_command(
        name="chart",
        description="zeigt die statistiken des spielers an",
        options = [
            interactions.Option(
                name="username",
                description="username des Spielers",
                type=interactions.OptionType.STRING,
                required=True,
            ),
            interactions.Option(
                name="interval_length",
                description="Länge des gewünschten Zeitraumes in Wochen",
                type=interactions.OptionType.INTEGER,
                required=False,
            ),
            interactions.Option(
                name="interval_end",
                description="Enddatum des gewünschten Zeitraumes, Format 01/01/1970",
                type=interactions.OptionType.STRING,
                required=False,
            ),
            interactions.Option(
                name="size",
                description="size of chart, default m",
                type=interactions.OptionType.STRING,
                required=False,
                choices=[
                    interactions.Choice(name="s", value="s"), 
                    interactions.Choice(name="m", value="m"),
                    interactions.Choice(name="l", value="l"), 
                    interactions.Choice(name="xl", value="xl"),
                ],
            ),
        ],
    )
    async def chart(self, ctx: interactions.CommandContext, *,username, interval_length=8, interval_end= datetime.datetime.today(), size="m"):        
        if not self._db.check_player(username):
            return "Nutzer nicht gefunden"
        await ctx.defer()
        if(type(interval_end) == str):
            interval_end = datetime.datetime.strptime(interval_end, "%d/%m/%Y")
            interval_end = interval_end + datetime.timedelta(hours=23, minutes=59, seconds=59)
        elif(type(interval_end) == datetime.datetime):
            pass
        else:
            await ctx.send("Enddatum falsches Format")
            return
        start_date = interval_end - datetime.timedelta(weeks = interval_length)
        if(AuthHandler.instance().check(ctx)):
            data = self._db.get_player_chart_history(username, start_date, interval_end)
            chartData = self._playerData.build_chart_dict(data)
            url = self._getChartURL(chartData, size)
            returnMsg = "```%s```%s" % (username, url)
            await ctx.send(returnMsg)
        else:
            await ctx.send("Keine Rechte diesen Befehl zu nutzen")

    #@commands.command(usage="<galaxy>",
    #                  brief="Zeigt potentiell Inaktive Spieler an",
    #                  help="Zeigt alle Spieler in Galaxy <galaxy> and, die potentiell Inaktiv "+
    #                       "sind. (min. 3 tage kein Punktewachstum). Spieler im urlaubsmodus " +
    #                       "werden leider mit augelisted")
    async def inactive(self, ctx: interactions.CommandContext, galaxy: int):
        if galaxy <1 or galaxy>9:
            return ctx.send("Galaxy muss zwischen 1 und 9 sein")

        #await ctx.send(self._getInactiveString(galaxy))
        await ctx.defer()
        if(AuthHandler.instance().check(ctx)):
            await ctx.send("currently under construction")
        else:
            await ctx.send("Keine Rechte diesen Befehl zu nutzen")
        
    #@stats.error
    async def stats_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Spielername fehlt!\nBsp.: !stats Sc0t')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    #@history.error
    async def history_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Spielername fehlt!\nBsp.: !history Sc0t')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')
    
    #@chart.error
    async def chart_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Spielername fehlt!\nBsp.: !chart Sc0t')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')

    #@inactive.error
    async def inactive_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Galaxy fehlt!\nBsp.: !inactive 1')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Keine rechte diesen Befehl zu nutzen')
        else:
            logging.error(error)
            await ctx.send('ZOMFG ¯\_(ツ)_/¯')

    def setup(self):
        logging.info("Stats: Get Data references")

    def updateUserDataCallback(self):
        logging.info("Stats: Update UserData references")
    
    def updateHistoryDataCallback(self):
        logging.info("Stats: Update HistoryData references")

    def _getInactiveString(self, galaxy: int):
        inactivePlayers = self._getLoosingPointsPlayer(galaxy)
        sortedInactivePlayerPlanets = self._getFilteredAndSortedInactivePlayerPlanets(inactivePlayers, galaxy)

        resultStr = "```"
        for user,systems in sortedInactivePlayerPlanets:
            resultStr += "{:<20}".format(user)
            for system in systems:
                resultStr += "{:<4}".format(system)
            resultStr += "\n"
        return resultStr + "```"

    def _getFilteredAndSortedInactivePlayerPlanets(self, inactivePlayers: dict, galaxy):
        filteredPlayerPlanets: dict = {}

        #filter inactive players
        for user in inactivePlayers:
            if(inactivePlayers[user] >=3): #3 = threshold for amount of datapoints of loosing points
                filteredPlayerPlanets[user] = []
                for planet in self._userData[user]["planets"]:
                    planetGalaxy = int(planet.split(":")[0])
                    planetSystem = int(planet.split(":")[1])
                    if(galaxy == planetGalaxy and not planetSystem in filteredPlayerPlanets[user]):
                        filteredPlayerPlanets[user].append(planetSystem)

        #sort
        sortedPlayerPlanets = []
        for user in filteredPlayerPlanets:
            sortedPlayerPlanets.append((user,filteredPlayerPlanets[user]))
        sortedPlayerPlanets.sort(key=lambda x: x[1][0])
        return sortedPlayerPlanets

    def _getLoosingPointsPlayer(self, galaxy: int):
        inactiveData: dict = {}
        for user in self._historyData:
            historyData = self._historyData[user]
            last = historyData[0]
            for current in historyData[1:]:
                lastPoints = int(last["gesamt"].replace(".",""))
                currentPoints = int(current["gesamt"].replace(".",""))
                cUsername = current["username"]

                if lastPoints >= currentPoints:
                    if cUsername in self._userData:
                        for planet in self._userData[cUsername]["planets"]:
                            if int(planet.split(":")[0]) == galaxy:
                                if cUsername in inactiveData:
                                    inactiveData[cUsername] += 1
                                    break
                                else:
                                    inactiveData[cUsername] = 1
                                    break
                else:
                    inactiveData.pop(user,None)
                last = current
        return inactiveData

    def _getChartURL(self, chartData: dict, size: str):
        qc = QuickChart()

        if size == 's':
                qc.width = 500
                qc.height = 300
        elif size == 'm':
                qc.width = 720
                qc.height = 480
        elif size == 'l':
                qc.width = 1280
                qc.height = 720
        elif size == 'xl':
                qc.width = 1980
                qc.height = 1080
        else: #m
                qc.width = 720
                qc.height = 480
           
        qc.device_pixel_ratio = 2.0
        qc.config = {
            "type": "line",
            "data": {
                "labels": chartData["date"],
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

    def _getHistoryString(self, username):
        if not self._db.check_player(username):
            return "Nutzer nicht gefunden"
        
        #only use last 7 entrys
        data = self._db.get_player_history(username) #get for last 7 days
        chartData = self._playerData.build_history_dict(data)
        returnMsg = f"```Spieler {username}\n\n"
        returnMsg +="{0:11} {1:7} {2:10} {3:10} {4:10}\n".format("Datum", "P.", "Gesamt", "Flotte", "Gebäude")
        for entry in chartData:
            returnMsg += "{0:11} {1:3} {2:10} {3:10} {4:10}\n".format(entry["date"], str(entry["platz"]),
                                                                     entry["gesamt"] ,entry["flotte"], entry["gebäude"])
        returnMsg += "{0:9} {1:5} {2:10} {3:10} {4:10}\n".format("Diff.", 
                                                                 (chartData[len(chartData)-1]["platz"])-(chartData[len(chartData)-2]["platz"]),
                                                                 (chartData[len(chartData)-1]["gesamt"])-(chartData[len(chartData)-2]["gesamt"]),
                                                                 (chartData[len(chartData)-1]["flotte"])-(chartData[len(chartData)-2]["flotte"]),
                                                                 (chartData[len(chartData)-1]["gebäude"])-(chartData[len(chartData)-2]["gebäude"]))
        return returnMsg + "```"

    def _getStatsString(self, username):
        
        if not self._db.check_player:
            return "Nutzer nicht gefunden"
        
        userData = self._db.get_player_stats(username)
        #"username", "platz", "allianz", "gesamt", "flotte", "defensive", "gebäude", "forschung"
        returnMsg = "```"
        #name
        returnMsg += "{0:30}{1}\n".format(self._fields[0].capitalize(),username)
        #platz
        returnMsg += "{0:30}{1:10} ({2})\n".format(self._fields[1].capitalize(),str(userData[1][0]), str(userData[1][0]-userData[0][0]))
        #Allianz
        returnMsg += "{0:30}{1}\n".format(self._fields[2].capitalize(),userData[1][1])
        #gesamt
        returnMsg += "{0:30}{1:10} ({2})\n".format(self._fields[3].capitalize(),str(userData[1][2]), str(userData[1][2]-userData[0][2]))
        #flotte
        returnMsg += "{0:30}{1:10} ({2})\n".format(self._fields[4].capitalize(),str(userData[1][3]), str(userData[1][3]-userData[0][3]))
        #defensive
        returnMsg += "{0:30}{1:10} ({2})\n".format(self._fields[5].capitalize(),str(userData[1][4]), str(userData[1][4]-userData[0][4]))
        #gebäude
        returnMsg += "{0:30}{1:10} ({2})\n".format(self._fields[6].capitalize(),str(userData[1][5]), str(userData[1][5]-userData[0][5]))
        #forschung
        returnMsg += "{0:30}{1:10} ({2})\n".format(self._fields[7].capitalize(),str(userData[1][6]), str(userData[1][6]-userData[0][6]))
        
        #addPlanetData
        userplanets = self._db.get_playerplanets(username)
        usermoons = self._db.get_playermoons(username)
        returnMsg += "\n{0:30}\n".format("Bekannte Planeten")
        returnMsg += "{0:7} Mond?\n".format("Pos.")
        for planetPos in userplanets:
            if planetPos in usermoons:
                returnMsg += "{:7}  \u2713\n".format(planetPos)
            else:
                returnMsg += "{:7}\n".format(planetPos)
        
        return returnMsg + "```"

    def clearFetchedData(self, data: list):
        result = []
        for row in data:
            result.append(row[0])
        result.reverse()
        return result

    def formatDate(self, data: list):
        result = []
        for row in data:
            entry = row[0].strftime("%d.%m.%Y")
            result.append(str(entry))
        result.reverse()
        return result

    def get_general_points(self, player_name: str):
        playerId = self._db.get_player_id_by_name(player_name)
        self._db.setup()
        cursor = self._db.mydb.cursor(buffered=True)
        generalQuery = "SELECT generalScore FROM data.data WHERE playerId = " + str(playerId) + " order by date DESC LIMIT 30;"
        cursor.execute(generalQuery)
        value = cursor.fetchall()
        cursor.close()
        self._db.mydb.commit()
        self._db.teardown()
        return Stats.clearFetchedData(self, value)


    def get_fleet_points(self, player_name: str):
        playerId = self._db.get_player_id_by_name(player_name)
        self._db.setup()
        cursor = self._db.mydb.cursor()
        fleetQuery = "SELECT fleetScore FROM data.data WHERE playerId = " + str(playerId) + " order by date DESC LIMIT 30;"
        cursor.execute(fleetQuery)
        value = cursor.fetchall()
        cursor.close()
        self._db.mydb.commit()
        self._db.teardown()
        return Stats.clearFetchedData(self, value)

    def get_research_points(self, player_name: str):
        playerId = self._db.get_player_id_by_name(player_name)
        self._db.setup()
        cursor = self._db.mydb.cursor()
        researchQuery = "SELECT researchScore FROM data.data WHERE playerId = " + str(playerId) + " order by date DESC LIMIT 30;"
        cursor.execute(researchQuery)
        value = cursor.fetchall()
        cursor.close()
        self._db.mydb.commit()
        self._db.teardown()
        return Stats.clearFetchedData(self, value)

    def get_building_points(self, player_name: str):
        playerId = self._db.get_player_id_by_name(player_name)
        self._db.setup()
        cursor = self._db.mydb.cursor()
        buildingQuery = "SELECT buildingScore FROM data.data WHERE playerId = " + str(playerId) + " order by date DESC LIMIT 30;"
        cursor.execute(buildingQuery)
        value = cursor.fetchall()
        cursor.close()
        self._db.mydb.commit()
        self._db.teardown()
        return Stats.clearFetchedData(self, value)

    def get_defense_points(self, player_name: str):
        playerId = self._db.get_player_id_by_name(player_name)
        self._db.setup()
        cursor = self._db.mydb.cursor()
        defensiveQuery = "SELECT defensiveScore FROM data.data WHERE playerId = " + str(playerId) + " order by date DESC LIMIT 30;"
        cursor.execute(defensiveQuery)
        value = cursor.fetchall()
        cursor.close()
        self._db.mydb.commit()
        self._db.teardown()
        return Stats.clearFetchedData(self, value)

    def get_date(self, player_name: str):
        playerId = self._db.get_player_id_by_name(player_name)
        self._db.setup()
        cursor = self._db.mydb.cursor()
        dateQuery = "SELECT data.date FROM data.data WHERE playerId = " + str(playerId) + " order by date DESC LIMIT 30;"
        cursor.execute(dateQuery)
        value = cursor.fetchall()
        cursor.close()
        self._db.mydb.commit()
        self._db.teardown()

        return Stats.formatDate(self, value)

    def build_compare_datasets(self, data: dict):
        datasets = []
        colors = list()
        colors.append({"border": 'rgb(255, 99, 132)', "background": 'rgba(255, 99, 132, .5)'})
        colors.append({"border": 'rgb(54, 162, 235)', "background": 'rgba(54, 162, 235, .5)'})
        colors.append({"border": 'rgb(75, 192, 192)', "background": 'rgba(75, 192, 192, .5)'})
        colors.append({"border": 'rgb(255, 205, 86)', "background": 'rgba(255, 205, 86, .5)'})
        colors.append({"border": 'rgb(76, 0, 153)', "background": 'rgba(76, 0, 153, .5)'})
        counter = 0
        for key, value in data.items():
            player_dataset = {}
            data_player = value
            if not key == "date":
                player_dataset["yAxisId"] = "points"
                player_dataset["label"] = str(key)
                player_dataset["steppedLine"] = True
                player_dataset["fill"] = False
                for key2, value2 in data_player.items():
                    player_dataset["data"] = value2
                player_dataset["borderColor"] = colors[counter]["border"]
                player_dataset["backgroundColor"] = colors[counter]["background"]
                datasets.append(player_dataset)
                counter +=1
        return datasets

    def build_compare_chart(self, size, data: dict):
        qc = QuickChart()

        if size == 's':
            qc.width = 500
            qc.height = 300
        elif size == 'm':
            qc.width = 720
            qc.height = 480
        elif size == 'l':
            qc.width = 1280
            qc.height = 720
        elif size == 'xl':
            qc.width = 1980
            qc.height = 1080
        else:  # m
            qc.width = 720
            qc.height = 480

        qc.device_pixel_ratio = 2.0
        qc.config = {
            "type": "line",
            "data": {
                "labels": data["date"],
                "datasets": Stats.build_compare_datasets(self, data)
            },
            "options": {
                "scales": {
                    "xAxes": [{
                        "stacked": True
                    }],
                    "yAxes": [{
                        "id": "points",
                        "display": True,
                        "position": "right",
                        "stacked": False,
                    }]
                }, "elements": {
                    "point": {
                        "pointStyle": "star"
                    },
                },
            }
        }
        return qc.get_short_url()


    @interactions.extension_command(
        name="compare_chart",
        description="Vergleicht die Punkte der angegebenen Spieler miteinander",
        options = stats_options.compare_options
    )
    async def compare_chart(self, ctx: interactions.CommandContext, *, comparator: int, size:str = 'm', player_1: str, player_2: str, player_3="", player_4="", player_5=""):        
        await ctx.defer()
        if(AuthHandler.instance().check(ctx)):
            player_list = []
            if self._db.check_player(player_1):
                player_list.append(player_1)
            if self._db.check_player(player_2):
                player_list.append(player_2)
            if self._db.check_player(player_3):
                player_list.append(player_3)
            if self._db.check_player(player_4):
                player_list.append(player_4)
            if self._db.check_player(player_5):
                player_list.append(player_5)

            data_dict = dict()
            for player in player_list:
                player_dict = dict()
                if comparator == 1:
                    player_dict["general"] = Stats.get_general_points(self, player)
                elif comparator == 2:
                    player_dict["fleet"] = Stats.get_fleet_points(self, player)
                elif comparator == 3:
                    player_dict["research"] = Stats.get_research_points(self, player)
                elif comparator == 4:
                    player_dict["buildings"] = Stats.get_building_points(self, player)
                elif comparator == 5:
                    player_dict["defense"] = Stats.get_defense_points(self, player)
                else:
                    player_dict["general"] = Stats.get_general_points(self, player)
                data_dict["date"] = Stats.get_date(self, player)
                data_dict[player] = player_dict
            await ctx.send(Stats.build_compare_chart(self, size, data_dict))
        else:
            await ctx.send("Keine Rechte diesen Befehl zu nutzen")


def setup(bot: interactions.Client):
    Stats(bot)
