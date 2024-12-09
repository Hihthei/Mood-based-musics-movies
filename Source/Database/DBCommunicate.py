import mysql.connector

class DBCommunicateError (Exception):
    # Error Unknow - 0
    # Error Database connection - 1/9
    # Error Content - 10/19
    # Error Users - 20/29
    # Error Mood - 30/39
    # Error UsersTaste - 40/49
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
            raise DBCommunicateError("Error Not Table", 20)
        
        terminal = self.__database.cursor()
        command = f"SELECT Users.userID, Users.hashpassword FROM Users WHERE Users.userName = '{username}'"
        terminal.execute(command)
        result = terminal.fetchall()
        terminal.close()
        if not result:
            raise DBCommunicateError("Error User Not Exist", 21)
        return result[0]

    def add_User(self, username:str, hashPassword:str):
        if not self.__database:
            raise DBCommunicateError("Error Not Connected to Database", 3)
        elif not self.__is_Table("Users"):
            raise DBCommunicateError("Error Not Table", 20)
        try:
            if self.__is_User(username=username):
                raise DBCommunicateError("Error User Exist", 22)
        except DBCommunicateError as e:
            raise e
        
        terminal = self.__database.cursor()
        command = f"INSERT INTO Users (userName, hashPassword) VALUES ('{username}', '{hashPassword}')"
        terminal.execute(command)
        terminal.close()
        self.__commit()

    def change_UserMood(self, userID:int, moodName:str):
        if not self.__database:
            raise DBCommunicateError("Error Not Connected to Database", 3)
        try:
            if not self.__is_User(userID=userID):
                raise DBCommunicateError("Error User Not Exist", 21)
        except DBCommunicateError as e:
            raise e

        try:
            moodName_list = self.get_MoodName()
            if moodName not in moodName_list:
                raise DBCommunicateError("Error Not in Mood", 31)
        except DBCommunicateError as e:
            raise e
        
        terminal = self.__database.cursor()
        command = f"UPDATE Users SET Users.moodName = '{moodName}' WHERE Users.userID = {userID}"
        terminal.execute(command)
        terminal.close()
        self.__commit()

    def remove_User(self, username:str):
        if not self.__database:
            raise DBCommunicateError("Error Not Connected to Database", 3)
        elif not self.__is_Table("Users"):
            raise DBCommunicateError("Error Not Table", 20)
        try:
            if not self.__is_User(username=username):
                raise DBCommunicateError("Error User Not Exist", 21)
        except DBCommunicateError as e:
            raise e
        
        terminal = self.__database.cursor()
        command = f"DELETE FROM Users WHERE Users.userName = '{username}'"
        terminal.execute(command)
        terminal.close()
        self.__commit()

    def get_MoodName(self) -> list:
        if not self.__database:
            raise DBCommunicateError("Error Not Connected to Database", 3)
        elif not self.__is_Table("Mood"):
            raise DBCommunicateError("Error Not Table", 30)
        
        terminal =  self.__database.cursor()
        terminal.execute("SELECT * FROM Mood")
        result = terminal.fetchall()
        terminal.close()
        return list(i[0] for i in result)

    def show_Table(self):
        if not self.__database:
            raise DBCommunicateError("Error Not Connected to Database", 3)
        
        terminal = self.__database.cursor()
        terminal.execute("show tables")
        print(terminal.fetchall())
        terminal.close()

    def show_Content(self, title:list = None, author:list = None, isMusic:bool = None):
        if not self.__database:
            raise DBCommunicateError("Error Not Connected to Database", 3)
        elif not self.__is_Table("Content"):
            raise DBCommunicateError("Error Not Table", 10)
        
        terminal = self.__database.cursor()
        command = "SELECT Content.title, Content.author, Content.isMusic FROM Content"
        if title or author or isMusic != None:
            command += " WHERE "
        if title:
            command += "Content.title in ("
            first = True
            for i in title:
                if first:
                    command += f"'{i}'"
                    first = False
                else:
                    command += f", '{i}'"
            command += ")"
        if author:
            if title:
                command += " and "
            command += "Content.author in ("
            first = True
            for i in author:
                if first:
                    command += f"'{i}'"
                    first = False
                else:
                    command += f", '{i}'"
            command += ")"
            if isMusic != None:
                command += " and "
        if isMusic != None:
            command += f"Content.isMusic = {1 if isMusic else 0}"

        try:
            terminal.execute(command)
            result = terminal.fetchall()
            terminal.close()
            return result
        except:
            terminal.close()
            raise DBCommunicateError("Error Unknow", 0)
        

    def show_Content_Mood(self, userID:int, moodName:str = None):
        if not self.__database:
            raise DBCommunicateError("Error Not Connected to Database", 3)
        elif not self.__is_Table("UsersTaste"):
            raise DBCommunicateError("Error Not Table", 40)
        elif not self.__is_Table("Mood"):
            raise DBCommunicateError("Error Not Table", 30)
        try:
            if not self.__is_User(userID=userID):
                raise DBCommunicateError("Error User Not Exist", 21)
        except DBCommunicateError as e:
            raise e
        
        terminal = self.__database.cursor()
        if not moodName:
            command = f"""  SELECT c.title, COALESCE(mf.moodName, um.moodName) AS moodName, c.isMusic
                            FROM content c
                            JOIN (
                                SELECT um.contentID, um.moodName, 
                                    RANK() OVER (PARTITION BY um.contentID ORDER BY COUNT(*) DESC) AS rang
                                FROM userstaste um
                                GROUP BY um.contentID, um.moodName
                                ORDER BY COUNT(*) DESC
                            ) um ON c.contentID = um.contentID
                            LEFT JOIN (
                                SELECT mf.contentID, mf.moodName
                                FROM userstaste mf
                                WHERE mf.userID = {userID}
                            ) mf ON c.contentID = mf.contentID
                            WHERE um.rang = 1"""
        else:
            command = f"""  SELECT c.title, COALESCE(mf.moodName, um.moodName) AS moodName, c.isMusic
                            FROM content c
                            JOIN (
                                SELECT um.contentID, um.moodName, 
                                    RANK() OVER (PARTITION BY um.contentID ORDER BY COUNT(*) DESC) AS rang
                                FROM userstaste um
                                GROUP BY um.contentID, um.moodName
                                ORDER BY COUNT(*) DESC
                            ) um ON c.contentID = um.contentID
                            LEFT JOIN (
                                SELECT mf.contentID, mf.moodName
                                FROM userstaste mf
                                WHERE mf.userID = {userID}
                            ) mf ON c.contentID = mf.contentID
                            WHERE COALESCE(mf.moodName, um.moodName) = '{moodName}' AND um.rang = 1"""
        
        terminal.execute(command)
        result = terminal.fetchall()
        terminal.close()
        return result

    def show_Users(self):
        if not self.__database:
            raise DBCommunicateError("Error Not Connected to Database", 3)
        elif not self.__is_Table("Users"):
            raise DBCommunicateError("Error Not Table", 20)

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
            if i[0] == Name:
                terminal.close()
                return True
        terminal.close()
        return False

    def __is_User(self, username:str = None, userID:int = None) -> bool:
        if not self.__database:
            raise DBCommunicateError("Error Not Connected to Database", 3)
        elif not self.__is_Table("Users"):
            raise DBCommunicateError("Error Not Table", 20)

        if not username and not userID:
            raise DBCommunicateError("Error Not Available userName or userID", 23)

        terminal = self.__database.cursor()
        command = "SELECT users.userName FROM Users WHERE "

        if username:
            command += f"Users.userName = '{username}'"
            if userID:
                command += f" or Users.userID = {userID}"
        else:
            command += f"Users.userID = {userID}"

        terminal.execute(command)
        result = terminal.fetchall()
        terminal.close()
        return True if result else False

    def __commit(self):
        try:
            self.__database.commit()
        except mysql.connector.Error as e:
            self.__database.rollback()
            raise DBCommunicateError("Error Commit Failed", 100)

try:
    dbCommunicate = DBCommunicate("root", "!Cd2@5Cprb")
    print(dbCommunicate.show_Content_Mood(3, 'happy'))
except DBCommunicateError as e:
    print(e)