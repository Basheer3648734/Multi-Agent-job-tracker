
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os

class GmailAuthenticator:
    def __init__(self, credentials_path):
        self.credentials_path = credentials_path
        self.creds = None
        self.scopes=["https://www.googleapis.com/auth/gmail.readonly"]

    def authenticate(self):
        # Load credentials from the specified path
        if os.path.exists(self.credentials_path):
            self.creds = Credentials.from_authorized_user_file(
                self.credentials_path, self.scopes
            )
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "client_secret_gmail.json", self.scopes
                )
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.credentials_path, "w") as token:
                token.write(self.creds.to_json())
        return self.creds