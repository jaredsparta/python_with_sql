# 2nd Iteration of Task 2

**Notes**
- The first iteration can be found [here](https://github.com/jaredsparta/python_with_sql/tree/master/task2)
- This one builds upon the first one and is more generalised.
- It can create a table from any ```.csv``` file, read data from a ```.csv``` file and write to a corresponding table etc.
- The ```test.csv``` file was used to test option 2
- **CHANGE THE SERVER, DB, USERNAME, PASSWORD** found in the file for you to use
- **Try to keep ```.csv``` files in the same directory as the ```main.py``` file and keep track of where your running the python interpreter from**

<br>

**Limitations**
- All datatypes when creating a table are defaulted to ```varchar(255)```. We can possibly fix this in the next iteration by checking for boolean values, integers, floats etc.
- The program assumes the ```.csv``` file's first row consists of the column names. We could possibly input an ```if``` condition to ask them how the ```.csv``` files are ordered -- this is easy to implement.

<br>

**Explanation**
- This iteration makes use of a separate class I wrote in another file (for clarity) called ```formatter.py```
- This class contains some methods that allow me to bypass the limitations stated in the first iteration.
- Should work for the vast majority of cases.
```python
    class Formatter:
    def __init__(self):
        pass

    # Removes all non-alphanumeric characters in a string
    def remove_weird_characters(self, str_arg):
        temp_list = list(str_arg)
        for num in range(len(temp_list)):
            if not temp_list[num].isalnum():
                temp_list[num] = ""
        return_string = "".join(temp_list)
        return return_string


    # Removes all non-alphanumeric characters from a list of strings
    # This makes use oif the above function and applies it to all values
    def remove_weird_characters_from_list(self, list_of_strings):
        retr = list(map(self.remove_weird_characters, list_of_strings))
        return retr


    # This will format a string that contains a single quote properly
    def format_for_insertion(self, str_arg):
        if "'" in str_arg:
            str_arg = str_arg.replace("'", "''")
        return_string = f"'{str_arg}'"
        return return_string


    # This will return the first row (the headings) of a csv file as a list
    def get_headings(self, csv_file_path):
        with open(csv_file_path, "r", newline='') as data:
            reader = csv.reader(data)
            retr = []
            for row in reader:
                retr = row
                break
            return retr

```

<br>

- I initialise the class and connect to the appropriate servers etc. and create a cursor to allow for queries to be made.
```python
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
```

<br>

- These are just two methods that allow the user to see the tables in the database and the columns in a given table. These were created for visual clarity and ease of use.
```python
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
        # I return it in a list for ease of visiblity - much more friendly than separate lines
        retr = []
        for _ in row:
            for val in _:
                retr.append(val)
        return retr
```

<br>

- This block lets us create a table from any ```.csv``` file. This generalises the first iteration.
```python
    # OPTION 1
    # CHECKED = YES
    def create_table(self):
        # Asks for the .csv file path
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
        # This solves the limitations mentioned in iteration 1
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

        # Puts the column names in the correct format for adding to a query
        col_in_query = ",".join(column_names)
        with open(csv_file, newline='') as data:
            reader = csv.reader(data)
            # This assumes the first line of the .csv file is the column names
            # This will ensure they won't be added to the table as the first row
            next(iter(reader))

            # This block will loop through all the rows in the file and add them
            # to the table at every loop
            for row in reader:
                # This will remove non alpha-numeric characters
                retr = list(map(self.format_for_insertion, row))
                retr = ",".join(retr)
                query = f"INSERT INTO {table_name} ({col_in_query}) VALUES ({retr})"
                
                try:
                    self.cursor.execute(query)
                    self.connection.commit()
                except:
                    continue

        print("\nTable created!")
```

<br>

- This will be able to add a given.csv file into a table that exists. 
```python
    # OPTION 2
    # CHECKED = YES
    # Adds values from a .csv file into a table
    def csv_to_table(self):
        self.show_possible_tables()
        table_name = input("\nInput table name:\n")
        csv_file = input("\nInput path to .csv file:\n")

        # Retrieves the column names and makes them ready for querying as a string
        col_names = self.make_column_names_of_table(table_name)
        col_names_as_string = ", ".join(col_names)

        # Errors can occur if the csv file doesnt exist etc.
        try:    
            # Goes through line by line in the csv file and adds them to the table
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
        except:
            return print("\nSomething went wrong!")
```

<br>

- This will do the opposite of the one above, it can get any data from a table in the DB and write it into a ```.csv``` file.
```python
    # OPTION 3
    # CHECKED = YES
    # Get values from a table and put it into a .csv file
    def table_to_csv(self):
        # Shows tables to get data from
        self.show_possible_tables()
        table_name = input("\nInput table name:\n")

        # Prints the columns to choose from
        print("")
        print(self.make_column_names_of_table(table_name))
        column_name_to_identify = input("\nWhich column to grab the data?\n")


        # Grabs the rows to grab 
        values = input(f"\nFrom {column_name_to_identify} type the rows to grab: (separate by commas)\n")

        retr_list = values.split(",")

        csv_name = input("\nName the new .csvfile: (end it with a .csv)\n")

        # Possible errors if the names dont exist etc.
        # This catches them
        try:
            with open(csv_name, "w", newline="") as file:
                writer = csv.writer(file)
                for val in retr_list:
                    y = self.cursor.execute(f"SELECT * FROM {table_name} WHERE {column_name_to_identify} = '{val.strip()}'").fetchone()
                    writer.writerow(y)
        except:
            print("\nSomething went wrong!")
```

<br>

- Like in iteration 1, I let the user query ```SELECT``` statements for flexibility in database querying.
```python
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
```

<br>

- The ```choices``` method builds upon the first one also. I got rid of a check function by not even trying to cast ```str``` values into ```int``` and hence saved some lines of code.
```python
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
```

<br>

- Finally, this block executes and lets one use the manager.
```python
    # Input your own server, database, username and password to use this manager
if __name__ == "__main__":
    server = "JaredPC\JS_1"
    database = "TASK"
    username = "sa"
    password = "passw0rd"
    main = SQLManager(server, database, username, password)
    main.choices()
```