import mysql.connector

class DBCommunicateError (Exception):
    # Error Unknow - 0
    # Error Database connection - 1/9
    # Error Content - 10/19
    # Error Users - 20/29
    # Error Mood - 30/39
    # Error UsersTaste - 40/49
    # Error Playlist - 50/59
    # Error UserAuthorization - 60/69
    # Error ContentRelation - 70/79
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

    def assign_Mood_To_Content(self, userID:int, contentID:int, moodName:str):
        try:
            if not self.__is_User(userID=userID):
                raise DBCommunicateError("Error User Not Exist", 21)
            if not self.__is_Content(contentID):
                raise DBCommunicateError("Error Content Not Exist", 11)
            if moodName not in self.get_MoodName():
                raise DBCommunicateError(f"Error Mood {moodName} Not Exist", 31)
        except DBCommunicateError as e:
            raise e

        terminal = self.__database.cursor()
        command = f"""  SELECT COUNT(*) FROM UsersTaste 
                        WHERE UsersTaste.userID = {userID} AND UsersTaste.contentID = {contentID}"""
        
        terminal.execute(command)
        result = terminal.fetchone()
        terminal.close()

        if result[0] == 0:
            terminal = self.__database.cursor()
            command = f"""  INSERT INTO UsersTaste (userID, contentID, moodName)
                            VALUES ({userID}, {contentID}, '{moodName}')"""
            terminal.execute(command)
            self.__commit()
            terminal.close()

    def update_Mood_For_Content(self, userID:int, contentID:int, newMoodName:str):
        try:
            if not self.__is_User(userID=userID):
                raise DBCommunicateError("Error User Not Exist", 21)
            if not self.__is_Content(contentID):
                raise DBCommunicateError("Error Content Not Exist", 11)
            if newMoodName not in self.get_MoodName():
                raise DBCommunicateError(f"Error Mood {newMoodName} Not Exist", 31)
        except DBCommunicateError as e:
            raise e

        terminal = self.__database.cursor()
        command = f"""  UPDATE UsersTaste
                        SET UsersTaste.moodName = '{newMoodName}'
                        WHERE UsersTaste.userID = {userID} AND UsersTaste.contentID = {contentID}"""
        terminal.execute(command)
        self.__commit()
        terminal.close()

    def add_Playlist(self, userID:int, playlistName:str):
        try:
            if self.__is_Playlist(playlistName):
                raise DBCommunicateError("Error Playlist Already Exist", 51)
            elif not self.__is_Table("UsersAuthorization"):
                raise DBCommunicateError("Error Not Table", 60)
            elif not self.__is_User(userID=userID):
                raise DBCommunicateError("Error User NOT Exist", 21)
        except DBCommunicateError as e:
            raise e
        
        terminal = self.__database.cursor()
        command = f"INSERT INTO Playlist (playlistName) VALUE ('{playlistName}')"
        terminal.execute(command)
        try:
            playlistID = self.get_PlaylistID(playlistName)
            command = f"INSERT INTO UsersAuthorization (userID, playlistID, authorization) VALUE ({userID}, {playlistID}, 1)"
            terminal.execute(command)
            self.__commit()
            terminal.close()
        except DBCommunicateError as e:
            self.remove_Playlist(playlistName)
            self.__commit()
            terminal.close()
            raise DBCommunicateError("Error Cannot Add Playlist : " + e.message, 53)
    
    def add_Playlist_Content(self, userID:int, playlistName:str, contentID:int):
        try:
            if not self.__is_User(userID=userID):
                raise DBCommunicateError("Error User Not Exist", 21)
            elif self.__is_Content_Playlist(playlistName, contentID):
                raise DBCommunicateError("Error Content Already In Playlist", 53)
            elif not self.__is_Authorize(userID, playlistName):
                return False
            playlistID = self.get_PlaylistID(playlistName)
        except DBCommunicateError as e:
            raise e
        
        terminal = self.__database.cursor()
        command = f"INSERT INTO ContentRelation (contentID, playlistID) VALUE ({contentID}, {playlistID})"
        terminal.execute(command)
        self.__commit()
        terminal.close()
    
    def remove_Playlist(self, userID:int, playlistName:str):
        try:
            if not self.__is_Playlist(playlistName):
                raise DBCommunicateError("Error Playlist Not Exist", 52)
            elif not self.__is_Authorize(userID, playlistName):
                return False
        except DBCommunicateError as e:
            raise e
        
        terminal = self.__database.cursor()
        try:
            self.remove_Playlist_All(userID, playlistName)
            playlistID = self.get_PlaylistID(playlistName)
            command = f"DELETE FROM UsersAuthorization WHERE UsersAuthorization.playlistID = {playlistID}"
            terminal.execute(command)
            command = f"DELETE FROM Playlist WHERE Playlist.playlistName = '{playlistName}'"
            terminal.execute(command)
            self.__commit()
            terminal.close()
        except DBCommunicateError as e:
            terminal.close()
            raise e
    
    def remove_Playlist_Content(self, userID:int, playlistName:str, contentID:int):
        try:
            if not self.__is_User(userID=userID):
                raise DBCommunicateError("Error User Not Exist", 21)
            elif not self.__is_Content_Playlist(playlistName, contentID):
                raise DBCommunicateError("Error Content Not In Playlist", 53)
            elif not self.__is_Authorize(userID, playlistName):
                return False
            playlistID = self.get_PlaylistID(playlistName)
        except DBCommunicateError as e:
            raise e
        
        terminal = self.__database.cursor()
        command = f"DELETE FROM ContentRelation WHERE ContentRelation.playlistID = {playlistID} and ContentRelation.contentID = {contentID}"
        terminal.execute(command)
        self.__commit()
        terminal.close()

    def remove_Playlist_All(self, userID:int, playlistName:str):
        try:
            if not self.__is_Table("ContentRelation"):
                raise DBCommunicateError("Error Not Table", 10)
            elif not self.__is_User(userID=userID):
                raise DBCommunicateError("Error User Not Exist", 21)
            elif not self.__is_Playlist(playlistName):
                raise DBCommunicateError("Error Playlist Not Exist", 51)
            elif not self.__is_Authorize(userID, playlistName):
                return False
            playlistID = self.get_PlaylistID(playlistName)
        except DBCommunicateError as e:
            raise e
        
        terminal = self.__database.cursor()
        command = f"DELETE FROM ContentRelation WHERE ContentRelation.playlistID = {playlistID}"
        terminal.execute(command)
        self.__commit()
        terminal.close()

    def add_Authorization(self, userID:int, new_userID:int, playlistName:str):
        try:
            if not self.__is_Playlist(playlistName):
                raise DBCommunicateError("Error Playlist Not Exist", 52)
            elif not self.__is_User(userID=userID):
                raise DBCommunicateError("Error User Not Exist", 21)
            elif self.__is_Authorize(new_userID, playlistName):
                raise DBCommunicateError("Error User Already Authorized", 62)
            elif not self.__is_Authorize(userID, playlistName):
                raise DBCommunicateError("Error User Cant Modifed Authorization", 64)
            playlistID = self.get_PlaylistID(playlistName)

            terminal = self.__database.cursor()
            command = f"INSERT INTO UsersAuthorization (userID, playlistID, authorization) VALUES ({new_userID}, {playlistID}, 1)"
            terminal.execute(command)
            self.__commit()
            terminal.close()
        except DBCommunicateError as e:
            raise e

    def remove_Authorization(self, userID:int, remove_userID:int, playlistName:str):
        try:
            if not self.__is_Playlist(playlistName):
                raise DBCommunicateError("Error Playlist Not Exist", 52)
            elif not self.__is_User(userID=userID):
                raise DBCommunicateError("Error User Not Exist", 21)
            elif not self.__is_Authorize(remove_userID, playlistName):
                raise DBCommunicateError("Error User Not Authorized", 61)
            elif not self.__is_Authorize(userID, playlistName):
                raise DBCommunicateError("Error User Cant Modifed Authorization", 64)
            
            playlistID = self.get_PlaylistID(playlistName)
            
            terminal = self.__database.cursor()
            command = f"DELETE FROM UsersAuthorization WHERE userID = {userID} AND playlistID = {playlistID}"
            terminal.execute(command)
            self.__commit()
            terminal.close()

            command = f"SELECT COUNT(*) FROM UsersAuthorization WHERE playlistID = {playlistID}"
            terminal.execute(command)
            count = terminal.fetchone()[0]
            terminal.close()
            
            if count == 0:
                self.remove_Playlist(userID, playlistName)

        except DBCommunicateError as e:
            raise e

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

    def get_UserID(self, userName:str) -> int:
        try:
            if not self.__is_User(username=userName):
                raise DBCommunicateError("Error User Not Exist", 21)
        except DBCommunicateError as e:
            raise e
        
        terminal = self.__database.cursor()
        command = f"SELECT UsersID.userName FROM UsersID WHERE Users.userName = {userName}"
        terminal.execute(command)
        result = terminal.fetchall()
        terminal.close()
        return result
        
    def get_PlaylistID(self, playlistName:str) -> int:
        try:
            if not self.__is_Playlist(playlistName):
                raise DBCommunicateError("Error Playlist Not Exist", 52)
        except DBCommunicateError as e:
            raise e
        
        terminal = self.__database.cursor()
        command = f"SELECT Playlist.playlistID FROM Playlist WHERE Playlist.playlistName = '{playlistName}'"
        terminal.execute(command)
        result = terminal.fetchall()
        terminal.close()
        return result[0][0]

    def show_Table(self):
        if not self.__database:
            raise DBCommunicateError("Error Not Connected to Database", 3)
        
        terminal = self.__database.cursor()
        terminal.execute("show tables")
        print(terminal.fetchall())
        terminal.close()

    def show_Content(self, title:str = None, author:str = None, isMusic:bool = None) -> list:
        if not self.__database:
            raise DBCommunicateError("Error Not Connected to Database", 3)
        elif not self.__is_Table("Content"):
            raise DBCommunicateError("Error Not Table", 10)
        
        terminal = self.__database.cursor()
        command = "SELECT Content.title, Content.author, Content.isMusic, Content.moodName FROM Content"
        if title or author or isMusic != None:
            command += " WHERE "
        if title:
            command += f"Content.title LIKE ('%{title}%')"
        if author:
            if title:
                command += " and "
            command += f"Content.author LIKE ('%{author}%')"
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
        
    def show_Content_Mood(self, userID:int, moodName:str = None) -> list:
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
            command = f"""  SELECT g.title, g.author, g.isMusic, coalesce(ut.moodName, g.moodName) as moodName
                            FROM global_taste g
                            LEFT OUTER JOIN(
                            SELECT ut.contentID, ut.moodName
                            FROM userstaste ut
                            WHERE ut.contentID = 1) ut
                            ON ut.contentID = g.contentID"""
        else:
            command = f"""  SELECT g.title, g.author, g.isMusic, coalesce(ut.moodName, g.moodName) as moodName
                            FROM global_taste g
                            LEFT OUTER JOIN(
                            SELECT ut.contentID, ut.moodName
                            FROM userstaste ut
                            WHERE ut.contentID = 1) ut
                            ON ut.contentID = g.contentID
                            WHERE coalesce(ut.moodName, g.moodName) = {moodName}"""
        
        terminal.execute(command)
        result = terminal.fetchall()
        terminal.close()
        return result

    def show_Playlist(self, userID:int) -> list:
        try:
            if not self.__is_Table("Playlist"):
                raise DBCommunicateError("Error Not Table", 50)
            elif not self.__is_User(userID=userID):
                raise DBCommunicateError("Error User Not Exist", 21)
        except DBCommunicateError as e:
            raise e
        
        terminal = self.__database.cursor()
        command = f"""  SELECT p.playlistName
                        FROM Playlist p
                        INNER JOIN
                        (SELECT ua.playlistID
                        FROM UsersAuthorization ua
                        WHERE ua.userID = {userID}) ua
                        on p.playlistID = ua.playlistID;"""
        terminal.execute(command)
        result = terminal.fetchall()
        terminal.close()
        return result

    def show_Playlist_Content(self, userID:int, playlistName:str) -> list:
        try:
            if not self.__is_Table("Content"):
                raise DBCommunicateError("Error Not Table", 10)
            elif not self.__is_Table("ContentRelation"):
                raise DBCommunicateError("Error Not Table", 70)
            elif not self.__is_Authorize(userID, playlistName):
                return False
            playlistID = self.get_PlaylistID(playlistName)
        except DBCommunicateError as e:
            if e.code == 52:
                return []
            raise e
        
        terminal = self.__database.cursor()
        command = f"""  SELECT c.title, c.title, c.isMusic
                        FROM content c
                        INNER JOIN (
                        SELECT cr.contentID
                        FROM contentrelation cr
                        WHERE cr.playlistID = {playlistID}) cr on c.contentID = cr.contentID"""
        terminal.execute(command)
        result = terminal.fetchall()
        terminal.close()
        return result

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
        try:
            if not self.__is_Table("Users"):
                raise DBCommunicateError("Error Not Table", 20)
        except DBCommunicateError as e:
            raise e

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

    def __is_Content(self, contentID:int) -> bool:
        try:
            if not self.__is_Table("UsersAuthorization"):
                raise DBCommunicateError("Error Not Table", 60)
        except DBCommunicateError as e:
            raise e
        
        terminal = self.__database.cursor()
        command = f"SELECT Content.contentID FROM Content WHERE Content.contentID = {contentID}"
        terminal.execute(command)
        result = terminal.fetchall()
        terminal.close()
        return True if result else False

    def __is_Content_Playlist(self, playlistName:str, contentID:int):
        try:
            if not self.__is_Table("ContentRelation"):
                raise DBCommunicateError("Error Not Table", 70)
            elif not self.__is_Playlist(playlistName):
                raise DBCommunicateError("Error Playlist Not Exist", 52)
            elif not self.__is_Content(contentID):
                raise DBCommunicateError("Error Content Not Exist", 11)
            playlistID = self.get_PlaylistID(playlistName)
        except DBCommunicateError as e:
            raise e
        
        terminal = self.__database.cursor()
        command = f"SELECT ContentRelation.ContentID FROM ContentRelation WHERE ContentRelation.playlistID = {playlistID} and ContentRelation.contentID = {contentID}"
        terminal.execute(command)
        result = terminal.fetchall()
        terminal.close()
        return True if result else False

    def __is_Playlist(self, PlaylistName:str) -> bool:
        try:
            if not self.__is_Table("Playlist"):
                raise DBCommunicateError("Error Not Table", 50)
        except DBCommunicateError as e:
            raise e

        terminal = self.__database.cursor()
        command = f"SELECT Playlist.playlistName FROM Playlist WHERE Playlist.playlistName = '{PlaylistName}'"
        terminal.execute(command)
        result = terminal.fetchall()
        terminal.close()
        return True if result else False

    def __is_Authorize(self, userID:int, playlistName:int):
        try:
            if not self.__is_Table("UsersAuthorization"):
                raise DBCommunicateError("Error Not Table", 60)
            elif not self.__is_User(userID=userID):
                raise DBCommunicateError("Error User Not Exist", 21)
            elif not self.__is_Playlist(playlistName):
                raise DBCommunicateError("Error Content Not Exist", 11)
            playlistID = self.get_PlaylistID(playlistName)
        except DBCommunicateError as e:
            raise e

        terminal = self.__database.cursor()
        command = f"SELECT UsersAuthorization.authorization FROM UsersAuthorization WHERE UsersAuthorization.userID = {userID} and UsersAuthorization.playlistID = {playlistID}"
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

# db = DBCommunicate("root", "!Cd2@5Cprb")
# print(db.show_Content())