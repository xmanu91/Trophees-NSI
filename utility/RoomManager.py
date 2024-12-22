import SQLProvider as sql
from mysql.connector import Error as sqlError

class RoomManager:
    def __init__(self, SQLProvider: sql.SQLProvider):
        self.SQLProvider = SQLProvider
        self.currentRoomID = None
    
    def getAllRooms(self):
        response = self.SQLProvider.get('SELECT * FROM connected_users')
        if response == None:
            return []
        rooms = [row for row in response] 
        print(rooms)
        return rooms
    
    def createRoom(self, roomName: str, username: str):
        try:
            roomId = self.SQLProvider.insert('INSERT INTO connected_users VALUES ({}, {})'.format(username, roomName))
        except sqlError as err:
            print(err)
        self.currentRoomID = roomId

    def joinRoom(self, roomName: str, username: str):
        rooms = self.getAllRooms()
        if roomName in rooms:
            pass
