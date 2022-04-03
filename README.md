# Python SDK for the TelePay API

![TelePay Python](https://github.com/TelePay-cash/telepay-python/blob/dev/docs/cover.jpg?raw=true)

Official TelePay client library for the Python language, so you can easely process cryptocurrency payments using the REST API.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/pypi/v/telepay?color=%2334D058&label=Version)](https://pypi.org/project/telepay)
[![Last commit](https://img.shields.io/github/last-commit/telepay-cash/telepay-python.svg?style=flat)](https://github.com/telepay-cash/telepay-python/commits)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/telepay-cash/telepay-python)](https://github.com/telepay-cash/telepay-python/commits)
[![Github Stars](https://img.shields.io/github/stars/telepay-cash/telepay-python?style=flat&logo=github)](https://github.com/telepay-cash/telepay-python/stargazers)
[![Github Forks](https://img.shields.io/github/forks/telepay-cash/telepay-python?style=flat&logo=github)](https://github.com/telepay-cash/telepay-python/network/members)
[![Github Watchers](https://img.shields.io/github/watchers/telepay-cash/telepay-python?style=flat&logo=github)](https://github.com/telepay-cash/telepay-python)
[![GitHub contributors](https://img.shields.io/github/contributors/telepay-cash/telepay-python?label=code%20contributors)](https://github.com/telepay-cash/telepay-python/graphs/contributors)


## Installation

Install the package with pip:

```bash
pip install telepay
```

Or using [Poetry](https://python-poetry.org/):

```bash
poetry add telepay
```

## Using the library

Refer to the [TelePay Docs](https://telepay.readme.io) and follow the [first steps guide](https://telepay.readme.io/reference/first-steps), you'll get your TelePay account and API key.

To make requests to the TelePay API, you need to import a client. We have two clients:
* `TelePaySyncClient`: make requests synchronously.
* `TelePayAsyncClient` make requests asynchronously.

**Import and use the client**

```python
from telepay.v1 import TelePaySyncClient, TelePayAsyncClient

client = TelePaySyncClient(secret_api_key)
client = TelePayAsyncClient(secret_api_key)
```

**Use the client as a context manager**

We recommend using the client as a context manager, like this:

```python
with TelePaySyncClient(secret_api_key) as client:
    # use the client
    ...
```

or

```python
async with TelePayAsyncClient(secret_api_key) as client:
    # use the client
    ...
```

## API endpoints

The API endpoints are documented in the [TelePay documentation](https://telepay.readme.io/reference/endpoints), refer to that pages to know more about them.

To manage the requests, if the client is async, you should use the `await` keyword, like this:

```python
response = await client.method(...)
```

Where `method` is the endpoint method.

**get_me**

Info about the current merchant. [Read docs](https://telepay.readme.io/reference/getme).

```python
account = client.get_me()
```

**get_balance**

Get your merchant wallet assets with corresponding balance. [Read docs](https://telepay.readme.io/reference/getbalance)

```python
wallets = client.get_balance()
```

**get_assets**

Get assets suported by TelePay. [Read docs](https://telepay.readme.io/reference/getassets).

```python
assets = client.get_assets()
```

**get_invoices**

Get your merchant invoices. [Read docs](https://telepay.readme.io/reference/getinvoices).

```python
invoices = client.get_invoices()
```

**get_invoice**

Get invoice details, by ID. [Read docs](https://telepay.readme.io/reference/getinvoice).

```python
invoices = client.get_invoice(number)
```

**create_invoice**

Creates an invoice, associated to your merchant. [Read docs](https://telepay.readme.io/reference/createinvoice).

```python
invoice = client.create_invoice(
    asset='TON',
    blockchain='TON',
    network='mainnet',
    amount=1,
    description='Product',
    metadata={
        'color': 'red',
        'size': 'large',
    },
    success_url='https://example.com/success',
    cancel_url='https://example.com/cancel',
    expires_at=30
)
```

## ToDo

* Transfer
* Withdraw
* Get withdraw fee
* Webhooks

## Contributors ✨

The library is made by ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://lugodev.com"><img src="https://avatars.githubusercontent.com/u/18733370?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Carlos Lugones</b></sub></a><br /><a href="https://github.com/telepay-cash/telepay-python/commits?author=lugodev" title="Code">💻</a></td>
    <td align="center"><a href="http://showwcase.com/ravenclawldz"><img src="https://avatars.githubusercontent.com/u/68219934?v=4" width="100px;" alt=""/><br /><sub><b>Ravenclaw.ldz</b></sub></a><br /><a href="https://github.com/telepay-cash/telepay-python/commits?author=ravenclawldz" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
