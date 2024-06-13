import sys                                                                                                                     # Importing the sys module for system-specific parameters
import requests                                                                                                                # Importing the requests module for making HTTP requests
from loguru import logger                                                                                                      # Importing loguru for advanced logging capabilities
logger.remove()                                                                                                                # Removing any pre-existing loggers
logger.add(sys.stdout, level="TRACE")                                                                                          # Adding a logger to output to stdout with TRACE level
logger.add("05 Log.txt", level="TRACE", rotation="10 MB", compression="zip")                                                   # Adding a logger to write to a file with rotation and compression

def get_anonym_with_requests_library(url, useragent, working_proxies_list):                                                    # Defining a function for making anonymous requests
    logger.info(f"Starting def get_anonym_with_requests_library for URL {url}")                                                # Logging the start of the function
    logger.info(f"Following useragent was received from def configure_fake_useragent: {useragent}")                            # Logging the received user agent
    logger.info(f"Following proxy list was received from proxy_checker.py module: {working_proxies_list}")                     # Logging the received proxy list
    my_header = {"user-agent": useragent }                                                                                     # Setting the user agent in the header

    while True:                                                                                                                # Starting an infinite loop
        for proxy in working_proxies_list:                                                                                     # Iterating through the list of working proxies
            if "localhost" in proxy:                                                                                           # Checking if the proxy is localhost
                logger.info(f"Sending an anonymous request to: {url} through: localhost")                                      # Logging the request through localhost
                response = requests.get(url, headers=my_header)                                                                # Sending the request through localhost
                logger.info(f"Response status: {response}")                                                                    # Logging the response status
                return response                                                                                                # Returning the response
            elif "://" in proxy:                                                                                               # Checking if the proxy has a protocol specified
                proxy_dict = {protocol: f"{proxy}" for protocol in ["http", "https", "ftp", "ftps", "socks", "socks4", "socks4a", "socks5", "socks5h"]}  # Creating a proxy dictionary with protocols
            else:                                                                                                              # If no protocol is specified
                proxy_dict = {                                                                                                 # Creating a proxy dictionary with default protocols
                    "http": f"http://{proxy}",                                                                                 # HTTP proxy
                    "https": f"http://{proxy}",                                                                                # HTTPS proxy
                    "ftp": f"ftp://{proxy}",                                                                                   # FTP proxy
                    "ftps": f"ftps://{proxy}",                                                                                 # FTPS proxy
                    "socks": f"socks://{proxy}",                                                                               # SOCKS proxy
                    "socks4": f"socks4://{proxy}",                                                                             # SOCKS4 proxy
                    "socks4a": f"socks4a://{proxy}",                                                                           # SOCKS4a proxy
                    "socks5": f"socks5://{proxy}",                                                                             # SOCKS5 proxy
                    "socks5h": f"socks5h://{proxy}"                                                                            # SOCKS5h proxy
                }
            logger.info(f"Created dictionary of proxy for requests library: {proxy_dict}")                                     # Logging the created proxy dictionary
            try:                                                                                                               # Starting a try block to catch exceptions
                logger.info(f"Sending an anonymous request to: {url} through: {proxy_dict}")                                   # Logging the request through the proxy
                response = requests.get(url, headers=my_header, proxies=proxy_dict)                                            # Sending the request through the proxy
                logger.info(f"Response status: {response}")                                                                    # Logging the response status
                return response                                                                                                # Returning the response
            except requests.exceptions.ProxyError as e:                                                                        # Catching proxy connection errors
                logger.info(f"Proxy connection error: {e}")                                                                    # Logging the proxy connection error
            except requests.exceptions.SSLError as e:                                                                          # Catching SSL errors
                logger.info(f"SSL error when connecting to the proxy: {e}")                                                    # Logging the SSL error
            except requests.exceptions.RequestException as e:                                                                  # Catching general request exceptions
                logger.info(f"Request error: {e}")                                                                             # Logging the request error
        logger.info("All proxies in the list failed. Getting a new list of proxies:")                                          # Logging that all proxies failed and a new list is needed
