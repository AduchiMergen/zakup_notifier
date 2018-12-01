from datetime import datetime
from urllib.parse import urljoin, urlencode

import requests
from django.conf import settings
from django_rq import enqueue

from apps.contracts.models import (
    Contract, Customer, Supplier
)
from .send_to_tg import send_contracts

PAGE_SIZE = 50


def normalize_date(date):
    if not date:
        return None
    return date[:10]


def get_or_create_customer(customer: dict):
    inn = customer.get('inn',)
    kpp = customer.get('kpp', 0)
    name = customer.get('fullName')
    reg_num = customer.get('regNum')
    address = customer.get('postalAddress')

    customer_obj, created = Customer.objects.get_or_create(
        defaults={'reg_number': reg_num},
        kpp=kpp, inn=inn, name=name, address=address
    )
    return customer_obj


def get_or_create_suppliers(suppliers: list):
    suppls = []

    def _full_name(contract):
        return ' '.join(contract.values()) if contract else 'Unknown'

    for supplier in suppliers:
        inn = supplier.get('inn')
        kpp = supplier.get('kpp', 0)
        name = supplier.get('organizationName')
        address = supplier.get('factualAddress')
        part_type = supplier.get('participantType')
        contact_name = _full_name(supplier.get('contactInfo'))

        suppl, created = Supplier.objects.get_or_create(
            defaults={'inn': inn},
            kpp=kpp, name=name, address=address, participant=part_type,
            contact_info=contact_name, inn=inn, legal_form=''
        )

        suppls.append(suppl)
    return suppliers


def _get_total_contracts(url, params):
    r = requests.get(url, params=urlencode(params))
    return r.json().get('contracts', {}).get('total')


def get_urls(url, request_params):
    pages = []
    total = _get_total_contracts(url, request_params)

    if total > 0:
        max_page = total // PAGE_SIZE \
            if total > PAGE_SIZE else 1
        if total % PAGE_SIZE > 0:
            max_page += 1

        for page in range(1, max_page + 1):
            if page > 1:
                request_params['page'] = page
            url = urljoin(url, '?' + urlencode(request_params))
            pages.append(url)

    return pages


def parse_contracts(date_from=datetime.utcnow()):
    bulk_items = []
    params = {
        'sort': '-signDate',
        'customerregion': 70,
        'pricerange': '1000000-5000000'
    }
    url = urljoin(settings.CLEARSPENDING_URL, 'contracts/search/')

    for url in get_urls(url, params):
        r = requests.get(url)
        response_data = r.json()

        contracts = response_data.get('contracts', {})
        data_list = contracts.get('data', [])

        # data_list = list(filter(lambda contr: contr.get('fz') == '44', data_list))

        for contract in data_list:
            mongo_id = contract.get('mongo_id')
            if Contract.objects.filter(ext_mongo_id=mongo_id).exists():
                continue

            item = {
                'meta_data': contract,
                'fz': contract.get('fz'),
                'price': contract.get('price'),
                'number': contract.get('number'),
                'provider_id': contract.get('id'),
                'reg_number': contract.get('regNum'),
                'form': contract.get('printFormUrl', ''),
                'ext_mongo_id': contract.get('mongo_id'),
                'region_code': contract.get('regionCode'),
                'contract_url': contract.get('contractUrl'),
                'description': contract.get('documentBase', ''),
                'sign_date': normalize_date(contract.get('signDate')),
                'publish_date': normalize_date(contract.get('publishDate')),
                'protocol_date': normalize_date(contract.get('protocolDate')),
            }
            item.update({
                'customer': get_or_create_customer(contract.get('customer', {}))
            })
            bulk_items.append(Contract(**item))

    contract_items = Contract.objects.bulk_create(
        bulk_items, batch_size=PAGE_SIZE
    )

    enqueue(send_contracts, contract_items)
    # enqueue(extend_contract, contract_items)
