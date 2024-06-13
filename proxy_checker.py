import sys                                                                                                                     # Importing the sys module for system-specific parameters
import requests                                                                                                                # Importing the requests module for making HTTP requests
import concurrent.futures                                                                                                      # Importing concurrent.futures for working with threads and processes
import threading                                                                                                               # Importing threading for working with threads
from loguru import logger                                                                                                      # Importing loguru for advanced logging capabilities
logger.remove()                                                                                                                # Removing any pre-existing loggers

# Proxy_checker manual settings:
LINK = "https://ipv4.icanhazip.com/"                                                                                           # Site for checking IP
MAX_THREADS = 10                                                                                                               # Define the maximum number of threads
TIMEOUT = 60                                                                                                                   # Stop checking proxies after n seconds
lock = threading.Lock()                                                                                                        # Only one thread works at a time
write_to_file = "02 Working proxies.txt"                                                                                       # File to write working proxies to
proxy_list_small = "03 Proxy list short.txt"                                                                                   # File containing a small list of proxies
proxy_list_big = "04 Proxy list long.txt"                                                                                      # File containing a big list of proxies

def check_one_proxy(proxy):                                                                                                    # Define a function to check one proxy
    proxy = proxy.lower()                                                                                                      # Convert the proxy to lowercase

    if "localhost" in proxy:                                                                                                   # Check if the proxy is localhost
        response = requests.get(LINK, timeout=TIMEOUT)                                                                         # Send a request to the link without a proxy
        ip_address = response.text.strip()                                                                                     # Get the IP address from the response
        logger.info(f"Direct connection is working, IP: {ip_address}")                                                         # Log the working direct connection
        return proxy                                                                                                           # Return the proxy
    elif "://" in proxy:                                                                                                       # Check if the proxy includes a protocol
        proxy_dict = {protocol: f"{proxy}" for protocol in ["http", "https", "ftp", "ftps", "socks", "socks4", "socks4a", "socks5", "socks5h"]}  # Create a dictionary for the proxy
    else:                                                                                                                      # If the proxy does not include a protocol
        proxy_dict = {                                                                                                         # Create a dictionary with various protocols
            "http": f"http://{proxy}",                                                                                         # HTTP proxy
            "https": f"http://{proxy}",                                                                                        # HTTPS proxy
            "ftp": f"ftp://{proxy}",                                                                                           # FTP proxy
            "ftps": f"ftps://{proxy}",                                                                                         # FTPS proxy
            "socks": f"socks://{proxy}",                                                                                       # SOCKS proxy
            "socks4": f"socks4://{proxy}",                                                                                     # SOCKS4 proxy
            "socks4a": f"socks4a://{proxy}",                                                                                   # SOCKS4A proxy
            "socks5": f"socks5://{proxy}",                                                                                     # SOCKS5 proxy
            "socks5h": f"socks5h://{proxy}"                                                                                    # SOCKS5H proxy
        }
    try:                                                                                                                       # Start a try block to catch exceptions
        response = requests.get(LINK, proxies=proxy_dict, timeout=TIMEOUT)                                                     # Send a request through the proxy
        ip_address = response.text.strip()                                                                                     # Get the IP address from the response
        with lock:                                                                                                             # Acquire the lock
            logger.info(f"Proxy is working: {proxy} ; IP: {ip_address}")                                                       # Log the working proxy
        return proxy                                                                                                           # Return the proxy
    except requests.exceptions.Timeout:                                                                                        # Catch timeout exceptions
        with lock:                                                                                                             # Acquire the lock
            logger.info(f"Timeout occurred while checking proxy: {proxy}")                                                     # Log the timeout
    except requests.exceptions.RequestException:                                                                               # Catch general request exceptions
        with lock:                                                                                                             # Acquire the lock
            logger.info(f"Proxy is invalid: {proxy}")                                                                          # Log the invalid proxy

def check_proxy_list(proxies_list):                                                                                            # Define a function to check a list of proxies
    working_proxies_list = []                                                                                                  # Create a list of only working proxies
    leng_from = len(proxies_list)                                                                                              # Get the length of the proxies list
    logger.info(f"Received {leng_from} proxies (or connection type). Starting checks in {MAX_THREADS} threads with a timeout of {TIMEOUT} seconds:")  # Log the start of checks
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:                                           # Create a thread pool for parallel execution of checks
        results = executor.map(check_one_proxy, proxies_list)                                                                  # Start checking each proxy in the list
        for result in results:                                                                                                 # Iterate through the results
            if result not in working_proxies_list and result is not None:                                                      # Check if the result is not already in the list and is not None
                working_proxies_list.append(result)                                                                            # Add the proxy to the list of working proxies
    leng_to = len(working_proxies_list)                                                                                        # Get the length of the working proxies list
    logger.info(f"{leng_to} working proxies (or connection type) were found.")                                                 # Log the number of working proxies
    return working_proxies_list                                                                                                # Return the list of working proxies

