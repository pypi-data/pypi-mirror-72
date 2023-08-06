import abc
import hashlib
import hmac
from typing import Any, Dict
from urllib.parse import urlencode


class IceCubedClientABC(abc.ABC):
    @abc.abstractproperty
    def _has_auth_details(self) -> bool:
        pass

    @abc.abstractmethod
    def sign(self, params: Dict[str, Any]) -> str:
        pass


class IceCubedClientBase(IceCubedClientABC):
    BASE_URI = "https://ice3x.com/api/v1/"

    def __init__(self, api_key: str = None, secret: str = None) -> None:
        """Instantiate the client

        Args:
            api_key: An ICE3X public API key
            secret: An ICE3X private API key
        """

        self.api_key = api_key
        self.secret = secret

    @property
    def _has_auth_details(self) -> bool:
        """Internal helper function which checks that an API key and secret have been provided"""

        return all([self.secret is not None, self.api_key is not None])

    def sign(self, params: Dict[str, Any]) -> str:
        """Sign a dict of query params for private API calls

        Args:
            params: A dict of query params

        Returns:
            A sha512 signed payload
        """

        assert self.secret is not None, "A client secret is required to sign requests."

        query = urlencode(params)
        signature = hmac.new(self.secret.encode(), query.encode(), hashlib.sha512)

        return signature.hexdigest()
