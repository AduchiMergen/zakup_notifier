from datetime import datetime
from urllib.parse import urljoin, urlencode

import requests
from django.conf import settings
from django_rq import enqueue

from apps.contracts.models import (
    Contract, Customer, Supplier
)
from apps.core.utils import str_to_bool


def extend_contract(contracts):

    for contract in contracts:
        url = urljoin(settings.CLEARSPENDING_URL, 'contracts/get/')
        r = requests.get(url, params={'regnum': contract.reg_number})
        response = r.json()

