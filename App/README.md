# Parthib's AI Assistant (Flask + Gemini + SQLite)

## Description
A small AI Assistant web app (Flask) using Gemini (Google Gen AI). Implements 3 functions:
- Answer (factual)
- Summarize (text -> summary)
- Create (creative writing)

Includes: prompt templates, SQLite logs, feedback mechanic.

## Requirements
- Python 3.9+
- pip
- Gemini API key (set in environment variable GEMINI_API_KEY)
- Recommended: a virtualenv

## Install
1. Create & activate virtualenv (optional)
   python -m venv venv
   source venv/bin/activate  # mac/linux
   venv\Scripts\activate     # windows

2. Install dependencies
   pip install -r requirements.txt

3. Set your Gemini API key:
   export GEMINI_API_KEY= (your_key_here)   # mac/linux
   set GEMINI_API_KEY= (your_key_here)      # windows

   Optionally set model:
   export GEMINI_MODEL="gemini-1.5-flash"

4. Start the app
   python app.py

5. Open http://127.0.0.1:8000 in your browser.

## If Gemini SDK isn't available
The app will fall back to a mock response so you can continue developing. Install the proper Google GenAI SDK if you want real responses.

## Database
A SQLite file `data.sqlite3` is created automatically. Use `admin/logs` to inspect logs:
http://127.0.0.1:8000/admin/logs

## Turning into React + FastAPI later
- Keep the Flask endpoints as a spec for the API.
- When ready to migrate, build a React UI and keep using `/api/assistant` and `/api/feedback`.

## Notes
- Keep prompt templates in `prompt_templates.py`.
- For production, secure your API keys and do not commit them to git.