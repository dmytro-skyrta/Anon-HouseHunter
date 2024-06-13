import sys                                                                                                              # Importing the sys module for system-specific parameters
from loguru import logger                                                                                               # Importing loguru for advanced logging capabilities

logger.remove()                                                                                                         # Removing any pre-existing loggers
logger.add(sys.stdout, level="TRACE")                                                                                   # Adding logger to output to console with TRACE level
logger.add("05 Log.txt", level="TRACE", rotation="10 MB", compression="zip")                                            # Adding logger to output to a file with TRACE level, rotating at 10MB and compressing to zip
saving_file_for_object_to_search = "06 Last object to search.txt"                                                       # Defining the filename to save the search object

class Property:                                                                                                         # Defining a class for Property
    def __init__(self, property_type, location, radius, max_price):                                                     # Initializing the Property class
        self.property_type = property_type                                                                              # Setting the property type
        self.location = location                                                                                        # Setting the location
        self.radius = radius                                                                                            # Setting the search radius
        self.max_price = max_price                                                                                      # Setting the maximum price

    def __str__(self):                                                                                                  # Defining the string representation of the Property object
        return f"Property: Type: {self.property_type}, Location: {self.location}, Radius: {self.radius} km, Max Price: {self.max_price} Euro"  # Returning a formatted string representation

def object_to_search_user_input():                                                                                      # Defining a function to get user input for the search object
    while True:                                                                                                         # Starting an infinite loop to get valid input
        property_type = input("1. What would you like to search for? Chose 1 for apartment and 2 for house: ")          # Asking the user to choose the property type
        if property_type == "1": property_type = "Apartment"; break                                                     # If input is 1, set property type to Apartment and break the loop
        elif property_type == "2": property_type = "House"; break                                                       # If input is 2, set property type to House and break the loop
        else: print("Incorrect input. Please choose only 1 or 2.")                                                      # If input is invalid, prompt the user again

    while True:                                                                                                         # Starting an infinite loop to get valid location input
        location = input("2. Chose the region for searching:\n"                                                         # Asking the user to choose the location
                         "1 - 83489 Berchtesgaden\n"
                         "2 - 83483 Bischofswiesen\n"
                         "3 - 83486 Wimbachschloß\n"
                         "4 - 83486 Ramsau bei Berchtesgaden\n"
                         "5 - 83487 Marktschellenberg\n"
                         "Enter 1-5: ")
        if location == "1": location = "83489 Berchtesgaden"; break                                                     # If input is 1, set location to Berchtesgaden and break the loop
        elif location == "2": location = "83483 Bischofswiesen"; break                                                  # If input is 2, set location to Bischofswiesen and break the loop
        elif location == "3": location = "83486 Wimbachschloß"; break                                                   # If input is 3, set location to Wimbachschloß and break the loop
        elif location == "4": location = "83486 Ramsau bei Berchtesgaden"; break                                        # If input is 4, set location to Ramsau bei Berchtesgaden and break the loop
        elif location == "5": location = "83487 Marktschellenberg"; break                                               # If input is 5, set location to Marktschellenberg and break the loop
        else: print("Incorrect input. Please choose only 1 or 2.")                                                      # If input is invalid, prompt the user again

    radius = int(input("3. Enter the search radius in kilometers: "))                                                   # Asking the user to enter the search radius
    max_price = int(input("4. Enter the maximum price per month: "))                                                    # Asking the user to enter the maximum price
    object_to_search = Property(property_type, location, radius, max_price)                                             # Creating a Property object with the user input
    return object_to_search                                                                                             # Returning the created Property object

def save_search_object_to_file(search_object, filename):                                                                # Defining a function to save the search object to a file
    with open(filename, 'w') as file:                                                                                   # Opening the file in write mode
        file.write(f"Property Type: {search_object.property_type}\n")                                                   # Writing the property type to the file
        file.write(f"Location: {search_object.location}\n")                                                             # Writing the location to the file
        file.write(f"Radius: {search_object.radius}\n")                                                                 # Writing the radius to the file
        file.write(f"Max Price: {search_object.max_price}\n")                                                           # Writing the maximum price to the file

def load_search_object_from_file(filename):                                                                             # Defining a function to load the search object from a file
    with open(filename, 'r') as file:                                                                                   # Opening the file in read mode
        lines = file.readlines()                                                                                        # Reading all lines from the file
    property_type = lines[0].split(": ")[1].strip()                                                                     # Extracting the property type from the first line
    location = lines[1].split(": ")[1].strip()                                                                          # Extracting the location from the second line
    radius = int(lines[2].split(": ")[1].strip().split()[0])                                                            # Extracting the radius from the third line
    max_price = int(lines[3].split(": ")[1].strip().split()[0])                                                         # Extracting the max price from the fourth line
    return Property(property_type, location, radius, max_price)                                                         # Returning a Property object with the extracted values

def get_object_to_search():                                                                                             # Defining a function to get the search object
    while True:                                                                                                         # Starting an infinite loop to get valid input
        repeat_search_choice = input("OBJECT TO SEARCH CONFIGURATION: Do you want to repeat the last saved search? (yes/no): ").lower()  # Asking the user if they want to repeat the last search
        if repeat_search_choice == "yes":                                                                               # If input is yes
            object_to_search = load_search_object_from_file(saving_file_for_object_to_search)                           # Load the search object from the file
            return (object_to_search)                                                                                   # Return the loaded search object
        elif repeat_search_choice == "no":                                                                              # If input is no
            object_to_search = object_to_search_user_input()                                                            # Get the search object from user input
            save_search_object_to_file(object_to_search, saving_file_for_object_to_search)                              # Save the search object to the file
            logger.info(f"Property was saved to {saving_file_for_object_to_search}")                                    # Log that the property was saved
            return (object_to_search)                                                                                   # Return the search object
        else:  print("Incorrect input. Please choose only yes or no.")                                                  # If input is invalid - ask the user again

if __name__ == "__main__":                                                                                              # If the script is run directly
    object_to_search = get_object_to_search()                                                                           # Get the object to search
    logger.info(f"Object to search: {object_to_search}")                                                                # Log the object to search