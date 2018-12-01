from datetime import date

from django.conf import settings
from django.template.loader import render_to_string


def send_contracts_to_telegram(gateway):
    context = {
        'data': date.today(),
        'contracts': [
            {'name': 'test contract'}
        ],
    }
    message = render_to_string(template_name='telegram/message.txt', context=context)
    gateway.send_message(chat_id=settings.TELEGRAM_CHAT_ID, message=message)
