#!C:/python/python3.9.1
print("Content-Type:text/html\n\n")
print()
import mysql.connector
import cgi

print("<h1>Hello Ajay</h1>")

form = cgi.FieldStorage()
username = form.getvalue('username')
password = form.getvalue('password')

conn=mysql.connector.connect(host='localhost',username='root',password='',database='vehicles')

my_cursor=conn.cursor()

my_cursor.execute("insert into drivers values(%s,%s)",(username,password))


conn.commit()
conn.close()

print("Connection successfully created!")
