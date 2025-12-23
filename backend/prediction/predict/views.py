from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .ml_model import HousePricePredictor

@csrf_exempt  # Dev-only: remove when wiring CSRF on frontend
def form_api(request):
    if request.method == "POST":
        import json
        try:
            data = json.loads(request.body or '{}')
            size = float(data.get("size"))
            bedrooms = int(data.get("bedrooms"))
            age = float(data.get("age"))
            print(f"Received data - Size: {size}, Bedrooms: {bedrooms}, Age: {age}")
        except (ValueError, TypeError, json.JSONDecodeError):
            return HttpResponseBadRequest("Invalid input payload")

        predictor = HousePricePredictor()
        predicted = predictor.predict(size, bedrooms, age)
        return JsonResponse({"predicted_price": predicted})

    return HttpResponseBadRequest("Only POST is supported")