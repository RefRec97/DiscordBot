from quickchart import QuickChart

from bot_utils.db import DataBase
import options.moon_options as moon_options
import interactions


class Moon(interactions.Extension):
    def __init__(self, bot: interactions.Client):
        self.bot: interactions.Client = bot
        self.db = DataBase()

    def get_alliance_by_player(self, playerId: int):

        self.db.setup()
        cursor = self.db.mydb.cursor()

        allianceQuery = "SELECT allianceId FROM data.players WHERE playerId = " + str(playerId) + ";"
        cursor.execute(allianceQuery)
        value = cursor.fetchall()[0][0]
        cursor.close()
        self.db.mydb.commit()
        self.db.teardown()
        return value

    def get_moons(self, galaxy: int):

        self.db.setup()
        cursor = self.db.mydb.cursor()

        phalanxLevelQuery = "SELECT phalanxlvl, solarsystem, position, playerId FROM data.moons WHERE galaxy = " + str(
            galaxy) + ";"
        cursor.execute(phalanxLevelQuery)
        value = cursor.fetchall()
        cursor.close()
        self.db.mydb.commit()
        self.db.teardown()
        return value


    def get_coalitions(self, alliance: str):
        self.db.setup()
        cursor = self.db.mydb.cursor()

        coalitionQuery = "SELECT allianceId, partnerAllianceId FROM data.coalitions WHERE allianceId = " + alliance + ";"
        cursor.execute(coalitionQuery)
        coalitions = cursor.fetchall()
        cursor.close()
        self.db.mydb.commit()
        self.db.teardown()
        return coalitions


    def calculate_phalanx_range(self, phalanx: int):
        if phalanx < 1:
            return 0
        return (phalanx * phalanx) - 1


    def calculate_start_system(self, system: int, range: int):
        start = system
        if range > 1:
            range = Moon.calculate_phalanx_range(self, range)
            start = system - range

        if start < 1:
            start = 1
        return start


    def calculate_end_system(self, system: int, range: int):
        end = system
        if range > 1:
            range = Moon.calculate_phalanx_range(self, range)
            end = system + range

        if end > 400:
            end = 400
        return end


    def calculate_phalanx_systems(self, system: int, phalanx: int):
        data = set()
        start_system = Moon.calculate_start_system(self, system, phalanx)
        end_system = Moon.calculate_end_system(self, system, phalanx)

        if start_system < end_system:
            for i in range(start_system, end_system + 1):
                data.add(i)

        return data


    def get_chart_url(self, chartData: dict, size: str):
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
                "labels": chartData["systems"],
                "datasets": [{
                    "yAxisID": "phalanx",
                    "label": "Moon",
                    "steppedLine": False,
                    "backgroundColor": "rgb(0,0,205)",
                    "borderColor": "rgb(0,0,205)",
                    "data": chartData["moons"],
                    "fill": False,
                    "showLine": False,
                    "pointRadius": 15,
                }, {
                    "yAxisID": "phalanx",
                    "label": "Enemy",
                    "borderColor": 'rgba(205,0,0,1)',
                    "backgroundColor": 'rgba(205,0,0,0.1)',
                    "steppedLine": True,
                    "data": chartData["enemies"],
                    "fill": True,
                }, {
                    "yAxisID": "phalanx",
                    "label": "Friend",
                    "borderColor": 'rgba(0,139,0,1)',
                    "backgroundColor": 'rgba(0,139,0,0.1)',
                    "steppedLine": True,
                    "data": chartData["friends"],
                    "fill": True,
                }]
            },
            "options": {
                "scales": {
                    "xAxes": [{
                        "stacked": True
                    }],
                    "yAxes": [{
                        "id": "phalanx",
                        "display": True,
                        "position": "left",
                        "stacked": False,
                    }]
                }, "elements": {
                    "point": {
                        "pointStyle": "star"
                    },
                }
            }
        }
        return qc.get_short_url()

    def is_friend(self, allianceId: int):
        result = Moon.get_coalitions(self, str(allianceId))
        if len(result) > 0:
            return True
        return False

    def initializeDataDict(self):
        chartData = dict()
        systems = []
        moons = []
        enemies = []
        friends = []
        for i in range(1, 401):
            systems.append(i)
            moons.append(None)
            enemies.append(None)
            friends.append(None)
        chartData["systems"] = systems
        chartData["moons"] = moons
        chartData["enemies"] = enemies
        chartData["friends"] = friends
        return chartData

    @interactions.extension_command(name="phalanx_map",
                                    description="Zeigt die Phalanxgebiete in einem angegebenen Bereich an",
                                    options=moon_options.phalanx_map_options)
    async def phalanx_map(self, ctx: interactions.CommandContext, *, galaxy: int, start_system: int, end_system: int):
        await ctx.defer()
        if end_system - start_system > 200:
            await ctx.defer()
            await ctx.send("Maximal 200 Systeme als Bereich")

        result = Moon.get_moons(self, galaxy)
        entries = {}
        for moon in result:
            moon_entry = {"phalanx": int(moon[0]), "system": int(moon[1]), "position": moon[2], "playerId": moon[3],
                          "allianceId": Moon.get_alliance_by_player(self, moon[3]),
                          "is_friend": Moon.is_friend(self, Moon.get_alliance_by_player(self, moon[3]))}
            entries[len(entries) + 1] = moon_entry

        chartData = Moon.initializeDataDict(self)
        friends = chartData["friends"]
        enemies = chartData["enemies"]
        moons = chartData["moons"]
        for index in range(len(entries)):
            entry = entries[index + 1]
            data = Moon.calculate_phalanx_systems(self, entry["system"], entry["phalanx"])
            if entry["is_friend"]:
                moons[int(entry["system"]) - 1] = int(entry["phalanx"])
            else:
                moons[int(entry["system"]) - 1] = -1 * int(entry["phalanx"])
            for system in data:
                if entry["is_friend"]:
                    friends[system - 1] = 1
                else:
                    enemies[system - 1] = -1

        friends = [0 if v is None else v for v in friends]
        enemies = [0 if v is None else v for v in enemies]
        chartData["systems"] = chartData["systems"][start_system:end_system]
        chartData["friends"] = friends[start_system:end_system]
        chartData["enemies"] = enemies[start_system:end_system]
        chartData["moons"] = moons[start_system:end_system]

        await ctx.send(str(Moon.get_chart_url(self, chartData, 'xl')))


def setup(bot: interactions.Client):
    Moon(bot)
