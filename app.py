from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)
key = os.getenv("OPENAI_API_KEY")
print("Loaded OpenAI Key:", key)
openai.api_key = key


@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg.lower().startswith("goal:"):
        goal = incoming_msg.split(":", 1)[1].strip()
        prompt = f"Break down the following goal into daily learning tasks:\n\n{goal}"
        try:
            reply = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
            )
            response_text = reply["choices"][0]["message"]["content"]
            msg.body(f"📋 Here's your task breakdown:\n\n{response_text}")
        except Exception:
            msg.body("❌ GPT error: Check API key or rate limits.")
    else:
        msg.body("👋 Hi! Send your goal like this:\n\n*Goal: Learn Java*")

    return str(resp)


@app.route("/", methods=["GET"])
def home():
    return "🟢 WhatsApp Bot is live."


if __name__ == "__main__":
    app.run()
