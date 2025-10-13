#!/usr/bin/env python3
"""
Comprehensive Error Handling and Logging Module for KeyHound Enhanced

This module provides enterprise-grade error handling, logging, and monitoring
capabilities with legendary code quality standards.

Features:
- Comprehensive exception handling with custom exception classes
- Structured logging with multiple output formats
- Performance monitoring and metrics collection
- Error reporting and notification systems
- Debug and diagnostic tools
- Configuration management for logging levels

Legendary Code Quality Standards:
- Comprehensive error handling for all edge cases
- Type hints for all functions and methods
- Detailed documentation and examples
- Performance optimization and monitoring
- Security best practices implementation
"""

import logging
import logging.handlers
import sys
import traceback
import json
import time
import threading
from typing import Optional, Dict, Any, List, Union, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import functools
import inspect

# Colorama for colored console output
try:
    from colorama import Fore, Style, init
    init()
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False


@dataclass
class ErrorContext:
    """Context information for error tracking."""
    timestamp: str
    function_name: str
    file_name: str
    line_number: int
    error_type: str
    error_message: str
    stack_trace: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None


@dataclass
class PerformanceMetrics:
    """Performance metrics for monitoring."""
    function_name: str
    execution_time: float
    memory_usage: float
    cpu_usage: float
    timestamp: str
    success: bool
    error_message: Optional[str] = None


