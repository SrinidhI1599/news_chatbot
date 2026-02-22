# Import the logging module to enable logging in the application
import logging

# Configure the basic settings for the logging system
logging.basicConfig(
    
    # Set the logging level to INFO (shows INFO, WARNING, ERROR, CRITICAL messages)
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s", # Define the log message format with timestamp and level
    handlers=[logging.StreamHandler()] # Send log output to the console (standard output)
)