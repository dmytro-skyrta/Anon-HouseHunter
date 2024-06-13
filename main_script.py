import sys                                                                                                              # Importing the sys module for system-specific parameters
import fake_useragent                                                                                                   # Importing fake_useragent to generate fake user agents
from proxy_checker import configure_connection_choice                                                                   # Importing function to configure proxy connections
from object_to_search import get_object_to_search                                                                       # Importing function to get the object to search
from request_anonym_with_requests_library import get_anonym_with_requests_library                                       # Importing function for anonymous requests
from request_from_kleinanzeigen_with_undetected_selenium_chromedriver import *                                          # Importing functions for handling Kleinanzeigen with Selenium
from telegram_bot import *                                                                                              # Importing functions to configure the Telegram bot
from bs4 import BeautifulSoup                                                                                           # Importing BeautifulSoup for parsing HTML content
from loguru import logger                                                                                               # Importing loguru for advanced logging capabilities

logger.remove()                                                                                                         # Removing any pre-existing loggers

def configure_logging():                                                                                                # Defining a function to configure logging
    while True:
        logger_choice = input("LOGGING CONFIGURATION: Do you want to see logs in the console? (yes/no): ").lower()      # Prompting user for logging choice
        if logger_choice == "yes":
            logger.add(sys.stdout, level="TRACE")                                                                       # Adding logger to output to console
            logger.add("05 Log.txt", level="TRACE", rotation="10 MB", compression="zip")                                # Adding logger to output to a file with rotation and compression
            logger.info("Logging enabled.")                                                                             # Logging that logging has been enabled
            break
        elif logger_choice == "no":
            logger.add("05 Log.txt", level="TRACE", rotation="10 MB", compression="zip")                                # Adding logger to output to a file with rotation and compression
            logger.info("Logging disabled.")                                                                            # Logging that logging has been disabled
            break
        else:
            print("Incorrect input. Please choose only yes or no.")                                                     # Handling incorrect input

def configure_fake_useragent():                                                                                         # Defining a function to configure a fake user agent
    while True:
        useragent_choice = input("FAKE USERAGENT CONFIGURATION: Do you want to create a fake useragent? (yes/no): ").lower()  # Prompting user for fake user agent choice
        if useragent_choice == "yes":
            useragent = fake_useragent.UserAgent().random                                                               # Creating a fake user agent
            logger.info(f"Created fake useragent: {useragent}")                                                         # Logging the created fake user agent
            return useragent
        elif useragent_choice == "no":
            logger.info("Fake useragent creation skipped.")                                                             # Logging that fake user agent creation was skipped
            return None
        else:
            print("Incorrect input. Please choose only yes or no.")                                                     # Handling incorrect input

def configure_object_to_search():                                                                                       # Defining a function to configure the object to search
    logger.info(f"Getting object with get_search_object:")                                                              # Logging the start of object retrieval
    object_to_search = get_object_to_search()                                                                           # Getting the object to search
    logger.info(object_to_search)                                                                                       # Logging the retrieved object
    return object_to_search

def http2ip(url, useragent, working_proxies_list):                                                                      # Defining a function to get IP and location using anonymous request
    logger.info(f"Getting response from {url} with def get_anonym_with_requests_library:")                              # Logging the start of the request
    response = get_anonym_with_requests_library(url, useragent, working_proxies_list)                                   # Getting the response
    logger.info(f"Parsing the response received from {url} with BeautifulSoup:")                                        # Logging the start of parsing
    soup = BeautifulSoup(response.text, "lxml")                                                                         # Parsing the response text with BeautifulSoup
    ipv4 = soup.find("div", class_="ip").text.strip()                                                                   # Extracting the IP address from the parsed content
    location = soup.find("div", id="ip-info-country").text.splitlines()[1].strip()                                      # Extracting the location from the parsed content
    logger.info(f"We are looking like user from:\nipv4: {ipv4}\nlocation: {location}")                                  # Logging the IP and location

