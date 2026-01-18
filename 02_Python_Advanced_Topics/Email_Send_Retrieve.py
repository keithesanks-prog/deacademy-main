# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# def send_email(subject, body, to_email):
#     from_email = "axiosconsults@gmail.com"
#     password = "pxwd njlc okxg ioeu"  # You need to use an App Password, not your regular Gmail password
    
#     # Note: For Gmail, you need to:
#     # 1. Enable 2-factor authentication
#     # 2. Generate an App Password at: https://myaccount.google.com/apppasswords
#     # 3. Use the App Password here (not your regular password)
    
#     if not password:
#         print("⚠️  WARNING: Email password is empty!")
#         print("To send emails via Gmail, you need to:")
#         print("1. Enable 2-factor authentication on your Gmail account")
#         print("2. Generate an App Password at: https://myaccount.google.com/apppasswords")
#         print("3. Add the App Password to the 'from_password' variable")
#         return

#     msg = MIMEText(body)
#     msg["Subject"] = subject
#     msg["From"] = from_email
#     msg["To"] = to_email

#     try:
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#             server.login(from_email, password)
#             server.sendmail(from_email, to_email, msg.as_string())
#             print(f"✓ Email sent successfully to {to_email}")
#     except smtplib.SMTPAuthenticationError:
#         print("✗ Authentication failed. Check your email and App Password.")
#     except smtplib.SMTPException as e:
#         print(f"✗ SMTP error occurred: {e}")
#     except Exception as e:
#         print(f"✗ Error sending email: {e}")

# # Change this variable to send to a different email address
# recipient_email = "axiosconsults@gmail.com"
# send_email("Test Subject", "This is a test email.", recipient_email)

import imaplib
import email


def retrieve_email():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login("axiosconsults@gmail.com", "pxwd njlc okxg ioeu")
    mail.select("inbox")
    

    typ,data = mail.search(None, 'ALL')
    email_ids = data[0].split()


    for email_id in email_ids:
        typ,data = mail.fetch(email_id,'(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        print(f"From:{msg['From']}")
        print(f"Subject:{msg['Subject']}")

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if part.get_content_type == 'text/plain' and "attachment" not in content_disposition:
                    payload = part.get_payload(decode=True)
                    if payload:
                        try:
                            print(payload.decode())
                        except UnicodeDecodeError:
                            print("Could not decode this part.")
                    else:
                        msg.get_payload(decode=True)
                        if payload:
                            print(payload.decode())
                        else:
                            print("No decodable payload found")
    mail.close()
    mail.logout()

retrieve_email()
    
