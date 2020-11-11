import pyodbc

jserver = "databases1.spartaglobal.academy"
jdatabase = "Northwind"
jusername = "SA"
jpassword = "Passw0rd2018"

class SQLAutoConnection:
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


    # Creates a query using .execute()
    def make_table(self):
        table_name = input("\nWhat should the table be called?\n--> ")
        while True:
            try:
                number_of_col = int(input("\nHow many columns?\n--> "))
                break
            except:
                continue
        
        query_string = ""
        length = len(query_string)
                
        for _ in range(number_of_col):
            col_name = input(f"\nInput name of column {_ + 1}: ")
            col_datatype = input(f"Input the datatype of this column: ")
            query_string = query_string + col_name + " " + col_datatype + ","

        query_string = query_string[:length-1]

        self.cursor.execute(f"CREATE TABLE {table_name} ({query_string});")
        self.connection.commit()


    # Allows one to insert data into a table
    def insert_into(self):
        query = input("Input in a valid format your insert statement:\n")
        self.cursor.execute(query)
        self.connection.commit()


    def query_db(self):
        query_str = input("Insert your  query:\n")
        try:
            self.cursor.execute(query_str)
        except:
            print("\nError!")


    def choices(self):
        while True:
            print("""\nOptions:
                        1. Make table
                        2. Insert values into a table
                        3. Query
                        4. Exit""")
            choice = input("---> ").strip()

            if int(choice) == 1:
                self.make_table()
                print("\nTable created!")

            if int(choice) == 2:
                self.insert_into()
                print("\nYou've inserted data!")

            if int(choice) == 3:
                pass

            if int(choice) == 4:
                break
            

if __name__ == "__main__":
    c = SQLAutoConnection(jserver, jdatabase, jusername, jpassword)
    row = c.cursor.execute("SELECT * FROM JS_table")
    print(row)