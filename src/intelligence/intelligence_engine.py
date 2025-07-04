# intelligence_engine.py

import json
import numpy as np
import logging
import time

from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from src.market_analysis.data_processor import MarketData
from src.intelligence.subsystem_evolution import EnhancedIntelligenceOrchestrator
from src.market_analysis.microstructure_analyzer import MarketMicrostructureEngine
from src.intelligence.subsystems.enhanced_dopamine_subsystem import EnhancedDopamineSubsystem
from src.shared.types import Features

logger = logging.getLogger(__name__)

class IntelligenceEngine:
    def __init__(self, config, memory_file="data/intelligence_memory.json"):
        self.config = config
        self.memory_file = memory_file
        
        # Core subsystem orchestration (DNA, Temporal, Immune)
        self.orchestrator = EnhancedIntelligenceOrchestrator(config)
        
        # Microstructure analysis (4th subsystem)
        self.microstructure_engine = MarketMicrostructureEngine()
        
        # Enhanced Dopamine subsystem (5th subsystem) - Complete trading psychology system
        self.dopamine_subsystem = EnhancedDopamineSubsystem(config)
        
        # Real-time adaptation (dependency injection to avoid circular imports)
        self.adaptation_engine = None
        
        # Pattern storage
        self.patterns = defaultdict(list)
        self.recent_outcomes = deque(maxlen=100)
        
        # Bootstrap state tracking
        self.historical_processed = False
        self.bootstrap_stats = {
            'total_bars_processed': 0,
            'patterns_discovered': 0,
            'bootstrap_time': 0,
            'dna_patterns_learned': 0,
            'temporal_cycles_found': 0,
            'immune_threats_learned': 0,
            'microstructure_patterns_learned': 0
        }
        
        # Subsystem training progress tracking
        self.subsystem_training_progress = {
            'dna': {'sequences_processed': 0, 'learning_events': 0},
            'temporal': {'cycles_analyzed': 0, 'learning_events': 0},
            'immune': {'threats_detected': 0, 'learning_events': 0},
            'microstructure': {'patterns_analyzed': 0, 'learning_events': 0}
        }
        
        self.load_patterns(self.memory_file)

    def _get_adaptation_engine(self):
        """Get adaptation engine via dependency injection"""
        if self.adaptation_engine is None:
            from src.core.dependency_registry import get_service
            try:
                self.adaptation_engine = get_service('adaptation_engine')
            except ValueError:
                # Fallback to direct creation if not registered
                from src.agent.real_time_adaptation import RealTimeAdaptationEngine
                self.adaptation_engine = RealTimeAdaptationEngine(model_dim=64)
                logger.warning("Adaptation engine not in registry, created directly")
        return self.adaptation_engine

    def save_patterns(self, filepath: str):
        """Enhanced save with all subsystem patterns"""
        if not filepath or filepath.strip() == "":
            filepath = "data/intelligence_memory.json"
            logger.warning(f"Empty filepath provided, using default: {filepath}")
        
        orchestrator_stats = self.orchestrator.get_comprehensive_stats()
        microstructure_features = self.microstructure_engine.get_microstructure_features()
        adaptation_stats = self._get_adaptation_engine().get_comprehensive_stats()
        
        data = {
            'patterns': dict(self.patterns),
            'recent_outcomes': list(self.recent_outcomes),
            'historical_processed': self.historical_processed,
            'bootstrap_stats': self.bootstrap_stats,
            'subsystem_training_progress': self.subsystem_training_progress,
            'orchestrator_stats': orchestrator_stats,
            'microstructure_features': microstructure_features,
            'adaptation_stats': adaptation_stats,
            'saved_at': datetime.now().isoformat()
        }
        
        try:
            import os, numpy as np
            
            def _np_encoder(obj):
                """Convert NumPy scalars/arrays to vanilla Python types."""
                if isinstance(obj, (np.integer,)):
                    return int(obj)
                if isinstance(obj, (np.floating,)):
                    return float(obj)
                if isinstance(obj, (np.bool_,)):
                    return bool(obj)
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                raise TypeError(f"{type(obj)} is not JSON serializable")
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=_np_encoder)
                
            logger.info("Enhanced patterns saved with all four subsystems")
        except Exception as e:
            logger.error(f"Error saving enhanced patterns: {e}")
    
    def load_patterns(self, filepath: str):
        """Enhanced load with all subsystem patterns"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            self.patterns = defaultdict(list, data.get('patterns', {}))
            self.recent_outcomes = deque(data.get('recent_outcomes', []), maxlen=100)
            self.historical_processed = data.get('historical_processed', False)
            
            self.bootstrap_stats = data.get('bootstrap_stats', {
                'total_bars_processed': 0,
                'patterns_discovered': 0,
                'bootstrap_time': 0,
                'dna_patterns_learned': 0,
                'temporal_cycles_found': 0,
                'immune_threats_learned': 0,
                'microstructure_patterns_learned': 0
            })
            
            self.subsystem_training_progress = data.get('subsystem_training_progress', {
                'dna': {'sequences_processed': 0, 'learning_events': 0},
                'temporal': {'cycles_analyzed': 0, 'learning_events': 0},
                'immune': {'threats_detected': 0, 'learning_events': 0},
                'microstructure': {'patterns_analyzed': 0, 'learning_events': 0}
            })
            
            if self.historical_processed:
                orchestrator_stats = data.get('orchestrator_stats', {})
                logger.info(f"Loaded enhanced intelligence patterns with all subsystems:")
                logger.info(f"  DNA={orchestrator_stats.get('dna_evolution', {}).get('total_sequences', 0)}")
                logger.info(f"  Temporal={orchestrator_stats.get('temporal_cycles', 0)}")
                logger.info(f"  Immune={orchestrator_stats.get('immune_system', {}).get('total_antibodies', 0)}")
                logger.info(f"  Microstructure patterns loaded")
            
        except FileNotFoundError:
            logger.info("No existing enhanced patterns found, starting fresh with all subsystems")
        except Exception as e:
            logger.error(f"Error loading enhanced patterns: {e}")
        
    def bootstrap_from_historical_data(self, historical_data):
        """Enhanced bootstrap with comprehensive subsystem training"""
        logger.info("Starting comprehensive historical data bootstrap for all 4 subsystems...")
        start_time = datetime.now()
        
        try:
            # Debug the historical data structure
            logger.info(f"Historical data type: {type(historical_data)}")
            logger.info(f"Historical data keys: {list(historical_data.keys()) if isinstance(historical_data, dict) else 'Not a dict'}")
            
            total_bars = 0
            
            # Process each timeframe with comprehensive subsystem training
            for timeframe in ['4h', '1h', '15m', '5m', '1m']:
                bars_key = f'bars_{timeframe}'
                if bars_key in historical_data:
                    bars = historical_data[bars_key]
                    logger.info(f"Found {bars_key}, type: {type(bars)}, length: {len(bars) if hasattr(bars, '__len__') else 'No length'}")
                    if bars and hasattr(bars, '__len__') and len(bars) > 0:
                        logger.info(f"First item in {bars_key}: type={type(bars[0])}, content={str(bars[0])[:200]}...")
                    
                    # Enhanced processing with all subsystems
                    processed = self._process_historical_bars_comprehensive(bars, timeframe)
                    total_bars += processed
                    logger.info(f"Processed {processed} {timeframe} bars across all subsystems")
            
            # Comprehensive subsystem training phase
            self._comprehensive_subsystem_training()
            
            # Initialize adaptation engine with historical context
            self._initialize_adaptation_engine()
            
            # Update bootstrap stats with all subsystems
            self.bootstrap_stats['total_bars_processed'] = total_bars
            self.bootstrap_stats['patterns_discovered'] = self._count_total_patterns()
            self.bootstrap_stats['bootstrap_time'] = (datetime.now() - start_time).total_seconds()
            
            # Detailed subsystem stats
            orchestrator_stats = self.orchestrator.get_comprehensive_stats()
            self.bootstrap_stats['dna_patterns_learned'] = orchestrator_stats.get('dna_evolution', {}).get('total_sequences', 0)
            self.bootstrap_stats['temporal_cycles_found'] = orchestrator_stats.get('temporal_cycles', 0)
            self.bootstrap_stats['immune_threats_learned'] = orchestrator_stats.get('immune_system', {}).get('total_antibodies', 0)
            
            microstructure_features = self.microstructure_engine.get_microstructure_features()
            self.bootstrap_stats['microstructure_patterns_learned'] = microstructure_features.get('pattern_count', 0) if isinstance(microstructure_features, dict) else 0
            
            # Close progress bars after bootstrap to prevent interference with live trading logs
            self.orchestrator.close_progress_bars(self.microstructure_engine)
            
            # Mark all subsystems as live trading to prevent progress bar reinitialization
            self.orchestrator.dna_subsystem._live_trading_started = True
            self.orchestrator.temporal_subsystem._live_trading_started = True
            self.orchestrator.immune_subsystem._live_trading_started = True
            self.microstructure_engine._live_trading_started = True
            
            self.historical_processed = True
            
            logger.info(f"Enhanced bootstrap complete: {total_bars} bars processed across all subsystems")
            logger.info(f"DNA patterns: {self.bootstrap_stats['dna_patterns_learned']}")
            logger.info(f"Temporal cycles: {self.bootstrap_stats['temporal_cycles_found']}")
            logger.info(f"Immune threats: {self.bootstrap_stats['immune_threats_learned']}")
            logger.info(f"Microstructure patterns: {self.bootstrap_stats['microstructure_patterns_learned']}")
            logger.info(f"Total time: {self.bootstrap_stats['bootstrap_time']:.1f}s")
            
            self.save_patterns(self.memory_file)
            
        except Exception as e:
            logger.error(f"Enhanced bootstrap error: {e}")
            self.historical_processed = False
    
    def _process_historical_bars_comprehensive(self, bars, timeframe):
        """Process historical bars with training for all four subsystems"""
        if not bars or len(bars) < 5:  # Need more data for comprehensive training
            return 0
        
        logger.debug(f"Comprehensive processing {len(bars)} bars for {timeframe}")
        
        try:
            # Extract price/volume data
            if isinstance(bars[0], dict):
                prices = [bar['close'] for bar in bars]
                volumes = [bar['volume'] for bar in bars]
                timestamps = [bar['timestamp'] / 10000000 - 62135596800 for bar in bars]
            elif isinstance(bars[0], (list, tuple)):
                prices = [bar[4] for bar in bars]
                volumes = [bar[5] if len(bar) > 5 else 1000 for bar in bars]
                timestamps = [bar[0] / 10000000 - 62135596800 for bar in bars]
            else:
                logger.warning(f"Unknown bar data structure: {type(bars[0])}")
                return 0
                
        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Error processing bars structure: {e}")
            return 0
        
        processed_count = 0
        window_size = min(100, len(bars) // 4)  # Larger window for comprehensive training
        
        logger.info(f"Starting comprehensive processing with window_size={window_size}")
        
        # Process overlapping windows for comprehensive training
        step_size = max(1, window_size // 4)  # Overlapping windows for better training
        
        for i in range(window_size, len(bars), step_size):
            try:
                window_prices = prices[i-window_size:i+1]
                window_volumes = volumes[i-window_size:i+1]
                window_timestamps = timestamps[i-window_size:i+1]
                
                # Extract comprehensive market features
                market_features = self._extract_comprehensive_market_features(
                    window_prices, window_volumes, window_timestamps
                )
                
                # 1. DNA Subsystem Training
                dna_training_result = self._train_dna_subsystem(
                    window_prices, window_volumes, market_features
                )
                
                # 2. Temporal Subsystem Training
                temporal_training_result = self._train_temporal_subsystem(
                    window_prices, window_timestamps
                )
                
                # 3. Immune Subsystem Training
                immune_training_result = self._train_immune_subsystem(
                    market_features
                )
                
                # 4. Microstructure Subsystem Training
                microstructure_training_result = self._train_microstructure_subsystem(
                    window_prices, window_volumes
                )
                
                # Generate synthetic outcomes for training based on all subsystem signals
                synthetic_outcome = self._generate_comprehensive_synthetic_outcome(
                    dna_training_result, temporal_training_result, 
                    immune_training_result, microstructure_training_result,
                    market_features
                )
                
                # Train all subsystems with the synthetic outcome
                self._apply_comprehensive_learning(
                    dna_training_result, temporal_training_result,
                    immune_training_result, microstructure_training_result,
                    synthetic_outcome, market_features
                )
                
                processed_count += 1
                
                # Progress logging every 50 windows
                if processed_count % 50 == 0:
                    logger.info(f"Comprehensive training progress: {processed_count} windows processed for {timeframe}")
                
            except Exception as e:
                logger.error(f"Error in comprehensive window processing at {i}: {e}")
                continue
        
        logger.info(f"Comprehensive processing complete: {processed_count} windows for {timeframe}")
        
        # Add clean line break after progress bar updates for major processing phases
        if processed_count > 50 and timeframe == "1m":  # Only for 1m timeframe which has most activity
            print()
            
        return processed_count
    
    def _extract_comprehensive_market_features(self, prices: List[float], volumes: List[float],
                                             timestamps: List[float]) -> Dict:
        """Extract comprehensive features for all subsystems"""
        if len(prices) < 20:
            return {}
        
        # Enhanced feature extraction for all subsystems
        price_array = np.array(prices[-50:])
        volume_array = np.array(volumes[-50:])
        
        # Price dynamics
        returns = np.diff(price_array) / price_array[:-1]
        volatility = np.std(returns) if len(returns) > 1 else 0
        momentum = (price_array[-1] - price_array[-10]) / price_array[-10] if len(price_array) >= 10 and price_array[-10] != 0 else 0
        
        # Volume dynamics
        volume_momentum = (np.mean(volume_array[-5:]) - np.mean(volume_array[-15:-5])) / np.mean(volume_array[-15:-5]) if len(volume_array) >= 15 else 0
        volume_volatility = np.std(volume_array) / np.mean(volume_array) if np.mean(volume_array) > 0 else 0
        
        # Price-volume relationship
        price_volume_corr = np.corrcoef(price_array[-20:], volume_array[-20:])[0,1] if len(price_array) >= 20 else 0
        if np.isnan(price_volume_corr):
            price_volume_corr = 0
        
        # Position and range analysis
        price_range = max(prices) - min(prices)
        price_position = (prices[-1] - min(prices)) / price_range if price_range > 0 else 0.5
        
        # Time-based features
        if timestamps:
            try:
                dt = datetime.fromtimestamp(timestamps[-1])
                time_of_day = (dt.hour * 60 + dt.minute) / 1440
                day_of_week = dt.weekday() / 6.0
            except:
                time_of_day = 0.5
                day_of_week = 0.5
        else:
            time_of_day = 0.5
            day_of_week = 0.5
        
        # Advanced technical indicators for microstructure analysis
        rsi = self._calculate_rsi(price_array, 14) if len(price_array) >= 15 else 50
        
        # Bollinger Bands
        if len(price_array) >= 20:
            bb_upper, bb_lower = self._calculate_bollinger_bands(price_array, 20, 2)
            bb_position = (price_array[-1] - bb_lower[-1]) / (bb_upper[-1] - bb_lower[-1]) if bb_upper[-1] != bb_lower[-1] else 0.5
        else:
            bb_position = 0.5
        
        # MACD for temporal analysis
        if len(price_array) >= 26:
            ema_12 = self._calculate_ema(price_array, 12)
            ema_26 = self._calculate_ema(price_array, 26)
            macd = (ema_12[-1] - ema_26[-1]) / price_array[-1] if price_array[-1] != 0 else 0
        else:
            macd = 0
        
        # Market stress indicators for immune system
        extreme_moves = sum(1 for r in returns[-10:] if abs(r) > volatility * 2) if volatility > 0 else 0
        stress_indicator = extreme_moves / min(10, len(returns))
        
        # Liquidity indicators for microstructure
        volume_spike_count = sum(1 for i in range(-10, 0) if i < len(volume_array) and 
                               volume_array[i] > np.mean(volume_array[max(0, i-5):i]) * 1.5)
        liquidity_depth = 1.0 - (volume_spike_count / 10.0)
        
        return {
            # Core features
            'volatility': volatility,
            'price_momentum': momentum,
            'volume_momentum': volume_momentum,
            'volume_volatility': volume_volatility,
            'time_of_day': time_of_day,
            'day_of_week': day_of_week,
            'price_position': price_position,
            'price_volume_correlation': price_volume_corr,
            
            # Technical indicators
            'rsi': rsi / 100.0,  # Normalize to 0-1
            'bb_position': bb_position,
            'macd': macd,
            
            # Regime indicators
            'stress_indicator': stress_indicator,
            'liquidity_depth': liquidity_depth,
            'regime': self._classify_market_regime(volatility, momentum, stress_indicator),
            
            # Raw data for subsystems
            'returns': returns.tolist() if len(returns) > 0 else [],
            'price_changes': [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices)) if prices[i-1] != 0],
            'volume_ratios': [volumes[i] / volumes[i-1] for i in range(1, len(volumes)) if volumes[i-1] > 0]
        }
    
    def _train_dna_subsystem(self, prices: List[float], volumes: List[float], 
                           market_features: Dict) -> Dict:
        """Train DNA subsystem with enhanced pattern learning"""
        try:
            # Enhanced DNA encoding with market context
            volatility = market_features.get('volatility', 0)
            momentum = market_features.get('price_momentum', 0)
            
            dna_sequence = self.orchestrator.dna_subsystem.encode_market_state(
                prices[-20:], volumes[-20:], volatility, momentum
            )
            
            if dna_sequence:
                # Analyze the sequence
                dna_signal = self.orchestrator.dna_subsystem.analyze_sequence(dna_sequence)
                
                # Track training progress
                self.subsystem_training_progress['dna']['sequences_processed'] += 1
                
                return {
                    'subsystem': 'dna',
                    'sequence': dna_sequence,
                    'signal': dna_signal,
                    'strength': abs(dna_signal),
                    'market_context': {
                        'volatility': volatility,
                        'momentum': momentum
                    }
                }
            
        except Exception as e:
            logger.error(f"Error in DNA subsystem training: {e}")
        
        return {'subsystem': 'dna', 'signal': 0.0, 'strength': 0.0, 'sequence': ''}
    
    def _train_temporal_subsystem(self, prices: List[float], timestamps: List[float]) -> Dict:
        """Train temporal subsystem with cycle detection"""
        try:
            # Enhanced temporal analysis
            temporal_signal = self.orchestrator.temporal_subsystem.analyze_cycles(
                prices, timestamps
            )
            
            # Extract cycle information
            cycles_info = []
            if len(self.orchestrator.temporal_subsystem.dominant_cycles) > 0:
                cycles_info = list(self.orchestrator.temporal_subsystem.dominant_cycles)[-1]
            
            # Track training progress
            self.subsystem_training_progress['temporal']['cycles_analyzed'] += 1
            
            return {
                'subsystem': 'temporal',
                'signal': temporal_signal,
                'strength': abs(temporal_signal),
                'cycles_info': cycles_info,
                'cycle_count': len(cycles_info) if isinstance(cycles_info, list) else 0
            }
            
        except Exception as e:
            logger.error(f"Error in temporal subsystem training: {e}")
        
        return {'subsystem': 'temporal', 'signal': 0.0, 'strength': 0.0, 'cycles_info': []}
    
    def _train_immune_subsystem(self, market_features: Dict) -> Dict:
        """Train immune subsystem with threat detection"""
        try:
            # Enhanced threat detection
            immune_signal = self.orchestrator.immune_subsystem.detect_threats(market_features)
            
            # Track training progress
            self.subsystem_training_progress['immune']['threats_detected'] += 1
            
            # Classify threat type
            threat_type = 'none'
            if immune_signal < -0.3:
                threat_type = 'high_threat'
            elif immune_signal < -0.1:
                threat_type = 'moderate_threat'
            elif immune_signal > 0.1:
                threat_type = 'false_positive'
            
            return {
                'subsystem': 'immune',
                'signal': immune_signal,
                'strength': abs(immune_signal),
                'threat_type': threat_type,
                'antibody_count': len(self.orchestrator.immune_subsystem.antibodies)
            }
            
        except Exception as e:
            logger.error(f"Error in immune subsystem training: {e}")
        
        return {'subsystem': 'immune', 'signal': 0.0, 'strength': 0.0, 'threat_type': 'none'}
    
    def _train_microstructure_subsystem(self, prices: List[float], volumes: List[float]) -> Dict:
        """Train microstructure subsystem with order flow analysis"""
        try:
            # Enhanced microstructure analysis
            microstructure_result = self.microstructure_engine.analyze_market_state(
                prices, volumes
            )
            
            # Extract key signals
            microstructure_signal = microstructure_result.get('microstructure_signal', 0.0)
            regime_adjusted_signal = microstructure_result.get('regime_adjusted_signal', 0.0)
            
            # Extract order flow features
            order_flow = microstructure_result.get('order_flow', {})
            smart_money_flow = order_flow.get('smart_money_flow', 0.0)
            liquidity_depth = order_flow.get('liquidity_depth', 0.5)
            
            # Track training progress
            self.subsystem_training_progress['microstructure']['patterns_analyzed'] += 1
            
            return {
                'subsystem': 'microstructure',
                'signal': microstructure_signal,
                'regime_adjusted_signal': regime_adjusted_signal,
                'strength': abs(microstructure_signal),
                'smart_money_flow': smart_money_flow,
                'liquidity_depth': liquidity_depth,
                'order_flow': order_flow,
                'regime_state': microstructure_result.get('regime_state', {})
            }
            
        except Exception as e:
            logger.error(f"Error in microstructure subsystem training: {e}")
        
        return {
            'subsystem': 'microstructure', 
            'signal': 0.0, 
            'strength': 0.0,
            'smart_money_flow': 0.0,
            'liquidity_depth': 0.5
        }
    
    def _generate_comprehensive_synthetic_outcome(self, dna_result: Dict, temporal_result: Dict,
                                                immune_result: Dict, microstructure_result: Dict,
                                                market_features: Dict) -> float:
        """Generate synthetic outcome based on all four subsystem signals"""
        
        # Extract signals from all subsystems
        dna_signal = dna_result.get('signal', 0.0)
        temporal_signal = temporal_result.get('signal', 0.0)
        immune_signal = immune_result.get('signal', 0.0)
        microstructure_signal = microstructure_result.get('signal', 0.0)
        
        # Calculate signal strengths
        dna_strength = dna_result.get('strength', 0.0)
        temporal_strength = temporal_result.get('strength', 0.0)
        immune_strength = immune_result.get('strength', 0.0)
        microstructure_strength = microstructure_result.get('strength', 0.0)
        
        # Equal adaptive weights for subsystem discovery
        base_weights = {
            'dna': 0.25,
            'temporal': 0.25,
            'immune': 0.25,
            'microstructure': 0.25
        }
        
        # Adjust weights based on signal strength and market conditions
        total_strength = dna_strength + temporal_strength + immune_strength + microstructure_strength
        
        if total_strength > 0:
            # Weight by signal strength
            strength_weights = {
                'dna': dna_strength / total_strength,
                'temporal': temporal_strength / total_strength,
                'immune': immune_strength / total_strength,
                'microstructure': microstructure_strength / total_strength
            }
            
            # Combine base weights and strength weights
            final_weights = {
                'dna': base_weights['dna'] * 0.7 + strength_weights['dna'] * 0.3,
                'temporal': base_weights['temporal'] * 0.7 + strength_weights['temporal'] * 0.3,
                'immune': base_weights['immune'] * 0.7 + strength_weights['immune'] * 0.3,
                'microstructure': base_weights['microstructure'] * 0.7 + strength_weights['microstructure'] * 0.3
            }
        else:
            final_weights = base_weights
        
        # Calculate weighted signal
        weighted_signal = (
            dna_signal * final_weights['dna'] +
            temporal_signal * final_weights['temporal'] +
            immune_signal * final_weights['immune'] +
            microstructure_signal * final_weights['microstructure']
        )
        
        # Enhance signal based on consensus
        signals = [dna_signal, temporal_signal, immune_signal, microstructure_signal]
        
        # Calculate consensus
        positive_signals = sum(1 for s in signals if s > 0.1)
        negative_signals = sum(1 for s in signals if s < -0.1)
        consensus_strength = max(positive_signals, negative_signals) / len(signals)
        
        # Apply consensus bonus
        if consensus_strength > 0.75:
            weighted_signal *= 1.3  # Strong consensus bonus
        elif consensus_strength < 0.25:
            weighted_signal *= 0.7  # Weak consensus penalty
        
        # Market condition adjustments
        volatility = market_features.get('volatility', 0.02)
        if volatility > 0.05:  # High volatility reduces outcome reliability
            weighted_signal *= 0.8
        
        stress_indicator = market_features.get('stress_indicator', 0.0)
        if stress_indicator > 0.5:  # High stress reduces positive outcomes
            if weighted_signal > 0:
                weighted_signal *= 0.6
        
        # Add some noise for realistic training, but amplify for immune system training
        noise = np.random.normal(0, 0.1)
        synthetic_outcome = weighted_signal + noise

        # Amplify negative outcomes to ensure immune system learns threats
        if synthetic_outcome < -0.2:
            synthetic_outcome *= 2.0
        
        # Bound the outcome
        synthetic_outcome = float(np.clip(synthetic_outcome, -1.0, 1.0))
        
        return synthetic_outcome
    
    def _apply_comprehensive_learning(self, dna_result: Dict, temporal_result: Dict,
                                    immune_result: Dict, microstructure_result: Dict,
                                    outcome: float, market_features: Dict):
        """Apply learning to all subsystems based on synthetic outcome"""
        
        try:
            # 1. DNA Subsystem Learning
            dna_sequence = dna_result.get('sequence', '')
            if dna_sequence:
                self.orchestrator.dna_subsystem.learn_from_outcome(dna_sequence, outcome)
                self.subsystem_training_progress['dna']['learning_events'] += 1
            
            # 2. Temporal Subsystem Learning
            cycles_info = temporal_result.get('cycles_info', [])
            if cycles_info:
                self.orchestrator.temporal_subsystem.learn_from_outcome(cycles_info, outcome)
                self.subsystem_training_progress['temporal']['learning_events'] += 1
            
            # 3. Immune Subsystem Learning
            self.orchestrator.immune_subsystem.learn_threat(market_features, outcome)
            self.subsystem_training_progress['immune']['learning_events'] += 1
            
            # 4. Microstructure Subsystem Learning (with context)
            self.microstructure_engine.learn_from_outcome(outcome, microstructure_result)
            self.subsystem_training_progress['microstructure']['learning_events'] += 1
            
        except Exception as e:
            logger.error(f"Error in comprehensive learning: {e}")
    
    def _comprehensive_subsystem_training(self):
        """Additional comprehensive training phase for all subsystems"""
        logger.info("Starting comprehensive subsystem training phase...")
        
        try:
            # Cross-subsystem pattern discovery
            self._discover_cross_subsystem_patterns()
            
            # Subsystem evolution
            self._evolve_all_subsystems()
            
            # Generate synthetic market scenarios for additional training
            self._generate_synthetic_scenarios()
            
            logger.info("Comprehensive subsystem training completed")
            
        except Exception as e:
            logger.error(f"Error in comprehensive subsystem training: {e}")

    def _initialize_adaptation_engine(self):
        """Initialize the real-time adaptation engine with historical context"""
        logger.info("Initializing real-time adaptation engine with all subsystems...")
        
        # Process initialization events for each subsystem
        for i in range(10):
            self._get_adaptation_engine().process_market_event(
                'initialization',
                {
                    'pattern_count': i * 10, 
                    'bootstrap_complete': True,
                    'subsystem_count': 4,
                    'dna_patterns': self.subsystem_training_progress['dna']['sequences_processed'],
                    'temporal_cycles': self.subsystem_training_progress['temporal']['cycles_analyzed'],
                    'immune_threats': self.subsystem_training_progress['immune']['threats_detected'],
                    'microstructure_patterns': self.subsystem_training_progress['microstructure']['patterns_analyzed']
                },
                urgency=0.3
            )
    
    def _discover_cross_subsystem_patterns(self):
        """Discover patterns that involve multiple subsystems"""
        logger.info("Discovering cross-subsystem patterns...")
        
        # Get stats from all subsystems
        orchestrator_stats = self.orchestrator.get_comprehensive_stats()
        microstructure_features = self.microstructure_engine.get_microstructure_features()
        
        # Look for correlations between subsystem signals
        # This would involve analyzing historical performance of subsystem combinations
        # For now, we'll do basic pattern identification
        
        dna_patterns = orchestrator_stats.get('dna_evolution', {}).get('total_sequences', 0)
        temporal_cycles = orchestrator_stats.get('temporal_cycles', 0)
        immune_antibodies = orchestrator_stats.get('immune_system', {}).get('total_antibodies', 0)
        
        logger.info(f"Cross-pattern analysis: DNA={dna_patterns}, Temporal={temporal_cycles}, Immune={immune_antibodies}")
    
    def _evolve_all_subsystems(self):
        """Trigger evolution in all subsystems"""
        logger.info("Evolving all subsystems...")
        
        try:
            # Evolve immune system antibodies
            self.orchestrator.immune_subsystem.evolve_antibodies()
            
            # The DNA and temporal subsystems evolve automatically during learning
            
            logger.info("Subsystem evolution completed")
            
        except Exception as e:
            logger.error(f"Error in subsystem evolution: {e}")
    
    def _generate_synthetic_scenarios(self):
        """Generate synthetic market scenarios for additional training"""
        logger.info("Generating synthetic training scenarios...")
        
        # Generate various market scenarios
        scenarios = [
            # High volatility scenarios
            {'volatility': 0.08, 'momentum': 0.03, 'volume_momentum': 0.5, 'expected_outcome': -0.2},
            {'volatility': 0.09, 'momentum': -0.04, 'volume_momentum': 0.8, 'expected_outcome': -0.3},
            
            # Trending scenarios
            {'volatility': 0.02, 'momentum': 0.02, 'volume_momentum': 0.4, 'expected_outcome': 0.4},
            {'volatility': 0.025, 'momentum': -0.025, 'volume_momentum': 0.6, 'expected_outcome': 0.3},
            
            # Low volatility scenarios
            {'volatility': 0.005, 'momentum': 0.001, 'volume_momentum': 0.1, 'expected_outcome': 0.1},
            {'volatility': 0.008, 'momentum': -0.002, 'volume_momentum': -0.1, 'expected_outcome': 0.05},
        ]
        
        for scenario in scenarios:
            try:
                # Create synthetic market state
                market_state = {
                    'volatility': scenario['volatility'],
                    'price_momentum': scenario['momentum'],
                    'volume_momentum': scenario['volume_momentum'],
                    'time_of_day': 0.5,
                    'price_position': 0.5,
                    'stress_indicator': scenario['volatility'] * 10,
                    'regime': self._classify_market_regime(scenario['volatility'], scenario['momentum'], scenario['volatility'] * 10)
                }
                
                # Train immune system on synthetic scenarios
                self.orchestrator.immune_subsystem.learn_threat(market_state, scenario['expected_outcome'])
                
                # Train microstructure on synthetic scenarios
                self.microstructure_engine.learn_from_outcome(scenario['expected_outcome'])
                
            except Exception as e:
                logger.warning(f"Error in synthetic scenario training: {e}")
                continue
        
        logger.info("Synthetic scenario training completed")
    
    def _classify_market_regime(self, volatility: float, momentum: float, stress: float) -> str:
        """Classify market regime for subsystem training"""
        # Adaptive regime classification - let AI discover market states
        regime_score = stress * 2.0 + volatility * 10.0 + abs(momentum) * 50.0
        if regime_score > 2.0:  # Much higher threshold for adaptive discovery
            return 'crisis'
        elif regime_score > 1.0:  # Higher threshold
            return 'volatile' 
        else:
            return 'normal'
    
    def _calculate_rsi(self, prices: np.ndarray, period: int) -> float:
        """Calculate RSI"""
        if len(prices) < period + 1:
            return 50.0
        
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def _calculate_ema(self, prices: np.ndarray, period: int) -> np.ndarray:
        """Calculate EMA"""
        alpha = 2.0 / (period + 1)
        ema = np.zeros_like(prices)
        ema[0] = prices[0]
        
        for i in range(1, len(prices)):
            ema[i] = alpha * prices[i] + (1 - alpha) * ema[i-1]
        
        return ema
    
    def _calculate_bollinger_bands(self, prices: np.ndarray, period: int, std_dev: float):
        """Calculate Bollinger Bands"""
        if len(prices) < period:
            return np.full_like(prices, prices[-1] * 1.02), np.full_like(prices, prices[-1] * 0.98)
        
        rolling_mean = np.convolve(prices, np.ones(period)/period, mode='same')
        rolling_std = np.array([np.std(prices[max(0, i-period+1):i+1]) for i in range(len(prices))])
        
        upper_band = rolling_mean + (rolling_std * std_dev)
        lower_band = rolling_mean - (rolling_std * std_dev)
        
        return upper_band, lower_band
    
    def _calculate_enhanced_consensus(self, signals: List[float]) -> float:
        """Calculate consensus among all four subsystems"""
        if not signals:
            return 0.5
        
        # Directional agreement
        positive_signals = sum(1 for s in signals if s > 0.1)
        negative_signals = sum(1 for s in signals if s < -0.1)
        neutral_signals = sum(1 for s in signals if abs(s) <= 0.1)
        
        total_signals = len(signals)
        directional_consensus = max(positive_signals, negative_signals, neutral_signals) / total_signals
        
        # Magnitude agreement
        signal_magnitudes = [abs(s) for s in signals]
        if len(signal_magnitudes) > 1:
            magnitude_std = np.std(signal_magnitudes)
            magnitude_consensus = 1.0 / (1.0 + magnitude_std)
        else:
            magnitude_consensus = 1.0
        
        return directional_consensus * 0.7 + magnitude_consensus * 0.3
    
    def learn_from_outcome(self, trade):
        """Enhanced learning with all four subsystems"""
        outcome = trade.pnl / abs(trade.entry_price * 0.01) if trade.entry_price != 0 else 0
        
        try:
            # Enhanced learning context with all subsystems
            learning_context = {
                'dna_sequence': '',
                'cycles_info': [],
                'market_state': {},
                'microstructure_signal': 0.0
            }
            
            # Extract intelligence data if available
            if hasattr(trade, 'intelligence_data') and trade.intelligence_data:
                intelligence_data = trade.intelligence_data
                
                # DNA sequence
                if 'subsystem_outputs' in intelligence_data:
                    subsystem_outputs = intelligence_data['subsystem_outputs']
                    if isinstance(subsystem_outputs, dict):
                        learning_context['microstructure_signal'] = subsystem_outputs.get('microstructure', 0.0)
                
                # Market state for immune system
                if 'regime_context' in intelligence_data:
                    learning_context['market_state'] = intelligence_data['regime_context']
                
                # Temporal cycles
                if 'temporal_cycles' in intelligence_data:
                    learning_context['cycles_info'] = intelligence_data['temporal_cycles']
            
            # Fallback market state from trade features
            if not learning_context['market_state'] and hasattr(trade, 'features'):
                learning_context['market_state'] = {
                    'volatility': getattr(trade.features, 'volatility', 0.02),
                    'price_momentum': getattr(trade.features, 'price_momentum', 0.0),
                    'volume_momentum': getattr(trade.features, 'volume_momentum', 0.0),
                    'regime_confidence': getattr(trade.features, 'regime_confidence', 0.5)
                }
            
            # Learn in all subsystems
            self.orchestrator.learn_from_outcome(outcome, learning_context)
            
            # Learn in microstructure engine
            self.microstructure_engine.learn_from_outcome(outcome)
            
            # Learn in enhanced dopamine subsystem
            self.dopamine_subsystem.learn_from_outcome(outcome, {'trade_data': trade})
            
            # Update adaptation engine
            adaptation_context = {
                'volatility': learning_context['market_state'].get('volatility', 0.02),
                'predicted_confidence': getattr(trade, 'confidence', 0.5)
            }
            self._get_adaptation_engine().update_from_outcome(outcome, adaptation_context)
            
            # Process adaptation event
            urgency = min(1.0, abs(outcome) * 2.0)
            self._get_adaptation_engine().process_market_event(
                'trade_outcome',
                {'pnl': outcome, 'trade_data': trade},
                urgency=urgency
            )
            
            # Pattern learning
            if hasattr(trade, 'features'):
                pattern_id = self._create_pattern_id(trade.features)
                self.patterns[pattern_id].append(outcome)
                
                if len(self.patterns[pattern_id]) > 20:
                    self.patterns[pattern_id] = self.patterns[pattern_id][-20:]
            
            self.recent_outcomes.append(outcome)
            
        except Exception as e:
            logger.error(f"Error in enhanced learning from outcome: {e}")
    
    def _create_feature_tensor(self, market_features: Dict, orchestrator_result: Dict,
                             microstructure_result: Dict):
        """Create feature tensor for adaptation engine"""
        import torch
        
        features = [
            market_features.get('volatility', 0),
            market_features.get('price_momentum', 0),
            market_features.get('volume_momentum', 0),
            market_features.get('time_of_day', 0.5),
            market_features.get('price_position', 0.5),
            orchestrator_result.get('dna_signal', 0),
            orchestrator_result.get('temporal_signal', 0),
            orchestrator_result.get('immune_signal', 0),
            orchestrator_result.get('overall_signal', 0),
            microstructure_result.get('microstructure_signal', 0),
            microstructure_result.get('regime_adjusted_signal', 0),
            # Additional features for enhanced tensor
            market_features.get('margin_utilization', 0),
            market_features.get('buying_power_ratio', 1.0),
            market_features.get('daily_pnl_pct', 0.0)
        ]
        
        # Pad to 64 dimensions
        while len(features) < 64:
            features.append(0.0)
        
        return torch.tensor(features[:64], dtype=torch.float64, device='cpu')
    
    def _recognize_patterns(self, prices: np.ndarray, volumes: np.ndarray) -> float:
        """Enhanced pattern recognition with all subsystems"""
        if len(prices) < 10:
            return 0.0
            
        trend = (prices[-1] - prices[-10]) / prices[-10] if prices[-10] != 0 else 0
        vol_trend = (volumes[-1] - np.mean(volumes[-5:])) / np.mean(volumes[-5:]) if np.mean(volumes[-5:]) > 0 else 0
        
        # Enhanced pattern strength with volume confirmation
        if (trend > 0 and vol_trend > 0) or (trend < 0 and vol_trend < 0):
            pattern_strength = abs(trend) * (1 + abs(vol_trend))
        else:
            pattern_strength = abs(trend) * 0.5
        
        # Add volatility pattern detection
        volatility = np.std(prices) / np.mean(prices) if np.mean(prices) > 0 else 0
        if volatility > 0.04:  # High volatility pattern
            pattern_strength *= 0.8  # Reduce pattern confidence in high volatility
        
        return np.tanh(pattern_strength * 10)
    
    def _create_pattern_id(self, features: Features) -> str:
        """Create pattern ID for legacy compatibility with enhanced features"""
        momentum_bucket = int(features.price_momentum * 5) + 5
        position_bucket = int(features.price_position * 4)
        vol_bucket = int(features.volatility * 100) // 10
        
        # Add subsystem information to pattern ID
        dna_bucket = int((features.dna_signal + 1) * 5)
        micro_bucket = int((features.microstructure_signal + 1) * 5)
        
        return f"p{momentum_bucket}_{position_bucket}_{vol_bucket}_d{dna_bucket}_m{micro_bucket}"
    
    def _alert_timestamp_failure(self, timestamp):
        """Alert system to timestamp validation failure"""
        try:
            # Log critical alert
            logger.critical(f"SYSTEM ALERT: Timestamp validation failed - {timestamp}")
            
            # Track timestamp failures for pattern analysis
            if not hasattr(self, 'timestamp_failures'):
                self.timestamp_failures = []
            
            self.timestamp_failures.append({
                'timestamp': timestamp,
                'timestamp_type': type(timestamp).__name__,
                'time': time.time()
            })
            
            # Keep only last 100 failures
            self.timestamp_failures = self.timestamp_failures[-100:]
            
        except Exception as e:
            logger.error(f"Failed to log timestamp failure alert: {e}")
    
    def _alert_insufficient_data(self, price_count: int, volume_count: int):
        """Alert system to insufficient data for feature extraction"""
        try:
            logger.critical(f"SYSTEM ALERT: Insufficient data - Prices: {price_count}, Volumes: {volume_count}")
            
            # Track data insufficiency patterns
            if not hasattr(self, 'data_insufficiency_events'):
                self.data_insufficiency_events = []
            
            self.data_insufficiency_events.append({
                'price_count': price_count,
                'volume_count': volume_count,
                'time': time.time()
            })
            
            # Keep only last 100 events
            self.data_insufficiency_events = self.data_insufficiency_events[-100:]
            
        except Exception as e:
            logger.error(f"Failed to log data insufficiency alert: {e}")
    
    def _calculate_dynamic_signal_weights(self, signals: list, market_features: dict, consensus_strength: float) -> list:
        """Calculate dynamic weights based on signal quality, reliability, and recent performance"""
        try:
            # Initialize subsystem performance tracking if not exists
            if not hasattr(self, 'subsystem_performance'):
                self.subsystem_performance = {
                    'dna': {'correct_predictions': 0, 'total_predictions': 0, 'recent_accuracy': 0.5},
                    'temporal': {'correct_predictions': 0, 'total_predictions': 0, 'recent_accuracy': 0.5},
                    'immune': {'correct_predictions': 0, 'total_predictions': 0, 'recent_accuracy': 0.5},
                    'microstructure': {'correct_predictions': 0, 'total_predictions': 0, 'recent_accuracy': 0.5},
                    'dopamine': {'correct_predictions': 0, 'total_predictions': 0, 'recent_accuracy': 0.5}
                }
            
            # Signal quality metrics (strength, consistency, reliability)
            signal_names = ['dna', 'temporal', 'immune', 'microstructure', 'dopamine']
            base_weights = []
            
            for i, (signal, name) in enumerate(zip(signals, signal_names)):
                # 1. Signal strength component (0-1)
                signal_strength = min(1.0, abs(signal))
                
                # 2. Signal reliability based on recent performance (0-1)
                performance = self.subsystem_performance[name]
                if performance['total_predictions'] > 10:
                    reliability = performance['recent_accuracy']
                else:
                    reliability = 0.5  # Default for insufficient data
                
                # 3. Market condition suitability (0-1)
                suitability = self._calculate_subsystem_suitability(name, market_features)
                
                # 4. Signal consistency (how well it aligns with consensus)
                if consensus_strength > 0:
                    if signal * consensus_strength > 0:  # Same direction as consensus
                        consistency = min(1.0, abs(signal) / max(0.1, abs(consensus_strength)))
                    else:  # Contrarian signal
                        consistency = 0.3  # Lower weight for contrarian signals
                else:
                    consistency = 0.5  # Neutral when no consensus
                
                # Combine components with adaptive weights
                weight = (
                    signal_strength * 0.3 +      # Current signal strength
                    reliability * 0.4 +          # Historical performance  
                    suitability * 0.2 +          # Market condition fit
                    consistency * 0.1            # Consensus alignment
                )
                
                base_weights.append(max(0.05, weight))  # Minimum 5% weight
            
            # Normalize weights to sum to 1.0
            total_weight = sum(base_weights)
            if total_weight > 0:
                normalized_weights = [w / total_weight for w in base_weights]
            else:
                normalized_weights = [0.2] * 5  # Fallback to equal weights
            
            # Log weight distribution for monitoring
            if hasattr(self, 'weight_logging_counter'):
                self.weight_logging_counter += 1
            else:
                self.weight_logging_counter = 0
            
            # Log every 100 calculations to avoid spam
            if self.weight_logging_counter % 100 == 0:
                weight_str = ", ".join(f"{name}: {w:.3f}" for name, w in zip(signal_names, normalized_weights))
                logger.info(f"Dynamic signal weights - {weight_str}")
            
            return normalized_weights
            
        except Exception as e:
            logger.error(f"Error calculating dynamic signal weights: {e}")
            return [0.2, 0.2, 0.2, 0.2, 0.2]  # Fallback to equal weights
    
    def _calculate_subsystem_suitability(self, subsystem_name: str, market_features: dict) -> float:
        """Calculate how suitable a subsystem is for current market conditions"""
        try:
            volatility = market_features.get('volatility', 0.02)
            price_momentum = market_features.get('price_momentum', 0.0)
            volume_momentum = market_features.get('volume_momentum', 0.0)
            time_of_day = market_features.get('time_of_day', 0.5)
            
            # Each subsystem has different strengths in different market conditions
            if subsystem_name == 'dna':
                # DNA system works well in trending markets
                trend_strength = abs(price_momentum)
                return min(1.0, trend_strength * 3.0 + 0.3)
            
            elif subsystem_name == 'temporal':
                # Temporal system works well during specific time periods
                # Peak performance during market open/close
                time_factor = abs(time_of_day - 0.5) * 2  # Distance from midday
                return min(1.0, time_factor * 0.8 + 0.4)
            
            elif subsystem_name == 'immune':
                # Immune system excels in volatile, risky conditions
                return min(1.0, volatility * 20 + 0.2)
            
            elif subsystem_name == 'microstructure':
                # Microstructure works well with high volume activity
                volume_factor = abs(volume_momentum)
                return min(1.0, volume_factor * 2.0 + 0.3)
            
            elif subsystem_name == 'dopamine':
                # Dopamine system works consistently across conditions
                # Slight preference for moderate volatility
                vol_preference = 1.0 - abs(volatility - 0.03) * 10
                return max(0.3, min(1.0, vol_preference))
            
            else:
                return 0.5  # Default suitability
                
        except Exception as e:
            logger.error(f"Error calculating subsystem suitability for {subsystem_name}: {e}")
            return 0.5
    
    def _coordinate_subsystem_learning(self, learning_data: dict):
        """Coordinate concurrent learning phases across subsystems to prevent conflicts"""
        try:
            # Initialize learning coordination if not exists
            if not hasattr(self, 'learning_coordinator'):
                import threading
                self.learning_coordinator = {
                    'active_learners': set(),
                    'learning_queue': [],
                    'coordination_lock': threading.Lock(),
                    'max_concurrent_learners': 2,  # Limit concurrent learning
                    'learning_round': 0
                }
            
            coordinator = self.learning_coordinator
            
            with coordinator['coordination_lock']:
                # Determine which subsystems need learning updates
                subsystems_to_update = []
                
                # Priority-based learning scheduling
                learning_priorities = {
                    'dopamine': learning_data.get('trade_outcome', 0) * 2,  # Highest priority for trade outcomes
                    'immune': learning_data.get('risk_violation', 0) * 1.8,  # High priority for risk events
                    'dna': learning_data.get('pattern_match', 0) * 1.5,     # Medium-high for patterns
                    'temporal': learning_data.get('time_relevance', 0) * 1.2, # Medium for time-based
                    'microstructure': learning_data.get('volume_significance', 0) * 1.0 # Base priority
                }
                
                # Sort by priority (descending)
                sorted_subsystems = sorted(learning_priorities.items(), key=lambda x: x[1], reverse=True)
                
                # Schedule learning updates
                for subsystem_name, priority in sorted_subsystems:
                    if priority > 0.1:  # Only learn if significant priority
                        if len(coordinator['active_learners']) < coordinator['max_concurrent_learners']:
                            # Start learning immediately
                            coordinator['active_learners'].add(subsystem_name)
                            self._start_subsystem_learning(subsystem_name, learning_data, priority)
                        else:
                            # Queue for later
                            coordinator['learning_queue'].append((subsystem_name, learning_data, priority))
                
                coordinator['learning_round'] += 1
                
                # Log coordination status
                if coordinator['learning_round'] % 50 == 0:
                    active_str = ", ".join(coordinator['active_learners'])
                    queue_len = len(coordinator['learning_queue'])
                    logger.info(f"Learning coordination - Active: [{active_str}], Queued: {queue_len}")
            
        except Exception as e:
            logger.error(f"Error in subsystem learning coordination: {e}")
    
    def _start_subsystem_learning(self, subsystem_name: str, learning_data: dict, priority: float):
        """Start learning process for a specific subsystem"""
        try:
            # Update subsystem performance tracking with learning data
            if hasattr(self, 'subsystem_performance'):
                performance = self.subsystem_performance[subsystem_name]
                
                # Update prediction accuracy if we have outcome data
                if 'actual_outcome' in learning_data and 'predicted_outcome' in learning_data:
                    predicted = learning_data['predicted_outcome']
                    actual = learning_data['actual_outcome']
                    
                    # Simple accuracy: same direction = correct
                    correct = (predicted * actual) > 0
                    
                    performance['total_predictions'] += 1
                    if correct:
                        performance['correct_predictions'] += 1
                    
                    # Update recent accuracy (rolling average)
                    if performance['total_predictions'] > 0:
                        accuracy = performance['correct_predictions'] / performance['total_predictions']
                        # Weighted average: 80% historical, 20% current
                        performance['recent_accuracy'] = (
                            performance['recent_accuracy'] * 0.8 + accuracy * 0.2
                        )
                
                # Trigger actual subsystem learning
                self._trigger_subsystem_learning(subsystem_name, learning_data, priority)
                
        except Exception as e:
            logger.error(f"Error starting learning for {subsystem_name}: {e}")
        finally:
            # Remove from active learners when done
            if hasattr(self, 'learning_coordinator'):
                self.learning_coordinator['active_learners'].discard(subsystem_name)
                self._process_learning_queue()
    
    def _trigger_subsystem_learning(self, subsystem_name: str, learning_data: dict, priority: float):
        """Trigger actual learning update for specific subsystem"""
        try:
            if subsystem_name == 'dopamine' and hasattr(self.orchestrator, 'dopamine_subsystem'):
                # Update dopamine learning
                outcome = learning_data.get('trade_outcome', 0)
                if abs(outcome) > 0.01:  # Significant outcome
                    self.orchestrator.dopamine_subsystem.update_dopamine_response(outcome, priority)
            
            elif subsystem_name == 'immune' and hasattr(self.orchestrator, 'immune_subsystem'):
                # Update immune system
                risk_data = learning_data.get('risk_violation', 0)
                if risk_data > 0:
                    self.orchestrator.immune_subsystem.learn_from_threat(learning_data)
            
            elif subsystem_name == 'dna' and hasattr(self.orchestrator, 'dna_subsystem'):
                # Update DNA patterns
                pattern_data = learning_data.get('pattern_match', 0)
                if abs(pattern_data) > 0.1:
                    self.orchestrator.dna_subsystem.evolve_patterns(learning_data)
            
            elif subsystem_name == 'temporal' and hasattr(self.orchestrator, 'temporal_subsystem'):
                # Update temporal patterns
                time_data = learning_data.get('time_relevance', 0)
                if abs(time_data) > 0.1:
                    self.orchestrator.temporal_subsystem.update_cycles(learning_data)
            
            elif subsystem_name == 'microstructure':
                # Update microstructure analysis
                volume_data = learning_data.get('volume_significance', 0)
                if abs(volume_data) > 0.1:
                    if hasattr(self, 'microstructure_engine'):
                        self.microstructure_engine.learn_from_outcome(learning_data)
        
        except Exception as e:
            logger.error(f"Error triggering learning for {subsystem_name}: {e}")
    
    def _process_learning_queue(self):
        """Process queued learning requests when capacity becomes available"""
        try:
            coordinator = self.learning_coordinator
            
            while (len(coordinator['active_learners']) < coordinator['max_concurrent_learners'] and 
                   coordinator['learning_queue']):
                
                # Get highest priority item from queue
                coordinator['learning_queue'].sort(key=lambda x: x[2], reverse=True)
                subsystem_name, learning_data, priority = coordinator['learning_queue'].pop(0)
                
                # Start learning
                coordinator['active_learners'].add(subsystem_name)
                self._start_subsystem_learning(subsystem_name, learning_data, priority)
        
        except Exception as e:
            logger.error(f"Error processing learning queue: {e}")

    def _default_features(self) -> Features:
        """Enhanced default features with all subsystems"""
        return Features(
            price_momentum=0, volume_momentum=0, price_position=0.5, volatility=0,
            time_of_day=0.5, pattern_score=0, confidence=0, 
            # All five subsystem signals
            dna_signal=0, micro_signal=0, temporal_signal=0, immune_signal=0, 
            microstructure_signal=0.0, dopamine_signal=0.0, overall_signal=0,
            # Enhanced features
            regime_adjusted_signal=0.0, adaptation_quality=0.5,
            smart_money_flow=0.0, liquidity_depth=0.5, regime_confidence=0.5
        )
    
    def _count_total_patterns(self) -> int:
        """Count total patterns across all subsystems"""
        orchestrator_stats = self.orchestrator.get_comprehensive_stats()
        
        total = 0
        dna_stats = orchestrator_stats.get('dna_evolution', {})
        total += dna_stats.get('total_sequences', 0)
        
        immune_stats = orchestrator_stats.get('immune_system', {})
        total += immune_stats.get('total_antibodies', 0)
        
        total += orchestrator_stats.get('temporal_cycles', 0)
        total += len(self.patterns)
        
        # Add microstructure patterns
        microstructure_features = self.microstructure_engine.get_microstructure_features()
        if isinstance(microstructure_features, dict):
            total += len(microstructure_features.get('patterns', {}))
        
        return total

    def get_stats(self) -> Dict:
        """Enhanced statistics with all four subsystems"""
        orchestrator_stats = self.orchestrator.get_comprehensive_stats()
        adaptation_stats = self._get_adaptation_engine().get_comprehensive_stats()
        microstructure_features = self.microstructure_engine.get_microstructure_features()
        
        # Extract subsystem counts
        dna_stats = orchestrator_stats.get('dna_evolution', {})
        immune_stats = orchestrator_stats.get('immune_system', {})
        temporal_cycles = orchestrator_stats.get('temporal_cycles', 0)
        
        # Count microstructure patterns
        micro_patterns_count = 0
        if isinstance(microstructure_features, dict):
            micro_patterns_count = microstructure_features.get('pattern_count', 0)
        
        # Get dopamine subsystem stats
        dopamine_stats = 0
        try:
            dopamine_metrics = self.dopamine_subsystem.get_enhanced_performance_metrics()
            if isinstance(dopamine_metrics, dict) and dopamine_metrics.get('status') != 'insufficient_data':
                dopamine_stats = dopamine_metrics.get('total_updates', 0)
        except:
            dopamine_stats = 0
        
        return {
            'total_patterns': len(self.patterns),
            'recent_performance': np.mean(self.recent_outcomes) if self.recent_outcomes else 0,
            'pattern_count': sum(len(outcomes) for outcomes in self.patterns.values()),
            'historical_processed': self.historical_processed,
            'bootstrap_stats': self.bootstrap_stats,
            'subsystem_training_progress': self.subsystem_training_progress,
            # Individual subsystem stats - ALL 5 SUBSYSTEMS
            'dna_patterns': dna_stats.get('total_sequences', 0),
            'micro_patterns': micro_patterns_count,
            'temporal_patterns': temporal_cycles,
            'immune_patterns': immune_stats.get('total_antibodies', 0),
            'dopamine_patterns': dopamine_stats,
            # Detailed subsystem stats
            'orchestrator': orchestrator_stats,
            'adaptation': adaptation_stats,
            'microstructure': microstructure_features
        }
    
    def extract_features(self, data: MarketData) -> Features:
        """
        Enhanced and corrected feature extraction with all four subsystems.
        This version ensures data integrity and avoids fabricating data.
        """
        # --- Pre-computation Guards ---
        # Ensure we have enough data points to calculate features meaningfully.
        if len(data.prices_1m) < 20 or len(data.volumes_1m) < 20:
            logger.error(f"CRITICAL: Insufficient data for feature extraction. Prices: {len(data.prices_1m)}, Volumes: {len(data.volumes_1m)}")
            logger.error("ALERT: Returning default features due to insufficient market data")
            self._alert_insufficient_data(len(data.prices_1m), len(data.volumes_1m))
            return self._default_features()

        # Use the most recent 20 data points for stable calculations.
        prices = np.array(data.prices_1m[-20:])
        volumes = np.array(data.volumes_1m[-20:])

        # --- Basic Market Features ---
        # Safely calculate momentum, position, and volatility.
        short_ma = np.mean(prices[-5:])
        long_ma = np.mean(prices)
        price_momentum = (short_ma - long_ma) / long_ma if long_ma > 0 else 0

        recent_vol = np.mean(volumes[-5:])
        avg_vol = np.mean(volumes)
        volume_momentum = (recent_vol - avg_vol) / avg_vol if avg_vol > 0 else 0

        high = np.max(prices)
        low = np.min(prices)
        price_position = (prices[-1] - low) / (high - low) if high > low else 0.5

        volatility = np.std(prices) / np.mean(prices) if np.mean(prices) > 0 else 0

        # --- Timestamp and Time-based Features ---
        # Safely parse the timestamp from the data source. Avoid fallbacks to current time.
        try:
            # The primary timestamp should be a standard Unix timestamp.
            now = datetime.fromtimestamp(data.timestamp)
            time_of_day = (now.hour * 60 + now.minute) / 1440
        except (OSError, ValueError, OverflowError):
            logger.error(f"CRITICAL: Invalid timestamp format received: {data.timestamp}. Cannot calculate time features.")
            logger.error(f"Timestamp type: {type(data.timestamp)}, Value: {data.timestamp}")
            logger.error("ALERT: Returning default features due to timestamp validation failure")
            # CRITICAL: Alert system to timestamp validation failure
            self._alert_timestamp_failure(data.timestamp)
            return self._default_features()

        # --- Multi-Timeframe Analysis ---
        # Enhanced analysis with higher timeframes for better trend detection
        tf_analysis = self._analyze_multi_timeframe(data, price_momentum)
        
        # --- Subsystem Feature Preparation ---
        # This dictionary will be passed to the subsystems.
        market_features = {
            'volatility': volatility,
            'price_momentum': price_momentum,
            'volume_momentum': volume_momentum,
            'time_of_day': time_of_day,
            'price_position': price_position,
            'account_balance': data.account_balance,
            'margin_utilization': data.margin_utilization,
            'buying_power_ratio': data.buying_power_ratio,
            'daily_pnl_pct': data.daily_pnl_pct,
            'regime': self._classify_market_regime(volatility, price_momentum, volatility * 10),
            # Enhanced with all timeframe features
            'trend_1m': tf_analysis['trend_1m'],
            'trend_5m': tf_analysis['trend_5m'],
            'trend_15m': tf_analysis['trend_15m'],
            'trend_1h': tf_analysis['trend_1h'],
            'trend_4h': tf_analysis['trend_4h'],
            'trend_alignment': tf_analysis['trend_alignment'],
            'higher_tf_bias': tf_analysis['higher_tf_bias'],
            'volatility_1m': tf_analysis['volatility_1m'],
            'volatility_5m': tf_analysis['volatility_5m'],
            'volatility_15m': tf_analysis['volatility_15m'],
            'volatility_1h': tf_analysis['volatility_1h'],
            'volatility_4h': tf_analysis['volatility_4h']
        }
        
        # IMPORTANT: Do not fabricate timestamps for temporal analysis.
        # The temporal subsystem requires real timestamps if available.
        # If not, it should gracefully handle an empty list.
        timestamps = [] # Pass empty list, as MarketData doesn't provide a list of timestamps.

        # --- Subsystem Processing ---
        # Wrap in a try-except block to catch any errors during signal processing.
        try:
            # 1. DNA Subsystem
            dna_sequence = self.orchestrator.dna_subsystem.encode_market_state(
                data.prices_1m, data.volumes_1m, volatility, price_momentum
            )
            dna_signal = self.orchestrator.dna_subsystem.analyze_sequence(dna_sequence) if dna_sequence else 0.0
            
            # 2. Temporal Subsystem
            temporal_signal = self.orchestrator.temporal_subsystem.analyze_cycles(data.prices_1m, timestamps)
            
            # 3. Immune Subsystem
            immune_signal = self.orchestrator.immune_subsystem.detect_threats(market_features)
            
            # 4. Microstructure Subsystem
            microstructure_result = self.microstructure_engine.analyze_market_state(
                data.prices_1m, data.volumes_1m
            )
            microstructure_signal = microstructure_result.get('microstructure_signal', 0.0)
            regime_adjusted_signal = microstructure_result.get('regime_adjusted_signal', 0.0)
            
            # Extract additional microstructure features
            order_flow = microstructure_result.get('order_flow', {})
            regime_state = microstructure_result.get('regime_state', {})
            
            smart_money_flow = order_flow.get('smart_money_flow', 0.0)
            liquidity_depth = order_flow.get('liquidity_depth', 0.5)
            regime_confidence = regime_state.get('confidence', 0.5)
            
            # 5. Dopamine Subsystem - P&L-based reward signal
            dopamine_market_data = {
                'unrealized_pnl': getattr(data, 'unrealized_pnl', 0.0),
                'daily_pnl': getattr(data, 'daily_pnl', 0.0),
                'open_positions': getattr(data, 'open_positions', 0.0),
                'current_price': data.prices_1m[-1] if data.prices_1m else 0.0
            }
            dopamine_signal = self.dopamine_subsystem.get_simple_signal(dopamine_market_data)

        except Exception as e:
            logger.error(f"Error during subsystem processing in extract_features: {e}")
            return self._default_features()

        # --- Dynamic Signal Quality Weighting ---
        subsystem_signals = [dna_signal, temporal_signal, immune_signal, microstructure_signal, dopamine_signal]
        consensus_strength = self._calculate_enhanced_consensus(subsystem_signals)
        
        # Calculate dynamic weights based on signal quality, reliability, and recent performance
        weights = self._calculate_dynamic_signal_weights(
            subsystem_signals, 
            market_features, 
            consensus_strength
        )
        overall_signal = sum(signal * weight for signal, weight in zip(subsystem_signals, weights))
        
        signal_strength = sum(abs(s) for s in subsystem_signals)
        pattern_score = self._recognize_patterns(prices, volumes)
        
        confidence = max(0.1, min(1.0, 
            signal_strength * 0.4 + 
            consensus_strength * 0.3 + 
            pattern_score * 0.2 + 
            regime_confidence * 0.1
        ))

        # --- Real-time Adaptation ---
        adaptation_quality = 0.5 # Default value
        try:
            adaptation_context = {
                'volatility': volatility,
                'trend_strength': abs(price_momentum),
                'volume_regime': min(1.0, volume_momentum + 0.5),
                'time_of_day': time_of_day,
                'regime_confidence': regime_confidence
            }
            feature_tensor = self._create_feature_tensor(market_features, 
                                                       {'dna_signal': dna_signal, 'temporal_signal': temporal_signal, 
                                                        'immune_signal': immune_signal, 'overall_signal': overall_signal},
                                                       microstructure_result)
            adaptation_decision = self._get_adaptation_engine().get_adaptation_decision(feature_tensor, adaptation_context)
            adaptation_quality = adaptation_decision.get('adaptation_quality', 0.5)
        except Exception as e:
            logger.error(f"Adaptation engine failed during feature extraction: {e}")

        # --- Final Feature Construction ---
        return Features(
            price_momentum=price_momentum,
            volume_momentum=volume_momentum,
            price_position=price_position,
            volatility=volatility,
            time_of_day=time_of_day,
            pattern_score=pattern_score,
            confidence=confidence,
            dna_signal=dna_signal,
            micro_signal=microstructure_signal,
            temporal_signal=temporal_signal,
            immune_signal=immune_signal,
            microstructure_signal=microstructure_signal,
            dopamine_signal=dopamine_signal,
            overall_signal=overall_signal,
            regime_adjusted_signal=regime_adjusted_signal,
            adaptation_quality=adaptation_quality,
            smart_money_flow=smart_money_flow,
            liquidity_depth=liquidity_depth,
            regime_confidence=regime_confidence,
            # Multi-timeframe features - all timeframes
            trend_1m=tf_analysis['trend_1m'],
            trend_5m=tf_analysis['trend_5m'],
            trend_15m=tf_analysis['trend_15m'],
            trend_1h=tf_analysis['trend_1h'],
            trend_4h=tf_analysis['trend_4h'],
            trend_alignment=tf_analysis['trend_alignment'],
            higher_tf_bias=tf_analysis['higher_tf_bias'],
            volatility_1m=tf_analysis['volatility_1m'],
            volatility_5m=tf_analysis['volatility_5m'],
            volatility_15m=tf_analysis['volatility_15m'],
            volatility_1h=tf_analysis['volatility_1h'],
            volatility_4h=tf_analysis['volatility_4h']
        )
    
    def _analyze_multi_timeframe(self, data: MarketData, price_momentum: float) -> Dict:
        """
        Enhanced multi-timeframe analysis for better trend detection and market bias
        """
        try:
            # Initialize default values for all timeframes
            analysis = {
                'trend_1m': 0.0,
                'trend_5m': 0.0,
                'trend_15m': 0.0,
                'trend_1h': 0.0,
                'trend_4h': 0.0,
                'trend_alignment': 0.0,
                'higher_tf_bias': 0.0,
                'volatility_1m': 0.02,
                'volatility_5m': 0.02,
                'volatility_15m': 0.02,
                'volatility_1h': 0.02,
                'volatility_4h': 0.02
            }
            
            # 1M Timeframe Analysis
            if hasattr(data, 'prices_1m') and len(data.prices_1m) >= 20:
                prices_1m = np.array(data.prices_1m[-20:])
                
                # 1M trend strength
                m1_short_ma = np.mean(prices_1m[-5:])
                m1_long_ma = np.mean(prices_1m)
                analysis['trend_1m'] = (m1_short_ma - m1_long_ma) / m1_long_ma if m1_long_ma > 0 else 0.0
                
                # 1M volatility
                analysis['volatility_1m'] = np.std(prices_1m) / np.mean(prices_1m) if np.mean(prices_1m) > 0 else 0.02
            
            # 5M Timeframe Analysis
            if hasattr(data, 'prices_5m') and len(data.prices_5m) >= 15:
                prices_5m = np.array(data.prices_5m[-15:])
                
                # 5M trend strength
                m5_short_ma = np.mean(prices_5m[-3:])
                m5_long_ma = np.mean(prices_5m)
                analysis['trend_5m'] = (m5_short_ma - m5_long_ma) / m5_long_ma if m5_long_ma > 0 else 0.0
                
                # 5M volatility
                analysis['volatility_5m'] = np.std(prices_5m) / np.mean(prices_5m) if np.mean(prices_5m) > 0 else 0.02
            
            # 15M Timeframe Analysis
            if hasattr(data, 'prices_15m') and len(data.prices_15m) >= 12:
                prices_15m = np.array(data.prices_15m[-12:])
                
                # 15M trend strength
                m15_short_ma = np.mean(prices_15m[-3:])
                m15_long_ma = np.mean(prices_15m)
                analysis['trend_15m'] = (m15_short_ma - m15_long_ma) / m15_long_ma if m15_long_ma > 0 else 0.0
                
                # 15M volatility
                analysis['volatility_15m'] = np.std(prices_15m) / np.mean(prices_15m) if np.mean(prices_15m) > 0 else 0.02
            
            # 1H Timeframe Analysis (safe fallback if no data from NinjaTrader)
            if hasattr(data, 'prices_1h') and len(data.prices_1h) >= 10:
                prices_1h = np.array(data.prices_1h[-10:])
                
                # 1H trend strength
                h1_short_ma = np.mean(prices_1h[-3:])
                h1_long_ma = np.mean(prices_1h)
                analysis['trend_1h'] = (h1_short_ma - h1_long_ma) / h1_long_ma if h1_long_ma > 0 else 0.0
                
                # 1H volatility
                analysis['volatility_1h'] = np.std(prices_1h) / np.mean(prices_1h) if np.mean(prices_1h) > 0 else 0.02
            
            # 4H Timeframe Analysis (safe fallback if no data from NinjaTrader)
            if hasattr(data, 'prices_4h') and len(data.prices_4h) >= 6:
                prices_4h = np.array(data.prices_4h[-6:])
                
                # 4H trend strength
                h4_short_ma = np.mean(prices_4h[-2:])
                h4_long_ma = np.mean(prices_4h)
                analysis['trend_4h'] = (h4_short_ma - h4_long_ma) / h4_long_ma if h4_long_ma > 0 else 0.0
                
                # 4H volatility
                analysis['volatility_4h'] = np.std(prices_4h) / np.mean(prices_4h) if np.mean(prices_4h) > 0 else 0.02
            
            # Multi-Timeframe Alignment
            # Calculate how well all 5 timeframes agree on direction
            trend_1m = analysis['trend_1m']
            trend_5m = analysis['trend_5m']
            trend_15m = analysis['trend_15m']
            trend_1h = analysis['trend_1h']
            trend_4h = analysis['trend_4h']
            
            # All timeframes for comprehensive alignment
            trends = [trend_1m, trend_5m, trend_15m, trend_1h, trend_4h]
            positive_trends = sum(1 for t in trends if t > 0.001)
            negative_trends = sum(1 for t in trends if t < -0.001)
            
            # Enhanced alignment scoring with all 5 timeframes
            if positive_trends >= 4 and negative_trends == 0:
                analysis['trend_alignment'] = 0.9  # Very strong bullish alignment
            elif negative_trends >= 4 and positive_trends == 0:
                analysis['trend_alignment'] = -0.9  # Very strong bearish alignment
            elif positive_trends >= 3 and negative_trends <= 1:
                analysis['trend_alignment'] = 0.6  # Strong bullish alignment
            elif negative_trends >= 3 and positive_trends <= 1:
                analysis['trend_alignment'] = -0.6  # Strong bearish alignment
            elif positive_trends > negative_trends:
                analysis['trend_alignment'] = 0.3  # Weak bullish alignment
            elif negative_trends > positive_trends:
                analysis['trend_alignment'] = -0.3  # Weak bearish alignment
            else:
                analysis['trend_alignment'] = 0.0  # No clear alignment
            
            # Higher Timeframe Bias (4H has most weight, then 1H, 15m, 5m, 1m)
            # This gives the "big picture" market direction weighted by timeframe importance
            weights = [0.05, 0.1, 0.2, 0.3, 0.35]  # 1m, 5m, 15m, 1h, 4h weights
            analysis['higher_tf_bias'] = np.average(trends, weights=weights)
            
            # Log multi-timeframe analysis for debugging
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"Multi-TF Analysis: 1m={trend_1m:.4f}, 5m={trend_5m:.4f}, 15m={trend_15m:.4f}, "
                           f"1H={trend_1h:.4f}, 4H={trend_4h:.4f}, Alignment={analysis['trend_alignment']:.3f}, "
                           f"Bias={analysis['higher_tf_bias']:.4f}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in multi-timeframe analysis: {e}")
            # Return safe defaults for all timeframes
            return {
                'trend_1m': 0.0,
                'trend_5m': 0.0,
                'trend_15m': 0.0,
                'trend_1h': 0.0,
                'trend_4h': 0.0,
                'trend_alignment': 0.0,
                'higher_tf_bias': 0.0,
                'volatility_1m': 0.02,
                'volatility_5m': 0.02,
                'volatility_15m': 0.02,
                'volatility_1h': 0.02,
                'volatility_4h': 0.02
            }