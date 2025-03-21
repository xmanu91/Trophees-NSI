from nt import strerror
from utility.SQLProvider import SQLProvider
from utility.ErrorHandler import raiseAnError
from mysql.connector import Error as sqlError
from utility import consolLog

class RoomManager:
    def __init__(self, SQLProvider: SQLProvider, username: str) -> None:
        self.SQLProvider = SQLProvider
        self.username = username
        self.userId= None
        self.currentRoomID = -1
        self.currentRound = 0
    
    def getAllRooms(self, state: str | None = None) -> list[tuple]:
        if state:
            response = self.SQLProvider.get("SELECT * FROM rooms WHERE state=%s", (state,))
        else:
            response = self.SQLProvider.get("SELECT * FROM rooms")
            
        if response is None:
            return []
        rooms = [row for row in response]
        return rooms

    def getAllRoomsIds(self) -> list[int]:
        response = self.SQLProvider.get("SELECT room_id FROM rooms")
        if response is None:
            return []
        rooms = [row for row in response]
        return rooms

    def getNumberOfConnectedUsersInRoom(self, roomId: int) -> int:
        response = self.SQLProvider.get("SELECT count(username) FROM connected_users WHERE room_id=%s", (str(roomId),))
        if response:
            return response[0][0]
        else: return -1
    
    def getCurrentRoomName(self) -> str:
        try:
            response = self.SQLProvider.get("SELECT room_name FROM rooms WHERE room_id=%s", (str(self.currentRoomID),))
            if response is None:
                return "Unknown room"
            return response[0][0]
        except sqlError as err:
            raiseAnError(err)
            return ""
    
    def createConnection(self, roomId: int) -> None:
        consolLog.info("RoomId :", roomId)
        try:
            response = self.SQLProvider.insert("INSERT INTO connected_users (username, room_id) VALUES (%s, %s)", (self.username, roomId), returnedValue='user_id')
            if response:
                self.userId = response
                consolLog.info('UserId :', self.userId)
                self.currentRoomID = -1
        except sqlError as err:
            consolLog.error(err)

    def createRoom(self, roomName: str) -> None:
        try:
            room = self.SQLProvider.insert("INSERT INTO rooms (room_id, creator, room_name, theme, state, rounds_number, round_time) VALUES (DEFAULT,%s, %s, %s, 'lobby', 4, 60)", (self.username, roomName, 'DEFAULT'), returnedValue="room_id")
            if room:
                self.createConnection(room)
        except sqlError as err:
            consolLog.error(err)
        
    def closeRoom(self, roomId: int) -> None:
        try:
            self.SQLProvider.executeSQL("DELETE FROM drawings WHERE room_id=%s", (str(roomId),))
            self.SQLProvider.executeSQL("DELETE FROM connected_users WHERE room_id=%s", (str(roomId),))
            self.SQLProvider.executeSQL("DELETE FROM votes WHERE room_id=%s", (str(roomId),))
            self.SQLProvider.executeSQL("DELETE FROM rooms WHERE room_id=%s", (str(roomId),))
        except sqlError as err:
            consolLog.error(err)
        self.currentRoomID = -1

    def closeConnection(self) -> None:
        try:
            consolLog.info("Fermeture de la connexion de : ", self.username)
            self.SQLProvider.executeSQL("DELETE FROM connected_users WHERE user_id=%s", (str(self.userId),))
        except sqlError as err:
            consolLog.error(err)
        self.currentRoomID = -1

    def setRoomState(self, state: str) -> None:
        try:
            self.SQLProvider.executeSQL("UPDATE rooms SET state=%s WHERE room_id=%s", (state, str(self.currentRoomID)))
        except sqlError as err:
            consolLog.error(err) 
    
    def setRoundsNumber(self, number: int) -> None:
        try:
            self.SQLProvider.executeSQL("UPDATE rooms SET rounds_number=%s WHERE room_id=%s", (number, self.currentRoomID))
        except sqlError as err:
            consolLog.error(err) 

    def setRoundTime(self, time: int) -> None:
        try:
            self.SQLProvider.executeSQL("UPDATE rooms SET round_time=%s WHERE room_id=%s", (time, self.currentRoomID))
        except sqlError as err:
            consolLog.error(err) 
    
    def getUsersInCurrentRoom(self) -> list[str]:
        try:
            response = self.SQLProvider.get("SELECT username FROM connected_users WHERE room_id=%s", (str(self.currentRoomID),))
            if response is None:
                return []
            users = [user[0] for user in response]  # type: ignore
            return users
        except sqlError as err:
            raiseAnError(err)
            consolLog.error(err)
            return []

    def getRoundsNumber(self) -> int:
        try:
            response = self.SQLProvider.get('SELECT rounds_number FROM rooms WHERE room_id=%s', (str(self.currentRoomID),))
            if response:
                return response[0][0]
            else: return -1
        except sqlError as err:
            consolLog.error(err)
            raiseAnError(err)
            return -1

    def getRoundTime(self) -> int:
        try:
            response = self.SQLProvider.get('SELECT round_time FROM rooms WHERE room_id=%s', (str(self.currentRoomID),))
            if response:
                return response[0][0]
            else: 
                raiseAnError("Récupéation du timer impossible")
                consolLog.error("Récupéation du timer impossible")
                return 60
        except sqlError as err:
            raiseAnError(err)
            consolLog.error(err)
            return 60

    def getRoomState(self) -> str:
        try:
            response = self.SQLProvider.get('SELECT state FROM rooms WHERE room_id=%s', (str(self.currentRoomID),))
            if response:
                return response[0][0]
            else: return "None"
        except sqlError as err:
            consolLog.error(err)
            raiseAnError(err)
            return "None"

    def getRoomCreator(self) -> str:
        try:
            response = self.SQLProvider.get('SELECT creator FROM rooms WHERE room_id=%s', (str(self.currentRoomID),))
            if response:
                return response[0][0]
            else: return "None"
        except sqlError as err:
            consolLog.error(err)
            raiseAnError(err)
            return "None"

    def setUsername(self, newUsername: str) -> None:
        self.username = newUsername

    def doesRoomExist(self, roomId: str) -> bool:
        if not roomId.isdigit():
            return False
        try:
            response = self.SQLProvider.get('SELECT room_name FROM rooms WHERE room_id=%s', (str(roomId),))
            consolLog.info(response)
            if response:
                return len(response) > 0
            else: return False
        except sqlError as err:
            consolLog.error(err)
            return False

    def doesUserConnectedInRoom(self, roomId: int, username: str) -> bool:
        try:
            response = self.SQLProvider.get('SELECT username FROM connected_users WHERE room_id=%s and username=%s', (str(roomId), username))
            if response:
                return len(response) > 0
            else: return False
        except sqlError as err:
            consolLog.error(err)
            raiseAnError(err)
            return False
        
