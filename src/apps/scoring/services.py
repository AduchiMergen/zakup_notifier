from apps.contracts.models import Contract
from apps.scoring.models import Placer


def score(contract: Contract):
    score = 0
    placer_inn = contract.meta_data['placer']['mainInfo']['inn']
    try:
        placer = Placer.objects.get(inn=placer_inn)
        score += placer.score
    except:
        pass
    return score
