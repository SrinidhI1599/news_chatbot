# Importing required libraries
import logging # Import logging module for tracking errors and application events
import feedparser # Import feedparser to read and parse RSS feeds (Google News RSS)
import google.genai as genai # Import Google Gemini AI client library
from settings import gemini_key, model # Import API key and model configuration from settings file
import urllib.parse # Import urllib.parse to encode query strings safely for URLs

# Initialize Gemini client using the API key
client = genai.Client(api_key=gemini_key)

# Initialize Gemini client using the API key
def fetch_google_news(query, max_results=5):
    """
    Fetch latest news articles from Google News RSS feed.
    """
    try:
        encoded_query = urllib.parse.quote_plus(str(query))  # Encode spaces and special characters in query for URL safety
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en" # Construct Google News RSS URL with encoded query
        feed = feedparser.parse(rss_url) # Parse the RSS feed data from the URL
        articles = [] # Initialize an empty list to store article data  

        # Loop through feed entries up to the max_results limit
        for entry in feed.entries[:max_results]:
            # Append each article as a dictionary
            articles.append({ 
                "title": entry.title, # Extract article title
                "description": getattr(entry, "summary", ""), # Extract description safely (empty if missing)
                "url": entry.link # Extract article URL
            })

        # Return the list of fetched articles
        return articles
    except Exception as e:
        logging.error(f"Google news fetch error: {e}") # Log any error that occurs during news fetching
        return [] # Return empty list if an error occurs


# Function to send prompt to Gemini model and get response
def call_gemini(prompt):
    try:
        response = client.models.generate_content(model=model, contents=prompt) # Call Gemini API with model and prompt
        return response.text # Return the generated response text
    except Exception as e:
        logging.error(f"Gemini API error: {e}") # Log any error during Gemini API call
        return "⚠️ The Gemini API quota has been exceeded. Please try again later or upgrade your plan." # Return fallback message on failure
