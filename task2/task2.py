import pyodbc
import csv

# 

class ProductsManager:
    def __init__(self, server, database, username, password):
        self.connection = pyodbc.connect(f"""
                DRIVER=ODBC Driver 17 for SQL Server;
                SERVER={server};
                DATABASE={database};
                UID={username};
                PWD={password}""")
        self.cursor = self.connection.cursor()

    # OPTION 0
    # Should be the first option - creates a table from .csv file
    def create_table_from_csv(self):
        csv_file = input("\nGive the relative path to the .csv file: ")
        table_name = input("What should the table be called? ")
        col_names = []
        with open(csv_file, newline='') as csvfile:
            rows = csv.reader(csvfile)
            for r in rows:
                col_names = r
                break

        query_2 = ""
        for name in col_names:
            query_2 += name + " varchar(255),"
        print(query_2)
        query_2 = query_2[12:len(query_2)-1]     
        
        query = ascii(f"CREATE TABLE {table_name} ({query_2}) ")
        print(query)
        #try:
        #    self.cursor.execute(query)
        #    self.commit()
        #except:
        #    return print("Something went wrong!")
        #
        #print("\nTable created!")
        #input("Press <ENTER> to put all values in the table")
        #col_names2 = ",".join(col_names)
        #with open(csv_file, newline='', fileEncoding="UTF-8-BOM") as csvfile:
        #    rows = csv.reader(csvfile)
        #    next(iter(rows))
        #    for row in rows:
        #        q2 = ",".join(row)
        #        q = f"INSERT INTO {table_name} ({col_names2}) VALUES ({q2})"
        #        self.cursor.execute(q)
        #        self.commit()


    # OPTION 1
    # Shows all the data for the films
    def show_all_movies(self):
        pass

    # OPTION 2
    # Search data by film title
    def show_data_for_title(self):
        title = input("\nWhat title are you looking for? ")
        query = f"SELECT * FROM Movies WHERE primaryTitle = {title}"
        try:
            self.cursor.execute(query)
        except:
            return print("Something went wrong!")

    def choices(self):
        while True:
            # Shows options the user can do
            print("""
                    Options:
                    0. Convert the .csv file into a table in the Database
                    1. Show all movie data
                    2. Search movies by title and return data
                    3. Choose movies and convert their data into a .txt file
                    4. Retrieve data from the database and convert it into a .txt file
                    5. Query the database
                    6. EXIT
                    """)
            choose = input("--->  ")

            if not choose.isdigit():
                print("\nTry again")


            elif int(choose) == 1:
                pass
            

            elif int(choose) == 2:
                pass
            

            elif int(choose) == 3:
                pass
            

            elif int(choose) == 4:
                pass
            

            elif int(choose) == 5:
                pass
            

            # Exits the loop
            elif int(choose) == 6:
                break
            

            elif int(choose) == 0:
                self.create_table_from_csv()

            else:
                print("\nTry again")

if __name__ == "__main__":
    server = "JaredPC\JS_1"
    database = "TASK"
    username = "sa"
    password = "passw0rd"
    main = ProductsManager(server, database, username, password)
    main.choices()