import os
from app import app
from flask_mail import Mail, Message

# email server variable
email_settings = {
    "TESTNG": False,
    "MAIL_USE_TLS": False,
    "DEBUG": False,
    "MAIL_SERVER": "smtp.gmail.com",
    "MAIL_PORT": 465,
    "MAIL_USE_SSL": True,
    "MAIL_ASCII_ATTACHMENTS": True,
    "MAIL_USERNAME": os.environ.get('MAIL_USERNAME'),
    "MAIL_PASSWORD": os.environ.get('MAIL_PASSWORD'),
    "MAIL_DEFAULT_SENDER": os.environ.get('MAIL_DEFAULT_SENDER'),
    "ADMIN_EMAIL": os.environ.get('ADMIN_EMAIL')
}

app.config.update(email_settings)

mail = Mail(app)


def sendEmail(result):
    '''
    Populate results from contact form entries and
    return results via Flask Mail to specified email
    address.
    '''
    msg = Message("Contact form submission from Channel Lead Resources",
                  recipients=[email_settings["ADMIN_EMAIL"]])

    msg.body = """
    Hi there,

    A user has submiited the following feedback:

    Category Name:  {}
    Subject:    {}
    Feedback/Suggestion:   {}
    Suggestion: {}
    Name:   {}
    Slack:  {}
    Email:  {}

    Regards,
    The CI Channel Lead team

    """.format(result['category'],
               result['subject'],
               result['feedback'],
               result['feedback_url'],
               result['name'],
               result['slackName'],
               result['emailAddress']
               )

    mail.send(msg)
