from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from classes.ss14login.ss14exception import SS14VerificationTokenError


class SS14Login:
    """
    SS14Login Class

    This class provides functionality to perform login operations on the SS14 website.

    Attributes:
        LOGIN_URL (str): The URL of the login page.
        BASE_URL (str): The base URL of the SS14 website.
    """

    LOGIN_URL = "https://central.spacestation14.io/web/Identity/Account/Login"
    BASE_URL = "https://central.spacestation14.io/web/"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})

        self.verification_token = None

    def _get_verification_token(self) -> None:
        """
        Retrieves the verification token required for login from the login page.

        Raises:
            SS14VerificationTokenError: If the verification token is not found on the login page.
            requests.RequestException: If there is an issue accessing the login page.
        """
        response = self.session.get(self.LOGIN_URL)
        if response.status_code != 200:
            raise requests.RequestException(f"Unable to access the LOGIN_URL. Status code: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        token_element = soup.find("input", {"name": "__RequestVerificationToken"})
        if token_element:
            self.verification_token = token_element.get("value")
            return
        
        raise SS14VerificationTokenError("Element with name '__RequestVerificationToken' not found.")

    def login(self, email_or_username: str, password: str) -> bool:
        """
        Logs in to the SS14 website using the provided credentials.

        Args:
            email_or_username (str): The email or username for login.
            password (str): The password for login.

        Returns:
            bool: True if login is successful, False otherwise.

        Raises:
            requests.RequestException: If there is an issue with the login request.
        """
        if not self.verification_token:
            self._get_verification_token()

        payload = {
            "Input.EmailOrUsername": email_or_username,
            "Input.Password": password,
            "__RequestVerificationToken": self.verification_token,
            "Input.RememberMe": "false"
        }

        response = self.session.post(self.LOGIN_URL, data=payload)
        if response.status_code != 200:
            raise requests.RequestException(f"Unable to login. Status code: {response.status_code}")
        
        if urljoin(self.BASE_URL, "Identity/Account/Login") != response.url: # Fun fact. It takes you to another page, so even if there is a two-step process, it will work.
            return True
        
        return False
