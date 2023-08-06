import requests
import json
import os


class AuthException(Exception):
    """Custom exception for authentication errors"""

    def __init__(self, message):
        self.message = message


class Client:
    """Client exposes the public api for sethealth"""

    def __init__(
        self, key=os.environ["SETHEALTH_KEY"], secret=os.environ["SETHEALTH_SECRET"]
    ):
        self.key = key
        self.secret = secret

    def getToken(self, **kwargs):
        """getToken returns a new short-living token
        to be used by client side"""

        try:
            payload = {"key": self.key, "secret": self.secret}
            if "test-mode" in kwargs:
                payload["test-mode"] = kwargs.test_mode

            if "expires-in" in kwargs:
                payload["expires-in"] = kwargs.expires_in

            if "user-id" in kwargs:
                payload["user-id"] = kwargs.user_id

            response = requests.post(
                url="https://api.set.health/token",
                headers={"Content-Type": "application/json; charset=utf-8"},
                data=json.dumps(payload),
            )
            if response.status_code != 200:
                raise AuthException("Bad auth")

            jsonContent = response.json()
            if "token" not in jsonContent:
                raise AuthException("Bad response")

            return jsonContent["token"]
        except requests.exceptions.RequestException:
            raise AuthException("Bad request")
