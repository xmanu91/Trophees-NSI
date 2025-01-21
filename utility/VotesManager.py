from utility.SQLProvider import SQLProvider
from mysql.connector import Error as sqlError

class VotesManager:
    def __init__(self, sqlManager: SQLProvider, roomId: str, username: str):
        self.sqlManager = sqlManager
        self.roomId = roomId
        self.username = username
        self.drawings = []

    def getDrawings(self):
        try: 
            # Utilisation de paramètres dans la requête SELECT
            response = self.sqlManager.get("SELECT creator, pixels FROM drawings WHERE room_id=%s AND creator<>%s", (self.roomId, self.username))
            if response is None:
                return None
            self.drawings = [(drawing[0], eval(drawing[1])) for drawing in response]  # type: ignore
            return self.drawings
        except sqlError as err:
            print(err)

    def vote(self, attributedVote):
        try:
            # Utilisation de paramètres dans la requête INSERT
            self.sqlManager.insert("INSERT INTO votes (voter, attributedVote, room_id) VALUES (%s, %s, %s)", 
                                   (self.username, attributedVote, self.roomId))
        except sqlError as err:
            print(err)

    def getVotes(self):
        try:
            # Utilisation de paramètres dans la requête SELECT
            response = self.sqlManager.get("SELECT * FROM votes WHERE room_id=%s", (self.roomId))
            if response is None:
                return None
            votes = [vote for vote in response]
            return votes
        except sqlError as err:
            print(err)

    def getWinner(self):
        votes = self.getVotes()
        if votes is None:
            return None

        # Count the votes
        usersDict = {} 
        for vote in votes:
            if vote[1] in usersDict:  # type: ignore
                usersDict[vote[1]] += 1  # type: ignore
            else: 
                usersDict[vote[1]] = 1  # type: ignore
        # Getting the winners
        results = [v for k, v in usersDict.items()]
        winners = []
        for i in range(len(results)):
            if results[i] == max(results):
                winners.append(list(usersDict.keys())[i])
        
        return winners
