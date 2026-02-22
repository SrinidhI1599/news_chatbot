# Import the os module to interact with the operating system
# (used here to read environment variables)
import os

# Import load_dotenv function from dotenv package
# This function loads environment variables from a .env file into the system environment
from dotenv import load_dotenv

# Load the environment variables from the .env file into the program
# After this line, you can access variables using os.getenv()
load_dotenv()

# Read the environment variable named 'gemini_class'
# This is typically where you store your API key securely in the .env file
gemini_key = os.getenv('gemini_class')

# Define the model name as a string
# This specifies which Gemini model you want to use in your application
model = 'gemini-3-flash'

# Print the model name to the console
# Useful for debugging or confirming which model is being used
print(model)