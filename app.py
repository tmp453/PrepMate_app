import spacy
from spacy.cli import download
from flask import Flask, jsonify
from prepmate import generate_prepmate, suggest_meetings, recommend_resources

app = Flask(__name__)

# Function to dynamically load SpaCy models
def load_model(model_name):
    try:
        return spacy.load(model_name)
    except OSError:
        download(model_name)
        return spacy.load(model_name)

# Local storage to hold test data
local_storage = {
    "conversations": [
        {
            "topic": "AI development",
            "summary": "Discussed AI roadmap",
            "participants": ["john@example.com"],
            "tags": ["potential"]
        }
    ],
    "emails": [
        {
            "subject": "Follow-up on AI project",
            "from": "jane@example.com",
            "to": ["john@example.com"],
            "timestamp": "2024-11-30T11:00:00"
        }
    ],
    "calendar": []
}

# Endpoint: Pre-meeting Briefs
@app.route('/prebrief', methods=['GET'])
def get_prebrief():
    # Dynamically load the English SpaCy model
    nlp = load_model("en_core_web_sm")
    
    # Process prebrief generation
    prebrief = generate_prepmate(
        local_storage["conversations"],
        local_storage["emails"],
        local_storage["calendar"]
    )
    print(f"Generated Prebrief: {prebrief}")  # Debugging log
    return jsonify(prebrief)

# Endpoint: Meeting Suggestions
@app.route('/meetingsuggestions', methods=['GET'])
def get_meetingsuggestions():
    print(f"Conversations in local_storage: {local_storage['conversations']}")  # Debugging log
    print(f"Emails in local_storage: {local_storage['emails']}")  # Debugging log

    # Dynamically load the multilingual SpaCy model if needed
    nlp_multilang = load_model("xx_ent_wiki_sm")

    # Call the suggest_meetings function with proper arguments
    suggestions = suggest_meetings(
        local_storage["conversations"],
        local_storage["emails"]
    )

    print(f"Suggestions generated: {suggestions}")  # Debugging log
    return jsonify(suggestions)

# Endpoint: Resource Recommendations
@app.route('/resourcesrecommendations', methods=['GET'])
def get_resourcesrecommendations():
    # Dynamically load the English SpaCy model for resource recommendations
    nlp = load_model("en_core_web_sm")

    recommendations = recommend_resources(
        local_storage["conversations"],
        local_storage["emails"]
    )
    print(f"Generated Resource Recommendations: {recommendations}")  # Debugging log
    return jsonify(recommendations)

# Home endpoint
@app.route('/')
def home():
    print("Accessing Home Endpoint...")  # Debugging log
    return "Welcome to PrepMate! Use /prebrief, /meetingsuggestions, or /resourcesrecommendations to access the API endpoints."

# Favicon endpoint
@app.route('/favicon.ico')
def favicon():
    return '', 204  # Return empty response with HTTP 204 status (No Content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
