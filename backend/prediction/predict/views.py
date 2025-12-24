# predict/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .ml_model import HousePricePredictor
from .tasks import retrain_model, predict_async
import json
from datetime import datetime

@csrf_exempt
def predict(request):
    """Simple prediction endpoint"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            size = float(data["size"])
            bedrooms = int(data["bedrooms"])
            age = float(data["age"])
            
            predictor = HousePricePredictor()
            price = predictor.predict(size, bedrooms, age)
            
            return JsonResponse({
                "predicted_price": price,
                "timestamp": datetime.now().isoformat()
            })
        except:
            return JsonResponse({"error": "Invalid input"}, status=400)
    
    return JsonResponse({"error": "POST only"}, status=405)

@csrf_exempt
def trigger_retrain(request):
    """Manually trigger retraining"""
    if request.method == "POST":
        task = retrain_model.delay()
        return JsonResponse({
            "status": "queued",
            "task_id": task.id,
            "message": "Retraining started in background"
        })
    
    return JsonResponse({"error": "POST only"}, status=405)

@csrf_exempt
def model_info(request):
    """Get basic model info"""
    try:
        with open('model_metadata.json', 'r') as f:
            metadata = json.load(f)
        
        return JsonResponse({
            "status": "success",
            "metadata": metadata,
            "current_time": datetime.now().isoformat()
        })
    except:
        return JsonResponse({"status": "no_model"}, status=404)