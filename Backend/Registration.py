#!C:/python/python3.9.1
print("Content-Type:text/html\n\n")
print()
import mysql.connector
import cgi

print("<h1>Hello Ajay</h1>")

form = cgi.FieldStorage()
firstName = form.getvalue('firstName')
secondName = form.getvalue('secondName')
phone = form.getvalue('phone')
email = form.getvalue('email')
password = form.getvalue('password')
vehicleno =form.getvalue('vehicleno')

conn=mysql.connector.connect(host='localhost',username='root',password='',database='vehicles')

my_cursor=conn.cursor()

my_cursor.execute("insert into drivers values(%s,%s,%s,%s,%s,%s)",(firstName,secondName,phone,email,password,vehicleno))


conn.commit()
conn.close()

print("Connection successfully created!")
