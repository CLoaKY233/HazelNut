from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure secret key

# Discord webhook URL
discord_webhook_url = "https://discord.com/api/webhooks/1227505796321902703/XcwCOZMFZC9q2LTZnxV9bdzgccA3_wDJhKxcXYbdb2epgh2GQyOjzeYgMIUuwCoi0MOi"

def announce_to_discord(embed):
    """Send announcement message to Discord webhook."""
    data = {"embeds": [embed]}
    response = requests.post(discord_webhook_url, json=data)
    if response.status_code == 204:
        print("Webhook message sent successfully.")
    else:
        print(f"Failed to send webhook message. Status code: {response.status_code}")

def generate_embed(title, description, priority, department, color=None, thumbnail_url=None, footer_text=None, author_name=None, author_icon=None):
    """Generate a Discord embed message."""
    current_datetime = datetime.utcnow()
    date_str = current_datetime.strftime("%Y-%m-%d")

    footer_content = f"Announcer: {author_name}" if author_name else None
    if footer_text:
        footer_content = f"{footer_content} | {footer_text}" if footer_content else footer_text
    if department:
        footer_content = f"{footer_content} | Department: {department}" if footer_content else f"Department: {department}"

    color_mapping = {"low": 3066993, "medium": 15105570, "high": 15158332}
    color = color_mapping.get(priority, color)

    embed = {
        "title": title,
        "description": description,
        "color": color,
        "author": {"name": author_name, "icon_url": author_icon} if author_name else None,
        "footer": {"text": footer_content} if footer_content else None,
        "timestamp": current_datetime.isoformat(),
        "fields": [
            {"name": "Priority", "value": priority.capitalize(), "inline": True},
            {"name": "Date", "value": date_str, "inline": True}
        ]
    }

    if thumbnail_url:
        embed["thumbnail"] = {"url": thumbnail_url}

    return embed

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the Heroku Webhook Handler!"

@app.route('/heroku/webhook/<event_type>', methods=['POST'])
def handle_heroku_event(event_type):
    """Handle Heroku webhook events."""
    data = request.json
    app_name = data.get('data', {}).get('app', {}).get('name', 'Unknown')
    status = data.get('data', {}).get('status', 'Unknown')
    created_at = data.get('data', {}).get('created_at', 'Unknown')
    user_email = data.get('data', {}).get('user', {}).get('email', 'Unknown')

    title = f"Heroku {event_type.capitalize()} Event for App {app_name}"
    description = f"Status: {status}\nUser: {user_email}\nCreated At: {created_at}"
    priority = "medium"
    department = "Heroku"
    footer_text = "Heroku Webhook"
    
    embed = generate_embed(
        title,
        description,
        priority,
        department,
        author_name=footer_text,
        author_icon="https://i.imgur.com/2lQLSjo.png",
    )
    
    announce_to_discord(embed)
    return jsonify({"message": f"{event_type} event processed successfully."}), 200

if __name__ == '__main__':
    app.run(debug=True)
