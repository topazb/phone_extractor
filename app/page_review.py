# page_review.py

from flask import Flask, request, render_template, jsonify
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

app = Flask(__name__)

# Define a configuration variable to control the functionality
ENABLE_NOTIFICATIONS = True

# Define SMTP and email variables
SMTP_SERVER = os.environ.get('SMTP_SERVER')
SMTP_PORT = 587
SENDER_EMAIL = 'your_sender_email@gmail.com'
SENDER_EMAIL_PASSWORD = os.environ.get('SENDER_EMAIL_PASSWORD')
RECIPIENT_EMAIL = 'topazb@gmail.com'

# Define PUT URL and Book ID
PUT_URL_TEMPLATE = 'https://challenge22.alwaysdata.net/api/pages/{}'
BOOK_ID = '12'

@app.route('/page_review_dashboard')
def page_review_dashboard():
    return render_template('page_review_dashboard.html', ENABLE_NOTIFICATIONS=ENABLE_NOTIFICATIONS)


# Endpoint to toggle notifications
@app.route('/toggle_notifications', methods=['POST'])
def toggle_notifications():
    global ENABLE_NOTIFICATIONS
    data = request.get_json()
    ENABLE_NOTIFICATIONS = data.get('enabled', False)
    return jsonify({"message": "Notifications toggled successfully."})

# Function to send an email with additional data from the incoming request
def send_email(subject, body, page_author, page_url, page_title):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject

    # Include additional data from the incoming request in the email body
    email_body = f'''
    {body}

    Page Author: {page_author}
    Page URL: {page_url}
    Page Title: {page_title}
    '''

    msg.attach(MIMEText(email_body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
            server.quit()
            print("Email notification sent successfully.")
    except Exception as e:
        print(f"Failed to send email notification: {str(e)}")

# Function to handle the incoming request
def handle_requests(data):
    page_id = data.get('page_id')
    page_author = data.get('page_author')
    page_url = data.get('page_url')
    page_title = data.get('page_title')

    if page_id is None:
        return False, 'Missing page_id in incoming request data'

    # Check if notifications are enabled
    if ENABLE_NOTIFICATIONS:
        # Construct the PUT URL using the template
        put_url = PUT_URL_TEMPLATE.format(page_id)

        # Example: Define PUT data (modify as needed)
        put_data = {
            "book_id": BOOK_ID
        }

        # Get the authorization token from an environment variable
        authorization_token = os.environ.get('AUTHORIZATION_TOKEN')

        # Ensure the authorization token is not None before adding it to the header
        if authorization_token is not None:
            custom_header = {
                "Authorization": f"Token {authorization_token}",
                "Content-Type": "application/json"  # Set the content type as needed
            }

        # Example: Perform a PUT request
        try:
            response = requests.put(put_url, json=put_data, headers=custom_header)

            if response.status_code == 200:
                print("PUT request successfully sent.")
            else:
                print(f"Failed to send PUT request. Status code: {response.status_code}")

        except Exception as e:
            print(f"Failed to send PUT request: {str(e)}")

        # Send an email notification with additional data
        send_email('עמוד חדש מחכה לאישור', 'עמוד חדש מוסיף נתונים לגוגל שיטס.',
                   page_author, page_url, page_title)
    else:
        print("Email notifications and PUT requests are disabled.")

    return True, 'PUT request and email notification sent successfully'

if __name__ == '__main__':
    app.run(debug=True)
