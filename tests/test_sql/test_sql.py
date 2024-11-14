import mysql.connector

password = input()

mydb = mysql.connector.connect(host="localhost", user="root", passwd=password)

mycursor = mydb.cursor()

mycursor.execute("show databases")

for i in mycursor:
    print(i)