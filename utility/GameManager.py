from mysql.connector import Error as sqlError
from utility.SQLProvider import SQLProvider
from utility.ErrorHandler import raiseAnError
from utility.tools import getPath
from utility import consolLog
from random import choice
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
            consolLog.error(err)

    def getTheme(self) -> str:
        try: 
            result = self.sqlManager.get("SELECT theme FROM rooms WHERE room_id=%s", (str(self.roomId),))
            if result:
                return result[0][0]
            else: 
                consolLog.error("Récupération du theme impossible")
                raiseAnError("Récupération du theme impossible")
                return "ERR"
        except sqlError as err:
            consolLog.error(err)
            raiseAnError(err)
            return "ERR"

    def sendDrawing(self, path):
        print(self.getBinaryArray(path))
        try:
            if self.sqlManager.connectionType == 'local':
                self.sqlManager.insert("INSERT INTO drawings (creator, image, room_id) VALUES (%s, %s, %s)", 
                                   (self.username, self.getBinaryArray(path), self.roomId))
            else:
                self.sqlManager.insert("INSERT INTO drawings (creator, image, room_id) VALUES (%s, decode(%s, 'hex'), %s)", 
                                   (self.username, self.getBinaryArray(path), self.roomId))
        except sqlError as err:
            consolLog.error(err)

    
    def deleteDrawings(self):
        try:
            self.sqlManager.executeSQL('DELETE FROM drawings WHERE room_id=%s', (str(self.roomId),))
        except sqlError as err:
            consolLog.error(err)

    def loadThemes(self):
        with open(getPath("assets/themes.txt"), "r", encoding="utf-8") as file:
            themes = [line.strip() for line in file]
        return themes

    def getBinaryArray(self, path):
        with open(path, "rb") as image:
            f = image.read()
            b = bytes(f).hex()
            return b

    def getTempDir(self):
        return self.tempdir

    def resetTempDir(self):
        self.tempdir.cleanup()
        self.tempdir = tempfile.TemporaryDirectory()