import SQLProvider as sql
from dotenv import load_dotenv
from RoomManager import RoomManager

load_dotenv()

SQLProvider = sql.SQLProvider()
roomManager = RoomManager(SQLProvider=SQLProvider)

roomManager.createRoom("test", "test1")
roomManager.getAllRooms()