def kleinanzeigen(object_to_search, useragent, working_proxies_list):                                                   # Defining a function to search on Kleinanzeigen
    logger.info(f"object_to_search: {object_to_search}")                                                                # Logging the object to search
    if "Apartment" in object_to_search.property_type : property_type_code = "c203"                                      # Setting property type code for apartment
    elif "House" in object_to_search.property_type : property_type_code = "c205"                                        # Setting property type code for house
    if "Berchtesgaden" in object_to_search.location: property_location_code = "8319"                                    # Setting location code for Berchtesgaden
    elif "Bischofswiesen" in object_to_search.location: property_location_code = "5873"                                 # Setting location code for Bischofswiesen
    elif "Wimbachschloß" in object_to_search.location: property_location_code = "5874"                                  # Setting location code for Wimbachschloß
    elif "Ramsau bei Berchtesgaden" in object_to_search.location: property_location_code = "5875"                       # Setting location code for Ramsau bei Berchtesgaden
    elif "Marktschellenberg" in object_to_search.location: property_location_code = "11895"                             # Setting location code for Marktschellenberg
    url_with_patameters = f"https://www.kleinanzeigen.de/{property_type_code}l{property_location_code}r{object_to_search.radius}"  # Creating the URL with parameters
    logger.info(f"Getting response from {url_with_patameters} with def get_anonym:")                                    # Logging the start of the request
    links = get_from_kleinanzeigen_with_chromedriver(url_with_patameters, useragent, working_proxies_list)              # Getting the links from Kleinanzeigen
    saving_new_links(links)                                                                                             # Saving the new links
    if len(links) != 0 :                                                                                                # Checking if any links were found
        configure_telegram_bot(telegra_param_save_file, links)                                                          # Configuring the Telegram bot with the found links

def search_object_by_all_urls(urls, object_to_search, useragent, working_proxies_list):                                 # Defining a function to search objects by all URLs
    for url in urls:                                                                                                    # Iterating over each URL
        logger.info(f"We are starting to work with URL: {url}")                                                         # Logging the start of work with the URL
        if "2ip" in url:
            logger.info(f"Function for URL {url} was founded. Starting def http2ip:")                                   # Logging that function for 2ip URL was found
            http2ip(url, useragent, working_proxies_list)                                                               # Calling the http2ip function
        elif "kleinanzeigen.de" in url:
            logger.info(f"Function for URL {url} was founded. Starting def kleinanzeigen:")                             # Logging that function for Kleinanzeigen URL was found
            kleinanzeigen(object_to_search, useragent, working_proxies_list)                                            # Calling the kleinanzeigen function
        else:
            logger.info(f"No definition for {url} was found.")                                                          # Logging that no function definition was found for the URL

if __name__ == "__main__":                                                                                              # Checking if the script is run as the main program
    configure_logging()                                                                                                 # Calling the function to configure logging
    object_to_search = configure_object_to_search()                                                                     # Getting the object to search
    useragent = configure_fake_useragent()                                                                              # Configuring the fake user agent
    working_proxies_list = configure_connection_choice()                                                                # Configuring the proxy connections

    with open("01 URL list for searching.txt") as file:                                                                 # Opening the file containing the list of URLs
        urls = [line.strip() for line in file if line.startswith("http")]                                               # Reading and stripping lines starting with http
        urls = [url.strip() for url in urls]                                                                            # Stripping any remaining whitespace from URLs
    logger.info(f"We are taking list from: 01 URL list for searching.txt: {urls}")                                      # Logging the list of URLs

    search_object_by_all_urls(urls, object_to_search, useragent, working_proxies_list)                                  # Searching objects by all URLs



"""
--- Thanks for the advice on developing this project to: ---
github.com/yvlasenko

--- Inspired by ideas from: ---
github.com/pythontoday
youtube.com/@ErikSpichak

--- Links to checking an undetected entry through a webdriver: ---
driver.get("https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html")
driver.get("https://www.vindecoderz.com/EN/check-lookup/ZDMMADBMXHB001652")
"""
