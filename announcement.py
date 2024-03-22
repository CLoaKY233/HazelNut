import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox, QMessageBox
from PyQt5.QtCore import Qt
from datetime import datetime
import discord
import requests

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

class AnnouncementWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Enter the title of the announcement")
        layout.addWidget(self.title_edit)

        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Enter the description for your announcement")
        layout.addWidget(self.description_edit)

        self.footer_edit = QLineEdit()
        self.footer_edit.setPlaceholderText("Enter Name of the Announcer (Optional)")
        layout.addWidget(self.footer_edit)

        self.department_edit = QLineEdit()
        self.department_edit.setPlaceholderText("Enter the department name or abbreviation")
        layout.addWidget(self.department_edit)

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Medium", "High"])
        layout.addWidget(self.priority_combo)
        self.priority_combo.setCurrentIndex(0)  # Set default priority to Low        

        self.send_button = QPushButton("Send Announcement")
        self.send_button.clicked.connect(self.send_announcement)
        layout.addWidget(self.send_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

        # Apply dark mode stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                color: #FFFFFF;
                font-family: Arial, sans-serif;
                font-size: 18px;
            }

            QLabel {
                font-weight: bold;
            }

            QLineEdit, QTextEdit, QComboBox {
                border: 1px solid #434A54;
                padding: 8px;
                border-radius: 5px;
                background-color: #333333; /* Dark gray */
                color: #FFFFFF;
                font-size: 18px;
            }

            QPushButton {
                background-color: #4F83C2;
                color: #FFFFFF;
                border: none;
                padding: 12px 24px;
                border-radius: 5px;
                font-weight: bold;
                cursor: pointer;
                font-size: 18px;
            }

            QPushButton:hover {
                background-color: #5A90D2;
            }
        """)

    def send_announcement(self):
        confirmation = QMessageBox.question(self, "Confirmation", "Are you sure you want to send this announcement?", QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            title = self.title_edit.text()
            description = self.description_edit.toPlainText()
            priority = self.priority_combo.currentText().lower()
            department = self.department_edit.text()
            footer_text = self.footer_edit.text()

            embed = generate_embed(
                title,
                description,
                priority,
                department,
                author_name=footer_text,  # Using footer_text as author name
                author_icon="https://i.imgur.com/2lQLSjo.png",
            )

            announce(webhook_url, [embed])

            self.clear_inputs()

    def clear_inputs(self):
        self.title_edit.clear()
        self.description_edit.clear()
        self.priority_combo.setCurrentIndex(0)  # Reset priority to Low
        self.department_edit.clear()
        self.footer_edit.clear()

def main():
    app = QApplication(sys.argv)
    window = AnnouncementWidget()
    window.setWindowTitle("Discord Announcement Tool")
    window.showNormal()  # Open in fullscreen windowed mode
    window.resize(1600, 900)  # Set resolution to 1600x900
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
