# Anon-HouseHunter

Set your search criteria and receive all found properties on your mobile phone via Telegram at any frequency you choose. Be always the first to contact the property owner!

## Project Overview

Welcome to HausHunter, a powerful, scalable real estate search tool designed to help users find their perfect home in Berchtesgaden and beyond. Leveraging a microarchitecture, each module in HausHunter operates independently, enhancing debugging efficiency and enabling effortless scalability. This modularity ensures that components can be reused in other projects, making HausHunter a versatile addition to any developer's toolkit.

## Key Features

### 1. Microarchitecture: 
HausHunter's design is based on a microarchitecture, where each module functions autonomously. This improves debugging and allows the project to scale to any size effortlessly.

### 2. Scalable Search Scope: 
Initially focused on finding properties in Berchtesgaden, the search criteria can be easily expanded to cover all of Germany, providing flexibility for various user needs.

### 3. Customizable Search Sources: 
Users can search for properties across multiple websites. Adding new websites requires a short algorithm due to the unique features of each site, ensuring seamless integration.

### 4. Anonymized Data Collection: 
HausHunter can work with protected sites, retrieving data anonymously through proxies or TOR, employing fake user agents and other anonymization mechanisms to protect users from bans due to frequent requests or automation (scraping and parsing).

### 5. Dual Logging System: 
The project features a dual logging system. One stream logs information to the console (optional for the user), while the other automatically records logs to a text file, ensuring comprehensive tracking and easy debugging.

### 6. Data Storage: 
HausHunter saves all useful data in text files, creating lists of found properties, verified working proxies, Telegram bot parameters, and other valuable information, facilitating further use and analysis.

## Technical Highlights

### 1. Flexible Logging Configuration: 
Users can choose to enable or disable console logging, while file logging remains active to ensure data persistence.
Dynamic User-Agent Configuration: Users can opt to create a fake user agent, adding an extra layer of anonymity during data collection.

### 2. Proxy Management: 
HausHunter includes a robust proxy checker to validate proxies from provided lists, ensuring reliable and anonymous connections.
Seamless Web Scraping: Using Selenium with ChromeDriver, the project can navigate and extract data from various property listing sites, with mechanisms to handle different proxy setups and user agents.

### 3. Telegram Integration: 
Notifications about new property listings can be configured to be sent via a Telegram bot, keeping users promptly informed.

## How It Works

### 1. Logging Configuration: 
Users can choose their preferred logging setup, ensuring they receive the necessary feedback during the search process.

### 2. Search Object Configuration: 
Define the type of property, location, search radius, and maximum price, or repeat the last saved search configuration.

### 3. Connection Configuration: 
Choose the preferred connection method (direct, proxy, TOR), ensuring a secure and anonymous search process.

### 4. Site-Specific Searches: 
For each site, custom search functions handle the unique features of the site, ensuring accurate data collection.

### 5. Data Processing and Storage: 
Extracted data is logged, processed, and stored in text files for easy access and further use.

### 6. Notification System: 
Integrate with Telegram to receive updates on new property listings directly to your device.

## Conclusion

HausHunter is more than just a real estate search tool; it's a highly customizable and scalable solution that ensures user anonymity, flexible configurations, and comprehensive data handling. Its robust architecture and advanced features make it an ideal project for developers and real estate enthusiasts looking to efficiently find properties while maintaining privacy and flexibility.
