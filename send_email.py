import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

from dotenv import load_dotenv  # pip install python-dotenv

PORT = 587  
EMAIL_SERVER = ""  # Adjust server address

# Load the environment variables
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

# Read environment variables
sender_email = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")
bcc_email=''

def send_email(subject, subscription , subscriber, sub_email , expiration_date , service_type , service_plan , service_cost):
    # Create the base text message.
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("Fotis Kordogiannis", f"{sender_email}"))
    msg["To"] = sub_email
    msg["BCC"] = sender_email

    msg.set_content(
        f"""\
        Αγαπητέ συνεργάτη {subscriber},
        Θα θέλαμε να σας ενημερώσουμε ότι το πακέτο φιλοξενίας σας ({service_type}) για το {subscription} ({service_plan}) θα λήξει στις {expiration_date}.
        {service_cost}€ + ΦΠΑ.
        Παρακαλώ πολύ όπως μας απαντήσετε σε αυτό το e-mail για την ανανέωση της παρεχόμενης υπηρεσίας και την αποφυγή απενεργοποίησης του λογαριασμού σας.
        Στην απάντηση σας, παρακαλώ να συμπεριλάβετε τα στοιχεία τιμολόγησης με την επισήμανση αν πρόκειται για τιμολόγιο ή απόδειξη.

        Με εκτίμηση,
        Fotis Kordogiannis
        """
    )
    # Add the html version.  This converts the message into a multipart/alternative
    # container, with the original text message as the first part and the new html
    # message as the second part.
    msg.add_alternative(
        f"""\
    <html>
      <body>
        <p>Αγαπητέ συνεργάτη {subscriber},</p>
        <p>Θα θέλαμε να σας ενημερώσουμε ότι το πακέτο φιλοξενίας σας ({service_type}) για το <strong>{subscription} ({service_plan})</strong> θα λήξει στις <strong>{expiration_date}.</strong></p>
        <strong><p>{service_cost}€ + ΦΠΑ.</p></strong>
        <p>Παρακαλώ πολύ όπως μας απαντήσετε σε αυτό το e-mail για την ανανέωση της παρεχόμενης υπηρεσίας και την αποφυγή απενεργοποίησης του λογαριασμού σας.</p>
        <p>Στην απάντηση σας, παρακαλώ να συμπεριλάβετε τα στοιχεία τιμολόγησης με την επισήμανση αν πρόκειται για τιμολόγιο ή απόδειξη.</p>
        <p>Με εκτίμηση,</p>
        <p>Fotis Kordogiannis</p>
      </body>
    </html>
    """,
        subtype="html",
    )

    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.sendmail(sender_email, sub_email, msg.as_string())
        server.sendmail(sender_email, bcc_email, msg.as_string()) # send bcc email
