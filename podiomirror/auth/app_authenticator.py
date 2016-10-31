from podiomirror.auth.authenticator import Authenticator
from podiomirror.auth.token import Token


class AppAuthenticator(Authenticator):
    def __init__(self, client_id, client_secret, auto_refresh=True):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auto_refresh = auto_refresh

    def get_auth_data(self, app_id, app_token):
        return {
            'grant_type': 'app',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'app_id': app_id,
            'app_token': app_token
        }

    def generate_token(self, response, app_id):
        data = response.json()
        return Token(
            self.client_id,
            self.client_secret,
            app_id,
            access_token=data['access_token'],
            token_type=data['token_type'],
            expires_in=data['expires_in'],
            refresh_token=data['refresh_token'],
            auto_refresh=self.auto_refresh
        )
