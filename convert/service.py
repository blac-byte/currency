#covert/service.py
import requests
from django.core.cache import cache



class CurrencyServiceError(Exception):
    pass

def fetch_rate(from_country, to_country):
    cache_key = f"rate_{from_country}"
    rate_value = cache.get(cache_key)

    if rate_value is None:
        base_url = "https://v6.exchangerate-api.com/v6/f6b67af530c2ee053894bb8c"
        url = f"{base_url}/latest/{from_country}"

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # 🚨 IMPORTANT

            key = response.json()
            rates = key["conversion_rates"]

            cache.set(cache_key, rates, 1800)

            rate = rates[to_country]
            return rate

        except (requests.RequestException, KeyError, ValueError) as e:
            raise CurrencyServiceError("Currency service unavailable") from e

    # cache hit
    try:
        rate = rate_value[to_country]
        return rate
    except KeyError as e:
        raise CurrencyServiceError("Currency not found") from e





