import mysql.connector
import mysql.connector.cursor


def sql_show_databases(password:str):
    try:
        mydb = mysql.connector.connect(host="localhost", user="root", passwd=password)
        mycursor = mydb.cursor()
        mycursor.execute("show databases")
    except:
        mycursor = None

    return mycursor