from datetime import date

from django.conf import settings
from django.template.loader import render_to_string


def send_contracts_to_telegram(contracts, gateway):
    context = {
        'date': date.today(),
        'contracts': (contract.tg_data for contract in contracts),
    }
    message = render_to_string(template_name='telegram/message.txt', context=context)
    gateway.send_message(chat_id=settings.TELEGRAM_CHAT_ID, message=message)
