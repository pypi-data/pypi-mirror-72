from __future__ import annotations

from functools import wraps
from typing import Any, Dict

from ice3x.clients.abc import IceCubedClientBase
from ice3x.decorators import add_nonce, requires_authentication

try:
    from twisted.internet.defer import Deferred, inlineCallbacks
except ImportError:
    Deferred = None

    def inlineCallbacks(func):
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> None:
            raise ImportError(
                "twisted is required for the IceCubedAsyncClient. Try installing the with `pip install ice3x[async]`"
            )

        return inner


try:
    import treq
except ImportError:
    treq = None


class IceCubedAsyncClient(IceCubedClientBase):
    @inlineCallbacks
    def _fetch_resource(
        self, method: str, suffix: str, params: Dict[str, Any] = None
    ) -> Deferred:
        """Post request data to API."""

        if treq is None:
            raise ImportError(
                "treq is required for the IceCubedAsyncClient. Try installing the with `pip install ice3x[async]`"
            )

        if params is None:
            params = {}

        headers = {"User-Agent": "Mozilla/4.0 (compatible; Ice3x Async Python client)"}

        if method == "post":
            assert (
                self.api_key is not None
            ), f"An API key is required in order to access the {suffix} resource."

            headers["Key"] = self.api_key
            headers["Sign"] = self.sign(params)

        kwargs = {"params": params, "headers": headers}

        url = f"{self.BASE_URI}{suffix}"
        resp = yield treq.request(method, url, **kwargs)
        data = yield resp.json()
        return data

    def get_public_trade_info(self, trade_id: int, **params: Any) -> Deferred:
        """Fetch public info relating to a specified trade

        Args:
            trade_id: A valid trade id

        Returns:
            Data relating to the specified trade id
        """

        params.update({"trade_id": trade_id})
        return self._fetch_resource("get", "trade/info", params)

    def get_public_trade_list(self, **params: Any) -> Deferred:
        """Fetch a public facing list of trades

        Returns:
            A list of public trade data
        """

        return self._fetch_resource("get", "trade/list", params)

    def get_market_depth(self, **params: Any) -> Deferred:
        """Fetch the public market depth

        Returns:
            A market depth data
        """

        return self._fetch_resource("get", "stats/marketdepth", params)

    def get_pair_info(self, pair_id: int, **params: Any) -> Deferred:
        """"""

        params.update({"pair_id": pair_id})
        return self._fetch_resource("get", "pair/info", params)

    def get_pair_list(self, **params: Any) -> Deferred:
        """"""

        return self._fetch_resource("get", "pair/list", params)

    def get_currency_info(self, currency_id: int, **params: Any) -> Deferred:
        """"""

        params.update({"currency_id": currency_id})
        return self._fetch_resource("get", "currency/info", params)

    def get_currency_list(self, **params: Any) -> Deferred:
        """"""

        return self._fetch_resource("get", "currency/list", params)

    def get_orderbook_info(self, pair_id: int, **params: Any) -> Deferred:
        """"""

        params.update({"pair_id": pair_id})
        return self._fetch_resource("get", "orderbook/info", params)

    def get_market_depth_full(self, **params: Any) -> Deferred:
        """"""

        return self._fetch_resource("get", "stats/marketdepthfull", params)

    def get_market_depth_bt_cav(self, **params: Any) -> Deferred:
        """"""

        return self._fetch_resource("get", "stats/marketdepthbtcav", params)

    @add_nonce
    @requires_authentication
    def get_invoice_list(self, **params: Any) -> Deferred:
        """"""

        return self._fetch_resource("post", "invoice/list", params)

    @add_nonce
    @requires_authentication
    def get_invoice_info(self, invoice_id: int, **params: Any) -> Deferred:
        """"""

        params.update({"invoice_id": invoice_id})
        return self._fetch_resource("post", "invoice/info", params)

    @add_nonce
    @requires_authentication
    def get_invoice_pdf(self, invoice_id: int, **params: Any) -> Deferred:
        """"""

        params.update({"invoice_id": invoice_id})
        return self._fetch_resource("post", "invoice/pdf", params)

    @add_nonce
    @requires_authentication
    def cancel_order(self, order_id: int, **params: Any) -> Deferred:
        """"""

        params.update({"order_id": order_id})
        return self._fetch_resource("post", "order/cancel", params)

    @add_nonce
    @requires_authentication
    def create_order(
        self, pair_id: int, kind: str, price: float, amount: float, **params: Any
    ) -> Deferred:
        """Creates a new order given the provided inputs

        Args:
            paid_id: Currency pair id
            kind: Transaction type i.e. 'buy' or 'sell'
            price: The price to be transacted at
            volume: The volume to be transacted
        """

        params.update(
            {"pair_id": pair_id, "amount": amount, "price": price, "type": kind}
        )

        return self._fetch_resource("post", "order/new", params)

    @add_nonce
    @requires_authentication
    def get_order_info(self, order_id: int, **params: Any) -> Deferred:
        """"""

        params.update({"order_id": order_id})
        return self._fetch_resource("post", "order/info", params)

    @add_nonce
    @requires_authentication
    def get_order_list(self, **params: Any) -> Deferred:
        """"""

        return self._fetch_resource("post", "order/list", params)

    @add_nonce
    @requires_authentication
    def get_transaction_info(self, transaction_id: int, **params: Any) -> Deferred:
        """"""

        params.update({"transaction_id": transaction_id})
        return self._fetch_resource("post", "transaction/info", params)

    @add_nonce
    @requires_authentication
    def get_transaction_list(self, **params: Any) -> Deferred:
        """"""

        return self._fetch_resource("post", "transaction/list", params)

    @add_nonce
    @requires_authentication
    def get_trade_info(self, trade_id: int, **params: Any) -> Deferred:
        """"""

        params.update({"trade_id": trade_id})
        return self._fetch_resource("post", "trade/info", params)

    @add_nonce
    @requires_authentication
    def get_trade_list(self, **params: Any) -> Deferred:
        """"""

        return self._fetch_resource("post", "trade/list", params)

    @add_nonce
    @requires_authentication
    def get_balance_list(self, **params: Any) -> Deferred:
        """"""

        return self._fetch_resource("post", "balance/list", params)

    @add_nonce
    @requires_authentication
    def get_balance_info(self, currency_id: int, **params: Any) -> Deferred:
        """"""

        params.update({"currency_id": currency_id})
        return self._fetch_resource("post", "balance/info", params)
