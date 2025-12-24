# House Price Predictor

## Overview
Full-stack app to predict house prices using a Django REST API (backend), a React UI (frontend), and a scikit-learn regression model. Celery runs scheduled retraining; Redis (Memurai on Windows) is used as the task broker.

## Prerequisites (Windows)
- Python 3.10+ and `pip`
- Node.js 18+ and `npm`
- Redis-compatible service (Memurai recommended) or WSL Redis

## Project Structure
```
backend/
	prediction/            # Django project root
		manage.py
		prediction/          # settings, urls, celery app
		predict/             # app with views, tasks, model
frontend/
	prediction_ui/         # React (Vite + Tailwind)
```

## 1) Backend Setup
```bash
# from repo root
cd backend/prediction

# (recommended) create & activate a virtualenv
python -m venv .venv
.\.venv\Scripts\activate

# install dependencies
pip install -r ..\..\requirements.txt

# run Django migrations & start server
python manage.py migrate
python manage.py runserver
```
Backend runs at http://127.0.0.1:8000/

## 2) Broker (Redis via Memurai)
Memurai is a Redis-compatible Windows service.

```powershell
# In an elevated PowerShell (Run as Administrator)
Start-Service memurai
Get-Service memurai  # should show Status: Running
```

If you prefer WSL Redis, install WSL then run `sudo apt install -y redis-server` and `sudo service redis-server start` in WSL.

Celery uses these settings (override via env vars if needed):
- `CELERY_BROKER_URL=redis://localhost:6379/0`
- `CELERY_RESULT_BACKEND=redis://localhost:6379/1`

## 3) Celery Worker and Beat (Scheduler)
On Windows, run worker and beat in separate terminals.

Terminal A (worker):
```bash
cd backend/prediction
.\.venv\Scripts\activate
celery -A prediction worker -P solo -l info
```

Terminal B (beat):
```bash
cd backend/prediction
.\.venv\Scripts\activate
celery -A prediction beat -l info
```

Beat schedule is defined in `backend/prediction/prediction/celery.py` and triggers `predict.tasks.retrain_model` every 2 hours. If no CSV dataset is present, retraining uses synthetic data automatically.

## 4) Frontend Setup (React)
```bash
cd frontend/prediction_ui
npm install
npm run dev
```
Frontend runs at the URL printed by Vite (commonly http://localhost:5173/).

## API Endpoints
- `GET /` → simple health message
- `POST /api/predict/` → body: `{ "size": number, "bedrooms": number, "age": number }` → returns `{ "predicted_price": number }`
- `POST /api/retrain/` → enqueues background retraining task
- `GET /api/info/` → returns model metadata if available

### Quick tests
```bash
# Predict
curl -X POST http://127.0.0.1:8000/api/predict/ \
	-H "Content-Type: application/json" \
	-d "{\"size\": 2000, \"bedrooms\": 3, \"age\": 10}"

# Manual retrain
curl -X POST http://127.0.0.1:8000/api/retrain/

# Info
curl http://127.0.0.1:8000/api/info/
```

## Scheduled Retraining
- Celery Beat triggers `predict.tasks.retrain_model` periodically.
- If `backend/prediction/predict/data/new_listings.csv` exists (columns: `size,bedrooms,age,price`), it retrains from that file.
- Otherwise, it retrains using synthetic data to keep the model fresh.
- Artifacts (`model.joblib`, `scaler.joblib`, `model_metadata.json`) are stored under the `predict` app folder.

## Troubleshooting
- 404 at `/`: ensure project URLs include root → `path('', predict_views.home, name='home')` in `prediction/urls.py`.
- `-B` not supported on Windows: run worker and beat in separate terminals.
- Broker connection issues: ensure Memurai service is running; ports 6379 reachable; URLs match settings.
- CORS/CSRF during frontend POSTs: allowed origins configured in Django settings.

## Development Notes
- Default schedule: every 2 hours (`app.conf.beat_schedule` in `prediction/celery.py`). Adjust to your needs.
- To change retrain data source, drop a CSV at `backend/prediction/predict/data/new_listings.csv`.
- For production, configure `ALLOWED_HOSTS`, secure secrets, and run Redis/Celery/Django with proper process managers.
