from dotenv import load_dotenv
from os import getenv as env
from SQLProvider import SQLProvider

load_dotenv()

sqlProvider = SQLProvider()

if env('SQL_CONNECTION_TYPE') == 'local':
    sqlProvider.createDatabase('inkspiration')
    sqlProvider.useDatabase('inkspriration')

sqlProvider.executeSQL('CREATE TABLE IF NOT EXISTS connected_users (username VARCHAR(255), roomName VARCHAR(255))')
sqlProvider.executeSQL('CREATE TABLE IF NOT EXISTS drawings (creator VARCHAR(255), pixels TEXT, roomName VARCHAR(255))')
sqlProvider.executeSQL('CREATE TABLE IF NOT EXISTS votes (voter VARCHAR(255), attributedVote TEXT, roomName VARCHAR(255))')

sqlProvider.closeConnection()