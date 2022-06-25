import random
import string

ERRORS = {
    "forbidden": "You are not authorized to perform this action.",
    "unavailable": "This action is temporarly unavailable.",
    "account.not-found": "Account not found.",
    "invoice.not-found": "Invoice not found.",
    "transfer.insufficient-funds": "Transfer failed. Insufficient funds.",
    "transfer.not-possible": "Transfer failed. Not possible to perform.",
    "withdrawal.insufficient-funds": "Withdrawal failed. Insufficient funds.",
}


def random_text(length):
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))
