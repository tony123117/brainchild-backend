# Brainchild Buddy Backend

This is the Python backend for the Brainchild Buddy application, built with FastAPI.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file and add your Resend API key:
   ```
   RESEND_API_KEY=your_actual_api_key
   ```

3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

The server will run on `http://127.0.0.1:8000`.

## API Endpoints

- `POST /send`: Send contact form email
  - Body: JSON with `user_name`, `user_email`, `child_name`, `user_phone`, `message`

## CORS

CORS is configured to allow all origins. In production, update the `allow_origins` in `main.py` to your frontend URL.