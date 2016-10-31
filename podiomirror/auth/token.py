from datetime import datetime, timedelta

from podiomirror.transport import call_endpoint, POST


class Token:
    def __init__(self, client_id, client_secret, app_id, access_token, token_type, expires_in, refresh_token, auto_refresh=True):
        self.client_id = client_id
        self.client_secret = client_secret
        self.app_id = app_id
        self.access_token = access_token
        self.token_type = token_type
        self.expiry_time = datetime.now() + timedelta(seconds=expires_in)
        self.refresh_token = refresh_token
        self.auto_refresh = auto_refresh

    def is_token_valid(self):
        return datetime.now() < self.expiry_time

    def perform_token_refresh(self):
        refresh_data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token
        }
        response = call_endpoint('/oauth/token', POST, refresh_data)
        response.raise_for_status()

        data = response.json()
        self.access_token = data['access_token']
        self.expiry_time = datetime.now() + timedelta(seconds=int(data['expires_in']))
        self.refresh_token = data['refresh_token']

    def get_valid_token(self):
        if not self.is_token_valid():
            if self.auto_refresh:
                self.perform_token_refresh()
            else:
                raise RuntimeError('Failed to retrieve a valid token')

        return self.access_token