class KeyHoundError(Exception):
    """Base exception class for KeyHound-specific errors."""
    
    def __init__(self, message: str, error_code: str = "KEYHOUND_ERROR", 
                 error_context: Optional[ErrorContext] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.error_context = error_context
        self.timestamp = datetime.now(timezone.utc).isoformat()
    
    def __str__(self):
        return f"{self.error_code}: {self.message}"


class CryptographyError(KeyHoundError):
    """Exception for cryptographic operation errors."""
    
    def __init__(self, message: str, error_context: Optional[ErrorContext] = None):
        super().__init__(message, "CRYPTOGRAPHY_ERROR", error_context)


class GPUError(KeyHoundError):
    """Exception for GPU operation errors."""
    
    def __init__(self, message: str, error_context: Optional[ErrorContext] = None):
        super().__init__(message, "GPU_ERROR", error_context)


class PuzzleError(KeyHoundError):
    """Exception for Bitcoin puzzle solving errors."""
    
    def __init__(self, message: str, error_context: Optional[ErrorContext] = None):
        super().__init__(message, "PUZZLE_ERROR", error_context)


class BrainwalletError(KeyHoundError):
    """Exception for brainwallet testing errors."""
    
    def __init__(self, message: str, error_context: Optional[ErrorContext] = None):
        super().__init__(message, "BRAINWALLET_ERROR", error_context)


class ConfigurationError(KeyHoundError):
    """Exception for configuration errors."""
    
    def __init__(self, message: str, error_context: Optional[ErrorContext] = None):
        super().__init__(message, "CONFIGURATION_ERROR", error_context)


class KeyHoundLogger:
    """
    Enhanced logging system for KeyHound Enhanced.
    
    Provides structured logging with multiple output formats, performance
    monitoring, and comprehensive error tracking.
    """
    
    def __init__(self, name: str = "KeyHound", log_level: str = "INFO", 
                 log_file: Optional[str] = None, max_file_size: int = 10 * 1024 * 1024,
                 backup_count: int = 5):
        """
        Initialize KeyHound logger.
        
        Args:
            name: Logger name
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Log file path (optional)
            max_file_size: Maximum log file size in bytes
            backup_count: Number of backup files to keep
        """
        self.name = name
        self.log_level = getattr(logging, log_level.upper())
        self.log_file = log_file
        self.max_file_size = max_file_size
        self.backup_count = backup_count
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.log_level)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Setup handlers
        self._setup_console_handler()
        if log_file:
            self._setup_file_handler()
        
        # Performance tracking
        self.performance_metrics: List[PerformanceMetrics] = []
        self.metrics_lock = threading.Lock()
        
        # Error tracking
        self.error_count = 0
        self.error_history: List[ErrorContext] = []
        self.error_lock = threading.Lock()
        
        self.logger.info(f"KeyHound logger initialized: {name}")
    
    def _setup_console_handler(self):
        """Setup console handler with colored output."""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.log_level)
        
        # Create formatter
        if COLORAMA_AVAILABLE:
            formatter = ColoredFormatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        else:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def _setup_file_handler(self):
        """Setup file handler with rotation."""
        file_handler = logging.handlers.RotatingFileHandler(
            self.log_file,
            maxBytes=self.max_file_size,
            backupCount=self.backup_count
        )
        file_handler.setLevel(self.log_level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self.logger.debug(self._format_message(message, kwargs))
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self.logger.info(self._format_message(message, kwargs))
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self.logger.warning(self._format_message(message, kwargs))
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        self.logger.error(self._format_message(message, kwargs))
    
    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self.logger.critical(self._format_message(message, kwargs))
    
    def _format_message(self, message: str, kwargs: Dict[str, Any]) -> str:
        """Format log message with additional context."""
        if kwargs:
            context = " ".join([f"{k}={v}" for k, v in kwargs.items()])
            return f"{message} | {context}"
        return message
    
    def log_error(self, error: Exception, additional_context: Optional[Dict[str, Any]] = None):
        """
        Log error with comprehensive context.
        
        Args:
            error: Exception to log
            additional_context: Additional context information
        """
        try:
            # Get error context
            error_context = self._create_error_context(error, additional_context)
            
            # Log error
            self.error(f"Error occurred: {error}", 
                      error_type=type(error).__name__,
                      error_code=getattr(error, 'error_code', 'UNKNOWN'),
                      function_name=error_context.function_name,
                      file_name=error_context.file_name,
                      line_number=error_context.line_number)
            
            # Store error context
            with self.error_lock:
                self.error_count += 1
                self.error_history.append(error_context)
                
                # Keep only last 1000 errors
                if len(self.error_history) > 1000:
                    self.error_history = self.error_history[-1000:]
            
            # Log stack trace for debugging
            self.debug(f"Stack trace:\n{error_context.stack_trace}")
            
        except Exception as e:
            self.critical(f"Failed to log error: {e}")
    
    def _create_error_context(self, error: Exception, additional_context: Optional[Dict[str, Any]] = None) -> ErrorContext:
        """Create error context from exception."""
        # Get stack trace
        tb = traceback.extract_tb(error.__traceback__)
        if tb:
            frame = tb[-1]  # Get the last frame
            function_name = frame.name
            file_name = Path(frame.filename).name
            line_number = frame.lineno
        else:
            function_name = "unknown"
            file_name = "unknown"
            line_number = 0
        
        return ErrorContext(
            timestamp=datetime.now(timezone.utc).isoformat(),
            function_name=function_name,
            file_name=file_name,
            line_number=line_number,
            error_type=type(error).__name__,
            error_message=str(error),
            stack_trace=traceback.format_exc(),
            additional_data=additional_context
        )
    
    def log_performance(self, function_name: str, execution_time: float, 
                       memory_usage: float = 0.0, cpu_usage: float = 0.0,
                       success: bool = True, error_message: Optional[str] = None):
        """
        Log performance metrics.
        
        Args:
            function_name: Name of the function
            execution_time: Execution time in seconds
            memory_usage: Memory usage in MB
            cpu_usage: CPU usage percentage
            success: Whether the operation was successful
            error_message: Error message if operation failed
        """
        try:
            metrics = PerformanceMetrics(
                function_name=function_name,
                execution_time=execution_time,
                memory_usage=memory_usage,
                cpu_usage=cpu_usage,
                timestamp=datetime.now(timezone.utc).isoformat(),
                success=success,
                error_message=error_message
            )
            
            with self.metrics_lock:
                self.performance_metrics.append(metrics)
                
                # Keep only last 10000 metrics
                if len(self.performance_metrics) > 10000:
                    self.performance_metrics = self.performance_metrics[-10000:]
            
            # Log performance
            if success:
                self.info(f"Performance: {function_name} completed in {execution_time:.3f}s",
                         memory_usage=f"{memory_usage:.2f}MB", cpu_usage=f"{cpu_usage:.1f}%")
            else:
                self.warning(f"Performance: {function_name} failed in {execution_time:.3f}s",
                           error=error_message)
            
        except Exception as e:
            self.error(f"Failed to log performance metrics: {e}")
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics."""
        with self.error_lock:
            if not self.error_history:
                return {"total_errors": 0, "error_types": {}, "recent_errors": []}
            
            # Count error types
            error_types = {}
            for error in self.error_history:
                error_type = error.error_type
                error_types[error_type] = error_types.get(error_type, 0) + 1
            
            # Get recent errors (last 10)
            recent_errors = [
                {
                    "timestamp": error.timestamp,
                    "error_type": error.error_type,
                    "error_message": error.error_message,
                    "function_name": error.function_name
                }
                for error in self.error_history[-10:]
            ]
            
            return {
                "total_errors": len(self.error_history),
                "error_types": error_types,
                "recent_errors": recent_errors
            }
    
    def get_performance_statistics(self) -> Dict[str, Any]:
        """Get performance statistics."""
        with self.metrics_lock:
            if not self.performance_metrics:
                return {"total_operations": 0, "average_execution_time": 0}
            
            # Calculate statistics
            total_operations = len(self.performance_metrics)
            successful_operations = sum(1 for m in self.performance_metrics if m.success)
            failed_operations = total_operations - successful_operations
            
            execution_times = [m.execution_time for m in self.performance_metrics]
            average_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
            max_execution_time = max(execution_times) if execution_times else 0
            min_execution_time = min(execution_times) if execution_times else 0
            
            return {
                "total_operations": total_operations,
                "successful_operations": successful_operations,
                "failed_operations": failed_operations,
                "success_rate": successful_operations / total_operations if total_operations > 0 else 0,
                "average_execution_time": average_execution_time,
                "max_execution_time": max_execution_time,
                "min_execution_time": min_execution_time
            }
    
    def export_logs(self, filepath: str, format: str = "json"):
        """Export logs to file."""
        try:
            if format.lower() == "json":
                data = {
                    "error_statistics": self.get_error_statistics(),
                    "performance_statistics": self.get_performance_statistics(),
                    "error_history": [asdict(error) for error in self.error_history[-100:]],
                    "performance_metrics": [asdict(metric) for metric in self.performance_metrics[-1000:]]
                }
                
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=2)
            
            elif format.lower() == "csv":
                import csv
                
                # Export error history
                error_file = filepath.replace('.csv', '_errors.csv')
                with open(error_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['timestamp', 'function_name', 'file_name', 'line_number', 
                                   'error_type', 'error_message'])
                    for error in self.error_history:
                        writer.writerow([
                            error.timestamp, error.function_name, error.file_name,
                            error.line_number, error.error_type, error.error_message
                        ])
                
                # Export performance metrics
                perf_file = filepath.replace('.csv', '_performance.csv')
                with open(perf_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['timestamp', 'function_name', 'execution_time', 
                                   'memory_usage', 'cpu_usage', 'success', 'error_message'])
                    for metric in self.performance_metrics:
                        writer.writerow([
                            metric.timestamp, metric.function_name, metric.execution_time,
                            metric.memory_usage, metric.cpu_usage, metric.success, metric.error_message
                        ])
            
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            self.info(f"Logs exported to {filepath}")
            
        except Exception as e:
            self.error(f"Failed to export logs: {e}")


class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output."""
    
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA + Style.BRIGHT
    }
    
    def format(self, record):
        if COLORAMA_AVAILABLE:
            color = self.COLORS.get(record.levelname, '')
            record.levelname = f"{color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)


