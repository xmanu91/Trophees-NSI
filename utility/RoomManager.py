from utility.SQLProvider import SQLProvider
from mysql.connector import Error as sqlError
from utility import consolLog

class RoomManager:
    def __init__(self, SQLProvider: SQLProvider, username: str):
        self.SQLProvider = SQLProvider
        self.username = username
        self.userId= None
        self.currentRoomID = None
        self.currentRound = 0
    
    def getAllRooms(self):
        response = self.SQLProvider.get("SELECT * FROM rooms")
        if response is None:
            return []
        rooms = [row for row in response]
        return rooms

    def getAllRoomsIds(self):
        response = self.SQLProvider.get("SELECT room_id FROM rooms")
        if response is None:
            return []
        rooms = [row for row in response]
        return rooms

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
            consolLog.error(err)
    
    def createConnection(self, roomId: int):
        consolLog.info("RoomId :", roomId)
        try:
            response = self.SQLProvider.insert("INSERT INTO connected_users (username, room_id) VALUES (%s, %s)", (self.username, roomId), returnedValue='user_id')
        except sqlError as err:
            consolLog.error(err)
        self.userId = response
        consolLog.info('UserId :', self.userId)
        self.currentRoomID = roomId

    def createRoom(self, roomName):
        try:
            room = self.SQLProvider.insert("INSERT INTO rooms (room_id, creator, room_name, theme, state, rounds_number, round_time) VALUES (DEFAULT,%s, %s, %s, 'loby', 4, 60)", (self.username, roomName, 'DEFAULT'), returnedValue="room_id")
        except sqlError as err:
            consolLog.error(err)
        self.createConnection(room)

    def closeRoom(self, roomId):
        try:
            self.SQLProvider.executeSQL("DELETE FROM drawings WHERE room_id=%s", (str(roomId),))
            self.SQLProvider.executeSQL("DELETE FROM connected_users WHERE room_id=%s", (str(roomId),))
            self.SQLProvider.executeSQL("DELETE FROM votes WHERE room_id=%s", (str(roomId),))
            self.SQLProvider.executeSQL("DELETE FROM rooms WHERE room_id=%s", (str(roomId),))
        except sqlError as err:
            consolLog.error(err)
        self.currentRoomID = None

    def closeConnection(self):
        try:
            consolLog.info("Fermeture de la connexion de : ", self.username)
            self.SQLProvider.executeSQL("DELETE FROM connected_users WHERE user_id=%s", (str(self.userId),))
        except sqlError as err:
            consolLog.error(err)
        self.currentRoomID = None

    def setRoomState(self, state: str):
        try:
            self.SQLProvider.executeSQL("UPDATE rooms SET state=%s WHERE room_id=%s", (state, str(self.currentRoomID)))
        except sqlError as err:
            consolLog.error(err) 
    
    def setRoundsNumber(self, number: int):
        try:
            self.SQLProvider.executeSQL("UPDATE rooms SET rounds_number=%s WHERE room_id=%s", (number, self.currentRoomID))
        except sqlError as err:
            consolLog.error(err) 

    def setRoundTime(self, time: int):
        try:
            self.SQLProvider.executeSQL("UPDATE rooms SET round_time=%s WHERE room_id=%s", (time, self.currentRoomID))
        except sqlError as err:
            consolLog.error(err) 
    
    def getUsersInCurrentRoom(self) -> list[str] | None:
        try:
            response = self.SQLProvider.get("SELECT username FROM connected_users WHERE room_id=%s", (str(self.currentRoomID),))
            if response is None:
                return []
            users = [user[0] for user in response]  # type: ignore
            return users
        except sqlError as err:
            consolLog.error(err)

    def getRoundsNumber(self):
        try:
            response = self.SQLProvider.get('SELECT rounds_number FROM rooms WHERE room_id=%s', (str(self.currentRoomID),))
            return response[0][0]
        except sqlError as err:
            consolLog.error(err)

    def getRoundTime(self):
        try:
            response = self.SQLProvider.get('SELECT round_time FROM rooms WHERE room_id=%s', (str(self.currentRoomID),))
            return response[0][0]
        except sqlError as err:
            consolLog.error(err)

    def getRoomState(self):
        try:
            response = self.SQLProvider.get('SELECT state FROM rooms WHERE room_id=%s', (str(self.currentRoomID),))
            return response[0][0]
        except sqlError as err:
            consolLog.error(err)

    def getRoomCreator(self):
        try:
            response = self.SQLProvider.get('SELECT creator FROM rooms WHERE room_id=%s', (str(self.currentRoomID),))
            return response[0][0]
        except sqlError as err:
            consolLog.error(err)

    def setUsername(self, newUsername: str):
        self.username = newUsername

    def doesRoomExist(self, roomId: id) -> bool:
        if not roomId.isdigit():
            return False
        try:
            response = self.SQLProvider.get('SELECT room_name FROM rooms WHERE room_id=%s', (str(roomId),))
            consolLog.info(response)
            return len(response) > 0
        except sqlError as err:
            consolLog.error(err)

    def doesUserConnectedInRoom(self, roomId: id, username: str) -> bool:
        try:
            response = self.SQLProvider.get('SELECT username FROM connected_users WHERE room_id=%s and username=%s', (str(roomId), username))
            return len(response) > 0
        except sqlError as err:
            consolLog.error(err)
        
