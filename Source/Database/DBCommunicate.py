import mysql.connector

class DBCommunicateError (Exception):
    # Error Unknow - 0
    # Error Database connection - 1/9
    # Error Table - 10/19
    # Error Users - 20/29
    # Error Commit - 100/109

    def __init__(self, message:str, code:int = None):
        super().__init__(message)
        self.message = message
        self.code = code
    
    def __str__(self):
        return f"{self.message}: [{self.code}]" if self.code else self.message

class DBCommunicate:
    def __init__(self, user:str = None, password:str = None):
        try:
            self.__connect(user, password)
        except DBCommunicateError as e:
            print(e)
            raise e

    def __connect(self, user:str, password:str):
        self.__login = (user, password)
        try:
            self.__database = mysql.connector.connect(host="localhost", user=user, passwd=password, database="Mood_Based_MM")
        except mysql.connector.DatabaseError as e:
            self.__database = None
            if e.errno == 1045:
                raise DBCommunicateError("Error Connection, wrong User or password", 1)
            elif e.errno == 1047:
                raise DBCommunicateError("Error No Database mood_based_mm", 2)
            else:
                raise DBCommunicateError("Error Unknow", 0)
    
    def reconnecte(self, user:str = None, password:str = None):
        self.__login = (user, password) if (user and password) else self.__login
        try:
            self.__connect(self.__login[0], self.__login[1])
        except DBCommunicateError as e:
            raise e

    def close_connection(self):
        self.__database.close()

    def connect_User(self, username:str):
        if not self.__database:
            raise DBCommunicateError("Error Not Connected to Database", 3)
        elif not self.__is_Table("Users"):
            raise DBCommunicateError("Error Not Table", 10)
        
        terminal = self.__database.cursor()
        command = f"SELECT Users.userID, Users.hashpassword FROM Users WHERE Users.userName = '{username}'"
        terminal.execute(command)
        result = terminal.fetchall()
        terminal.close()
        if not result:
            raise DBCommunicateError("Error User Not Exist", 20)
        return result[0]

    def add_User(self, username:str, hashPassword:str):
        if not self.__database:
            raise DBCommunicateError("Error Not Connected to Database", 3)
        elif not self.__is_Table("Users"):
            raise DBCommunicateError("Error Not Table", 10)
        try:
            if self.__is_User(username):
                raise DBCommunicateError("Error User Exist", 21)
        except DBCommunicateError as e:
            raise e
        
        terminal = self.__database.cursor()
        command = f"INSERT INTO Users (userName, hashPassword) VALUES ('{username}', '{hashPassword}')"
        terminal.execute(command)
        terminal.close()
        try:
            self.__database.commit()
        except mysql.connector.Error as e:
            self.__database.rollback()
            raise DBCommunicateError("Error Commit Failed", 100)

    def remove_User(self, username:str):
        if not self.__database:
            raise DBCommunicateError("Error Not Connected to Database", 3)
        elif not self.__is_Table("Users"):
            raise DBCommunicateError("Error Not Table", 10)
        try:
            if not self.__is_User(username):
                raise DBCommunicateError("Error User Not Exist", 20)
        except DBCommunicateError as e:
            raise e
        
        terminal = self.__database.cursor()
        command = f"DELETE FROM Users WHERE Users.userName = '{username}'"
        terminal.execute(command)
        terminal.close()
        try:
            self.__database.commit()
        except mysql.connector.Error as e:
            self.__database.rollback()
            raise DBCommunicateError("Error Commit Failed", 100)

    def show_Table(self):
        if not self.__database:
            raise DBCommunicateError("Error Not Connected to Database", 3)
        
        terminal = self.__database.cursor()
        terminal.execute("show tables")
        print(terminal.fetchall())
        terminal.close()

    def show_Users(self):
        if not self.__database:
            raise DBCommunicateError("Error Not Connected to Database", 3)
        elif not self.__is_Table("Users"):
            raise DBCommunicateError("Error Not Table", 10)

        terminal = self.__database.cursor()
        terminal.execute("select * from Users")
        print(terminal.fetchall())

        terminal.close()

    def __is_Table(self, Name:str) -> bool:
        if not self.__database:
            raise DBCommunicateError("Error Not Connected to Database", 3)
        terminal = self.__database.cursor()
        terminal.execute("show tables")
        Name = Name.lower()
        for i in terminal.fetchall():
            if i[0] == Name.lower():
                terminal.close()
                return True
        terminal.close()
        return False

    def __is_User(self, username:str) -> bool:
        if not self.__database:
            raise DBCommunicateError("Error Not Connected to Database", 3)
        elif not self.__is_Table("Users"):
            raise DBCommunicateError("Error Not Table", 10)

        terminal = self.__database.cursor()
        command = f"Select users.userName From Users Where users.userName = '{username}'"
        terminal.execute(command)
        result = terminal.fetchall()
        terminal.close()
        return True if result else False
