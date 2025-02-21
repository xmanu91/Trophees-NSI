from mysql.connector import Error as sqlError
from utility.SQLProvider import SQLProvider
from utility.tools import getPath
from random import choice
import os
import tempfile

class GameManager:

    def __init__(self, sqlManager: SQLProvider, username: str, roomId: int):
        self.sqlManager = sqlManager
        self.username = username
        self.roomId = roomId
        self.drawingTheme = ""
        self.tempdir = tempfile.TemporaryDirectory()

    def drawTheme(self):
        theme = choice(self.loadThemes())
        try: 
            self.sqlManager.insert("UPDATE rooms SET theme=%s WHERE room_id=%s", (theme, self.roomId))
            self.drawingTheme = theme
        except sqlError as err:
            print(err)

    def getTheme(self):
        try: 
            result = self.sqlManager.get("SELECT theme FROM rooms WHERE room_id=%s", (str(self.roomId),))
            return result[0][0]
        except sqlError as err:
            print(err)

    def sendDrawing(self, path):
        try:
            self.sqlManager.insert("INSERT INTO drawings (creator, image, room_id) VALUES (%s, decode(%s, 'hex'), %s)", 
                                   (self.username, self.get_binary_array(path), self.roomId))
        except sqlError as err:
            print(err)

    
    def deleteDrawings(self):
        try:
            self.sqlManager.executeSQL('DELETE FROM drawings WHERE room_id=%s', (str(self.roomId),))
        except sqlError as err:
            print(err)

    def loadThemes(self):
        with open(getPath("assets/themes.txt"), "r", encoding="utf-8") as file:
            themes = [line.strip() for line in file]
        return themes

    def get_binary_array(self, path):
        with open(path, "rb") as image:
            f = image.read()
            b = bytes(f).hex()
            return b

    def getTempDir(self):
        return self.tempdir

    def resetTempDir(self):
        self.tempdir.cleanup()
        self.tempdir = tempfile.TemporaryDirectory()