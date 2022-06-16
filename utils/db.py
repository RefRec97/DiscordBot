import mysql.connector
import utils.config as config
import datetime
class db:
    def __init__(self):
        # Creating connection object
        a = "a"
    
    def setup(self):
        self.mydb = mysql.connector.connect(
            host = config.dbRemoteIP,
            user = config.dbUsername,
            password = config.dbPassword,
            database = config.dbSchema
        )
    
    def teardown(self):
        self.mydb.close()

    def get_player_history(self,player_name):
        
        self.setup()
        select_cursor = self.mydb.cursor(buffered=True)

        #check player
        select_cursor.execute('Select data.*,players.name from data inner join players on data.playerId = players.playerId where players.name = %s;',player_name)
        result = select_cursor.fetchall()
        select_cursor.close()
        self.teardown()
        return result
        
    def add_auth(self, user, role):
        self.setup()
        cursor = self.mydb.cursor()
        #cursor.execute("insert into auth values (%s, %s);",user,role)
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
        result = cursor.fetchone()[0]
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
            'where players.name = %s order by galaxy asc, solarsystem asc, position asc;', (player,))
        data = cursor.fetchall()
        result = []
        for row in data:
            result.append(str(row[0])+":"+str(row[1])+":"+str(row[2]))
        
        cursor.close()
        self.teardown()
        return result

    def add_moon(self, galaxy, system, position, playerId, phalanx = 0, base = 0, robo = 0, jumpgate = 0):
        self.setup()
        cursor = self.mydb.cursor()
        cursor.execute('insert into moons '+
            '(galaxy, solarsystem, position, playerId, phalanxlvl, baselvl, robotlvl, jumpgate) '+
            'values (%s, %s, %s, %s, %s, %s, %s, %s);',
            (galaxy, system, position, playerId, phalanx, base, robo, jumpgate))
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
    
    def get_allypos_gal(self, allyname: str, gal):
        self.setup()
        cursor = self.mydb.cursor(buffered=True)
        result = []
        cursor.execute('select planets.galaxy, planets.solarsystem, planets.position from planets '+ 
            'inner join players on players.playerId = planets.playerId '+
            'inner join alliances on players.allianceId = alliances.allianceId '+
            'where alliances.name = %s and planets.galaxy = %s order by planets.solarsystem asc, planets.position asc;',(allyname,gal))
        data = cursor.fetchall()
        i = 0
        for plan in data:
            result.append(str(data[i][0])+":"+str(data[i][1])+":"+str(data[i][2]))
            i += 1
        
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