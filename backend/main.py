from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from typing import Any, Dict
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI()

# OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Google Sheets Authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("path_to_your_google_service_account.json", scope)
gc = gspread.authorize(credentials)

# Email Configuration
EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_email_password"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587

class QueryModel(BaseModel):
    query: str
    context: Dict[str, Any]

class GoogleSheetModel(BaseModel):
    sheet_name: str
    data: Dict[str, Any]

class EmailModel(BaseModel):
    recipient: str
    subject: str
    message: str

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Agent Assistant!"}

@app.post("/query")
async def handle_query(query_model: QueryModel):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"{query_model.context}: {query_model.query}",
            max_tokens=150
        )
        return {"response": response.choices[0].text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/add_to_sheet")
async def add_to_google_sheet(sheet_model: GoogleSheetModel):
    try:
        # Open the Google Sheet
        sheet = gc.open(sheet_model.sheet_name).sheet1
        # Append data as a new row
        sheet.append_row(list(sheet_model.data.values()))
        return {"message": "Data successfully added to the Google Sheet."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/send_email")
async def send_email(email_model: EmailModel):
    try:
        # Create email message
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = email_model.recipient
        msg["Subject"] = email_model.subject

        # Attach message body
        msg.attach(MIMEText(email_model.message, "plain"))

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, email_model.recipient, msg.as_string())

        return {"message": "Email sent successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
