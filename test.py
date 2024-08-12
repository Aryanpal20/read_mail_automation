import imaplib
import email
import os 
from email.header import decode_header
from dotenv import load_dotenv

load_dotenv()


username = os.getenv('username')
password = os.getenv('password')
def connect_to_email(username, password):
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        mail.login(username, password)
        return mail
    except imaplib.IMAP4.error as e:
        print(f'Failed to login: {e}')
        return None

def fetch_emails(mail):
    try:
        mail.select('inbox')
        status, messages = mail.search(None, 'ALL')
        email_ids = messages[0].split()

        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            
            subject, encoding = decode_header(msg.get('Subject', '') or 'No Subject')[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')

            print('Subject:', subject)
            print('From:', msg.get('From'))

            body = None
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get('Content-Disposition'))

                    if content_type == 'text/plain' and 'attachment' not in content_disposition:
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                if msg.get_content_type() == 'text/plain':
                    body = msg.get_payload(decode=True).decode()

            if body:
                print('Body:', body)
            else:
                print('No plain text body found')

    except Exception as e:
        print(f'An error occurred while fetching emails: {e}')

def main():
    mail = connect_to_email(username, password)
    if mail:
        fetch_emails(mail)
        mail.close()
        mail.logout()

if __name__ == "__main__":
    main()
