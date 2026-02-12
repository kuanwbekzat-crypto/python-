
from flask import Flask, render_template, request, session
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = "super-secret-key"  # session үшін

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/lesson/<int:num>")
def lesson(num):
    return render_template(f"lesson{num}.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "messages" not in session:
        session["messages"] = []

    if request.method == "POST":
        user_message = request.form.get("message")

        session["messages"].append({
            "role": "user",
            "content": user_message
        })

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=session["messages"]
            )

            bot_message = response.choices[0].message.content

            session["messages"].append({
                "role": "assistant",
                "content": bot_message
            })

            session.modified = True

        except Exception as e:
            session["messages"].append({
                "role": "assistant",
                "content": f"Қате: {e}"
            })

    return render_template("chat.html", messages=session["messages"])

@app.route("/clear")
def clear():
    session.pop("messages", None)
    return render_template("chat.html", messages=[])

if __name__ == "__main__":
    app.run(debug=True)

