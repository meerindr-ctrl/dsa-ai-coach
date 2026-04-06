from flask import Flask, request, jsonify
from openai import OpenAI
import random

app = Flask(__name__)
client = OpenAI(api_key="YOUR_OPENAI_KEY")

# Simple question bank
QUESTIONS = [
    {
        "question": "Explain Sliding Window",
        "concept": "Sliding Window is used for subarrays or substrings by maintaining a moving window."
    },
    {
        "question": "What is Two Pointers?",
        "concept": "Two pointers technique uses two indices to traverse data efficiently, often in sorted arrays."
    },
    {
        "question": "Explain Binary Search",
        "concept": "Binary search works on sorted arrays by repeatedly dividing the search space in half."
    }
]

@app.route("/")
def home():
    return "OK"

@app.route("/alexa", methods=["POST"])
def alexa():
    req = request.json

    if req["request"]["type"] == "LaunchRequest":
        return jsonify({
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Welcome to DSA AI Coach. Say give me a question."
                },
                "shouldEndSession": False
            }
        })
    intent_name = req["request"]["intent"]["name"]

    if intent_name == "AskQuestionIntent":
        q = random.choice(QUESTIONS)

        return jsonify({
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": q
                },
                "shouldEndSession": False
            }
        })
        
@app.route("/ask", methods=["GET"])
def ask():
    q = random.choice(QUESTIONS)
    return jsonify(q)

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.json
    question = data["question"]
    user_answer = data["answer"]
    concept = data["concept"]

    prompt = f"""
    Evaluate this DSA answer.

    Question: {question}
    Correct Concept: {concept}
    User Answer: {user_answer}

    Respond in 3 short lines:
    1. Correct or Incorrect
    2. What is wrong (if any)
    3. Correct explanation (simple)
    """

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({"feedback": response.choices[0].message.content})

if __name__ == "__main__":
    app.run()