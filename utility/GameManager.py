from mysql.connector import Error as sqlError
from SQLProvider import SQLProvider

class GameManager:

    def __init__(self, sqlManager: SQLProvider, username: str, roomName: str):
        self.sqlManager = sqlManager
        self.username = username
        self.roomName = roomName

    def sendDrawing(self, pixelList: list):
        try: 
            self.sqlManager.insert('INSERT INTO drawings (creator, pixels, roomName) VALUES ("{}", "{}", "{}")'.format(self.username, str(pixelList), self.roomName))
        except sqlError as err:
            print(err)