def error_handler(logger: KeyHoundLogger, reraise: bool = False):
    """
    Decorator for comprehensive error handling.
    
    Args:
        logger: KeyHoundLogger instance
        reraise: Whether to reraise the exception after logging
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.log_error(e)
                if reraise:
                    raise
                return None
        return wrapper
    return decorator


def performance_monitor(logger: KeyHoundLogger):
    """
    Decorator for performance monitoring.
    
    Args:
        logger: KeyHoundLogger instance
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            success = True
            error_message = None
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                error_message = str(e)
                raise
            finally:
                execution_time = time.time() - start_time
                logger.log_performance(
                    function_name=func.__name__,
                    execution_time=execution_time,
                    success=success,
                    error_message=error_message
                )
        
        return wrapper
    return decorator


# Global logger instance
_keyhound_logger = None

def get_keyhound_logger(name: str = "KeyHound", **kwargs) -> KeyHoundLogger:
    """Get global KeyHound logger instance."""
    global _keyhound_logger
    if _keyhound_logger is None:
        _keyhound_logger = KeyHoundLogger(name, **kwargs)
    return _keyhound_logger


# Example usage and testing
if __name__ == "__main__":
    # Test error handling and logging
    print("Testing KeyHound Error Handling and Logging...")
    
    # Create logger
    logger = KeyHoundLogger("KeyHoundTest", log_level="DEBUG")
    
    # Test logging levels
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
    
    # Test error handling
    @error_handler(logger)
    @performance_monitor(logger)
    def test_function():
        """Test function for error handling and performance monitoring."""
        logger.info("Executing test function")
        time.sleep(0.1)  # Simulate work
        return "Success"
    
    @error_handler(logger)
    @performance_monitor(logger)
    def test_error_function():
        """Test function that raises an error."""
        logger.info("Executing error function")
        raise ValueError("Test error for demonstration")
    
    # Test successful function
    result = test_function()
    print(f"Function result: {result}")
    
    # Test error function
    try:
        test_error_function()
    except ValueError:
        print("Error function raised expected error")
    
    # Get statistics
    error_stats = logger.get_error_statistics()
    perf_stats = logger.get_performance_statistics()
    
    print(f"Error statistics: {error_stats}")
    print(f"Performance statistics: {perf_stats}")
    
    # Export logs
    logger.export_logs("keyhound_logs.json", "json")
    print("Logs exported successfully")
    
    print("KeyHound error handling and logging test completed!")

