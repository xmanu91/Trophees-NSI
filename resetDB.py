from utility.SQLProvider import SQLProvider
from dotenv import load_dotenv
import os
import tempfile

load_dotenv()

sqlProvider = SQLProvider()

sqlProvider.executeSQL("SET statement_timeout = '10s';")  # Ajustez le temps selon vos besoins
print("Temps d'attente ajusté à 10 secondes")

sqlProvider.executeSQL('DROP table drawings;')
sqlProvider.executeSQL('DROP table connected_users;')
sqlProvider.executeSQL('DROP table votes;')
sqlProvider.executeSQL('DROP table rooms;')

print("Database reset")