def read_list_from_file(from_file):                                                                                            # Define a function to read a list of proxies from a file
    with open(from_file, "r") as file:                                                                                         # Open the file for reading
        proxies_list = [line.strip() for line in file]                                                                         # Create a list of proxies from the file
    return proxies_list                                                                                                        # Return the list of proxies

def write_list_to_file(working_proxies_list, write_to_file):                                                                   # Define a function to write a list of working proxies to a file
    leng_to = len(working_proxies_list)                                                                                        # Get the length of the working proxies list
    with lock:                                                                                                                 # Acquire the lock
        if working_proxies_list:                                                                                               # Check if the list of working proxies is not empty
            with open(write_to_file, "w") as output_file:                                                                      # Open the file for writing
                for proxy in working_proxies_list:                                                                             # Iterate through the working proxies list
                    output_file.write(proxy + "\n")                                                                            # Write each proxy to the file
            logger.info(f"{leng_to} working proxies successfully written to the file {write_to_file}.")                        # Log the success message
        else:                                                                                                                  # If the list of working proxies is empty
            logger.info("No working proxies to write to the file.")                                                            # Log the no working proxies message

def configure_connection_choice():                                                                                            # Define a function to configure connection choice
    while True:                                                                                                                # Start an infinite loop
        choice = input(                                                                                                        # Prompt the user for input
            "CONNECTION CONFIGURATION: Connection through:\n"
            "1 = proxy without a check of any lists of proxies \n"
            "2 = proxy with a check of a short list of proxies\n"
            "3 = proxy with a check of a long list of proxies\n"
            "4 = TOR\n"
            "5 = direct connection (Attention: This threatens a ban for frequent requests!)\n"
            "Make your choice: "
        )
        if choice == "1":                                                                                                      # If the user chooses option 1
            logger.info("You chose 1: connection without a proxy list check.")                                                 # Log the user's choice
            working_proxies_list = read_list_from_file(write_to_file)                                                          # Read the list of proxies from the file
            return working_proxies_list                                                                                        # Return the list of working proxies
        elif choice == "2":                                                                                                    # If the user chooses option 2
            logger.info("You chose 2: connection through a proxy with a check of a short list of proxies. Starting the checking procedure: ")  # Log the user's choice
            from_file = proxy_list_small                                                                                       # Set the file to read from
            working_proxies_list = check_proxy_list(read_list_from_file(from_file))                                            # Check the list of proxies
            write_list_to_file(working_proxies_list, write_to_file)                                                            # Write the working proxies to the file
            return working_proxies_list                                                                                        # Return the list of working proxies
        elif choice == "3":                                                                                                    # If the user chooses option 3
            logger.info("You chose 3: connection through a proxy with a check of a long list of proxies. Starting the checking procedure: ")  # Log the user's choice
            from_file = proxy_list_big                                                                                         # Set the file to read from
            working_proxies_list = check_proxy_list(read_list_from_file(from_file))                                            # Check the list of proxies
            write_list_to_file(working_proxies_list, write_to_file)                                                            # Write the working proxies to the file
            return working_proxies_list                                                                                        # Return the list of working proxies
        elif choice == "4":                                                                                                    # If the user chooses option 4
            logger.info("You chose 4: connection through TOR. Starting the connection through TOR:")                           # Log the user's choice
            working_proxies_list = check_proxy_list(["socks5://127.0.0.1:9050"])                                               # Check the connection through TOR
            return working_proxies_list                                                                                        # Return the list of working proxies
        elif choice == "5":                                                                                                    # If the user chooses option 5
            logger.info("You chose 5: direct connection. This threatens a ban for frequent requests!")                         # Log the user's choice
            working_proxies_list = check_proxy_list(["http://localhost:8080"])                                                 # Check the direct connection
#            working_proxies_list = check_proxy_list(["localhost"])                                                            # Alternative direct connection
            return working_proxies_list                                                                                        # Return the list of working proxies
        else:                                                                                                                  # If the user's input is incorrect
            logger.info("Incorrect input. Please choose only 1-5.")                                                            # Log the incorrect input message

if __name__ == "__main__":                                                                                                     # Check if the script is being run directly
    logger.add(sys.stdout, level="TRACE")                                                                                      # Add a logger to output to stdout with TRACE level
    working_proxies_list = configure_connection_choice()                                                                       # Call the function to configure connection choice
