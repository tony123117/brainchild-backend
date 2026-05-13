from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from mangum import Mangum

import resend
import os
import html
import time
from collections import defaultdict


# =========================================================
# APP SETUP
# =========================================================
app = FastAPI(
    title="Brain Child School API",
    version="1.0.0",
)

# =========================================================
# CORS
# =========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # Replace with frontend domain later
        # "https://brainchildintschools.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# RESEND CONFIG
# =========================================================
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

if not RESEND_API_KEY:
    raise RuntimeError("❌ RESEND_API_KEY is missing")

resend.api_key = RESEND_API_KEY


# =========================================================
# SIMPLE RATE LIMITER
# Prevent spam attacks 🛡️
# =========================================================
RATE_LIMIT = 5  # requests
RATE_WINDOW = 60  # seconds

request_log = defaultdict(list)


def rate_limiter(ip: str):
    now = time.time()

    # Keep only recent requests
    request_log[ip] = [
        t for t in request_log[ip]
        if now - t < RATE_WINDOW
    ]

    if len(request_log[ip]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please wait a minute.",
        )

    request_log[ip].append(now)


# =========================================================
# DATA MODEL
# =========================================================
class ContactForm(BaseModel):
    user_name: str = Field(..., min_length=2, max_length=100)
    user_email: EmailStr
    child_name: str = Field(..., min_length=2, max_length=100)
    user_phone: str = Field(..., min_length=7, max_length=30)
    message: str = Field(..., min_length=5, max_length=2000)


# =========================================================
# ROOT ROUTE
# =========================================================
@app.get("/")
def home():
    return {
        "message": "🚀 Brain Child School Backend Running"
    }


# =========================================================
# EMAIL TEMPLATE
# =========================================================
def build_email_template(form: ContactForm):

    # Escape user content for safety
    parent_name = html.escape(form.user_name)
    child_name = html.escape(form.child_name)
    email = html.escape(form.user_email)
    phone = html.escape(form.user_phone)
    message = html.escape(form.message).replace("\n", "<br>")

    return f"""
    <div style="
        font-family: Arial, sans-serif;
        background:#f9f5ef;
        padding:40px 20px;
        color:#2d4a3e;
    ">

        <div style="
            max-width:600px;
            margin:0 auto;
            background:#ffffff;
            border-radius:24px;
            overflow:hidden;
            box-shadow:0 10px 30px rgba(0,0,0,0.08);
            border:1px solid #ececec;
        ">

            <!-- HEADER -->
            <div style="
                background:linear-gradient(135deg, #2d4a3e, #3f6b59);
                padding:35px 24px;
                text-align:center;
                color:white;
            ">
                <h1 style="
                    margin:0;
                    font-size:30px;
                    font-weight:700;
                ">
                    📩 New Contact Submission
                </h1>

                <p style="
                    margin-top:10px;
                    font-size:14px;
                    opacity:0.9;
                ">
                    A parent just submitted an inquiry form.
                </p>
            </div>

            <!-- BODY -->
            <div style="padding:30px 24px;">

                <!-- Parent -->
                <div style="
                    background:#f8faf9;
                    border:1px solid #e7ece9;
                    padding:18px;
                    border-radius:16px;
                    margin-bottom:16px;
                ">
                    <p style="
                        margin:0;
                        font-size:12px;
                        font-weight:bold;
                        letter-spacing:1px;
                        color:#6b7280;
                        text-transform:uppercase;
                    ">
                        👨‍👩‍👧 Parent Name
                    </p>

                    <p style="
                        margin-top:8px;
                        font-size:16px;
                        font-weight:600;
                        color:#2d4a3e;
                    ">
                        {parent_name}
                    </p>
                </div>

                <!-- Child -->
                <div style="
                    background:#f8faf9;
                    border:1px solid #e7ece9;
                    padding:18px;
                    border-radius:16px;
                    margin-bottom:16px;
                ">
                    <p style="
                        margin:0;
                        font-size:12px;
                        font-weight:bold;
                        letter-spacing:1px;
                        color:#6b7280;
                        text-transform:uppercase;
                    ">
                        🧒 Child Name
                    </p>

                    <p style="
                        margin-top:8px;
                        font-size:16px;
                        font-weight:600;
                        color:#2d4a3e;
                    ">
                        {child_name}
                    </p>
                </div>

                <!-- Email -->
                <div style="
                    background:#f8faf9;
                    border:1px solid #e7ece9;
                    padding:18px;
                    border-radius:16px;
                    margin-bottom:16px;
                ">
                    <p style="
                        margin:0;
                        font-size:12px;
                        font-weight:bold;
                        letter-spacing:1px;
                        color:#6b7280;
                        text-transform:uppercase;
                    ">
                        📧 Email Address
                    </p>

                    <p style="
                        margin-top:8px;
                        font-size:16px;
                        font-weight:600;
                        color:#2d4a3e;
                    ">
                        {email}
                    </p>
                </div>

                <!-- Phone -->
                <div style="
                    background:#f8faf9;
                    border:1px solid #e7ece9;
                    padding:18px;
                    border-radius:16px;
                    margin-bottom:16px;
                ">
                    <p style="
                        margin:0;
                        font-size:12px;
                        font-weight:bold;
                        letter-spacing:1px;
                        color:#6b7280;
                        text-transform:uppercase;
                    ">
                        📞 Phone Number
                    </p>

                    <p style="
                        margin-top:8px;
                        font-size:16px;
                        font-weight:600;
                        color:#2d4a3e;
                    ">
                        {phone}
                    </p>
                </div>

                <!-- Message -->
                <div style="
                    background:#fff8e8;
                    border:1px solid #f5d97b;
                    padding:22px;
                    border-radius:18px;
                ">
                    <p style="
                        margin:0;
                        font-size:12px;
                        font-weight:bold;
                        letter-spacing:1px;
                        color:#9a6b00;
                        text-transform:uppercase;
                    ">
                        ✏️ Parent Message
                    </p>

                    <p style="
                        margin-top:14px;
                        line-height:1.8;
                        font-size:15px;
                        color:#3b3b3b;
                    ">
                        {message}
                    </p>
                </div>

            </div>

            <!-- FOOTER -->
            <div style="
                background:#f3f6f4;
                padding:18px;
                text-align:center;
                font-size:13px;
                color:#6b7280;
            ">
                🌱 Sent from Brain Child International School Website
            </div>

        </div>
    </div>
    """


# =========================================================
# SEND EMAIL ROUTE
# =========================================================
@app.post("/api/send")
async def send_email(form: ContactForm, request: Request):

    # Rate limiting
    client_ip = request.client.host
    rate_limiter(client_ip)

    try:

        html_content = build_email_template(form)

        response = resend.Emails.send({
            "from": "Brain Child School <onboarding@resend.dev>",
            "to": ["info@brainchildintschools.com"],
            "reply_to": form.user_email,
            "subject": f"📚 New Inquiry from {form.user_name}",
            "html": html_content,
        })

        return {
            "success": True,
            "message": "Email sent successfully 🚀",
            "email_id": response.get("id"),
        }

    except Exception as e:
        print("EMAIL ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail="Failed to send email",
        )


# =========================================================
# AWS LAMBDA HANDLER
# =========================================================
handler = Mangum(app)
