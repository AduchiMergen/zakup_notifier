from datetime import datetime
from urllib.parse import urljoin, urlencode

import django_rq
import requests
from django.conf import settings

from apps.core.jobs.queues.send_to_tg import send_contracts


def parse_contracts(date_from=datetime.utcnow()):
    bulk_items = []
    params = {
        'sort': '-price',
        'pricerange': '1000000-5000000'
    }
    url = urljoin(settings.CLEARSPENDING_URL, 'contracts/search/')

    r = requests.get(url, params=urlencode(params))
    response_data = r.json()

    contracts = response_data.get('contracts', {})
    total = contracts.get('total')
    data_list = contracts.get('data', [])

    django_rq.enqueue(send_contracts, contracts=[])
    return None
