from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import resend
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

resend.api_key = os.getenv("re_WuwNtqFK_35zNzCHP5XtkrqzJ393mQ52T")

class ContactForm(BaseModel):
    user_name: str
    user_email: str
    child_name: str
    user_phone: str
    message: str

@app.post("/send")
async def send_email(form: ContactForm):
    try:
        r = resend.Emails.send({
            "from": "Brainchild Schools <onboarding@resend.dev>",  # Use your verified domain here later
            "to": ["arum200909@gmail.com"],  # For testing, send to your own email
            "subject": f"New Inquiry from {form.user_name}",
            "html": f"""
                <h1>New Contact Form Submission</h1>
                <p><strong>Parent:</strong> {form.user_name}</p>
                <p><strong>Child:</strong> {form.child_name}</p>
                <p><strong>Email:</strong> {form.user_email}</p>
                <p><strong>Phone:</strong> {form.user_phone}</p>
                <p><strong>Message:</strong> {form.message}</p>
            """,
        })
        return {"message": "Email sent successfully", "id": r["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))