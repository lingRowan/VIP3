from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import re
from flask_cors import CORS

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Settings
SERVER_NAME = "TechHelp:chat"
WELCOME_MESSAGE = "Welcome to Tech Help! Ask your tech-related questions here."
MESSAGE_LIMIT = 50  # Limit to 50 messages
FILTER_WORDS = ["profanity1", "profanity2"]  # Add unwanted words here
MAX_AGE = timedelta(days=1)  # Messages older than this will be removed

# Available chat channels
CHANNELS = ["AI and the Web 2025", "Tech Help", "General Chat"]

# Initialize messages list with a welcome message
messages = [{"timestamp": datetime.now(), "username": "Server", "message": WELCOME_MESSAGE}]

# Function to filter unwanted words from messages
def filter_message(msg):
    for word in FILTER_WORDS:
        if word in msg.lower():
            return True
    return False

# Function to clean up old messages that exceed the MAX_AGE
def clean_old_messages():
    global messages
    now = datetime.now()
    messages = [m for m in messages if now - m["timestamp"] < MAX_AGE]

# Route to handle adding new messages
@app.route("/message", methods=["POST"])
def add_message():
    global messages
    data = request.json
    message = data.get("message", "")
    username = data.get("username", "Anonymous")

    # Check if the message contains unwanted words
    if filter_message(message):
        return jsonify({"error": "Message contains filtered content."}), 400

    # Add the message to the list
    messages.append({"timestamp": datetime.now(), "username": username, "message": message})
    clean_old_messages()

    # Limit the total number of messages
    if len(messages) > MESSAGE_LIMIT:
        messages.pop(0)  # Remove the oldest message

    # Example of active server response based on the message content
    if "help" in message.lower():
        messages.append({"timestamp": datetime.now(), "username": "Server", "message": "How can I assist you with tech today?"})

    return jsonify({"status": "Message added."})

# Route to get all messages
@app.route("/messages", methods=["GET"])
def get_messages():
    clean_old_messages()  # Clean old messages before returning the list
    return jsonify(messages)

# Route to get all available channels
@app.route("/channels", methods=["GET"])
def get_channels():
    return jsonify(CHANNELS)

# Route to add a new channel
@app.route("/add_channel", methods=["POST"])
def add_channel():
    global CHANNELS
    data = request.json
    new_channel = data.get("channel")

    if new_channel and new_channel not in CHANNELS:
        CHANNELS.append(new_channel)
        return jsonify({"channels": CHANNELS})
    else:
        return jsonify({"error": "Channel name is empty or already exists."}), 400

# Run the Flask app on port 5001
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
