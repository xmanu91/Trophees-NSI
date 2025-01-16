import SQLProvider as sql
from mysql.connector import Error as sqlError

class RoomManager:
    def __init__(self, SQLProvider: sql.SQLProvider, username: str):
        self.SQLProvider = SQLProvider
        self.username = username
        self.currentRoomID = None
    
    def getAllRooms(self):
        response = self.SQLProvider.get("SELECT * FROM rooms")
        if response == None:
            return []
        rooms = [row for row in response] 
        return rooms
    
    def getAllConnectedUsers(self):
        response = self.SQLProvider.get("SELECT * FROM connected_users")
        if response == None:
            return []
        users = [row for row in response] 
        return users
    
    def createConnection(self, roomId: int):
        try:
            users = self.getAllConnectedUsers()
            for user in users:
                if self.username == user[1]:
                    return Exception((201, "User already exists"))
            self.SQLProvider.insert("INSERT INTO connected_users (username, room_id) VALUES ('{}', '{}')".format(self.username, roomId))
        except sqlError as err:
            print(err)
        self.currentRoomID = roomId

    def createRoom(self, roomName):
        try:
            room = self.SQLProvider.insert("INSERT INTO rooms (room_id, room_name, theme) VALUES (DEFAULT, '{}', DEFAULT)".format(roomName), returnedValue="room_id")
        except sqlError as err:
            print(err)
        self.currentRoomID = room

    def closeRoom(self, roomId):
        try:
            self.SQLProvider.executeSQL("DELETE FROM rooms WHERE room_id='{}'".format(roomId))
        except sqlError as err:
            print(err)
        self.currentRoomID = None

    def closeConnection(self):
        try:
            self.SQLProvider.executeSQL("DELETE FROM connected_users WHERE username='{}'".format(self.username))
        except sqlError as err:
            print(err)
        self.currentRoomID = None
    
    def getUsersInCurrentRoom(self) -> list[str] | None:
        try:
            response = self.SQLProvider.get("SELECT username FROM connected_users WHERE room_id='{}'".format(self.currentRoomID))
            if response == None:
                return []
            users = [user[0] for user in response] # type: ignore
            return users # type: ignore
        except sqlError as err:
            print(err)

    def setUsername(self, newUsername: str):
        self.username = newUsername
