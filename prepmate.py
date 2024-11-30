from langdetect import detect
import spacy
from spacy.cli import download
from googletrans import Translator

# Function to dynamically load SpaCy models
def load_model(model_name):
    try:
        return spacy.load(model_name)  # Load model if available
    except OSError:
        download(model_name)  # Download model if not available
        return spacy.load(model_name)  # Load model after downloading

# Initialize Translator
translator = Translator()

# Detect the language of the text
def detect_language(text):
    return detect(text)

# Process text based on its language
def process_text_multilingual(text):
    language = detect_language(text)
    if language == "en":
        nlp = load_model("en_core_web_sm")  # Load English model dynamically
        doc = nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]
    else:
        translated = translator.translate(text, dest="en").text  # Translate to English
        nlp = load_model("en_core_web_sm")
        doc = nlp(translated)
        return [(ent.text, ent.label_) for ent in doc.ents]

# Generate Prepmate
def generate_prepmate(conversations, emails, calendar_events):
    prepmate = {
        "Context": "",
        "Time": None,
        "Location": None,
        "Participants": [],
        "Purpose": "",
        "Stakeholders": [],
        "Preparation Suggestions": []
    }

    # Process conversations
    for convo in conversations:
        prepmate["Context"] += convo.get("summary", "") + "\n"
        prepmate["Stakeholders"] += convo.get("participants", [])
        prepmate["Time"] = prepmate["Time"] or convo.get("time")
        prepmate["Location"] = prepmate["Location"] or convo.get("location")

    # Process emails
    for email in emails:
        prepmate["Time"] = prepmate["Time"] or email.get("timestamp")
        prepmate["Location"] = prepmate["Location"] or email.get("location")

        # Ensure 'from' and 'to' fields are lists
        email_from = email.get("from", [])
        email_to = email.get("to", [])

        if isinstance(email_from, str):
            email_from = [email_from]
        if isinstance(email_to, str):
            email_to = [email_to]

        prepmate["Stakeholders"] += email_from + email_to
        prepmate["Preparation Suggestions"].append(f"Check email: {email.get('subject', '')}")

    # Process calendar events
    for event in calendar_events:
        prepmate["Time"] = prepmate["Time"] or event.get("start")
        prepmate["Location"] = prepmate["Location"] or event.get("location")
        prepmate["Stakeholders"] += [attendee["email"] for attendee in event.get("attendees", [])]
        prepmate["Purpose"] += " " + event.get("summary", "")

    # Remove duplicates
    prepmate["Stakeholders"] = list(set(prepmate["Stakeholders"]))
    prepmate["Preparation Suggestions"] = list(set(prepmate["Preparation Suggestions"]))

    return prepmate

# Suggest meetings
def suggest_meetings(conversations, emails):
    suggestions = []
    for convo in conversations:
        if "potential" in convo.get("tags", []):  # Example logic
            suggestions.append({
                "meeting": f"Follow-up with {convo.get('participants', [])}",
                "reason": "Potential collaboration opportunity"
            })
    return suggestions

# Recommend resources based on conversations and emails
def recommend_resources(conversations, emails):
    resources = []

    # Process conversations to extract topics
    for convo in conversations:
        topic = convo.get("topic", "General Topic")
        resources.append({"type": "book", "title": f"Recommended book on {topic}"})
        resources.append({"type": "course", "title": f"Online course about {topic}"})

    # Process emails to extract additional resources
    for email in emails:
        subject = email.get("subject", "No Subject")
        resources.append({"type": "article", "title": f"Article related to: {subject}"})

    # Add general resources (example: Bill Gates' book recommendations)
    resources.append({"type": "book", "title": "Recommended by Bill Gates: 'The Road Ahead'"})
    resources.append({"type": "course", "title": "MIT OpenCourseWare: AI and Machine Learning"})

    return resources
