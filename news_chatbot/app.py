# Importing required libraries
import streamlit as st  # Import Streamlit for building the web-based chatbot UI
from api_handler import fetch_google_news, call_gemini  # Import functions to fetch news and call Gemini API
from prompt_manager import build_prompt  # Import function to build the prompt for the LLM
from response_processor import format_response  # Import function to clean/format model responses
import re  # Import regex module for pattern matching
from num2words import num2words  # Import num2words to convert numbers into ordinal words


# =========================
# UI TITLE
# =========================
st.title("📰 News Chatbot")  # Display the title of the application on the Streamlit page


# =========================
# SESSION STATE
# =========================
if "history" not in st.session_state:  # Check if conversation history exists in session state
    st.session_state.history = []  # Initialize history as an empty list if not present


# =========================
# ORDINAL LOOKUP
# =========================
ordinal_lookup = {num2words(i, to="ordinal"): i for i in range(1, 1001)}  # Create a dictionary mapping ordinal words (first, second) to numbers


# Function to detect ordinal words from user query
def parse_ordinal(query: str) -> int | None:  
    """Detect ordinal words like 'first', 'twenty first', etc."""
    text = query.lower().replace(" ", "-")  # Convert query to lowercase and replace spaces with hyphens for matching

    # Loop through ordinal lookup dictionary
    for word, value in ordinal_lookup.items():  

        # Check if ordinal word exists in query text
        if word in text:  
            return value  # Return the corresponding numeric value

    return None  # Return None if no ordinal word is found


# Function to get ordinal suffix for a number (st, nd, rd, th)
def get_suffix(n: int) -> str:  
    """Return ordinal suffix"""

    # Special case for numbers like 11th, 12th, 13th
    if 10 <= n % 100 <= 20:  
        return "th"  # Return "th" suffix
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")  # Return suffix based on last digit


# =========================
# MEMORY INTENT DETECTION
# =========================

# Function to detect if user is asking about chat history
def detect_memory_request(query: str):  
    """
    Returns:
    ("last", None)
    ("nth", n)
    ("history", None)
    (None, None)
    """

    q = query.lower()  # Convert query to lowercase for consistent matching

    # HISTORY
    # Detect history-related requests
    if re.search(r"\b(history|all questions|what have i asked|show questions)\b", q):  
        return "history", None  # Return history intent

    # LAST / PREVIOUS
    # Detect last question requests
    if re.search(r"\b(last|previous|latest|before)\b.*\b(question|ask|query)\b", q):  
        return "last", None  # Return last intent

    # NUMERIC ORDINAL
    # Detect numeric ordinal like 2nd question
    num_match = re.search(r"(\d+)(st|nd|rd|th)?\s+(question|query)", q)  
    if num_match:
        return "nth", int(num_match.group(1))  # Return nth intent with extracted number

    # WORD ORDINAL
    # Try detecting ordinal word like "third"
    word_n = parse_ordinal(q)  
    if word_n:
        return "nth", word_n  # Return nth intent with detected number

    return None, None  # Return None if no memory intent detected


# =========================
# CHAT INPUT
# =========================

# Display chat input box for user query
user_query = st.chat_input("Ask about the news...")  

# Execute logic only when user enters a query
if user_query:  

    intent, value = detect_memory_request(user_query)  # Detect if query is memory-related

    bot_response = ""  # Initialize bot response
    sources = None  # Initialize sources variable

    # =========================
    # MEMORY INTENTS
    # =========================

    # If memory-related intent is detected
    if intent is not None:  
        
        # Handle last question request
        if intent == "last":  
            if st.session_state.history:  # Check if history exists
                last_q = st.session_state.history[-1]["user"]  # Get last user question
                bot_response = f"Your last question was: '{last_q}'"  # Prepare response
            else:
                bot_response = "You haven't asked any questions yet."  # No history case

        # Handle full history request
        elif intent == "history":  

            if st.session_state.history:  # Check if history exists
                questions = [h["user"] for h in st.session_state.history]  # Extract all user questions
                formatted = "\n".join(
                    [f"{i+1}. {q}" for i, q in enumerate(questions)]  # Format numbered list
                )
                bot_response = f"Here is your question history:\n{formatted}"  # Prepare response
            else:
                bot_response = "No questions recorded yet."  # No history case

        # Handle nth question request
        elif intent == "nth":  

            n = value  # Extract requested number
            suffix = get_suffix(n)  # Get ordinal suffix

            if 0 < n <= len(st.session_state.history):  # Check if nth question exists
                nth_q = st.session_state.history[n - 1]["user"]  # Retrieve nth question
                bot_response = f"Your {n}{suffix} question was: '{nth_q}'"  # Prepare response
            else:
                bot_response = f"I don’t have a {n}{suffix} question recorded yet."  # Out-of-range case

        # MEMORY → NEVER SOURCES
        sources = None  # Memory responses do not include news sources

    # =========================
    # NEWS FLOW
    # =========================

    # If query is not memory-related, proceed with news fetching
    else:  

        with st.spinner("Fetching latest articles..."):  # Show loading spinner during news fetch
            articles = fetch_google_news(user_query)  # Fetch articles based on query

        with st.spinner("Generating response..."):  # Show loading spinner during LLM response generation
            prompt = build_prompt(
                st.session_state.history,  # Pass conversation history
                user_query,  # Pass user query
                articles  # Pass fetched articles
            )
            bot_response = call_gemini(prompt)  # Call Gemini API
            bot_response = format_response(bot_response)  # Clean response text

        sources = articles  # Store articles as sources

    # =========================
    # SAVE HISTORY
    # =========================
    entry = {
        "user": user_query,  # Save user query
        "bot": bot_response  # Save bot response
    }

    if sources is not None:  # If sources exist, include them in history
        entry["sources"] = sources

    st.session_state.history.append(entry)  # Append conversation entry to session history

    # =========================
    # DISPLAY CHAT
    # =========================

    # Loop through all conversation history entries
    for h in st.session_state.history:  

        with st.chat_message("user"):  # Display user message block
            st.write(h["user"])  # Show user text

        with st.chat_message("assistant"):  # Display assistant message block
            st.write(h["bot"])  # Show bot response

        # SHOW SOURCES ONLY IF PRESENT
        if "sources" in h:  # Check if sources exist for this entry
            st.write("### Sources")  # Display sources header
            for a in h["sources"]:  # Loop through article sources
                st.markdown(f"- [{a['title']}]({a['url']})")  # Display clickable article links