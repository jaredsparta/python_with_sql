# Task

![](images/task1.png)

**Explanation**
- As always, we will need ```pyodbc``` so install it into the environment with ```pip install pyodbc``` and import it using ```import pyodbc```

<br>

- I then create a class that will manage the entirety of this task:
```python
    class SQLInstance:
        def __init__(self, server, database, username, password):
            pass
```

<br>

- I will make a connection with the server using the class inputs. I put this into a separate function itself:
```python
    def make_connection(self, server, database, username, password):
        connection = pyodbc.connect(f"""
                DRIVER=ODBC Driver 17 for SQL Server;
                SERVER={server};
                DATABASE={database};
                UID={username};
                PWD={password}""")
        return connection
```

<br>

- I then assign the return value ```connection``` as a class attribute in the ```__init__``` method
```python
    def __init__(self, server, database, username, password):
        self.connection = self.make_connection(server, database, username, password)
```
<br>

- I then create a class method that will enable one to create a table within the database:
```python
    # Makes a table
    def make_table(self):
        table_name = input("\nWhat should the table be called?\n--> ")
        # Not inputting an integer will cause an error so I will catch it
        while True:
            try:
                number_of_col = int(input("\nHow many columns?\n--> "))
                break
            except:
                continue
        
        # This will be the query used to create the table
        query_string = ""
        length = len(query_string)
        
        # This will ask for the names and datatypes for the table
        for _ in range(number_of_col):
            col_name = input(f"\nInput name of column {_ + 1}: ")
            col_datatype = input(f"Input the datatype of this column: ")
            query_string = query_string + col_name + " " + col_datatype + ","

        # The query string will have an extra comma at the end, this removes it
        query_string = query_string[:length-1]

        # This will create the table and commit it
        self.cursor.execute(f"CREATE TABLE {table_name} ({query_string});")
        self.connection.commit()
```

<br>

- But now, one should be able to add additional columns if need be. I create a method to do this also:
```python
    # Allows one to add a column to a table
    def add_column(self):
        # Ask for the table to add to, the column name and its datatype
        table_name = input("\nWhich table to add a column? ").strip()
        col_name = input("What's the column name? ")
        col_datatype = input("What's the datatype? ")
        query = f"ALTER TABLE {table_name} ADD {col_name} {col_datatype};"
        
        print(f"\nThe current query is: {query}")
        
        choice = input("Would you like to continue? (Y/N) ").strip().upper()
        if choice == "Y":
            try:
                self.cursor.execute(query)
                self.connection.commit()
                print("\nColumn added!")
            except:
                print("\nSomething went wrong")
```

<br>

- Now we need a way to insert rows into our table:
```python
    # Allows one to insert a row into a table
    def insert_into(self):
        # Asks for the table's name, the columns to add to and their values
        table_name = input("Which table are you adding values to? ").strip()
        query_cols = input("Which columns are you adding to?\n")
        query_vals = input("What are the values?\n")

        # Creates the query to do so and asks if it's what they wanted
        query = f"INSERT INTO {table_name} ({query_cols}) VALUES ({query_vals})"
        print(f"\nThe current query is: {query}")


        # Changing a table can be a big error so I put this in just in case
        choice = input("Would you like to continue? (Y/N) ").strip()
        if choice == "Y":
            try:
                self.cursor.execute(query)
                self.connection.commit()
                print("\nRow added!")
            except:
                print("\nSomething went wrong")
```

<br>

- I will also allow one to query whatever they like:
```python
    def query_db(self):
        # This is the query string
        query_str = input("Insert your query:\n")
        # If the query causes an error, this will catch it
        try:
            result = self.cursor.execute(query_str)
            for row in result:
                print(row)
        except:
            print("\nError!")
```

<br>

- Finally, I will create a menu that allows one to choose what to do:
```python
    # Menu for what to do
    def choices(self):
        while True:
            print("""\nOptions:
                        1. Query
                        2. Make table
                        3. Add a row to a table
                        4. Add a column to a table
                        5. Exit""")
            choice = input("---> ").strip()

            if int(choice) == 1:
                self.query_db()


            elif int(choice) == 2:
                self.make_table()
                print("\nTable created!")


            elif int(choice) == 3:
                self.insert_into()


            elif int(choice) == 4:
                self.add_column()


            elif int(choice) == 5:
                break
            

            else:
                print("\nNot an option!")
```

<br>

- In the end, my ```__init__``` method will look like this:
```python
    # So when I create an object of this class, it will automatically connect
    # to the server and DB as inputted
    # It will also createa cursor to use
    # I then call the choices method
    def __init__(self, server, database, username, password):
        self.connection = self.make_connection(server, database, username, password)
        self.cursor = self.connection.cursor()
        self.choices()
```

<br>

- Finally, I will connect to the required server and database as per the task:
```python
    # Where the arguements will be the correct server, DB, user and password
    if __name__ == "__main__":
    c = SQLInstance(jserver, jdatabase, jusername, jpassword)
```