from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg.lower().startswith("goal:"):
        goal = incoming_msg.split(":", 1)[1].strip()
        prompt = f"Break down the following goal into daily learning tasks:\n\n{goal}"
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
            )
            result = response.choices[0].message.content.strip()
            msg.body(f"📋 Here's your task breakdown:\n\n{result}")
        except Exception as e:
            msg.body(f"❌ GPT error: {str(e)}")
    else:
        msg.body("👋 Hi! Send your goal like this:\n\n*Goal: Learn Java*")

    return str(resp)


@app.route("/", methods=["GET"])
def home():
    return "Bot is live with new OpenAI SDK 🚀"
