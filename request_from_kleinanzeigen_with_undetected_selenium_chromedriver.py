import time                                                                                                             # Importing the time module to use time.sleep for waiting
import sys                                                                                                              # Importing the sys module for system-specific functions
from selenium import webdriver                                                                                          # Importing the webdriver module from Selenium package
from selenium.webdriver.common.by import By                                                                             # Importing By class for locating elements
from loguru import logger                                                                                               # Importing the logger from loguru module

logger.remove()                                                                                                         # Removing existing logger configurations
logger.add(sys.stdout, level="TRACE")                                                                                   # Adding logger configuration to output logs to stdout
logger.add("05 Log.txt", level="TRACE", rotation="10 MB", compression="zip")                                            # Adding logger configuration to save logs to file

save_file_of_links = "07 Links of founded property.txt"

def get_from_kleinanzeigen_with_chromedriver(url, useragent=None, working_proxies_list=None):
    logger.info(f"useragent: {useragent}")
    logger.info(f"working_proxies_list: {working_proxies_list}")

    options = webdriver.ChromeOptions()                                                                                 # Creating ChromeOptions object for customizing Chrome browser
    options.add_argument("--disable-blink-features=AutomationControlled")                                               # Disabling Blink features to prevent detection
    if useragent: options.add_argument(f'user-agent={useragent}')
    if working_proxies_list:
        for proxy in working_proxies_list:
            logger.info(f"thought proxy: {proxy}")
            options.add_argument(f'--proxy-server={proxy}')
            try:
                with webdriver.Chrome(options=options) as driver:                                                       # Creating a Chrome webdriver instance
                     driver.get(url)                                                                                    # Navigating to the specified URL
                     time.sleep(10)                                                                                     # Waiting for 5 seconds to allow the page to load completely
                     elements = driver.find_elements(By.CSS_SELECTOR, ".ellipsis")                                # Finding all elements with class 'ellipsis'
                     links = [element.get_attribute("href") for element in elements]                                    # Extracting links from href attributes
                     logger.info(f"{len(links)} links of property ware found. Here they are: {links}")
                     if links != 0:
                        return links
            except Exception as exception:
                logger.info(exception)                                                                                  # Logging any exceptions that occur during execution

def saving_new_links(links):
    try:                                                                                                                # Reading existing links from the file
        with open(save_file_of_links, "r") as file:                                                                     # Open the file in read mode
            existing_links = file.read().splitlines()                                                                   # Read all lines and split them into a list
    except FileNotFoundError:
        existing_links = []                                                                                             # If the file does not exist, start with an empty list

    new_links = [link for link in links if link not in existing_links]                                                  # Filtering out links that are already in the file
                                                                                                                        # Appending new links to the file:
    with open(save_file_of_links, "a") as file:                                                                         # Open the file in append mode
        for link in new_links:
            file.write(link + "\n")
    logger.info(f"All new links ware saved in file: {save_file_of_links}")                                              # Write each new link to the file

def get_url_from_user():
    url = input("Enter the URL from Kleinanzeigen website you would like to scrape and parce: ")
    return url

if __name__ == "__main__":
    url = "https://www.kleinanzeigen.de/c203l8319r10"
#    url = get_url_from_user()
    saving_new_links(get_from_kleinanzeigen_with_chromedriver(url))

