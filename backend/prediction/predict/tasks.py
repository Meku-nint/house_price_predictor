from celery import shared_task
from .ml_model import HousePricePredictor
from datetime import datetime
@shared_task
def retrain_model():
    """Simple retraining task - runs every 2 hours"""
    print(f"[{datetime.now()}] Starting scheduled retraining...")
    
    try:
        predictor = HousePricePredictor()
        predictor.train_model()
        
        return {
            'status': 'success',
            'message': 'Model retrained successfully',
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }

@shared_task
def predict_async(size, bedrooms, age):
    """Async prediction (optional)"""
    predictor = HousePricePredictor()
    return predictor.predict(size, bedrooms, age)