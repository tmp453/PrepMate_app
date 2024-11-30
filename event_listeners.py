# Temporary storage to hold data
local_storage = {"conversations": [], "emails": [], "calendar": []}

# Store conversation data in temporary storage
def on_conversation_end(conversation_data):
    local_storage["conversations"].append(conversation_data)

# Store email data in temporary storage
def on_email_received(email_data):
    local_storage["emails"].append(email_data)

# Store calendar event data in temporary storage
def on_calendar_event_updated(event_data):
    local_storage["calendar"].append(event_data)
