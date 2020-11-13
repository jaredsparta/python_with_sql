# Task 2

**[2nd iteration](https://github.com/jaredsparta/python_with_sql/tree/master/task2.2)**

![](images/task2.png)

**Limitations**
- Sometimes, when the ```csv``` file is not properly encoded as utf-8 some weird characters are found, breaking the program. To overcome this, I had to hardcode the column titles.
- There was too much variation within ```.csv``` files to allow a more efficient way of creating tables to be done using my current knowledge. There could perhaps be a few python libraries I'm not aware of to fix this issue. Overall, with time allowed and my knowledge taken into consideration, this was the only way I saw how to achieve the acceptance criteria.

<br>

**Notes**
- I did test this code on a local SQL server instead of Sparta's AWS servers, due to potential connectivity issues. In that environment, this program did work as intended.
- **REMEMBER TO SWITCH THE SERVER, DATABASE, USERNAME AND PASSWORD IN THE ```if __name__ == '__main__':``` CODE BLOCK**
- The ```test.csv``` file was used to test ```Option 4``` in my code.

<br>

**Pre-requisites**
- One will need to install ```pyodbc``` using ```pip install pyodbc```.
- You will also need to import the following:
```python
    import pyodbc
    import csv
```

<br>

**Explanation**
- I create a class and put the server connection and cursor into the init method:
```python
    def __init__(self, server, database, username, password):
        # Connects to the server automatically
        self.connection = pyodbc.connect(f"""
                DRIVER=ODBC Driver 17 for SQL Server;
                SERVER={server};
                DATABASE={database};
                UID={username};
                PWD={password}""")
        self.cursor = self.connection.cursor()
```

<br>

- Option 0 will automatically export the ```.csv``` file into the Database. It will make a new table called ```Movies``` and import all the data into it.
- This part was hardcoded due to limitations explained above.
```python
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
```

<br>

- This will return all the data in the table
```python
    # OPTION 1
    # Shows all the data for the films
    def show_all_movies(self):
        try:
            x = self.cursor.execute("SELECT * FROM Movies")
            for _ in x:
                print(_)
        except:
            print("\nError! Are you sure there's a table called Movies?")

```

<br>

- This will allow the user to query the table purely from film title. This can be advantageous if they do not want to write the entire query themselves.
```python
    # OPTION 2
    # Search data by film title
    def show_data_for_title(self):
        title = input("\nWhat title are you looking for? ").title().strip()
        query = f"SELECT * FROM Movies WHERE primaryTitle = {title}"
        try:
            y = self.cursor.execute(query).fetchone()
            print(y)
        except:
            return print("Not found or something went wrong")
```

<br>

- This option will let the user convert rows they choose into a ```.csv``` file. I indicate which movies via their primaryTitle.
```python
    # OPTION 3
    # Choose movies and convert them into .csv
    def make_into_csv(self):
        name = input("\nChoose the name of the .csv file? (please include .csv at the end) " )
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
```

<br>

- If the user has another ```.csv``` file, they can also add this information into the table ```Movies``` using this method. This is taken from code in ```Option 0```.
```python
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
                    # This bit surrounds all values in a ''
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

```

<br>

- This will just let someone query the table. Note that this should only be used for ```SELECT``` statements.
```python
    # OPTION 5
    # Query the DB
    def query_db(self):
        print("\nThis accepts only SELECT statements")
        query = input("Type your query:\n")
        try:
            y = self.cursor.execute(query)
            for row in y:
                print(row)
        except:
            return print("\nError! Try again")
```

<br>

- The following defines which choices the user has. 
- The first ```if``` statement is meant to catch any errors associated with casting a string that isn't entirely composed of digits.

```python
    def choices(self):
        while True:
            # Shows options the user can do
            print("""
                    Options:
                    0. Convert the .csv file into a table in the Database
                    1. Show all movie data
                    2. Search movies by title and return data
                    3. Choose movies and convert their data into a .csv file
                    4. Query the database
                    5. EXIT
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
                self.query_db()
            

            # Exits the loop
            elif int(choose) == 5:
                break
            

            elif int(choose) == 0:
                self.create_table()

            else:
                print("\nTry again")

```

<br>

- Finally, I run the program. I tested this code on a local SQL server for ease and to eliminate connectivity issues. On that server, the code worked as intended.
```python
    if __name__ == "__main__":
    server = "JaredPC\JS_1"
    database = "TASK"
    username = "sa"
    password = "passw0rd"
    main = ProductsManager(server, database, username, password)
    main.choices()
```