import joblib
import numpy as np
import pandas as pd
import os
import json
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

class HousePricePredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        
        # Check if model exists
        if os.path.exists('model.joblib') and os.path.exists('scaler.joblib'):
            self.load_model()
        else:
            self.train_model()
    
    def train_model(self):
        """Train and save model"""
        print("Training new model...")
        
        # Generate NEW data each time (different seed)
        np.random.seed(int(datetime.now().timestamp()) % 1000)
        
        data = pd.DataFrame({
            'size': np.random.uniform(1000, 5000, 1000),
            'bedrooms': np.random.randint(1, 6, 1000),
            'age': np.random.uniform(0, 50, 1000),
        })
        
        # Add some market variation
        market_trend = 1 + (datetime.now().hour / 100)  # Slight trend based on time
        
        data['price'] = (
            data['size'] * 0.2 * market_trend + 
            data['bedrooms'] * 50000 - 
            data['age'] * 1000 + 
            np.random.normal(0, 50000, 1000)
        )
        
        # Train model
        X = data[['size', 'bedrooms', 'age']]
        y = data['price']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        self.model = LinearRegression()
        self.model.fit(X_train_scaled, y_train)
        
        # Save
        joblib.dump(self.model, 'model.joblib')
        joblib.dump(self.scaler, 'scaler.joblib')
        
        # Save metadata
        metadata = {
            'trained_at': datetime.now().isoformat(),
            'training_samples': len(X_train),
            'market_trend': market_trend
        }
        
        with open('model_metadata.json', 'w') as f:
            json.dump(metadata, f)
        
        print(f"Model trained and saved at {metadata['trained_at']}")
    
    def load_model(self):
        """Load existing model"""
        print("Loading existing model...")
        self.model = joblib.load('model.joblib')
        self.scaler = joblib.load('scaler.joblib')
    
    def predict(self, size, bedrooms, age):
        """Make prediction"""
        if self.model is None:
            self.load_model()
        
        input_df = pd.DataFrame([[size, bedrooms, age]], 
                               columns=['size', 'bedrooms', 'age'])
        input_scaled = self.scaler.transform(input_df)
        
        prediction = self.model.predict(input_scaled)[0]
        return round(prediction, 2)