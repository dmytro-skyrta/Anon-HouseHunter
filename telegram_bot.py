import requests                                                                                                         # Importing the requests module for making HTTP requests
import sys                                                                                                              # Importing sys module for system-specific parameters
from loguru import logger                                                                                               # Importing loguru for advanced logging capabilities
logger.remove()                                                                                                         # Removing any pre-existing loggers

telegra_param_save_file = '08 Telegram Bot Token and ChatID.txt'                                                        # File to store Telegram bot token and chat ID

def read_parameters_from_file(telegra_param_save_file):
    with open(telegra_param_save_file, 'r') as file:                                                                    # Open file for reading
        lines = file.readlines()                                                                                        # Read all lines
        bot_token = lines[0].strip().split('=')[1].strip().strip('"')                                                   # Extract and clean bot token from the file
        chat_id = lines[1].strip().split('=')[1].strip().strip('"')                                                     # Extract and clean chat ID from the file
    return bot_token, chat_id                                                                                           # Return bot token and chat ID

def write_parameters_to_file(telegra_param_save_file, bot_token, chat_id):
    with open(telegra_param_save_file, 'w') as file:                                                                    # Open file for writing
        file.write(f'bot_token = "{bot_token}"\n')                                                                      # Write bot token to the file
        file.write(f'chatID = "{chat_id}"\n')                                                                           # Write chat ID to the file

def configure_telegram_bot(telegra_param_save_file, text):
    bot_token, chat_id = read_parameters_from_file(telegra_param_save_file)                                             # Read bot token and chat ID from the file
    logger.info(f"Current bot token: {bot_token}")                                                                      # Log current bot token
    logger.info(f"Current chat ID: {chat_id}")                                                                          # Log current chat ID

    while True:
        user_choice = input("Do you want to use these parameters? (yes/no): ").lower()                                  # Prompt user for choice
        if user_choice == "yes":                                                                                        # If user chooses yes
            break                                                                                                       # Exit loop
        elif user_choice == "no":                                                                                       # If user chooses no
            bot_token = input("Enter new bot token: ").strip()                                                          # Prompt for new bot token
            chat_id = input("Enter new chat ID: ").strip()                                                              # Prompt for new chat ID
            write_parameters_to_file(telegra_param_save_file, bot_token, chat_id)                                       # Write new parameters to file
            break                                                                                                       # Exit loop
        else:
            logger.info("Incorrect input. Please choose only yes or no.")                                               # Log incorrect input message

    telegram_bot_send_text(bot_token, chat_id, text)                                                                    # Send text via Telegram bot

def telegram_bot_send_text(bot_token, chat_id, text):
    logger.info(f"{text}")                                                                                              # Log the text message
    for link in text:                                                                                                   # Iterate over each link in text
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"                                                    # Telegram bot API URL
        payload = {                                                                                                     # Payload for the API request
            'chat_id': chat_id,                                                                                         # Chat ID
            'text': link,                                                                                               # Message text (link)
            'parse_mode': 'Markdown'                                                                                    # Parse mode for formatting
        }
        response = requests.get(url, params=payload)                                                                    # Send GET request to Telegram API
        if response.status_code == 200:                                                                                 # If message is sent successfully
            logger.info(f"Message sent successfully: {link}")                                                           # Log success message
        else:
            logger.info(f"Failed to send message: {response.status_code}")                                              # Log failure message with status code
            logger.info(response.text)                                                                                  # Log API response text

if __name__ == "__main__":                                                                                              # If script is executed directly
    logger.add(sys.stdout, level="TRACE")                                                                               # Add logger to output to stdout with TRACE level
    sending_info = "test message python"                                                                                # Message to send via Telegram bot
    configure_telegram_bot(telegra_param_save_file, sending_info)                                                       # Configure and send message via Telegram bot