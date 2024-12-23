from SQLProvider import SQLProvider
from mysql.connector import Error as sqlError

class VotesManager:
    def __init__(self, sqlManager: SQLProvider, roomName: str, username: str):
        self.sqlManager = sqlManager
        self.roomName = roomName
        self.username = username
        self.drawings = []

    def getDrawings(self):
        try: 
            response = self.sqlManager.get('SELECT creator, pixels FROM drawings WHERE roomName="{}" AND creator<>"{}"'.format(self.roomName, self.username))
            if response == None:
                return None
            self.drawings = [drawing for drawing in response]
            return self.drawings
        except sqlError as err:
            print(err)

    def vote(self, attributedVote):
        try:
            self.sqlManager.insert('INSERT INTO votes (voter, attributedVote, roomName) VALUES ("{}", "{}", "{}")'.format(self.username, attributedVote, self.roomName))
        except sqlError as err:
            print(err)

    def getVotes(self):
        try:
            response = self.sqlManager.get('SELECT * FROM votes WHERE roomName="{}"'.format(self.roomName))
            if response == None:
                return None
            votes = [vote for vote in response]
            return votes
        except sqlError as err:
            print(err)

    def getWinner(self):
        votes = self.getVotes()
        if votes == None:
            return None

        #Count the votes
        usersDict = {} 
        for vote in votes:
            if vote[1] in usersDict: # type: ignore
                usersDict[vote[1]]+=1 # type: ignore
            else: 
                usersDict[vote[1]]=1 # type: ignore
        #Getting the winners
        results = [v for k, v in usersDict.items()]
        winners = []
        for i in range(len(results)):
            if results[i] == max(results):
                winners.append(list(usersDict.keys())[i])
        
        return winners