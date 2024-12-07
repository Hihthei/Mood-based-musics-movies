import mysql.connector

class Database:
    def __init__(self, user:str = None, password:str = None):
        self.connect(user, password)
        pass

    def __is_Table(self, Name:str) -> bool:
        terminal = self.__database.cursor()
        terminal.execute("show tables")

        for i in terminal.fetchall():
            if i[0] == Name.lower():
                terminal.close()
                return True
            
        terminal.close()
        return False

    def connect(self, user:str, password:str):
        try:
            self.__database = mysql.connector.connect(host="localhost", user=user, passwd=password, database="Mood_Based_MM")
        except mysql.connector.DatabaseError as e:
            self.__database = None
            self.databaseError = e.errno
        else:
            self.databaseError = 0
        
    def __create_Database(self, user:str, password:str):
        try:
            self.__database = mysql.connector.connect(host="localhost", user=user, passwd=password)
            terminal = self.__database.cursor()
            terminal.execute("CREATE DATABASE Mood_Based_MM")
            terminal.execute("USE Mood_Based_MM")
            terminal.close()
        except mysql.connector.DatabaseError as e:
            self.__database = None
            self.databaseError = e.errno
        else:
            self.databaseError = 0
        
    def is_User(self, username:str) -> bool:
        if self.__database == None:
            return None

        terminal = self.__database.cursor()

        command = f"Select users.userName From Users Where users.userName = '{username}'"

        terminal.execute(command)

        if terminal.fetchall():
            terminal.close()
            return True

        terminal.close()
        return False

    def add_User(self, username:str, hashPassword:str):
        if self.__database == None:
            return None

        if self.is_User(username):
            error = f"Error User: {username} Already is taken"
            raise mysql.connector.DatabaseError(error)
        
        terminal = self.__database.cursor()

        command = f"INSERT INTO Users (userName, hashPassword) VALUES ('{username}', '{hashPassword}')"

        terminal.execute(command)
        terminal.close()

    def remove_User(self, username:str):
        if self.__database == None:
            return None

        if not self.is_User(username):
            error = f"Error User: {username} isn't in the database"
            raise mysql.connector.DatabaseError(error)
        
        terminal = self.__database.cursor()

        command = f"DELETE FROM Users WHERE Users.userName = '{username}'"

        terminal.execute(command)
        terminal.close()

    def show_Table(self):
        if self.__database == None:
            return None
        
        terminal = self.__database.cursor()

        terminal.execute("show tables")
        print(terminal.fetchall())
    
        terminal.close()

    def show_Users(self):
        if self.__database == None:
            return None
        
        terminal = self.__database.cursor()

        terminal.execute("select * from Users")
        print(terminal.fetchall())
    
        terminal.close()

database = Database(user="root", password="!Cd2@5Cprb")
