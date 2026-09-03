
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64

from GmailAuthenticator import GmailAuthenticator


class EmailFetcherService:
    def __init__(self):
        self.gmail_authenticator = GmailAuthenticator("token.json")

    def get_gmail_service(self):
        creds = self.gmail_authenticator.authenticate()
        service = build("gmail", "v1", credentials=creds)
        return service

    def fetch_emails(self, service, user_id="me", label_ids=["INBOX"], q=""):
        try:
            response=[]
            results = service.users().messages().list(userId=user_id, labelIds=label_ids, q=q, maxResults=2).execute()
            messages = results.get("messages", [])
            if not messages:
                print("No messages found.")
                return []
            for message in messages:
                msg = service.users().messages().get(userId=user_id, id=message["id"], format="full").execute()
                response.append(get_email_body(msg))

        except HttpError as error:
            print(f"An error occurred: {error}")
        return response


def get_email_body(message_response):
    """
    Extracts and decodes the plain text body from a Gmail API message response.
    """
    payload = message_response.get('payload', {})
    
    # 1. Handle Single-part emails
    if 'parts' not in payload:
        body_data = payload.get('body', {}).get('data', '')
        if body_data:
            return base64.urlsafe_b64decode(body_data).decode('utf-8')
        return ""

    # 2. Handle Multipart emails
    parts = payload.get('parts', [])
    return parse_parts(parts)


def parse_parts(parts):
    """
    Recursively iterates through parts to find 'text/plain' or 'text/html' content.
    """
    for part in parts:
        mime_type = part.get('mimeType')
        body_data = part.get('body', {}).get('data', '')

        # Return plain text content if found
        if mime_type == 'text/plain' and body_data:
            return base64.urlsafe_b64decode(body_data).decode('utf-8')
        
        # Handle nested multipart structures (e.g., multipart/alternative inside multipart/mixed)
        if 'parts' in part:
            sub_body = parse_parts(part['parts'])
            if sub_body:
                return sub_body

    return ""