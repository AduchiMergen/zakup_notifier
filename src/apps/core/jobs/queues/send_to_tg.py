from django.conf import settings

from apps.scoring.services import score
from apps.telegram.gateway import TelegramGateway
from apps.telegram.services import send_contracts_to_telegram


def send_contracts(contracts: list):
    items = list()
    for contract in contracts:
        if score(contract) >= settings.SCORE:
            items.append(contract)
    if items:
        gateway = TelegramGateway(token=settings.TELEGRAM_TOKEN)
        send_contracts_to_telegram(contracts=items, gateway=gateway)
