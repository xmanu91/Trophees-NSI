from mysql.connector import Error as sqlError
from utility.SQLProvider import SQLProvider
from random import choice
import os

class GameManager:

    def __init__(self, sqlManager: SQLProvider, username: str, roomId: int):
        self.sqlManager = sqlManager
        self.username = username
        self.roomId = roomId
        self.drawingTheme = ""

    def drawTheme(self):
        theme = choice(self.loadThemes())
        try: 
            self.sqlManager.insert("UPDATE rooms SET theme=%s WHERE room_id=%s", (theme, self.roomId))
            self.drawingTheme = theme
        except sqlError as err:
            print(err)

    def sendDrawing(self, path):
        try:
            self.sqlManager.insert("INSERT INTO drawings (creator, image, room_id) VALUES (%s, decode(%s, 'hex'), %s)", 
                                   (self.username, self.get_binary_array(path), self.roomId))
        except sqlError as err:
            print(err)

    def loadThemes(self):
        with open("assets/themes.txt", "r", encoding="utf-8") as file:
            themes = [line.strip() for line in file]
        return themes

    def get_binary_array(self, path):
        with open(path, "rb") as image:
            f = image.read()
            b = bytes(f).hex()
            return b