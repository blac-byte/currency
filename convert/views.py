#convert/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache
from convert.service import fetch_rate, CurrencyServiceError
from decimal import Decimal, ROUND_HALF_UP

def home(request): 
    if request.method == "GET":
        return render(request, "home.html")


def convert_API(request): 
    print("POST DATA:", request.POST)
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
        
    try:
        from_value=Decimal(request.POST.get("from_value"))
  
        from_country=request.POST.get("from")
        to_country=request.POST.get("to")

        rate = fetch_rate(from_country, to_country)
        amount = rate * from_value

        return JsonResponse({"result": round_cur(amount)})
    

    except CurrencyServiceError:
        return JsonResponse({"error": "Service temporarily unavailable"}, status=503)


    except (TypeError, ValueError):
        return JsonResponse({
        "error": "Invalid input"
    }, status=400)


def round_cur(amount):
    if amount is None:
        raise CurrencyServiceError("Invalid amount value")

    return Decimal(str(amount)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

class CurrencyServiceError(Exception):
    pass