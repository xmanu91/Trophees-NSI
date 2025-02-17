from utility.SQLProvider import SQLProvider
from dotenv import load_dotenv
import os
import tempfile

load_dotenv()

sqlProvider = SQLProvider()

sqlProvider.executeSQL('DROP table drawings;')
sqlProvider.executeSQL('DROP table connected_users;')
sqlProvider.executeSQL('DROP table votes;')
sqlProvider.executeSQL('DROP table rooms;')

print("Database reset")