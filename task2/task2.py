import pyodbc
import csv


class ProductsManager:
    def __init__(self, server, database, username, password):
        # Connects to the server automatically
        self.connection = pyodbc.connect(f"""
                DRIVER=ODBC Driver 17 for SQL Server;
                SERVER={server};
                DATABASE={database};
                UID={username};
                PWD={password}""")
        self.cursor = self.connection.cursor()

    # OPTION 0
    # Should be the first option - creates a table from .csv file
    def create_table(self):
        # Creating the query and running it is the best way to do it
        query = """CREATE TABLE Movies (
                        titleType varchar(255),
                        primaryTitle varchar(255),
                        originalTitle varchar(255),
                        isAdult varchar(255),
                        startYear varchar(255),
                        endYear varchar(255),
                        runtimeMinutes varchar(255),
                        genres varchar(255))"""
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except:
            return print("Table exists!")

        # This will open the csv file and insert data one-by-one into the table
        with open("task2/imdbtitles.csv", newline='') as csvfile:
                rows = csv.reader(csvfile)
                # The first row contains only the column names so I skip it using iter and next
                next(iter(rows))
                # Iterates through all the rows
                for row in rows:
                    for num in range(8):
                        row[num] = f"'{row[num]}'"

                    q2 = ",".join(row)
                    query = f"""INSERT INTO Movies (titleType,
                                                    primaryTitle,
                                                    originalTitle,
                                                    isAdult,
                                                    startYear,
                                                    endYear,
                                                    runtimeMinutes,
                                                    genres)
                                VALUES ({q2})"""
                    # Some rows in the csv file cause a problem
                    # Need to find a way to fix this bit
                    try:
                        self.cursor.execute(query)
                        self.connection.commit()
                    except:
                        continue

    # OPTION 1
    # Shows all the data for the films
    def show_all_movies(self):
        try:
            x = self.cursor.execute("SELECT * FROM Movies")
            for _ in x:
                print(_)
        except:
            print("\nError! Are you sure there's a table called Movies?")

    # OPTION 2
    # Search data by film title
    def show_data_for_title(self):
        title = input("\nWhat title are you looking for? ").title().strip()
        query = f"SELECT * FROM Movies WHERE primaryTitle = {title}"
        try:
            y = self.cursor.execute(query).fetchone()
            print(y)
        except:
            return print("Something went wrong!")


    # OPTION 3
    # Choose movies and convert them into .csv
    def make_into_csv(self):
        name = input("\nWhat is the name of the .csv file? (please include .csv at the end) " )
        films = input("Please list the primaryTitle of each film you want to export separated by commas:\n")
        film_list = films.split(",")
        try:
            with open(f"task2/{name}", "w", newline="") as file:
                writer = csv.writer(file)
                for film in film_list:
                    y = self.cursor.execute(f"SELECT * FROM Movies WHERE primaryTitle = '{film.strip()}'").fetchone()
                    writer.writerow(y)
        except:
            print("\nSomething went wrong!")



    # OPTION 4
    # Uses another .csv file to add values in the table
    # This block of code is repeated from OPTION 0
    # A better way to write this would be to have a separate method to insert
    # values into a database and vice-versa
    def add_more_movies(self):
        csv_file = input("\nInput path to file:\n")
        with open(csv_file, newline='') as csvfile:
                rows = csv.reader(csvfile)
                # Iterates through all the rows
                for row in rows:
                    for num in range(8):
                        row[num] = f"'{row[num]}'"
                    q2 = ",".join(row)
                    query = f"""INSERT INTO Movies (titleType,
                                                    primaryTitle,
                                                    originalTitle,
                                                    isAdult,
                                                    startYear,
                                                    endYear,
                                                    runtimeMinutes,
                                                    genres)
                                VALUES ({q2})"""
                    # Some rows in a csv file cause a problem
                    # Need to find a way to fix this bit
                    try:
                        self.cursor.execute(query)
                        self.connection.commit()
                    except:
                        continue



    # OPTION 5
    # Query the DB
    def query_db(self):
        query = input("\nType your query:\n")
        try:
            y = self.cursor.execute(query)
            for row in y:
                print(row)
        except:
            return print("\nError! Try again")


    def choices(self):
        while True:
            # Shows options the user can do
            print("""
                    Options:
                    0. Convert the imdbtitles.csv file into a table in the Database
                    1. Show all movie data
                    2. Search movies by title and return data
                    3. Choose movies and convert their data into a .csv file
                    4. Add more movies using another .csv file
                    5. Query the database
                    6. EXIT
                    """)
            choose = input("--->  ")

            if not choose.isdigit():
                print("\nTry again")


            elif int(choose) == 1:
                self.show_all_movies()
            

            elif int(choose) == 2:
                self.show_data_for_title()
            

            elif int(choose) == 3:
                self.make_into_csv()
            

            elif int(choose) == 4:
                self.add_more_movies()


            elif int(choose) == 5:
                self.query_db()
        

            # Exits the loop
            elif int(choose) == 6:
                break
            

            elif int(choose) == 0:
                self.create_table()

            else:
                print("\nTry again")


if __name__ == "__main__":
    server = "JaredPC\JS_1"
    database = "TASK"
    username = "sa"
    password = "passw0rd"
    main = ProductsManager(server, database, username, password)
    main.choices()
