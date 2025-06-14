# config.py

from dataclasses import dataclass, field
from typing import List

@dataclass
class ResearchConfig:
    """Research-aligned configuration with enhanced features"""
    
    # Core indicators based on academic research
    RSI_PERIOD: int = 14
    BB_PERIOD: int = 20
    BB_STD: float = 2.0
    EMA_PERIOD: int = 20
    SMA_PERIOD: int = 50
    VOLUME_PERIOD: int = 20
    
    # Multi-timeframe settings
    TIMEFRAMES: List[str] = field(default_factory=lambda: ["15m", "5m"])
    
    # Logistic Regression parameters
    ML_LOOKBACK: int = 100
    ML_RETRAIN_FREQUENCY: int = 12
    MIN_TRAINING_SAMPLES: int = 20
    
    # Enhanced signal thresholds (research-aligned)
    CONFIDENCE_THRESHOLD: float = 0.5          # Minimum to send any signal
    CONFIDENCE_HIGH: float = 0.8               # Excellent signals
    CONFIDENCE_MODERATE: float = 0.7           # Good signals  
    CONFIDENCE_LOW: float = 0.6                # Fair signals
    
    # Volume analysis thresholds
    VOLUME_BREAKOUT_THRESHOLD: float = 1.5     # Volume spike threshold
    VOLUME_CONFIRM_THRESHOLD: float = 1.2      # Volume confirmation
    VOLUME_WEAK_THRESHOLD: float = 0.8         # Below average volume
    
    # TCP Configuration
    TCP_HOST: str = "localhost"
    FEATURE_PORT: int = 5556
    SIGNAL_PORT: int = 5557
    
    # Model persistence
    MODEL_PATH: str = "models/logistic_model.joblib"
    SCALER_PATH: str = "models/feature_scaler.joblib"
    
    def __post_init__(self):
        """Ensure model directory exists"""
        import os
        os.makedirs(os.path.dirname(self.MODEL_PATH), exist_ok=True)