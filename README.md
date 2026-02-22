# 📰 News Chatbot (Google News + Gemini + Streamlit)

An AI-powered News Chatbot that fetches the latest news from **Google News RSS** and generates intelligent conversational responses using **Google Gemini AI**.
The application provides an interactive chat interface built with **Streamlit**, allowing users to ask questions about current news topics.

---

## 🚀 Features

* 🔎 Fetch real-time news using Google News RSS
* 🤖 AI-generated responses using Gemini API
* 💬 Conversational chat interface with history
* 🧠 Smart prompt engineering for better summaries
* 🔢 Converts numbers to words (optional enhancement)
* 🎨 Clean and interactive Streamlit UI
* 📂 Modular project structure

---

## 🏗️ Project Structure

```
news_chatbot/
│
├── app.py                      # Main Streamlit application
│
├── services/
│   └── api_handler.py          # Google News + Gemini API calls
│
├── prompts/
│   └── prompt_manager.py       # Prompt building logic
│
├── core/
│   └── response_processor.py   # Response formatting & cleaning
│
├── requirements.txt            # Dependencies
├── .env                        # API keys (not committed)
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/news_chatbot.git
cd news_chatbot
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```
GEMINI_API_KEY=your_api_key_here
```

You can get your Gemini API key from:

👉 https://ai.google.dev/

---

## ▶️ Running the Application

```bash
streamlit run app.py
```

App will run on:

```
http://localhost:8501
```

---

## 💡 How It Works

1. User enters a news-related query.
2. App fetches relevant news from Google News RSS.
3. News content is passed to Gemini with a structured prompt.
4. Gemini generates a summarized conversational response.
5. Response is cleaned and displayed in chat format.

---

## 🧠 Technologies Used

* Python
* Streamlit
* Google News RSS
* Google Gemini API
* Regex
* Num2Words
* dotenv

---

## 🔮 Future Improvements

* Voice input support 🎤
* Multi-language news 🌍
* News sentiment analysis 📊
* Topic filtering (sports, politics, tech)
* Docker deployment 🐳

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch
3. Commit changes
4. Push to branch
5. Open Pull Request

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Your Name**

If you like this project, please ⭐ the repository!

---

