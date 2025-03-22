from typing import Sequence
import mysql.connector
from os import getenv as env
import psycopg2
from utility import consolLog
from utility.ErrorHandler import raiseAnError
from mysql.connector.types import MySQLConvertibleType, RowType

class SQLProvider:
    def __init__(self):
        self.connectionType: str = env('SQL_CONNECTION_TYPE') or 'local'
        if self.connectionType == 'online':
            try:
                self.cnx = psycopg2.connect(user=env('SQL_USERNAME'), password=env('SQL_PASSWORD'), host=env('SQL_HOST'), port=env('SQL_PORT'), dbname="postgres")
            except psycopg2.Error as err:
                consolLog.error(err)
                raiseAnError(err)
        else: 
            try:
                self.cnx = mysql.connector.connect(user=env('SQL_USERNAME'), password=env('SQL_PASSWORD'), host=env('SQL_HOST'))
                self.cnx.autocommit = True # type: ignore
            except mysql.connector.Error as err:
                consolLog.error(err)
                raiseAnError(err)

        self.cursor = self.cnx.cursor()

    def createDatabase(self, dbName: str) -> None:
        try:
            self.cursor.execute(
                "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(dbName))
        except mysql.connector.Error as err:
            consolLog.error("Failed creating database: {}".format(err))
            raiseAnError(err)
    
    def useDatabase(self, dbName: str) -> None:
        try:
            self.cursor.execute("USE {}".format(dbName))
        except mysql.connector.Error as err:
            consolLog.error("Database {} does not exists.".format(dbName))
            raiseAnError(err)

    def insert(self, prompt: str, parameters: Sequence[MySQLConvertibleType] | None = None, returnedValue: str | None = None) -> int | None:
        """Permits to execute INSERT and UPDATE statements"""
        try:
            if parameters:
                if returnedValue and self.connectionType == "online":
                    self.cursor.execute(prompt + ("RETURNING {}".format(returnedValue)), parameters)
                    self.cnx.commit()
                    return int(self.cursor.fetchone()) # type: ignore
                else:
                    self.cursor.execute(prompt, parameters)
            else:
                self.cursor.execute(prompt)
    
            self.cnx.commit()
            return self.cursor.lastrowid
      
        except mysql.connector.Error as err:
            consolLog.error(err)
            raiseAnError(err)

    def get(self, prompt: str, parameters: Sequence[MySQLConvertibleType] | None = None):
        """Permits to execute SELECT statements"""
        try:
            if parameters:
                self.cursor.execute(prompt, parameters)
            else:
                self.cursor.execute(prompt) 
            response = self.cursor.fetchall()
            return response
        except mysql.connector.Error as err:
            consolLog.error(err)
            raiseAnError(err)

    def executeSQL(self, prompt: str, parameters: Sequence[MySQLConvertibleType] | None = None) -> None:
        try:
            if parameters:
                self.cursor.execute(prompt, parameters)
            else:
                self.cursor.execute(prompt) 
            self.cnx.commit()
        except mysql.connector.Error as err:
            consolLog.error(err)
            raiseAnError(err)

    def closeConnection(self) -> None:
        self.cnx.close()
        self.cursor.close()