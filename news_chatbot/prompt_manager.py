# Define a function to construct a prompt using conversation history, user query, and news articles
def build_prompt(history, user_query, articles):
    trimmed_history = history[-3:] # Keep only the last 3 conversation turns to avoid overly long prompts
    conversation = "\n".join([f"User: {h['user']}\nBot: {h['bot']}" for h in trimmed_history]) # Convert conversation history into a formatted string
    context_articles = "\n".join([f"- {a['title']}: {a['description']}" for a in articles]) # Convert article list into a readable context string

    # Define system-level instructions that guide the chatbot's behavior
    system_prompt = """
You are a professional news chatbot.
Role: Neutral journalist and explainer.
Constraints:
    - Summarize clearly and concisely
    - Always maintal factual accuracy
    - Cite sources when possible
    - Avoid speculation
    - Keep responses under 200 words"""

    # Create the user-specific prompt including conversation, question, and article context
    user_prompt = f"""
Conversation so far :
{conversation}

User just asked: {user_query}

Here are the recent articles:
{context_articles}

Respond conversationally, following the system instructions above.
"""
    
    # Combine system and user prompts into a single final prompt string
    return f"{system_prompt}\n{user_prompt}"