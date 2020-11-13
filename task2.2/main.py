import pyodbc
import csv
from formatter import Formatter
from csv_functions import CSVFunctions


class SQLManager(Formatter):
    def __init__(self, server, database, username, password):
        # Connects to the server automatically
        self.connection = pyodbc.connect(f"""
                DRIVER=ODBC Driver 17 for SQL Server;
                SERVER={server};
                DATABASE={database};
                UID={username};
                PWD={password}""")
        self.cursor = self.connection.cursor()


    # A method that allows one to see all tables in the database
    def show_possible_tables(self):
        y = self.cursor.execute("SELECT * FROM information_schema.tables")
        table_list = []
        for _ in y:
            table_list.append(_[2])
        print(f"\nThe available tables are: {table_list}")


    # Returns a list of the column names of the table
    def make_column_names_of_table(self, table_name):
        query = f"""SELECT COLUMN_NAME
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = '{table_name}'
                    ORDER BY ORDINAL_POSITION"""
        row = self.cursor.execute(query)
        retr = []
        for _ in row:
            for val in _:
                retr.append(val)
        return retr


    # OPTION 1
    # CHECKED = YES
    def create_table(self):
        # Creating the query and running it is the best way to do it
        csv_file = input("\nInput path to .csv file:\n")

        # If the file path is incorrect then this will cause an error
        try:
            csv_file_headings = self.get_headings(csv_file)
        except:
            return print("Error, try again")

        # Show possible tables in case they try to add a table that already exists
        self.show_possible_tables()
        table_name = input("\nWhat should the table be called?\n")

        # This will format all the headings by removing non-alphanumeric characters
        column_names = self.remove_weird_characters_from_list(csv_file_headings)
        column_names_with_datatype = list(map(lambda x: x + " varchar(255)", column_names))
        col_names_for_query = ",".join(column_names_with_datatype)
        query = f"CREATE TABLE {table_name} ({col_names_for_query})"

        # In case there are errors in the query (i.e. the table might exist already)
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except:
            return print("\nTable exists!")


        col_in_query = ",".join(column_names)
        with open(csv_file, newline='') as data:
            reader = csv.reader(data)
            next(iter(reader))
            for row in reader:
                retr = list(map(self.format_for_insertion, row))
                retr = ",".join(retr)
                query = f"INSERT INTO {table_name} ({col_in_query}) VALUES ({retr})"
                
                try:
                    self.cursor.execute(query)
                    self.connection.commit()
                except:
                    continue

        print("\nTable created!")


    # OPTION 2
    # CHECKED = YES
    # Adds values from a .csv file into a table
    def csv_to_table(self):
        self.show_possible_tables()
        table_name = input("\nInput table name:\n")
        csv_file = input("\nInput path to .csv file:\n")

        col_names = self.make_column_names_of_table(table_name)
        col_names_as_string = ", ".join(col_names)
        
        with open(csv_file, newline='') as data:
            reader = csv.reader(data)
            for row in reader:
                retr = list(map(self.format_for_insertion, row))
                retr = ",".join(retr)
                query = f"INSERT INTO {table_name} ({col_names_as_string}) VALUES ({retr})"
                
                try:
                    self.cursor.execute(query)
                    self.connection.commit()
                except:
                    continue


    # OPTION 3
    # CHECKED = YES
    # Get values from a table and put it into a .csv file
    def table_to_csv(self):
        self.show_possible_tables()
        table_name = input("\nInput table name:\n")

        print("")
        print(self.make_column_names_of_table(table_name))
        column_name_to_identify = input("\nWhich column to grab the data?\n")

        values = input(f"\nFrom {column_name_to_identify} type the rows to grab: (separate by commas)\n")

        retr_list = values.split(",")

        csv_name = input("\nName the new .csvfile: (end it with a .csv)\n")

        try:
            with open(csv_name, "w", newline="") as file:
                writer = csv.writer(file)
                for val in retr_list:
                    y = self.cursor.execute(f"SELECT * FROM {table_name} WHERE {column_name_to_identify} = '{val.strip()}'").fetchone()
                    writer.writerow(y)
        except:
            print("\nSomething went wrong!")


    # OPTION 4
    # CHECKED = YES
    # Query the DB
    def query_db(self):
        self.show_possible_tables()
        print("\nThis accepts only SELECT statements")
        query = input("Type your query:\n")
        try:
            y = self.cursor.execute(query)
            for row in y:
                print(row)
        except:
            return print("\nError! Try again")

    # Defines the choices
    def choices(self):
        while True:
            # Shows options the user can do
            print("""
                    Options:
                    1. Convert a .csv file into a table in the database
                    2. Add values from a .csv file into a table
                    3. Add values from a table into a .csv file
                    4. Query the database
                    5. EXIT
                    """)
            choose = input("--->  ").strip()

            if choose == "1":
                self.create_table()

            elif choose == "2":
                self.csv_to_table() 
            
            elif choose == "3":
                self.table_to_csv()
            
            elif choose == "4":
                self.query_db()   

            elif choose == "5":
                break

            else:
                print("\nTry again")


if __name__ == "__main__":
    server = "JaredPC\JS_1"
    database = "TASK"
    username = "sa"
    password = "passw0rd"
    main = SQLManager(server, database, username, password)
    main.choices()
