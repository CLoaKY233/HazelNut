from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import discord
import requests
from flask import Flask, jsonify, request


app = Flask(__name__)

app.static_folder = 'assets'
app.secret_key = 'your_secret_key_here'  # Change this to a secure secret key

# Replace with your actual Discord webhook URL (keep it private)
webhook_url = "https://discord.com/api/webhooks/1220432858506596514/jSPYUE9hgfMlpWNaIusHvVqO6uFWPhnDJHfNSCuEwdPqS-nyFtRgnKQvJK-PUed61Zps"

def announce(url, embeds):
    """Send announcement message to Discord webhook."""
    data = {"embeds": embeds}
    response = requests.post(url, json=data)

    if response.status_code == 204:
        print("Webhook message sent successfully.")
    else:
        print(f"Failed to send webhook message. Status code: {response.status_code}")

def generate_embed(title, description, priority, department, color=None, thumbnail_url=None, footer_text=None, author_name=None, author_icon=None):
    """Generate a Discord embed message."""
    current_datetime = datetime.utcnow()
    date_str = current_datetime.strftime("%Y-%m-%d")

    footer_content = f"Announcer: {author_name}"  # Default footer content

    if footer_text:
        footer_content += f" | {footer_text}"
    if department:
        footer_content += f" | Department: {department}"

    # Set color based on priority
    if priority == "low":
        color = 3066993  # Green
    elif priority == "medium":
        color = 15105570  # Orange
    elif priority == "high":
        color = 15158332  # Red

    embed = {
        "title": title,
        "description": description,
        "color": color,
        "author": {"name": author_name, "icon_url": author_icon} if author_name else None,
        "footer": {"text": footer_content},
        "timestamp": current_datetime.isoformat(),
        "fields": [
            {"name": "Priority", "value": priority.capitalize(), "inline": True},
            {"name": "Date", "value": date_str, "inline": True}
        ]
    }

    if thumbnail_url:
        embed["thumbnail"] = {"url": thumbnail_url}

    return embed

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        department = request.form['department']
        footer_text = request.form['footer_text']

        embed = generate_embed(
            title,
            description,
            priority,
            department,
            author_name=footer_text,  # Using footer_text as author name
            author_icon="https://i.imgur.com/2lQLSjo.png",
        )

        announce(webhook_url, [embed])
        flash('Announcement sent successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)