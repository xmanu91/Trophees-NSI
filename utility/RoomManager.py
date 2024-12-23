import SQLProvider as sql
from mysql.connector import Error as sqlError

class RoomManager:
    def __init__(self, SQLProvider: sql.SQLProvider, username: str):
        self.SQLProvider = SQLProvider
        self.username = username
        self.currentRoomID = None
    
    def getAllRooms(self):
        response = self.SQLProvider.get('SELECT * FROM connected_users')
        if response == None:
            return []
        rooms = [row for row in response] 
        return rooms
    
    def createConnection(self, roomName: str):
        try:
            rooms = self.getAllRooms()
            for room in rooms:
                if self.username in room:
                    return Exception((201, "User already exists"))
            self.SQLProvider.insert('INSERT INTO connected_users (username, roomName) VALUES ("{}", "{}")'.format(self.username, roomName))
        except sqlError as err:
            print(err)
        self.currentRoomID = roomName

    def closeConnection(self):
        try:
            self.SQLProvider.executeSQL('DELETE FROM connected_users WHERE username="{}"'.format(self.username))
        except sqlError as err:
            print(err)
        self.currentRoomID = None
    
    def getUsersInCurrentRoom(self) -> list[str] | None:
        try:
            response = self.SQLProvider.get('SELECT username FROM connected_users WHERE roomName="{}"'.format(self.currentRoomID))
            if response == None:
                return []
            users = [user[0] for user in response] # type: ignore
            return users # type: ignore
        except sqlError as err:
            print(err)

    def setUsername(self, newUsername: str):
        self.username = newUsername

