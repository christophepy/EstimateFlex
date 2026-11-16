class CurrencyService:

    def __init__(self, settings_service):
        self.settings_service = settings_service

    def convert(self, amount_eur, currency):

        settings = self.settings_service.get()

        rate = settings.exchange_rates.get(
            currency,
            1.0,
        )

        return round(
            amount_eur * rate,
            2,
        )
