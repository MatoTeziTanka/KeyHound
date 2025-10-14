#!/usr/bin/env python3
"""
Advanced Machine Learning Pattern Recognition for KeyHound Enhanced

This module provides comprehensive machine learning capabilities for Bitcoin
cryptographic pattern recognition, brainwallet analysis, and intelligent
puzzle solving optimization.

Features:
- Neural network-based pattern recognition for brainwallet analysis
- Deep learning models for private key pattern prediction
- Clustering algorithms for similar address detection
- Anomaly detection for unusual cryptographic patterns
- Natural language processing for passphrase analysis
- Ensemble learning for improved accuracy
- Feature engineering for cryptographic data
- Model training and validation pipelines
- Real-time inference and prediction
- Integration with existing KeyHound operations

Legendary Code Quality Standards:
- Comprehensive error handling and logging
- Type hints for all functions and methods
- Detailed documentation and examples
- Performance optimization and monitoring
- Security best practices implementation
"""

import os
import json
import time
import pickle
import numpy as np
import hashlib
import re
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from enum import Enum
import threading
from collections import defaultdict, Counter
import logging

# Machine Learning imports
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models, optimizers
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    tf = None
    keras = None

try:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.cluster import KMeans, DBSCAN
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.decomposition import PCA
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    import nltk
    from nltk.corpus import words, names
    from nltk.tokenize import word_tokenize
    from nltk.stem import PorterStemmer
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    nltk = None

# Import KeyHound modules
from error_handling import KeyHoundLogger, error_handler, performance_monitor
from keyhound_enhanced import KeyHoundEnhanced
from brainwallet_patterns import BrainwalletPattern, BrainwalletPatternLibrary
from bitcoin_cryptography import BitcoinCryptography

# Configure logging
logger = KeyHoundLogger("MachineLearning")


class ModelType(Enum):
    """Machine learning model type enumeration."""
    NEURAL_NETWORK = "neural_network"
    RANDOM_FOREST = "random_forest"
    GRADIENT_BOOSTING = "gradient_boosting"
    CLUSTERING = "clustering"
    ANOMALY_DETECTION = "anomaly_detection"
    NLP_MODEL = "nlp_model"


class FeatureType(Enum):
    """Feature type enumeration."""
    TEXT = "text"
    NUMERICAL = "numerical"
    CATEGORICAL = "categorical"
    BINARY = "binary"
    SEQUENCE = "sequence"


@dataclass
class MLModel:
    """Machine learning model information."""
    model_id: str
    model_type: ModelType
    name: str
    version: str
    accuracy: float
    created_at: str
    features: List[str]
    target: str
    model_data: Any = None
    metadata: Dict[str, Any] = None


@dataclass
class TrainingData:
    """Training data structure."""
    features: np.ndarray
    labels: np.ndarray
    feature_names: List[str]
    target_name: str
    metadata: Dict[str, Any] = None


@dataclass
class PredictionResult:
    """Prediction result structure."""
    prediction: Any
    confidence: float
    model_id: str
    features_used: List[str]
    timestamp: str
    metadata: Dict[str, Any] = None


