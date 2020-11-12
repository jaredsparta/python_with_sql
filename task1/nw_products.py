import pyodbc
from task import SQLInstance

server = "JaredPC\JS_1"
database = "Northwind"
username = "sa"
password = "passw0rd"

# This class will inherit from the SQLInstance class
# This allows us to re-use the code to connect to the server automatically
class Products(SQLInstance):
    def __init__(self, server, database, username, password):
        super().__init__(server, database, username, password)

    # Returns the average UnitPrice
    def print_average(self):
        query = "SELECT AVG(UnitPrice) FROM Products"
        avg = self.cursor.execute(query).fetchone()
        print(f"\nThe average UnitPrice is {avg[0]}")


    # Shows the column names in the Products DB
    def show_col(self):
        super().show_col_names("Products")


# Runs if executing file and not importing it
if __name__ == "__main__":
    c = Products(server, database, username, password)
    c.print_average()
