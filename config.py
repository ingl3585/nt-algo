# config.py

class Config:
    # File paths
    FEATURE_FILE = r"C:\\Users\\ingle\\OneDrive\\Desktop\\Actor_Critic_ML_NT\\features\\features.csv"
    MODEL_PATH   = r"C:\\Users\\ingle\\OneDrive\\Desktop\\Actor_Critic_ML_NT\\model\\actor_critic_model.pth"

    # Model architecture - Optimized for enhanced Ichimoku/EMA features
    INPUT_DIM   = 9     # close, volume, tenkan_kijun, price_cloud, future_cloud, ema_cross, tenkan_momentum, kijun_momentum, lwpe
    HIDDEN_DIM  = 128   # Sufficient for 9 ternary signal inputs
    ACTION_DIM  = 3     # Hold, Long, Short
    LOOKBACK    = 1

    # Training parameters - Adjusted for ternary signal complexity
    BATCH_SIZE  = 32
    GAMMA       = 0.95
    ENTROPY_COEF= 0.05
    LR          = 1e-4

    # Position sizing
    BASE_SIZE   = 4
    MAX_SIZE    = 10
    MIN_SIZE    = 1

    # Prediction parameters - Adjusted for better neutral signal handling
    TEMPERATURE = 1.8  # Slightly lower for more decisive actions with neutral signals

    # Enhanced feature weights for ternary signal confidence calculation
    ICHIMOKU_WEIGHT = 0.30     # Increased weight for enhanced Ichimoku signals
    EMA_WEIGHT = 0.20          # Weight for EMA signals  
    MOMENTUM_WEIGHT = 0.15     # Weight for momentum signals (can be neutral)
    VOLUME_WEIGHT = 0.15       # Weight for volume signals
    LWPE_WEIGHT = 0.20         # Weight for LWPE signals

    # Enhanced risk management with neutral signal considerations
    CONFIDENCE_THRESHOLD = 0.55  # Slightly lower to account for neutral signals reducing overall confidence
    MAX_DRAWDOWN_PCT = 0.02     # 2% max drawdown per trade
    
    # Signal quality thresholds
    MIN_SIGNAL_ALIGNMENT = 0.6  # Minimum signal alignment for high-confidence trades
    NEUTRAL_SIGNAL_PENALTY = 0.1  # Penalty factor for neutral signals in trending decisions
    
    # Feature normalization bounds
    PRICE_NORMALIZATION = True
    VOLUME_LOOKBACK = 20
    
    # Enhanced signal processing parameters
    SIGNAL_SMOOTHING = True      # Enable signal smoothing to reduce noise
    NEUTRAL_ZONE_SIZE = 0.0001   # Size of neutral zone as percentage of price (0.01%)
    MOMENTUM_LOOKBACK = 3        # Bars to look back for momentum calculation
    
    # Validation parameters
    MAX_NEUTRAL_SIGNALS = 4      # Maximum neutral signals before reducing confidence
    SIGNAL_VALIDATION_STRICT = True  # Enable strict signal validation