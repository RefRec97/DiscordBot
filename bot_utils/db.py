import os
import mysql.connector
import datetime

from bot_utils import bot_password_token_file as config

class DataBase:
    def __init__(self):
        # Creating connection object
        self.mydb = None
    
    def setup(self):
        try:
            self.mydb = mysql.connector.connect(
                host=str(config.dbRemoteIP),
                user=str(config.dbUsername),
                password=str(config.dbPassword),
                database=str(config.dbSchema)
            )
        except:
            print("DB nicht gestartet")

    def teardown(self):
        self.mydb.close()

    def get_player_id_by_name(self, player_name):
        self.setup()
        cursor = self.mydb.cursor()

        playerNameQuery = "SELECT playerId FROM players Where name =\"" + str(player_name) + "\";"
        cursor.execute(playerNameQuery)
        value = cursor.fetchall()[0][0]
        cursor.close()
        self.mydb.commit()
        self.teardown()
        return value

    def get_player_chart_history(self,player_name, start_date, end_date):
        
        self.setup()
        select_cursor = self.mydb.cursor(buffered=True)

        #check player
        select_cursor.execute('Select data.generalRank, data.generalScore, data.buildingScore,'+
            ' data.researchScore, data.fleetScore, data.date, data.defensiveScore from data'+
            ' inner join players on data.playerId = players.playerId'+
            ' where players.name = %s and data.date > %s and data.date < %s order by date asc;',(player_name, start_date, end_date,))
        result = select_cursor.fetchall()
        select_cursor.close()
        self.teardown()
        return result
    
    def get_player_history(self, player_name):
        
        self.setup()
        select_cursor = self.mydb.cursor(buffered=True)

        #check player
        select_cursor.execute('Select data.generalRank, data.generalScore, data.buildingScore,'+
            ' data.fleetScore, data.date from data'+
            ' inner join players on data.playerId = players.playerId'+
            ' where players.name = %s order by date desc;',(player_name,))
        data = select_cursor.fetchall()
        row_count = select_cursor.rowcount
        result = []
        temp = []
        if row_count > 7:
            i = 7
        else:
            i = row_count
        
        for row in data:
            temp.append(row)
            i = i - 1
            if i < 1:
                break

        for row in reversed(temp):
            result.append(row)
        
        select_cursor.close()
        self.teardown()
        return result

    def get_player_stats(self,player_name):
        
        self.setup()
        select_cursor = self.mydb.cursor(buffered=True)
        today = str(datetime.date.today()) + "%"
        select_cursor.execute("Select * from data where date like %s;",(today,))
        row_count = select_cursor.rowcount
        if row_count > 0:
            today = str(datetime.date.today()) + "%"
            yesterday = str(datetime.date.today() - datetime.timedelta(days=1)) + "%"
        else:
            today = str(datetime.date.today()- datetime.timedelta(days=1)) + "%"
            yesterday = str(datetime.date.today() - datetime.timedelta(days=2)) + "%"
        
        #check player
        #"username", "platz", "allianz", "gesamt", "flotte", "defensive", "gebäude", "forschung"
        #generalRank, ,generalScore, fleetScore, defensiveScore, buildingScore, researchScore
        select_cursor.execute('Select data.generalRank, alliances.name, data.generalScore,'+
            ' data.fleetScore, data.defensiveScore, data.buildingScore, data.researchScore from data'+
            ' inner join players on data.playerId = players.playerId'+
            ' inner join alliances on players.allianceId = alliances.allianceId'+
            ' where players.name = %s and (date like %s or date like %s) order by date asc;',(player_name,today,yesterday))
        result = select_cursor.fetchall()
        select_cursor.close()
        self.teardown()
        return result


    def get_all_player_stats(self, delta: int):
        #get palyer stats for 2 dates to determine inactives
        self.setup()
        select_cursor = self.mydb.cursor(buffered=True)
        today = str(datetime.date.today()) + "%"
        select_cursor.execute("Select * from data where date like %s;",(today,))
        row_count = select_cursor.rowcount
        if row_count > 0:
            today = str(datetime.date.today()) + "%"
            yesterday = str(datetime.date.today() - datetime.timedelta(days=delta)) + "%"
        else:
            today = str(datetime.date.today()- datetime.timedelta(days=1)) + "%"
            yesterday = str(datetime.date.today() - datetime.timedelta(days=delta+1)) + "%"
        
        #check player
        #"username", "platz", "allianz", "gesamt", "flotte", "defensive", "gebäude", "forschung"
        #generalRank, ,generalScore, fleetScore, defensiveScore, buildingScore, researchScore
        select_cursor.execute('Select data.generalScore, data.playerId from data'+
            ' where date like %s or date like %s order by date asc;',(today,yesterday))
        result = select_cursor.fetchall()
        select_cursor.close()
        self.teardown()
        return result
    
    def add_auth(self, user, role):
        self.setup()
        cursor = self.mydb.cursor()
        cursor.execute('insert into auth values (%s,%s);',(user,role))
        self.mydb.commit()
        cursor.close()
        self.teardown()
    
    def update(self, user, role):
        self.setup()
        cursor = self.mydb.cursor()
        cursor.execute('update auth set role = %s where authUser = %s;',(role, user))
        self.mydb.commit()
        cursor.close()
        self.teardown()

    def delete_auth(self, user):
        self.setup()
        cursor = self.mydb.cursor()
        cursor.execute('delete from auth where authUser = %s;',(user,))
        self.mydb.commit()
        cursor.close()
        self.teardown()

    def check_auth(self, user):
        self.setup()
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute('select role from auth where authUser = %s order by role desc;',(user,))
        row_count = cursor.rowcount
        if row_count > 0:
            result = cursor.fetchone()[0]
        else:
            result = False
        cursor.close()
        self.teardown()
        return result

    def check_player(self, player):
        self.setup()
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute('select * from players where name = %s;',(player,))
        row_count = cursor.rowcount
        if row_count > 0:
            result = True
        else:
            result = False
        cursor.close()
        self.teardown()
        return result

    def check_planets(self, galaxy, system, position):
        self.setup()
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute('select * from planets where galaxy = %s and solarsystem = %s and position = %s;',(galaxy, system, position))
        row_count = cursor.rowcount
        if row_count > 0:
            result = True
        else:
            result = False
        cursor.close()
        self.teardown()
        return result
    def get_playerplanets_raw(self, player):
        self.setup()
        cursor = self.mydb.cursor()
        cursor.execute('select planets.galaxy, planets.solarsystem, planets.position from planets '+
            'inner join players on players.playerId = planets.playerId '+
            'where players.name = %s order by galaxy asc, solarsystem asc, position asc;', (player,))
        data = cursor.fetchall()
        result = []
        for row in data:
            dict = {"galaxy": row[0], "system": row[1], "position": row[2]}
            result.append(dict)
        
        cursor.close()
        self.teardown()
        return result

    def get_playerplanets(self, player):
        self.setup()
        cursor = self.mydb.cursor()
        cursor.execute('select planets.galaxy, planets.solarsystem, planets.position from planets '+
            'inner join players on players.playerId = planets.playerId '+
            'where players.name = %s order by galaxy asc, solarsystem asc, position asc;', (player,))
        data = cursor.fetchall()
        result = []
        for row in data:
            result.append(str(row[0])+":"+str(row[1])+":"+str(row[2]))
        
        cursor.close()
        self.teardown()
        return result

    def add_planet(self, galaxy, system, position, playerId):
        self.setup()
        cursor = self.mydb.cursor()
        cursor.execute('insert into planets (galaxy, solarsystem, position, playerId) values (%s, %s, %s, %s);',(galaxy, system, position, playerId))
        self.mydb.commit()
        cursor.close()
        self.teardown()
    
    def del_planet(self, galaxy, system, position):
        self.setup()
        cursor = self.mydb.cursor()
        cursor.execute('delete from planets where galaxy = %s and solarsystem = %s and position = %s;',(galaxy, system, position))
        self.mydb.commit()
        cursor.close()
        self.teardown()
    
    def get_id(self, player):
        self.setup()
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute('select playerId from players where name = %s;',(player,))
        result = cursor.fetchone()[0]
        cursor.close()
        self.teardown()
        return result

    def check_moon(self, galaxy, solarsystem, position):
        self.setup()
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute('select * from moons where galaxy = %s and solarsystem = %s and position = %s;',(galaxy, solarsystem, position))
        row_count = cursor.rowcount
        if row_count > 0:
            result = True
        else:
            result = False
        cursor.close()
        self.teardown()
        return result
    
    def get_playermoons(self, player):
        self.setup()
        cursor = self.mydb.cursor()
        cursor.execute('select moons.galaxy, moons.solarsystem, moons.position from moons '+
            'inner join players on players.playerId = moons.playerId '+
            'where players.name = %s order by galaxy asc, solarsystem asc, position desc;', (player,))
        data = cursor.fetchall()
        result = []
        for row in data:
            result.append(str(row[0])+":"+str(row[1])+":"+str(row[2]))
        
        cursor.close()
        self.teardown()
        return result

    def add_moon(self, galaxy, system, position, playerId, phalanx, base, robo, jumpgate):
        self.setup()
        cursor = self.mydb.cursor()
        cursor.execute('insert into moons '+
            '(galaxy, solarsystem, position, playerId, phalanxlvl, baselvl, robotlvl, jumpgate) '+
            'values (%s, %s, %s, %s, %s, %s, %s, %s);',
            (galaxy, system, position, playerId, phalanx, base, robo, jumpgate))
        self.mydb.commit()
        cursor.close()
        self.teardown()
    
    def update_moon(self, galaxy, system, position, phalanx, base, robo, jumpgate):
        self.setup()
        cursor = self.mydb.cursor()
        cursor.execute('update moons '+
            'set phalanxlvl = %s, baselvl = %s, robotlvl = %s, jumpgate = %s '+
            'where galaxy = %s and solarsystem = %s and position = %s;',
            (phalanx, base, robo, jumpgate, galaxy, system, position))
        self.mydb.commit()
        cursor.close()
        self.teardown()

    def del_moon(self, galaxy, system, position):
        self.setup()
        cursor = self.mydb.cursor()
        cursor.execute('delete from moons where galaxy = %s and solarsystem = %s and position = %s;',(galaxy, system, position))
        self.mydb.commit()
        cursor.close()
        self.teardown()

    def check_time(self, date):
        self.setup()
        date = str(date) + "%"
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute('select date from data where date like %s order by date desc;',(date,))
        timestamp = cursor.fetchone()[0]
        
        cursor.close()
        self.teardown()
        return timestamp

    def check_ally(self, allyname):
        self.setup()
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute('select * from alliances where name = %s;',(allyname,))
        row_count = cursor.rowcount
        if row_count > 0:
            result = True
        else:
            result = False
        cursor.close()
        self.teardown()
        return result

    def get_top_ally(self, allyname: str):
        self.setup()
        cursor = self.mydb.cursor(buffered=True)
        result: dict = {}
        today = datetime.date.today()
        date = str(today) + "%"
        cursor.execute('select data.generalRank, players.name, data.generalScore, data.fleetScore from data '+ 
            'inner join players on data.playerId = players.playerId '+
            'inner join alliances on players.allianceId = alliances.allianceId '+
            'where data.date like %s and alliances.name = %s order by data.generalRank asc;',(date, allyname))
        data = cursor.fetchall()
        for i in range(10):
            result['p'+str(i)] = {'generalRank': data[i][0], 'name': data[i][1], 'generalScore': data[i][2], 'fleetScore': data[i][3]}
        
        cursor.close()
        self.teardown()
        return result
    
    def get_allypos_gal(self, allyname: str, gal: str, orderByPlayer: bool):
        self.setup()
        cursor = self.mydb.cursor(buffered=True)
        result = []
        if orderByPlayer:
            cursor.execute('select planets.galaxy, planets.solarsystem, planets.position, players.name from planets '+ 
                'inner join players on players.playerId = planets.playerId '+
                'inner join alliances on players.allianceId = alliances.allianceId '+
                'where alliances.name = %s and planets.galaxy = %s order by players.name asc, planets.solarsystem asc, planets.position asc;',(allyname,gal))
        else:
            cursor.execute('select planets.galaxy, planets.solarsystem, planets.position, players.name from planets '+ 
                'inner join players on players.playerId = planets.playerId '+
                'inner join alliances on players.allianceId = alliances.allianceId '+
                'where alliances.name = %s and planets.galaxy = %s order by planets.solarsystem asc, planets.position asc;',(allyname,gal))
        data = cursor.fetchall()

        for plan in data:
            galaxy_text = str(plan[0])
            system_text = str(plan[1])
            while len(system_text) < 3:
                system_text = " " + system_text
            position_text = str(plan[2])
            while len(position_text) < 2:
                position_text = " " + position_text
            result.append(galaxy_text+":"+system_text+":"+position_text+" - "+str(plan[3]) + " \t\n")
        
        cursor.close()
        self.teardown()
        return result

    def add_updatechannel(self, channel):
        self.setup()
        cursor = self.mydb.cursor()
        cursor.execute('insert into updates values (%s);',(channel,))
        self.mydb.commit()
        cursor.close()
        self.teardown()

    def check_updatechannel(self, channel):
        self.setup()
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute('select * from updates where channelId = %s;',(channel,))
        row_count = cursor.rowcount
        if row_count > 0:
            result = True
        else:
            result = False
        cursor.close()
        self.teardown()
        return result

    def get_updatechannel(self):
        self.setup()
        result = []
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute('select * from updates;')
        data = cursor.fetchall()
        for channel in data:
            result.append(channel[0])
        cursor.close()
        self.teardown()
        return result