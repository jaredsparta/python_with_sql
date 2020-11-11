import pyodbc
from task import SQLInstance

server = "JaredPC\JS_1"
database = "TASK"
username = "sa"
password = "passw0rd"

class Products(SQLInstance):
    def __init__(self, server, database, username, password):
        super().__init__(server, database, username, password)


c = Products(server, database, username, password)
print(c.cursor)