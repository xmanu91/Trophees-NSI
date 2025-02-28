import utility.tools

from utility.SQLProvider import SQLProvider
from mysql.connector import Error as sqlError
from utility import consolLog

import os
import tempfile

class VotesManager:
    def __init__(self, sqlManager: SQLProvider, roomId: str, username: str, tempdir: tempfile.TemporaryDirectory):
        self.tempdir = tempdir
        self.sqlManager = sqlManager
        self.roomId = roomId
        self.username = username
        self.drawings = []
        self.participants = []

    def getDrawings(self):
        try: 
            utility.tools.initialiseDirectory(self.tempdir.name)
            consolLog.info("RoomId : ", self.roomId)
            # Utilisation de paramètres dans las requête SELECT
            response = self.sqlManager.get("SELECT creator, image FROM drawings WHERE room_id=%s and creator<>%s", (str(self.roomId), self.username))
            if response is None:
                return None
            self.drawings = [(drawing[0], drawing[1]) for drawing in response]  # type: ignore
            self.participants = [drawing[0] for drawing in response]  # type: ignore
            consolLog.info("response" + str(response), "self.drawings:" + str(self.drawings), "self.participants: " + str(self.participants))
            for drawing in self.drawings:
                self.saveDrawing(drawing[1], drawing[0])
            return self.drawings
        except sqlError as err:
            consolLog.error(err)

    def getDrawing(self, username: str):
        try: 
            consolLog.info("RoomId : ", self.roomId)
            # Utilisation de paramètres dans la requête SELECT
            response = self.sqlManager.get("SELECT creator, image FROM drawings WHERE room_id=%s and creator=%s", (str(self.roomId), username))
            if response is None:
                return None
            self.saveDrawing(response[0][1], response[0][0])
            return (response[0][1], response[0][0])
        except sqlError as err:
            consolLog.error(err)

    def vote(self, attributedVote, rating: int):
        try:
            # Utilisation de paramètres dans la requête INSERT
            self.sqlManager.insert("INSERT INTO votes (voter, attributedVote, rating, room_id) VALUES (%s, %s, %s, %s)", 
                                   (self.username, attributedVote, rating, str(self.roomId)))
        except sqlError as err:
            consolLog.error(err)

    def getVotes(self):
        try:
            # Utilisation de paramètres dans la requête SELECT
            response = self.sqlManager.get("SELECT * FROM votes WHERE room_id=%s", (str(self.roomId),))
            if response is None:
                return None
            votes = [vote for vote in response]
            return votes
        except sqlError as err:
            consolLog.error(err)

    def getWinners(self):
        votes = self.getVotes()
        if votes is None:
            return None

        # Count the votes
        usersDict = {} 
        for vote in votes:
            if vote[1] in usersDict:  # type: ignore
                usersDict[vote[1]] += vote[2]  # type: ignore
            else: 
                usersDict[vote[1]] = vote[2]  # type: ignore
        # Getting the winners
        results = [v/len(self.participants) for k, v in usersDict.items()]
        winners = []
        for i in range(len(results)):
            if results[i] == max(results):
                winners.append(list(usersDict.keys())[i])
        
        return winners

    def saveDrawing(self, binary, name):
        out = None
  
        try: 
            # creating files in output folder for writing in binary mode 
            out = open(os.path.join(self.tempdir.name, name.strip() + '.png'), 'wb') 
            
            # writing image data 
            out.write(binary) 

        except Exception as err:
            consolLog.error(err)
            
        # closing output file object 
        finally: 
            out.close()