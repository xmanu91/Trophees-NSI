from mysql.connector import Error as sqlError
from SQLProvider import SQLProvider
from random import choice

class GameManager:

    def __init__(self, sqlManager: SQLProvider, username: str, roomId: int):
        self.sqlManager = sqlManager
        self.username = username
        self.roomId = roomId
        self.drawingTheme = ""

    def drawTheme(self):
        theme = choice(self.loadThemes())
        try: 
            self.sqlManager.insert("UPDATE rooms SET theme='{}' WHERE room_id={}".format(theme, self.roomId))
            self.drawingTheme = theme
        except sqlError as err:
            print(err)

    def sendDrawing(self, pixelList: list):
        try: 
            self.sqlManager.insert("INSERT INTO drawings (creator, pixels, room_id) VALUES ('{}', '{}','{}')".format(self.username, str(pixelList), self.roomId))
        except sqlError as err:
            print(err)

    def loadThemes(self):
        with open("assets/themes.txt", "r", encoding="utf-8") as file:
            themes = [line.strip() for line in file]
        return themes