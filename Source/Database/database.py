import mysql.connector

class Database:
    def __init__(self):
        self.__database = None
        pass

    def connect(self, user:str, password:str):
        try:
            self.__database = mysql.connector.connect(host="localhost", user=user, passwd=password, database="Mood_Based_MM")
        except mysql.connector.DatabaseError as e:
            self.__database = None
            return e.errno
        
    def __create_Database(self, user:str, password:str):
        try:
            self.__database = mysql.connector.connect(host="localhost", user=user, passwd=password)
            terminal = self.__database.cursor()
            terminal.execute("CREATE DATABASE Mood_Based_MM")
            terminal.execute("USE Mood_Based_MM")
            terminal.close()
        except mysql.connector.DatabaseError as e:
            self.__database = None
            return e.errno