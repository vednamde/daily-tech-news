import openai
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

# ==== Get credentials from environment variables ====
openai.api_key = os.environ['OPENAI_API_KEY']
SENDER_EMAIL = os.environ['EMAIL_ADDRESS']
RECEIVER_EMAIL = os.environ['EMAIL_ADDRESS']
APP_PASSWORD = os.environ['EMAIL_PASSWORD']

def get_tech_news():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a tech news summarizer."},
            {"role": "user", "content": "Give me a list of the top 5 latest tech news headlines today with clickable URLs. Format in HTML list."}
        ],
        temperature=0.7
    )
    content = response['choices'][0]['message']['content']
    return f"<h2>📰 Top Tech News for {datetime.today().strftime('%Y-%m-%d')}</h2>{content}"

def send_email(news_html):
    msg = MIMEText(news_html, 'html')
    msg['Subject'] = "Your Daily AI-Curated Tech Digest"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    news = get_tech_news()
    send_email(news)
