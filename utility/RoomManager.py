from utility.SQLProvider import SQLProvider
from mysql.connector import Error as sqlError

class RoomManager:
    def __init__(self, SQLProvider: SQLProvider, username: str):
        self.SQLProvider = SQLProvider
        self.username = username
        self.currentRoomID = None
    
    def getAllRooms(self):
        response = self.SQLProvider.get("SELECT * FROM rooms")
        if response is None:
            return []
        rooms = [row for row in response]
        return rooms

    def getAllConnectedUsers(self):
        response = self.SQLProvider.get("SELECT * FROM connected_users")
        if response is None:
            return []
        users = [row for row in response]
        return users

    def getConnectedUsersNumberInRoom(self, roomId: int):
        response = self.SQLProvider.get("SELECT count(username) FROM connected_users WHERE room_id=%s", (str(roomId),))
        return response[0][0]
    
    def getCurrentRoomName(self):
        try:
            response = self.SQLProvider.get("SELECT room_name FROM rooms WHERE room_id=%s", (str(self.currentRoomID),))
            if response is None:
                return None
            return response[0][0]
        except sqlError as err:
            print(err)
    
    def createConnection(self, roomId: int):
        print('createConnection', roomId)
        try:
            users = self.getAllConnectedUsers()
            for user in users:
                if self.username == user[1]:
                    raise Exception((201, "User already exists"))
            self.SQLProvider.insert("INSERT INTO connected_users (username, room_id) VALUES (%s, %s)", (self.username, roomId))
        except sqlError as err:
            print(err)
        self.currentRoomID = roomId

    def createRoom(self, roomName):
        try:
            room = self.SQLProvider.insert("INSERT INTO rooms (room_id, creator, room_name, theme, state, rounds_number, round_time) VALUES (DEFAULT,%s, %s, %s, 'loby', 4, 60)", (self.username, roomName, 'DEFAULT'), returnedValue="room_id")
        except sqlError as err:
            print(err)
        self.createConnection(room)

    def closeRoom(self, roomId):
        try:
            self.SQLProvider.executeSQL("DELETE FROM drawings WHERE room_id=%s", (str(roomId),))
            self.SQLProvider.executeSQL("DELETE FROM connected_users WHERE room_id=%s", (str(roomId),))
            self.SQLProvider.executeSQL("DELETE FROM votesS WHERE room_id=%s", (str(roomId),))
            self.SQLProvider.executeSQL("DELETE FROM rooms WHERE room_id=%s", (str(roomId),))
        except sqlError as err:
            print(err)
        self.currentRoomID = None

    def closeConnection(self):
        try:
            print(self.username)
            self.SQLProvider.executeSQL("DELETE FROM connected_users WHERE username=%s", (str(self.username),))
        except sqlError as err:
            print(err)
        self.currentRoomID = None

    def setRoomState(self, state: str):
        try:
            self.SQLProvider.executeSQL("UPDATE rooms SET state=%s WHERE room_id=%s", (state, str(self.currentRoomID)))
        except sqlError as err:
            print(err) 
    
    def setRoundsNumber(self, number: int):
        try:
            self.SQLProvider.executeSQL("UPDATE rooms SET rounds_number=%s WHERE room_id=%s", (number, self.currentRoomID))
        except sqlError as err:
            print(err) 

    def setRoundTime(self, time: int):
        try:
            self.SQLProvider.executeSQL("UPDATE rooms SET round_time=%s WHERE room_id=%s", (time, self.currentRoomID))
        except sqlError as err:
            print(err) 
    
    def getUsersInCurrentRoom(self) -> list[str] | None:
        try:
            response = self.SQLProvider.get("SELECT username FROM connected_users WHERE room_id=%s", (str(self.currentRoomID),))
            if response is None:
                return []
            users = [user[0] for user in response]  # type: ignore
            return users
        except sqlError as err:
            print(err)

    def getRoundNumber(self):
        try:
            response = self.SQLProvider.get('SELECT rounds_number FROM rooms WHERE room_id=%s', (str(self.currentRoomID),))
            return response[0][0]
        except sqlError as err:
            print(err)

    def getRoundTime(self):
        try:
            response = self.SQLProvider.get('SELECT round_time FROM rooms WHERE room_id=%s', (str(self.currentRoomID),))
            return response[0][0]
        except sqlError as err:
            print(err)

    def getRoomState(self):
        try:
            response = self.SQLProvider.get('SELECT state FROM rooms WHERE room_id=%s', (str(self.currentRoomID),))
            return response[0][0]
        except sqlError as err:
            print(err)

    def getRoomCreator(self):
        try:
            response = self.SQLProvider.get('SELECT creator FROM rooms WHERE room_id=%s', (str(self.currentRoomID),))
            return response[0][0]
        except sqlError as err:
            print(err)

    def setUsername(self, newUsername: str):
        self.username = newUsername

