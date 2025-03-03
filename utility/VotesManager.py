from mysql.connector import Error as sqlError
from utility.SQLProvider import SQLProvider
from utility.RoomManager import RoomManager
from utility import consolLog
import utility.tools
import tempfile
import time
import os

class VotesManager:
    def __init__(self, sqlManager: SQLProvider, roomId: str, username: str, tempdir: tempfile.TemporaryDirectory, roomManager: RoomManager):
        self.tempdir = tempdir
        self.sqlManager = sqlManager
        self.roomManager = roomManager
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

    def vote(self, attributedVote, rating: int, round: int):
        try:
            # Utilisation de paramètres dans la requête INSERT
            self.sqlManager.insert("INSERT INTO votes (voter, attributedVote, rating, round, room_id) VALUES (%s, %s, %s, %s, %s)", 
                                   (self.username, attributedVote, rating, str(round),  str(self.roomId)))
        except sqlError as err:
            consolLog.error(err)

    def getVotes(self, round: int = None):
        try:
            if round:
                response = self.sqlManager.get("SELECT * FROM votes WHERE room_id=%s and round=%s", (str(self.roomId), str(round)))
            else:
                response = self.sqlManager.get("SELECT * FROM votes WHERE room_id=%s", (str(self.roomId),))
            if response is None:
                return None
            votes = [vote for vote in response]
            return votes
        except sqlError as err:
            consolLog.error(err)

    def getWinners(self, round: int = None):
        votes = self.getVotes(round)

        while len(votes) != self.roomManager.getConnectedUsersNumberInRoom(self.roomManager.currentRoomID):
            votes = self.getVotes(round)
            time.sleep(2)
            consolLog.warn("Tous les votes n'ont pas encore ete recup")
            self.getDrawings()
            self.drawnList = []

            for drawn in os.listdir(self.tempdir.name):
                self.drawnList.append(drawn)

            consolLog.vinfo("drawnList", self.drawnList)
            consolLog.vinfo("Votes dans getwinners:", votes)
            consolLog.vinfo("Participants :", self.participants)

        consolLog.vinfo("Tous les dessins sont recup.")
        
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

    def getPodium(self):
        votes = self.getVotes()
        if votes is None:
            return None
        
        scores = {}
        for vote in votes:
            scores[vote[1]] = scores.get(vote[1], 0) + vote[2]  # type: ignore
        
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        podium = [user for user, score in sorted_scores[:3]]
        return podium
        
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