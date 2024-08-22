from google.auth.credentials import AnonymousCredentials
from google.oauth2 import service_account

class APIKeyCredential(AnonymousCredentials):
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key
    def refresh(self, request):
        pass
    def apply(self, headers, token=None):
        headers['x-goog-api-key'] = self.api_key
        # headers['x-ios-bundle-identifier'] = 'com.jarklee.py_transcript'
        # headers['Authorization'] = f'Bearer {self.api_key}'
    def before_request(self, request, method, url, headers):
        self.apply(headers)

if __name__ == '__main__':

    SCOPES = ['https://www.googleapis.com/auth/sqlservice.admin']
    SERVICE_ACCOUNT_FILE = '/path/to/service.json'

    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
