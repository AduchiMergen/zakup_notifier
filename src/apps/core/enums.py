class FileTypes:
    PAYMENT, RECEIPT, SCAN = 0, 1, 2
    FILE_TYPES: tuple = (
        (SCAN, 'Scan'),
        (PAYMENT, 'Payment'),
        (RECEIPT, 'Receipt'),
    )


class CurrencyTypes:
    RUB, USD, EUR = 0, 1, 2
    CURRENCY_TYPES = (
        (RUB, 'Rubble'),
        (USD, 'Dollar'),
        (EUR, 'Euro'),
    )


class StageTypes:
    E, EC, ET, IN = 0, 1, 2, 3
    STAGE_TYPES = (
        (E, 'Исполнение'),
        (EC, 'Исполнение завершено'),
        (ET, 'Исполнение прекращено'),
        (IN, 'Аннулирован'),
    )
