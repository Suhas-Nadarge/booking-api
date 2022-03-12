from flask_mail import Message, smtplib
from flaskapp import mail, db
from flask_login import current_user
import os

# refrence : https://pythonhosted.org/Flask-Mail/
def send_email():


    with mail.connect() as conn:

        # html_message = content
        # subject = subject
        msg = Message(recipients=['nadargesuhas@gmail.com'],
                    html='<h2>Hello</h4>',
                    subject='Test')

        try:
            conn.send(msg)

        except smtplib.SMTPRecipientsRefused as e:
            pass
        
