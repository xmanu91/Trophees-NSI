from dotenv import load_dotenv
import sys
from os import getenv as env
import os
from utility.SQLProvider import SQLProvider

if getattr(sys, 'frozen', False):
    dotenv_path = os.path.join(sys._MEIPASS, '.env')
else:
    dotenv_path = '.env'

load_dotenv(dotenv_path=dotenv_path)

sqlProvider = SQLProvider()

if env('SQL_CONNECTION_TYPE') == 'local':
    sqlProvider.createDatabase('inkspired')
    sqlProvider.useDatabase('inkspired')

sqlProvider.executeSQL('CREATE TABLE IF NOT EXISTS rooms (room_id SERIAL NOT NULL, creator VARCHAR(255), room_name VARCHAR(255), theme VARCHAR(255), state VARCHAR(255), rounds_number int, round_time int, PRIMARY KEY(room_id))')

if env('SQL_CONNECTION_TYPE') == 'local':
    sqlProvider.executeSQL('CREATE TABLE IF NOT EXISTS drawings (creator VARCHAR(255), image TEXT, room_id int, FOREIGN KEY (room_id) REFERENCES rooms(room_id))')
else:
    sqlProvider.executeSQL('CREATE TABLE IF NOT EXISTS drawings (creator VARCHAR(255), image bytea, room_id int, FOREIGN KEY (room_id) REFERENCES rooms(room_id))')

sqlProvider.executeSQL('CREATE TABLE IF NOT EXISTS connected_users (user_id SERIAL NOT NULL, username VARCHAR(255), room_id int, PRIMARY KEY(user_id), FOREIGN KEY (room_id) REFERENCES rooms(room_id))')

sqlProvider.executeSQL('CREATE TABLE IF NOT EXISTS votes (voter VARCHAR(255), attributedVote TEXT, rating int, round int, room_id int, FOREIGN KEY (room_id) REFERENCES rooms(room_id))')