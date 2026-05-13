from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import resend
import os
from mangum import Mangum

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Later restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resend API Key
resend.api_key = os.getenv("RESEND_API_KEY")


# =========================
# DATA MODEL
# =========================
class ContactForm(BaseModel):
    user_name: str
    user_email: str
    child_name: str
    user_phone: str
    message: str


# =========================
# ROOT ROUTE
# =========================
@app.get("/")
def home():
    return {
        "message": "Brain Child School Backend Running 🚀"
    }


# =========================
# SEND EMAIL ROUTE
# =========================
@app.post("/api/send")
async def send_email(form: ContactForm):
    try:

        html_content = f"""
        <div style="font-family: Arial, sans-serif; background:#f9f5ef; padding:40px 20px; color:#2d4a3e;">

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
                            {form.user_name}
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
                            {form.child_name}
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
                            {form.user_email}
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
                            {form.user_phone}
                        </p>
                    </div>

                    <!-- MESSAGE -->
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
                            {form.message}
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

        r = resend.Emails.send({
            "from": "Brain Child <onboarding@resend.dev>",
            "to": ["info@brainchildintschools.com"],
            "subject": f"📚 New Inquiry from {form.user_name}",
            "html": html_content,
        })

        return {
            "message": "Email sent successfully",
            "id": r["id"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# AWS Lambda handler
handler = Mangum(app)
