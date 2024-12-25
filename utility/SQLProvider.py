import mysql.connector
from os import getenv as env
import psycopg2

class SQLProvider:
    def __init__(self):
        connectionType: str = env('SQL_CONNECTION_TYPE') or 'local'
        if connectionType == 'online':
            try:
                self.cnx = psycopg2.connect(user=env('SQL_USERNAME'), password=env('SQL_PASSWORD'), host=env('SQL_HOST'), port=env('SQL_PORT'), dbname="postgres")
            except psycopg2.Error as err:
                print(err)
        else: 
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

    def insert(self, prompt: str) -> int | None:
        """Permits to execute INSERT and UPDATE statements"""
        try:
            self.cursor.execute(prompt)
            self.cnx.commit()
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            print(err)

    def get(self, prompt: str):
        """Permits to execute SELECT statements"""
        try:
            self.cursor.execute(prompt)
            response = self.cursor.fetchall()
            return response
        except mysql.connector.Error as err:
            print(err)

    def executeSQL(self, prompt: str):
        try:
            self.cursor.execute(prompt)
            self.cnx.commit()
        except mysql.connector.Error as err:
            print(err)

    def closeConnection(self):
        self.cnx.close()
        self.cursor.close()