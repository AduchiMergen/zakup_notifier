from django.db.models import Sum

from apps.contracts.models import Contract
from apps.scoring.models import ProductOkpd2Score


def score(contract: Contract):
    score = 0
    try:
        score += contract.customer.customerscore.score
    except:
        pass

    score += ProductOkpd2Score.objects.filter(
        okpd2__in=contract.products.values_list('okpd2', flat=True)
    ).aggregate(score=Sum('score')).get('score')
    return score
