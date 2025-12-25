import joblib
import numpy as np
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

#  define the model artifact paths
BASE_DIR = Path(__file__).resolve().parent
ARTIFACT_DIR = BASE_DIR
MODEL_PATH = ARTIFACT_DIR / "model.joblib"
SCALER_PATH = ARTIFACT_DIR / "scaler.joblib"
METADATA_PATH = ARTIFACT_DIR / "model_metadata.json"
DATA_PATH = BASE_DIR / "data" / "new_listings.csv"


class HousePricePredictor:
    """Train once, then retrain on new data automatically."""

    def __init__(self):
        ARTIFACT_DIR.mkdir(exist_ok=True)
        self.model = None
        self.scaler = None

        if MODEL_PATH.exists() and SCALER_PATH.exists():
            self.load_model()
        else:
            self.train_model()

    def _fit(self, df: pd.DataFrame):
        X = df[["size", "bedrooms", "age"]]
        y = df["price"]
        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)

        self.model = LinearRegression()
        self.model.fit(X_train_scaled, y_train)

    def _save(self, market_trend: float, data_source: str):
        joblib.dump(self.model, MODEL_PATH)
        joblib.dump(self.scaler, SCALER_PATH)

        metadata = {
            "trained_at": datetime.utcnow().isoformat() + "Z",
            "training_samples": getattr(self.model, "n_samples_fit_", None),
            "market_trend": market_trend,
            "data_source": data_source,
        }
        METADATA_PATH.write_text(json.dumps(metadata, indent=2))

    def train_model(self):
        """Initial training on synthetic data (used only if no artifacts exist)."""
        np.random.seed(int(datetime.now().timestamp()) % 1000)

        data = pd.DataFrame({
            "size": np.random.uniform(1000, 5000, 1000),
            "bedrooms": np.random.randint(1, 6, 1000),
            "age": np.random.uniform(0, 50, 1000),
        })

        market_trend = 1 + (datetime.now().hour / 100)
        data["price"] = (
            data["size"] * 0.2 * market_trend
            + data["bedrooms"] * 50000
            - data["age"] * 1000
            + np.random.normal(0, 50000, 1000)
        )

        self._fit(data)
        self._save(market_trend, "synthetic")

    def retrain_from_csv(self, csv_path: Path = DATA_PATH):
        """Retrain the model using new labeled data from disk."""
        if not csv_path.exists():
            raise FileNotFoundError(f"Retrain data not found at {csv_path}")

        df = pd.read_csv(csv_path)
        required_cols = {"size", "bedrooms", "age", "price"}
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"CSV missing required columns: {sorted(missing)}")

        market_trend = 1 + (datetime.now().hour / 100)
        self._fit(df)
        self._save(market_trend, str(csv_path))

    def load_model(self):
        self.model = joblib.load(MODEL_PATH)
        self.scaler = joblib.load(SCALER_PATH)

    def predict(self, size, bedrooms, age):
        if self.model is None:
            self.load_model()

        input_df = pd.DataFrame([[size, bedrooms, age]], columns=["size", "bedrooms", "age"])
        input_scaled = self.scaler.transform(input_df)
        prediction = self.model.predict(input_scaled)[0]
        return round(prediction, 2)