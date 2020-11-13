import csv

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

# This is used to test the class above
if __name__ == "__main__":
    f  = Formatter()
    print(f.get_headings("imdbtitles.csv"))
