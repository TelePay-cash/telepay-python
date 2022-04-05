import hashlib
import json
from dataclasses import dataclass

import uvicorn
from colorama import Fore, Style
from fastapi import FastAPI, Request

from .errors import TelePayError

# events
INVOICE_COMPLETED = "invoice.completed"
INVOICE_CANCELLED = "invoice.cancelled"
INVOICE_EXPIRED = "invoice.expired"
INVOICE_DELETED = "invoice.deleted"


def get_signature(data, secret):
    """
    Get the webhook signature using the request data and your secret API key
    """
    hash_secret = hashlib.sha1(secret.encode()).hexdigest()
    hash_data = hashlib.sha512(data.encode()).hexdigest()
    signature = hashlib.sha512((hash_secret + hash_data).encode()).hexdigest()
    return signature


@dataclass
class TelePayWebhookListener:
    secret: str
    callback: callable
    host: str = "localhost"
    port: str = 5000
    url: str = "/webhook"
    log_level: str = "error"

    app = FastAPI()

    def __post_init__(self):
        @self.app.post(self.url)
        async def listen_webhook(request: Request):

            data = str(json.loads(await request.json()))

            request_signature = request.headers["Webhook-Signature"]

            signature = get_signature(str(data), self.secret)

            if signature != request_signature:
                raise TelePayError(
                    message="Invalid signature",
                    status_code=400,
                    # code='invalid_signature',
                )

            self.callback(request.headers, data)

            return "Thanks TelePay"

    def listen(self):
        url = f"http://{self.host}:{self.port}{self.url}"
        print(
            Fore.CYAN
            + r"""
             _____    _     ______
            |_   _|  | |    | ___ \
              | | ___| | ___| |_/ /_ _ _   _
              | |/ _ \ |/ _ \  __/ _` | | | |
              | |  __/ |  __/ | | (_| | |_| |
              \_/\___|_|\___\_|  \__,_|\__, |.cash 💎
                                        __/ |
                                       |___/
            """
        )
        print(
            Style.RESET_ALL
            + f"""
            [ Webhook listener ]

            * Docs: https://telepay.readme.io/reference/webhooks
            * Listening on {url} (Press CTRL+C to quit)
            """
        )
        uvicorn.run(self.app, host=self.host, port=self.port, log_level=self.log_level)
