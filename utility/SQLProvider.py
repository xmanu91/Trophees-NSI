import mysql.connector
from os import getenv as env

class SQLProvider:
    def __init__(self):
        try:
            self.cnx = mysql.connector.connect(user=env('SQL_USERNAME'), password=env('SQL_PASSWORD'), host=env('SQL_HOST'))
        except mysql.connector.Error as err:
            print(err)

        self.cursor = self.cnx.cursor()

    def createDatabase(self, dbName: str):
        try:
            self.cursor.execute(
                "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(dbName))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
    
    def useDatabase(self, dbName: str):
        try:
            self.cursor.execute("USE {}".format(dbName))
        except mysql.connector.Error:
            print("Database {} does not exists.".format(dbName))

    def insert(self, prompt: str):
        try:
            self.cursor.execute(prompt)
            self.cnx.commit()
        except mysql.connector.Error as err:
            print(err)

    def get(self, prompt: str):
        """Permits to execute SELECT statements"""
        try:
            self.cursor.execute(prompt)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)

    def executeSQL(self, prompt: str):
        try:
            self.cursor.execute(prompt)
        except mysql.connector.Error as err:
            print(err)

    def closeConnection(self):
        self.cnx.close()
        self.cursor.close()