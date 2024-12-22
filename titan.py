import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Titan Email Configuration
TITAN_SMTP_SERVER = "smtp.titan.email"
TITAN_SMTP_PORT = 587
TITAN_IMAP_SERVER = "imap.titan.email"
TITAN_IMAP_PORT = 993

# Credentials
TITAN_EMAIL = "your_titan_email@example.com"
TITAN_PASSWORD = "your_secure_password"

def configure_titan_smtp():
    """
    Configures and tests the Titan SMTP server for sending emails.
    """
    try:
        # Connect to Titan SMTP server
        with smtplib.SMTP(TITAN_SMTP_SERVER, TITAN_SMTP_PORT) as server:
            server.starttls()
            server.login(TITAN_EMAIL, TITAN_PASSWORD)

            # Create a test email
            test_email = MIMEMultipart()
            test_email['From'] = TITAN_EMAIL
            test_email['To'] = TITAN_EMAIL
            test_email['Subject'] = "Titan Email Configuration Test"
            test_email.attach(MIMEText("This is a test email from Titan configuration script.", 'plain'))

            # Send the test email
            server.sendmail(TITAN_EMAIL, TITAN_EMAIL, test_email.as_string())
            print("SMTP Test Email Sent Successfully!")
    except Exception as e:
        print(f"SMTP Configuration Error: {e}")

def configure_titan_imap():
    """
    Configures and tests the Titan IMAP server for receiving emails.
    """
    try:
        # Connect to Titan IMAP server
        with imaplib.IMAP4_SSL(TITAN_IMAP_SERVER, TITAN_IMAP_PORT) as imap:
            imap.login(TITAN_EMAIL, TITAN_PASSWORD)
            imap.select('inbox')

            # Search for emails
            status, messages = imap.search(None, 'ALL')
            if status == "OK":
                print("IMAP Configuration Successful!")
                print(f"Total Emails Found: {len(messages[0].split())}")
            else:
                print("IMAP Configuration Error: Unable to fetch emails.")
    except Exception as e:
        print(f"IMAP Configuration Error: {e}")

def automate_titan_email_setup():
    """
    Automates the full Titan email setup and configuration.
    """
    print("Starting Titan Email Configuration...")
    configure_titan_smtp()
    configure_titan_imap()
    print("Titan Email Configuration Completed!")

# Run the automation
automate_titan_email_setup()