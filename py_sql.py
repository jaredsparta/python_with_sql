# This will create a connection to our SQL DB from Python using PYODBC
import pyodbc

# Allows us to connect to an SQL instance
# We will connect to our Northwind DB

server = "databases1.spartaglobal.academy"
database = "Northwind"
username = "SA"
password = "Passw0rd2018"

connection = pyodbc.connect(
    f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}"
)

# A cursor is the location of one's mouse/current path
cursor = connection.cursor()

# In Northwind, there is a Customers table
# Using .fetchall() allows one to retrieve all the data inside that table
# .fetchall() is called by default so you don't need to do it

#cust_row = cursor.execute("SELECT * FROM Customers").fetchall()
#for records in cust_row:
#    print(records)

# Let's query another table called Products
prod_row = cursor.execute("SELECT TOP 10 * FROM JS_table").fetchone()
print(prod_row)

#query = "SELECT CustomerID FROM Customers WHERE City = ?"
#with cursor.execute(query, "London"):
#    row = cursor.fetchone()
#    while row:
#        print(f"{str(row[0])}")
#        row = cursor.fetchone()
