# Define a function to keep only the last few conversation turns from history
def trim_history(history, max_turns=3):
    return history[-max_turns:] # Return the last 'max_turns' items from the history list

# Define a function to clean and format the response text
def format_response(response_text):
    return response_text.strip() # Remove leading and trailing whitespace from the response text