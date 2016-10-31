from abc import ABC, abstractmethod

from PodioMirror.src.transport import call_endpoint, POST


class Authenticator(ABC):
    @abstractmethod
    def get_auth_data(self, app_id, app_token):
        pass

    @abstractmethod
    def generate_token(self, response, app_id):
        pass

    def authenticate_for_app(self, app_id, app_token):
        data = self.get_auth_data(app_id, app_token)
        response = call_endpoint('/oauth/token', POST, data)

        return self.generate_token(response, app_id)
