from celery import shared_task
from datetime import datetime
from pathlib import Path

from .ml_model import HousePricePredictor, DATA_PATH


@shared_task
def retrain_model():
    """Scheduled retraining; uses CSV if present, otherwise synthetic data."""
    print(f"[{datetime.now()}] Starting scheduled retraining...")

    predictor = HousePricePredictor()
    try:
        if Path(DATA_PATH).exists():
            predictor.retrain_from_csv(Path(DATA_PATH))
            source = str(DATA_PATH)
            mode = "csv"
        else:
            predictor.train_model()
            source = "synthetic"
            mode = "synthetic"

        return {
            "status": "success",
            "message": "Model retrained successfully",
            "data_source": source,
            "mode": mode,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "message": str(exc),
            "timestamp": datetime.now().isoformat(),
        }


@shared_task
def predict_async(size, bedrooms, age):
    """Async prediction (optional)."""
    predictor = HousePricePredictor()
    return predictor.predict(size, bedrooms, age)