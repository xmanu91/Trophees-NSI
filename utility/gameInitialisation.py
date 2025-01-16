from dotenv import load_dotenv
from os import getenv as env
from SQLProvider import SQLProvider

load_dotenv()

sqlProvider = SQLProvider()

if env('SQL_CONNECTION_TYPE') == 'local':
    sqlProvider.createDatabase('inkspiration')
    sqlProvider.useDatabase('inkspriration')

sqlProvider.executeSQL('CREATE TABLE IF NOT EXISTS rooms (room_id SERIAL NOT NULL, room_name VARCHAR(255), theme VARCHAR(255), PRIMARY KEY(room_id))')
sqlProvider.executeSQL('CREATE TABLE IF NOT EXISTS connected_users (username VARCHAR(255), room_id int, FOREIGN KEY (room_id) REFERENCES rooms(room_id))')
sqlProvider.executeSQL('CREATE TABLE IF NOT EXISTS drawings (creator VARCHAR(255), pixels TEXT, room_id int, FOREIGN KEY (room_id) REFERENCES rooms(room_id))')
sqlProvider.executeSQL('CREATE TABLE IF NOT EXISTS votes (voter VARCHAR(255), attributedVote TEXT,room_id int, FOREIGN KEY (room_id) REFERENCES rooms(room_id))')
