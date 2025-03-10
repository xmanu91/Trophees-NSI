import mysql.connector
from os import getenv as env
import psycopg2
from utility import consolLog

class SQLProvider:
    def __init__(self):
        self.connectionType: str = env('SQL_CONNECTION_TYPE') or 'local'
        if self.connectionType == 'online':
            try:
                self.cnx = psycopg2.connect(user=env('SQL_USERNAME'), password=env('SQL_PASSWORD'), host=env('SQL_HOST'), port=env('SQL_PORT'), dbname="postgres")
            except psycopg2.Error as err:
                consolLog.error(err)
        else: 
            try:
                self.cnx = mysql.connector.connect(user=env('SQL_USERNAME'), password=env('SQL_PASSWORD'), host=env('SQL_HOST'))
            except mysql.connector.Error as err:
                consolLog.error(err)

        self.cursor = self.cnx.cursor()

    def createDatabase(self, dbName: str):
        try:
            self.cursor.execute(
                "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(dbName))
        except mysql.connector.Error as err:
            consolLog.error("Failed creating database: {}".format(err))
    
    def useDatabase(self, dbName: str):
        try:
            self.cursor.execute("USE {}".format(dbName))
        except mysql.connector.Error:
            consolLog.error("Database {} does not exists.".format(dbName))

    def insert(self, prompt: str, parameters: tuple | None = None, returnedValue: str | None = None) -> int | None:
        """Permits to execute INSERT and UPDATE statements"""
        try:
            self.cursor.execute(prompt + ("RETURNING {}".format(returnedValue) if returnedValue else ""), parameters)
            self.cnx.commit()
            if self.connectionType == 'online' and returnedValue:
                return self.cursor.fetchone()[0]
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            consolLog.error(err)

    def get(self, prompt: str, parameters: tuple | None = None):
        """Permits to execute SELECT statements"""
        try:
            self.cursor.execute(prompt, parameters)
            response = self.cursor.fetchall()
            return response
        except mysql.connector.Error as err:
            consolLog.error(err)

    def executeSQL(self, prompt: str, parameters: tuple | None = None):
        try:
            self.cursor.execute(prompt, parameters)
            self.cnx.commit()
        except mysql.connector.Error as err:
            consolLog.error(err)

    def closeConnection(self):
        self.cnx.close()
        self.cursor.close()