import pyodbc

class ProductsManager:
    def __init__(self, server, database, username, password):
        self.connection = self.make_connection(server, database, username, password)
        self.cursor = self.connection.cursor()
    
    # Creates a connection with the following inputs
    def make_connection(self, server, database, username, password):
        connection = pyodbc.connect(f"""
                DRIVER=ODBC Driver 17 for SQL Server;
                SERVER={server};
                DATABASE={database};
                UID={username};
                PWD={password}""")
        return connection