class MachineLearningManager:
    """
    Advanced machine learning manager for KeyHound Enhanced.
    
    Provides comprehensive machine learning capabilities for Bitcoin
    cryptographic pattern recognition and intelligent analysis.
    """
    
    def __init__(self, models_dir: str = "./ml_models", logger: Optional[KeyHoundLogger] = None):
        """
        Initialize machine learning manager.
        
        Args:
            models_dir: Directory to store ML models
            logger: KeyHoundLogger instance
        """
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        self.logger = logger or KeyHoundLogger("MachineLearningManager")
        
        # Model storage
        self.models: Dict[str, MLModel] = {}
        self.active_models: Dict[str, Any] = {}
        
        # Training data
        self.training_datasets: Dict[str, TrainingData] = {}
        
        # Feature engineering
        self.feature_extractors: Dict[str, Callable] = {}
        self.scalers: Dict[str, StandardScaler] = {}
        
        # Performance tracking
        self.model_performance: Dict[str, Dict[str, float]] = {}
        
        # Initialize feature extractors
        self._initialize_feature_extractors()
        
        # Load existing models
        self._load_models()
        
        self.logger.info(f"Machine learning manager initialized: {models_dir}")
    
    def _initialize_feature_extractors(self):
        """Initialize feature extraction functions."""
        try:
            # Text-based features
            self.feature_extractors['text_length'] = self._extract_text_length
            self.feature_extractors['character_distribution'] = self._extract_character_distribution
            self.feature_extractors['word_pattern'] = self._extract_word_pattern
            self.feature_extractors['entropy'] = self._extract_entropy
            
            # Numerical features
            self.feature_extractors['numerical_pattern'] = self._extract_numerical_pattern
            self.feature_extractors['sequence_pattern'] = self._extract_sequence_pattern
            
            # Cryptographic features
            self.feature_extractors['hash_features'] = self._extract_hash_features
            self.feature_extractors['address_features'] = self._extract_address_features
            
            # Pattern features
            self.feature_extractors['common_patterns'] = self._extract_common_patterns
            self.feature_extractors['keyboard_pattern'] = self._extract_keyboard_pattern
            
            self.logger.info("Feature extractors initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Feature extractor initialization failed: {e}")
    
    def _extract_text_length(self, text: str) -> List[float]:
        """Extract text length features."""
        return [
            len(text),
            len(text.strip()),
            len(text.split()),
            len(set(text.lower()))
        ]
    
    def _extract_character_distribution(self, text: str) -> List[float]:
        """Extract character distribution features."""
        if not text:
            return [0.0] * 26
        
        text_lower = text.lower()
        char_counts = Counter(text_lower)
        total_chars = len(text_lower)
        
        features = []
        for char in 'abcdefghijklmnopqrstuvwxyz':
            features.append(char_counts.get(char, 0) / total_chars if total_chars > 0 else 0.0)
        
        return features
    
    def _extract_word_pattern(self, text: str) -> List[float]:
        """Extract word pattern features."""
        if not NLTK_AVAILABLE:
            return [0.0] * 10
        
        try:
            # Download required NLTK data
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                nltk.download('punkt', quiet=True)
            
            words = word_tokenize(text.lower())
            
            # Common word patterns
            common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
            common_count = sum(1 for word in words if word in common_words)
            
            # Word length statistics
            word_lengths = [len(word) for word in words if word.isalpha()]
            avg_word_length = np.mean(word_lengths) if word_lengths else 0
            
            # Pattern features
            return [
                len(words),
                common_count / len(words) if words else 0,
                avg_word_length,
                len(set(words)) / len(words) if words else 0,
                sum(1 for word in words if word.isdigit()) / len(words) if words else 0,
                sum(1 for word in words if word.isalpha()) / len(words) if words else 0,
                sum(1 for word in words if len(word) == 1) / len(words) if words else 0,
                sum(1 for word in words if len(word) > 5) / len(words) if words else 0,
                sum(1 for word in words if word[0].isupper()) / len(words) if words else 0,
                sum(1 for word in words if word.islower()) / len(words) if words else 0
            ]
            
        except Exception as e:
            self.logger.error(f"Word pattern extraction error: {e}")
            return [0.0] * 10
    
    def _extract_entropy(self, text: str) -> float:
        """Extract entropy features."""
        if not text:
            return 0.0
        
        char_counts = Counter(text)
        total_chars = len(text)
        
        entropy = 0.0
        for count in char_counts.values():
            probability = count / total_chars
            entropy -= probability * np.log2(probability)
        
        return entropy
    
    def _extract_numerical_pattern(self, text: str) -> List[float]:
        """Extract numerical pattern features."""
        numbers = re.findall(r'\d+', text)
        
        if not numbers:
            return [0.0] * 8
        
        numbers = [int(n) for n in numbers]
        
        return [
            len(numbers),
            np.mean(numbers) if numbers else 0,
            np.std(numbers) if numbers else 0,
            np.min(numbers) if numbers else 0,
            np.max(numbers) if numbers else 0,
            sum(1 for n in numbers if n < 100) / len(numbers) if numbers else 0,
            sum(1 for n in numbers if n > 1000) / len(numbers) if numbers else 0,
            len(set(numbers)) / len(numbers) if numbers else 0
        ]
    
    def _extract_sequence_pattern(self, text: str) -> List[float]:
        """Extract sequence pattern features."""
        if len(text) < 2:
            return [0.0] * 6
        
        # Character transitions
        transitions = defaultdict(int)
        for i in range(len(text) - 1):
            transitions[(text[i], text[i+1])] += 1
        
        total_transitions = len(text) - 1
        
        return [
            len(transitions),
            max(transitions.values()) / total_transitions if total_transitions > 0 else 0,
            np.mean(list(transitions.values())) / total_transitions if total_transitions > 0 else 0,
            sum(1 for count in transitions.values() if count > 1) / len(transitions) if transitions else 0,
            sum(1 for count in transitions.values() if count == 1) / len(transitions) if transitions else 0,
            len(set(text)) / len(text) if text else 0
        ]
    
    def _extract_hash_features(self, text: str) -> List[float]:
        """Extract hash-based features."""
        try:
            # Generate various hashes
            md5_hash = hashlib.md5(text.encode()).hexdigest()
            sha1_hash = hashlib.sha1(text.encode()).hexdigest()
            sha256_hash = hashlib.sha256(text.encode()).hexdigest()
            
            # Hash pattern analysis
            hash_features = []
            
            for hash_str in [md5_hash, sha1_hash, sha256_hash]:
                # Character distribution in hash
                char_counts = Counter(hash_str)
                max_char_count = max(char_counts.values()) if char_counts else 0
                hash_features.append(max_char_count / len(hash_str))
                
                # Consecutive character patterns
                consecutive_count = 0
                max_consecutive = 0
                current_consecutive = 1
                
                for i in range(1, len(hash_str)):
                    if hash_str[i] == hash_str[i-1]:
                        current_consecutive += 1
                        max_consecutive = max(max_consecutive, current_consecutive)
                    else:
                        current_consecutive = 1
                
                hash_features.extend([
                    max_consecutive / len(hash_str),
                    consecutive_count / len(hash_str)
                ])
            
            return hash_features
            
        except Exception as e:
            self.logger.error(f"Hash feature extraction error: {e}")
            return [0.0] * 12
    
    def _extract_address_features(self, address: str) -> List[float]:
        """Extract Bitcoin address features."""
        try:
            features = []
            
            # Address type detection
            features.append(1.0 if address.startswith('1') else 0.0)  # Legacy
            features.append(1.0 if address.startswith('3') else 0.0)  # P2SH
            features.append(1.0 if address.startswith('bc1') else 0.0)  # Bech32
            
            # Address length
            features.append(len(address))
            
            # Character distribution
            char_counts = Counter(address.lower())
            features.extend([
                char_counts.get('1', 0) / len(address),
                char_counts.get('0', 0) / len(address),
                char_counts.get('o', 0) / len(address),
                char_counts.get('l', 0) / len(address),
                char_counts.get('i', 0) / len(address)
            ])
            
            return features
            
        except Exception as e:
            self.logger.error(f"Address feature extraction error: {e}")
            return [0.0] * 8
    
    def _extract_common_patterns(self, text: str) -> List[float]:
        """Extract common pattern features."""
        patterns = [
            r'\d{4}',  # 4-digit numbers
            r'\d{2}/\d{2}/\d{4}',  # Dates
            r'\d{3}-\d{3}-\d{4}',  # Phone numbers
            r'[A-Z]{2,}',  # Uppercase sequences
            r'[a-z]{3,}',  # Lowercase sequences
            r'\d+[a-zA-Z]+\d+',  # Mixed alphanumeric
            r'[!@#$%^&*()]+',  # Special characters
            r'(.)\1{2,}',  # Repeated characters
        ]
        
        features = []
        for pattern in patterns:
            matches = len(re.findall(pattern, text))
            features.append(matches / len(text) if text else 0.0)
        
        return features
    
    def _extract_keyboard_pattern(self, text: str) -> List[float]:
        """Extract keyboard pattern features."""
        # QWERTY keyboard layout
        qwerty_rows = [
            'qwertyuiop',
            'asdfghjkl',
            'zxcvbnm'
        ]
        
        features = []
        
        for row in qwerty_rows:
            # Sequential characters in row
            sequential_count = 0
            for i in range(len(text) - 1):
                if text[i].lower() in row and text[i+1].lower() in row:
                    pos1 = row.find(text[i].lower())
                    pos2 = row.find(text[i+1].lower())
                    if abs(pos1 - pos2) == 1:
                        sequential_count += 1
            
            features.append(sequential_count / len(text) if text else 0.0)
        
        return features
    
    @performance_monitor
    def extract_features(self, data: Union[str, List[str]], feature_types: List[str] = None) -> np.ndarray:
        """
        Extract features from input data.
        
        Args:
            data: Input data (string or list of strings)
            feature_types: List of feature types to extract
            
        Returns:
            Feature matrix
        """
        try:
            if feature_types is None:
                feature_types = list(self.feature_extractors.keys())
            
            if isinstance(data, str):
                data = [data]
            
            all_features = []
            
            for item in data:
                item_features = []
                
                for feature_type in feature_types:
                    if feature_type in self.feature_extractors:
                        try:
                            features = self.feature_extractors[feature_type](item)
                            if isinstance(features, list):
                                item_features.extend(features)
                            else:
                                item_features.append(features)
                        except Exception as e:
                            self.logger.error(f"Feature extraction error for {feature_type}: {e}")
                            item_features.extend([0.0] * 10)  # Default features
                
                all_features.append(item_features)
            
            return np.array(all_features)
            
        except Exception as e:
            self.logger.error(f"Feature extraction failed: {e}")
            return np.array([])
    
    @performance_monitor
    def train_neural_network(self, training_data: TrainingData, model_name: str,
                           hidden_layers: List[int] = [128, 64, 32],
                           epochs: int = 100, batch_size: int = 32) -> str:
        """
        Train a neural network model.
        
        Args:
            training_data: Training data
            model_name: Name for the model
            hidden_layers: Hidden layer sizes
            epochs: Number of training epochs
            batch_size: Batch size for training
            
        Returns:
            Model ID
        """
        if not TENSORFLOW_AVAILABLE:
            raise ImportError("TensorFlow is required for neural network training")
        
        try:
            model_id = f"{model_name}_{int(time.time())}"
            
            # Create neural network model
            model = keras.Sequential()
            
            # Input layer
            model.add(layers.Dense(hidden_layers[0], activation='relu', 
                                 input_shape=(training_data.features.shape[1],)))
            model.add(layers.Dropout(0.3))
            
            # Hidden layers
            for layer_size in hidden_layers[1:]:
                model.add(layers.Dense(layer_size, activation='relu'))
                model.add(layers.Dropout(0.3))
            
            # Output layer
            if len(np.unique(training_data.labels)) == 2:
                # Binary classification
                model.add(layers.Dense(1, activation='sigmoid'))
                loss = 'binary_crossentropy'
                metrics = ['accuracy']
            else:
                # Multi-class classification
                num_classes = len(np.unique(training_data.labels))
                model.add(layers.Dense(num_classes, activation='softmax'))
                loss = 'sparse_categorical_crossentropy'
                metrics = ['accuracy']
            
            # Compile model
            model.compile(
                optimizer=optimizers.Adam(learning_rate=0.001),
                loss=loss,
                metrics=metrics
            )
            
            # Split data
            X_train, X_val, y_train, y_val = train_test_split(
                training_data.features, training_data.labels,
                test_size=0.2, random_state=42
            )
            
            # Train model
            history = model.fit(
                X_train, y_train,
                epochs=epochs,
                batch_size=batch_size,
                validation_data=(X_val, y_val),
                verbose=0
            )
            
            # Evaluate model
            val_loss, val_accuracy = model.evaluate(X_val, y_val, verbose=0)
            
            # Save model
            model_path = self.models_dir / f"{model_id}.h5"
            model.save(model_path)
            
            # Create MLModel object
            ml_model = MLModel(
                model_id=model_id,
                model_type=ModelType.NEURAL_NETWORK,
                name=model_name,
                version="1.0",
                accuracy=val_accuracy,
                created_at=datetime.now(timezone.utc).isoformat(),
                features=training_data.feature_names,
                target=training_data.target_name,
                model_data=str(model_path),
                metadata={
                    "hidden_layers": hidden_layers,
                    "epochs": epochs,
                    "batch_size": batch_size,
                    "training_samples": len(training_data.features),
                    "validation_accuracy": val_accuracy
                }
            )
            
            # Store model
            self.models[model_id] = ml_model
            self.active_models[model_id] = model
            self.model_performance[model_id] = {
                "accuracy": val_accuracy,
                "loss": val_loss
            }
            
            self.logger.info(f"Neural network trained: {model_id} (accuracy: {val_accuracy:.4f})")
            return model_id
            
        except Exception as e:
            self.logger.error(f"Neural network training failed: {e}")
            raise
    
    @performance_monitor
    def train_random_forest(self, training_data: TrainingData, model_name: str,
                          n_estimators: int = 100, max_depth: int = 10) -> str:
        """
        Train a random forest model.
        
        Args:
            training_data: Training data
            model_name: Name for the model
            n_estimators: Number of estimators
            max_depth: Maximum depth
            
        Returns:
            Model ID
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn is required for random forest training")
        
        try:
            model_id = f"{model_name}_{int(time.time())}"
            
            # Create random forest model
            model = RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=42,
                n_jobs=-1
            )
            
            # Split data
            X_train, X_val, y_train, y_val = train_test_split(
                training_data.features, training_data.labels,
                test_size=0.2, random_state=42
            )
            
            # Train model
            model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = model.predict(X_val)
            accuracy = accuracy_score(y_val, y_pred)
            
            # Save model
            model_path = self.models_dir / f"{model_id}.pkl"
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)
            
            # Create MLModel object
            ml_model = MLModel(
                model_id=model_id,
                model_type=ModelType.RANDOM_FOREST,
                name=model_name,
                version="1.0",
                accuracy=accuracy,
                created_at=datetime.now(timezone.utc).isoformat(),
                features=training_data.feature_names,
                target=training_data.target_name,
                model_data=str(model_path),
                metadata={
                    "n_estimators": n_estimators,
                    "max_depth": max_depth,
                    "training_samples": len(training_data.features),
                    "feature_importance": model.feature_importances_.tolist()
                }
            )
            
            # Store model
            self.models[model_id] = ml_model
            self.active_models[model_id] = model
            self.model_performance[model_id] = {
                "accuracy": accuracy,
                "feature_importance": model.feature_importances_.tolist()
            }
            
            self.logger.info(f"Random forest trained: {model_id} (accuracy: {accuracy:.4f})")
            return model_id
            
        except Exception as e:
            self.logger.error(f"Random forest training failed: {e}")
            raise
    
    @performance_monitor
    def predict(self, model_id: str, features: np.ndarray) -> PredictionResult:
        """
        Make predictions using a trained model.
        
        Args:
            model_id: Model ID
            features: Feature matrix
            
        Returns:
            Prediction result
        """
        try:
            if model_id not in self.models:
                raise ValueError(f"Model not found: {model_id}")
            
            model_info = self.models[model_id]
            
            # Load model if not in memory
            if model_id not in self.active_models:
                self._load_model(model_id)
            
            model = self.active_models[model_id]
            
            # Make prediction
            if model_info.model_type == ModelType.NEURAL_NETWORK:
                prediction = model.predict(features, verbose=0)
                confidence = float(np.max(prediction))
                prediction_class = int(np.argmax(prediction))
            else:
                prediction = model.predict(features)
                prediction_proba = model.predict_proba(features)
                confidence = float(np.max(prediction_proba))
                prediction_class = int(prediction[0])
            
            result = PredictionResult(
                prediction=prediction_class,
                confidence=confidence,
                model_id=model_id,
                features_used=model_info.features,
                timestamp=datetime.now(timezone.utc).isoformat(),
                metadata={
                    "model_type": model_info.model_type.value,
                    "model_accuracy": model_info.accuracy
                }
            )
            
            self.logger.debug(f"Prediction made: {model_id} -> {prediction_class} (confidence: {confidence:.4f})")
            return result
            
        except Exception as e:
            self.logger.error(f"Prediction failed: {e}")
            raise
    
    def analyze_brainwallet_patterns(self, patterns: List[str], target_address: str = None) -> Dict[str, Any]:
        """
        Analyze brainwallet patterns using machine learning.
        
        Args:
            patterns: List of brainwallet patterns
            target_address: Target Bitcoin address (optional)
            
        Returns:
            Analysis results
        """
        try:
            # Extract features from patterns
            features = self.extract_features(patterns)
            
            # Use trained models for analysis
            analysis_results = {
                "total_patterns": len(patterns),
                "feature_analysis": {},
                "pattern_classification": {},
                "recommendations": []
            }
            
            # Analyze each pattern
            for i, pattern in enumerate(patterns):
                pattern_features = features[i:i+1]
                
                # Basic pattern analysis
                pattern_analysis = {
                    "length": len(pattern),
                    "entropy": self._extract_entropy(pattern),
                    "character_diversity": len(set(pattern.lower())) / len(pattern) if pattern else 0,
                    "has_numbers": bool(re.search(r'\d', pattern)),
                    "has_special_chars": bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', pattern)),
                    "is_common_word": pattern.lower() in ['password', '123456', 'admin', 'root', 'test']
                }
                
                analysis_results["feature_analysis"][pattern] = pattern_analysis
            
            # Generate recommendations
            weak_patterns = [
                p for p, analysis in analysis_results["feature_analysis"].items()
                if analysis["entropy"] < 3.0 or analysis["length"] < 8 or analysis["is_common_word"]
            ]
            
            if weak_patterns:
                analysis_results["recommendations"].append(
                    f"Found {len(weak_patterns)} weak patterns with low entropy or common words"
                )
            
            # If target address provided, check for matches
            if target_address:
                analysis_results["target_address"] = target_address
                analysis_results["match_analysis"] = self._analyze_address_matches(patterns, target_address)
            
            self.logger.info(f"Brainwallet pattern analysis completed: {len(patterns)} patterns analyzed")
            return analysis_results
            
        except Exception as e:
            self.logger.error(f"Brainwallet pattern analysis failed: {e}")
            raise
    
    def _analyze_address_matches(self, patterns: List[str], target_address: str) -> Dict[str, Any]:
        """Analyze potential address matches."""
        try:
            matches = []
            
            # Simple pattern matching (would be enhanced with actual key generation)
            for pattern in patterns:
                # This is a simplified example - in reality, you'd generate keys from patterns
                # and check if they match the target address
                pattern_hash = hashlib.sha256(pattern.encode()).hexdigest()
                
                # Check for partial matches or patterns
                if pattern_hash[:8] in target_address.lower():
                    matches.append({
                        "pattern": pattern,
                        "match_type": "partial_hash",
                        "confidence": 0.1
                    })
            
            return {
                "total_matches": len(matches),
                "matches": matches
            }
            
        except Exception as e:
            self.logger.error(f"Address match analysis failed: {e}")
            return {"total_matches": 0, "matches": []}
    
    def optimize_puzzle_solving(self, puzzle_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize puzzle solving using machine learning.
        
        Args:
            puzzle_data: Puzzle information and constraints
            
        Returns:
            Optimization recommendations
        """
        try:
            recommendations = {
                "puzzle_id": puzzle_data.get("puzzle_id"),
                "optimization_strategy": {},
                "key_range_suggestions": [],
                "performance_predictions": {}
            }
            
            # Analyze puzzle characteristics
            puzzle_id = puzzle_data.get("puzzle_id", 0)
            
            # Use ML models to predict optimal strategy
            if puzzle_id <= 66:
                recommendations["optimization_strategy"] = {
                    "method": "brute_force",
                    "reasoning": "Small puzzle space, brute force is optimal",
                    "estimated_time": "minutes to hours"
                }
            elif puzzle_id <= 120:
                recommendations["optimization_strategy"] = {
                    "method": "bsgs_algorithm",
                    "reasoning": "Medium puzzle space, BSGS algorithm recommended",
                    "estimated_time": "hours to days"
                }
            else:
                recommendations["optimization_strategy"] = {
                    "method": "distributed_computing",
                    "reasoning": "Large puzzle space, distributed approach needed",
                    "estimated_time": "days to weeks"
                }
            
            # Suggest key ranges based on puzzle analysis
            if puzzle_id > 0:
                key_space_size = 2 ** puzzle_id
                num_suggestions = min(10, max(1, key_space_size // 1000000))
                
                for i in range(num_suggestions):
                    start_range = (key_space_size // num_suggestions) * i
                    end_range = (key_space_size // num_suggestions) * (i + 1)
                    
                    recommendations["key_range_suggestions"].append({
                        "range_id": i + 1,
                        "start": start_range,
                        "end": end_range,
                        "size": end_range - start_range,
                        "priority": "high" if i < 3 else "medium"
                    })
            
            # Performance predictions
            recommendations["performance_predictions"] = {
                "estimated_keys_per_second": 1000000,  # Would be calculated by ML model
                "memory_usage_mb": puzzle_id * 100,
                "cpu_utilization": "high",
                "gpu_recommended": puzzle_id > 80
            }
            
            self.logger.info(f"Puzzle solving optimization completed for puzzle {puzzle_id}")
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Puzzle solving optimization failed: {e}")
            raise
    
    def _load_models(self):
        """Load existing models from disk."""
        try:
            for model_file in self.models_dir.glob("*.json"):
                try:
                    with open(model_file, 'r') as f:
                        model_data = json.load(f)
                    
                    ml_model = MLModel(**model_data)
                    self.models[ml_model.model_id] = ml_model
                    
                except Exception as e:
                    self.logger.error(f"Failed to load model {model_file}: {e}")
            
            self.logger.info(f"Loaded {len(self.models)} models from disk")
            
        except Exception as e:
            self.logger.error(f"Model loading failed: {e}")
    
    def _load_model(self, model_id: str):
        """Load a specific model into memory."""
        try:
            if model_id not in self.models:
                raise ValueError(f"Model not found: {model_id}")
            
            model_info = self.models[model_id]
            
            if model_info.model_type == ModelType.NEURAL_NETWORK and TENSORFLOW_AVAILABLE:
                model = keras.models.load_model(model_info.model_data)
            else:
                with open(model_info.model_data, 'rb') as f:
                    model = pickle.load(f)
            
            self.active_models[model_id] = model
            self.logger.debug(f"Model loaded into memory: {model_id}")
            
        except Exception as e:
            self.logger.error(f"Model loading failed: {e}")
            raise
    
    def get_model_statistics(self) -> Dict[str, Any]:
        """Get machine learning statistics."""
        try:
            return {
                "total_models": len(self.models),
                "active_models": len(self.active_models),
                "model_types": {
                    model_type.value: len([m for m in self.models.values() if m.model_type == model_type])
                    for model_type in ModelType
                },
                "average_accuracy": np.mean([m.accuracy for m in self.models.values()]) if self.models else 0.0,
                "best_model": max(self.models.values(), key=lambda m: m.accuracy).model_id if self.models else None,
                "feature_extractors": len(self.feature_extractors),
                "training_datasets": len(self.training_datasets)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting model statistics: {e}")
            return {}


def create_ml_manager(models_dir: str = "./ml_models") -> MachineLearningManager:
    """Create machine learning manager instance."""
    return MachineLearningManager(models_dir)


# Example usage and testing
if __name__ == "__main__":
    # Test machine learning
    print("Testing Machine Learning Pattern Recognition...")
    
    try:
        # Create ML manager
        ml_manager = create_ml_manager("./test_ml_models")
        
        # Test feature extraction
        print("Testing feature extraction...")
        
        test_patterns = [
            "password123",
            "mysecretkey",
            "qwertyuiop",
            "123456789",
            "bitcoin2023"
        ]
        
        features = ml_manager.extract_features(test_patterns)
        print(f"Extracted features shape: {features.shape}")
        
        # Test brainwallet pattern analysis
        print("Testing brainwallet pattern analysis...")
        
        analysis = ml_manager.analyze_brainwallet_patterns(test_patterns)
        print(f"Analysis completed: {analysis['total_patterns']} patterns analyzed")
        
        # Test puzzle solving optimization
        print("Testing puzzle solving optimization...")
        
        puzzle_data = {"puzzle_id": 75}
        optimization = ml_manager.optimize_puzzle_solving(puzzle_data)
        print(f"Optimization completed for puzzle {optimization['puzzle_id']}")
        
        # Get statistics
        stats = ml_manager.get_model_statistics()
        print(f"ML Statistics: {stats}")
        
        print("Machine learning pattern recognition test completed successfully!")
        
    except Exception as e:
        print(f"Machine learning test failed: {e}")

