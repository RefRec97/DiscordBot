from quickchart import QuickChart

from bot_utils.db import DataBase
import options.moon_options as moon_options
import interactions
from bot_utils.authHandler import AuthHandler
import datetime


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

    def get_moon(self, galaxy: int, solarsystem: int, position: int):

        self.db.setup()
        cursor = self.db.mydb.cursor()

        moonQuery = "SELECT * FROM data.moons WHERE galaxy = " + str(galaxy) + " and solarsystem = " + str(solarsystem) + " and position = " + str(position)+ ";"
        cursor.execute(moonQuery)
        value = cursor.fetchall()
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

    def get_player_name(self, player_id: int):
        self.db.setup()
        cursor = self.db.mydb.cursor()

        playerNameQuery = "SELECT name FROM data.players Where playerId =" + str(player_id) + ";"
        cursor.execute(playerNameQuery)
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


    def calculate_start_system(self, system: int, phalanx: int):
        start = system
        if phalanx > 1:
            range = Moon.calculate_phalanx_range(self, phalanx)
            start = system - range

        if start < 1:
            start = 1
        return start


    def calculate_end_system(self, system: int, phalanx: int):
        end = system
        if phalanx > 1:
            range = Moon.calculate_phalanx_range(self, phalanx)
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
                    "datalabels": {
                        "title": {
                            "font": {
                              "weight": 'bold'
                            }
                        },       
                        "value": {
                            "color": 'green'
                        },
                    }
                }, {
                    "yAxisID": "phalanx",
                    "label": "Enemy",
                    "borderColor": 'rgba(205,0,0,1)',
                    "backgroundColor": 'rgba(205,0,0,0.1)',
                    "steppedLine": True,
                    "data": chartData["enemies"],
                    "fill": True,
                    "datalabels": {
                        "labels": {
                            "title": None,
                            "value": None
                        }
                    }
                }, {
                    "yAxisID": "phalanx",
                    "label": "Friend",
                    "borderColor": 'rgba(0,139,0,1)',
                    "backgroundColor": 'rgba(0,139,0,0.1)',
                    "steppedLine": True,
                    "data": chartData["friends"],
                    "fill": True,
                    "datalabels": {
                        "labels": {
                            "title": None,
                            "value": None
                        }
                    }
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
                }, "plugins": {
                    "datalabels": {
                        "anchor": 'end',
                        "align": 'top',
                        "color": '#fff',
                        "backgroundColor": 'rgba(34, 139, 34, 0.6)',
                        "borderColor": 'rgba(34, 139, 34, 1.0)',
                        "borderWidth": 1,
                        "borderRadius": 5,
                        "display": 'auto',
                        "title": {
                            "font": {
                              "weight": 'bold'
                            }
                        }
                    },
                },
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


    def create_map(self, galaxy: int, start_system: int, end_system: int):
            result = Moon.get_moons(self, galaxy)
            entries = {}
            
            for moon in result:
                alliance_name = Moon.get_alliance_by_player(self, moon[3])
                moon_entry = {"phalanx": int(moon[0]), "system": int(moon[1]), "position": moon[2], "playerId": moon[3],
                            "allianceId": alliance_name ,
                            "is_friend": Moon.is_friend(self, alliance_name )}
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
            
            return str(Moon.get_chart_url(self, chartData, 'xl'))

    @interactions.extension_command(name="moon_phalanx_map",
                                    description="Zeigt die Phalanxgebiete in einem angegebenen Bereich an",
                                    options=moon_options.phalanx_map_options)
    async def moon_phalanx_map(self, ctx: interactions.CommandContext, *, galaxy: int, start_system: int, end_system: int):
        try:
            await ctx.defer()
            if(AuthHandler.instance().check(ctx)):
                if end_system - start_system > 200:
                    await ctx.defer()
                    await ctx.send("Maximal 200 Systeme als Bereich")
                    return
                await ctx.send(Moon.create_map(self, galaxy, start_system, end_system))
            else:
                await ctx.send("Keine Rechte diesen Befehl zu nutzen")
            return
        except Exception as e:
            template = "Fehler aufgetreten, bitte Reflexrecon melden: {0} . Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            await ctx.send(message)
            return
        
    def create_moon_data(self, galaxy:int, solarsystem: int, position: int):
        db_result = Moon.get_moon(self, galaxy, solarsystem, position)
        result = ""
        if len(db_result) == 1:
            result_list = db_result[0]
            player_name = Moon.get_player_name(self, int(result_list[3]))
            if len(player_name) == 1:
                try:
                    player_name = player_name[0][0]
                except:
                    player_name = str(result_list[3]) + " (Keinen Namen gefunden)"
            result = result + "Galaxie: " + str(result_list[0]) + "\t"
            result = result + "System: " + str(result_list[1]) + "\t"
            result = result + "Position: " + str(result_list[2]) + "\n\n"
            result = result + "Spieler:\t\t" + str(player_name) + "\n\n"
            result = result + "Phlx.-Level:\t" + str(result_list[4]) + "\n"
            result = result + "Basis-Level:\t" + str(result_list[5]) + "\n"
            result = result + "Robo.-Level:\t" + str(result_list[6]) + "\n"
            result = result + "JmpG.-Level:\t" + str(result_list[7]) + "\n"
        else:
            result = "Keine Daten gefunden!"
        return "```python\n" + result + "```"

    @interactions.extension_command(name="moon_data",
                                    description="Zeigt die Ausbaustufen eines Mondes an. Aufrufbar ueber seine Position",
                                    options=moon_options.moon_data_options)
    async def moon_data(self, ctx: interactions.CommandContext, *, galaxy: int, solarsystem: int, position: int):
        try:
            await ctx.defer()
            if(AuthHandler.instance().check(ctx)):
                result = Moon.create_moon_data(self, galaxy, solarsystem, position)
                await ctx.send(str(result))
            else:
                await ctx.send("Keine Rechte diesen Befehl zu nutzen")
            return
        except Exception as e:
            template = "Fehler aufgetreten, bitte Reflexrecon melden: {0} . Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            await ctx.send(message)
            return
    
    def read_phalanxed_moon_data(self, galaxy):
        moons_enemies = []
        moons_friends = []
        result = Moon.get_moons(self, galaxy)
        for moon in result:
            moon_entry = {"phalanx": int(moon[0]), "system": int(moon[1]), "position": moon[2], "playerId": moon[3],
                        "allianceId": Moon.get_alliance_by_player(self, moon[3])}

            if Moon.is_friend(self, Moon.get_alliance_by_player(self, moon[3])):
                moons_friends.append(moon_entry)
            else:
                moons_enemies.append(moon_entry)
       
        entries = {"friends": moons_friends, "enemies": moons_enemies}
        return entries

    def is_phalanxed_moon(self, entry: dict(), solarsystem:int):
        phalanx = int(entry["phalanx"])
        system = int(entry["system"])

        if phalanx == 1:
            return solarsystem == system

        if phalanx > 1:
            min_system = Moon.calculate_start_system(self, system, phalanx)
            max_system = Moon.calculate_end_system(self, system, phalanx)
            return min_system <= solarsystem and solarsystem <= max_system
        return False

    def create_phalanxed_moon_table(self, galaxy, solarsystem):
        entries = Moon.read_phalanxed_moon_data(self, galaxy)
        enemies = dict()
        friends = dict()

        for friend in entries["friends"]:
            if Moon.is_phalanxed_moon(self, friend, solarsystem):
                key = (friend["system"], friend["position"])
                friends[key] = friend

        for enemy in entries["enemies"]:
            if Moon.is_phalanxed_moon(self, enemy, solarsystem):
                key = (enemy["system"], enemy["position"])
                enemies[key] = enemy
        
        result = []
        report = "Friends - Target (Galaxy= " + str(galaxy) + ", System= " + str(solarsystem) + ") \n\n"
        sorted_friend_keys = sorted(friends)
        for key in sorted_friend_keys:
            friend = friends[key]
            player_name = Moon.get_player_name(self, int(friend["playerId"]))
            if len(player_name) == 1:
                try:
                    player_name = player_name[0][0]
                except:
                    player_name = str(friend["playerId"]) + " (Keinen Namen gefunden)"
            report = report + "Sys: " + str(friend["system"]) + " Pos: " + str(friend["position"]) + " Phalanx: " + str(friend["phalanx"]) + " \t Spieler: " + str(player_name) + "\n"
        result.append(report)

        report = "Enemies - Target (Galaxy= " + str(galaxy) + ", System= " + str(solarsystem) + ") \n\n"
        sorted_enemy_keys = sorted(enemies)
        for key in sorted_enemy_keys:
            enemy = enemies[key]
            player_name = Moon.get_player_name(self, int(enemy["playerId"]))
            if len(player_name) == 1:
                try:
                    player_name = player_name[0][0]
                except:
                    player_name = str(enemy["playerId"]) + " (Keinen Namen gefunden)"
            report = report + "Sys: " + str(enemy["system"]) + " Pos: " + str(enemy["position"]) + " Phalanx: " + str(enemy["phalanx"]) + " \t Spieler: " + str(player_name) + "\n"
        result.append(report)
        return result

    @interactions.extension_command(name="moons_in_range",
                                    description="Zeigt alle Monde an die das Zielsystem phalanxen koennen.",
                                    options=moon_options.moons_in_range_options)
    async def moons_in_range(self, ctx: interactions.CommandContext, *, galaxy: int, solarsystem: int):
        try:
            await ctx.defer()
            if(AuthHandler.instance().check(ctx)):
                
                for result in Moon.create_phalanxed_moon_table(self, galaxy, solarsystem):
                    await ctx.send("```python\n" + str(result) + "```")
            else:
                await ctx.send("Keine Rechte diesen Befehl zu nutzen")
            return
        except Exception as e:
            template = "Fehler aufgetreten, bitte Reflexrecon melden: {0} . Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            await ctx.send(message)
            return

def setup(bot: interactions.Client):
    Moon(bot)
