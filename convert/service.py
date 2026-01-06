#covert/service.py
import requests
from django.core.cache import cache
from decimal import Decimal

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
            payload = {
                "rates": key["conversion_rates"],
                "last_updated": key["time_last_update_utc"],
            }

            cache.set(cache_key, payload, timeout=1800)


            rate = payload["rates"][to_country]
            return (Decimal(rate), payload["last_updated"])

        except (requests.RequestException, KeyError, ValueError) as e:
            raise CurrencyServiceError("Currency service unavailable") from e

    # cache hit
    try:
        rate = rate_value["rates"][to_country]
        time = rate_value["last_updated"]
        return rate, time
    except KeyError as e:
        raise CurrencyServiceError("Currency not found") from e





