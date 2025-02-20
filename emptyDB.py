from utility.SQLProvider import SQLProvider
from dotenv import load_dotenv

load_dotenv()

sqlProvider = SQLProvider()

# Ajuster le temps d'attente pour les requêtes
sqlProvider.executeSQL("SET statement_timeout = '30s';")  # Ajustez le temps selon vos besoins
print("Temps d'attente ajusté à 30 secondes")

# Vider les tables avec DELETE
sqlProvider.executeSQL('DELETE FROM drawings;')
print("Table drawings emptied")
sqlProvider.executeSQL('DELETE FROM connected_users;')
print("Table connected_users emptied")
sqlProvider.executeSQL('DELETE FROM votes;')
print("Table votes emptied")
sqlProvider.executeSQL('DELETE FROM rooms;')
print("Table rooms emptied")

print("Database reset")