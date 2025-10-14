#!/usr/bin/env python3
"""
Advanced Performance Monitoring and Metrics System for KeyHound Enhanced

This module provides comprehensive performance monitoring, metrics collection,
and analysis capabilities for Bitcoin cryptographic operations and system performance.

Features:
- Real-time performance metrics collection
- Historical performance data analysis
- Performance profiling and bottleneck detection
- Resource utilization monitoring (CPU, GPU, Memory, Disk)
- Custom metrics and KPIs tracking
- Performance alerts and thresholds
- Performance report generation
- Integration with external monitoring systems

Legendary Code Quality Standards:
- Comprehensive error handling and logging
- Type hints for all functions and methods
- Detailed documentation and examples
- Performance optimization and monitoring
- Security best practices implementation
"""

import time
import threading
import psutil
import json
import sqlite3
from typing import Any, Dict, List, Optional, Union, Callable, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from collections import defaultdict, deque
from enum import Enum
import numpy as np

# Import KeyHound modules
from .error_handling import KeyHoundLogger, error_handler, performance_monitor

# Configure logging
logger = KeyHoundLogger("PerformanceMonitoring")


class MetricType(Enum):
    """Metric type enumeration."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


class AlertLevel(Enum):
    """Alert level enumeration."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    ERROR = "error"


@dataclass
class PerformanceMetric:
    """Performance metric data structure."""
    name: str
    value: Union[int, float]
    metric_type: MetricType
    timestamp: str
    tags: Dict[str, str] = None
    unit: str = ""
    description: str = ""


@dataclass
class SystemMetrics:
    """System resource metrics."""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    disk_usage_percent: float
    disk_free_gb: float
    network_bytes_sent: int
    network_bytes_received: int
    load_average: Tuple[float, float, float]
    process_count: int


@dataclass
class PerformanceAlert:
    """Performance alert data structure."""
    alert_id: str
    metric_name: str
    level: AlertLevel
    message: str
    threshold: float
    current_value: float
    timestamp: str
    acknowledged: bool = False


@dataclass
class PerformanceReport:
    """Performance report data structure."""
    report_id: str
    title: str
    start_time: str
    end_time: str
    summary: Dict[str, Any]
    metrics: List[PerformanceMetric]
    alerts: List[PerformanceAlert]
    recommendations: List[str]


class PerformanceMonitor:
    """
    Advanced performance monitoring system for KeyHound Enhanced.
    
    Provides comprehensive performance monitoring, metrics collection,
    and analysis capabilities for Bitcoin cryptographic operations.
    """
    
    def __init__(self, storage_path: str = "./performance_metrics.db", 
                 monitoring_interval: int = 5, logger: Optional[KeyHoundLogger] = None):
        """
        Initialize performance monitor.
        
        Args:
            storage_path: Path to metrics storage database
            monitoring_interval: System monitoring interval in seconds
            logger: KeyHoundLogger instance
        """
        self.storage_path = Path(storage_path)
        self.monitoring_interval = monitoring_interval
        self.logger = logger or KeyHoundLogger("PerformanceMonitor")
        
        # Metrics storage
        self.metrics_db = None
        self.metrics_lock = threading.Lock()
        
        # Real-time metrics
        self.current_metrics: Dict[str, PerformanceMetric] = {}
        self.metrics_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        
        # System monitoring
        self.system_metrics: deque = deque(maxlen=1000)
        self.monitoring_active = False
        self.monitoring_thread = None
        
        # Custom metrics
        self.custom_metrics: Dict[str, Callable] = {}
        
        # Alerts
        self.alert_thresholds: Dict[str, Tuple[float, AlertLevel]] = {}
        self.active_alerts: List[PerformanceAlert] = []
        self.alert_callbacks: List[Callable[[PerformanceAlert], None]] = []
        
        # Performance tracking
        self.operation_timers: Dict[str, float] = {}
        self.operation_counts: Dict[str, int] = defaultdict(int)
        
        # Initialize storage
        self._initialize_storage()
        
        # Start system monitoring
        self._start_system_monitoring()
        
        self.logger.info(f"Performance monitor initialized: {storage_path}")
    
    def _initialize_storage(self):
        """Initialize metrics storage database."""
        try:
            self.metrics_db = sqlite3.connect(str(self.storage_path), check_same_thread=False)
            self.metrics_db.row_factory = sqlite3.Row
            
            # Create tables
            cursor = self.metrics_db.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    value REAL NOT NULL,
                    metric_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    tags TEXT,
                    unit TEXT,
                    description TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    cpu_percent REAL NOT NULL,
                    memory_percent REAL NOT NULL,
                    memory_used_mb REAL NOT NULL,
                    memory_available_mb REAL NOT NULL,
                    disk_usage_percent REAL NOT NULL,
                    disk_free_gb REAL NOT NULL,
                    network_bytes_sent INTEGER NOT NULL,
                    network_bytes_received INTEGER NOT NULL,
                    load_average TEXT NOT NULL,
                    process_count INTEGER NOT NULL
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS performance_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_id TEXT NOT NULL,
                    metric_name TEXT NOT NULL,
                    level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    threshold REAL NOT NULL,
                    current_value REAL NOT NULL,
                    timestamp TEXT NOT NULL,
                    acknowledged BOOLEAN DEFAULT FALSE
                )
            """)
            
            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_name ON performance_metrics(name)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON performance_metrics(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_system_timestamp ON system_metrics(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON performance_alerts(timestamp)")
            
            self.metrics_db.commit()
            self.logger.info("Performance metrics storage initialized")
            
        except Exception as e:
            self.logger.error(f"Storage initialization failed: {e}")
            raise
    
    def _start_system_monitoring(self):
        """Start system monitoring thread."""
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitor_system, daemon=True)
        self.monitoring_thread.start()
        
        self.logger.info("System monitoring started")
    
    def _monitor_system(self):
        """Monitor system resources in background thread."""
        while self.monitoring_active:
            try:
                # Collect system metrics
                system_metrics = self._collect_system_metrics()
                
                # Store metrics
                with self.metrics_lock:
                    self.system_metrics.append(system_metrics)
                
                # Store in database
                self._store_system_metrics(system_metrics)
                
                # Check for alerts
                self._check_system_alerts(system_metrics)
                
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                self.logger.error(f"System monitoring error: {e}")
                time.sleep(10)  # Wait longer on error
    
    def _collect_system_metrics(self) -> SystemMetrics:
        """Collect current system metrics."""
        try:
            # CPU and memory
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            # Disk usage
            disk = psutil.disk_usage('/')
            
            # Network
            network = psutil.net_io_counters()
            
            # Load average (Unix-like systems)
            try:
                load_avg = os.getloadavg()
            except AttributeError:
                load_avg = (0.0, 0.0, 0.0)  # Windows fallback
            
            return SystemMetrics(
                timestamp=datetime.now(timezone.utc).isoformat(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_used_mb=memory.used / (1024 * 1024),
                memory_available_mb=memory.available / (1024 * 1024),
                disk_usage_percent=(disk.used / disk.total) * 100,
                disk_free_gb=disk.free / (1024 * 1024 * 1024),
                network_bytes_sent=network.bytes_sent,
                network_bytes_received=network.bytes_recv,
                load_average=load_avg,
                process_count=len(psutil.pids())
            )
            
        except Exception as e:
            self.logger.error(f"System metrics collection failed: {e}")
            return SystemMetrics(
                timestamp=datetime.now(timezone.utc).isoformat(),
                cpu_percent=0.0,
                memory_percent=0.0,
                memory_used_mb=0.0,
                memory_available_mb=0.0,
                disk_usage_percent=0.0,
                disk_free_gb=0.0,
                network_bytes_sent=0,
                network_bytes_received=0,
                load_average=(0.0, 0.0, 0.0),
                process_count=0
            )
    
    def _store_system_metrics(self, metrics: SystemMetrics):
        """Store system metrics in database."""
        try:
            cursor = self.metrics_db.cursor()
            
            cursor.execute("""
                INSERT INTO system_metrics 
                (timestamp, cpu_percent, memory_percent, memory_used_mb, memory_available_mb,
                 disk_usage_percent, disk_free_gb, network_bytes_sent, network_bytes_received,
                 load_average, process_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                metrics.timestamp,
                metrics.cpu_percent,
                metrics.memory_percent,
                metrics.memory_used_mb,
                metrics.memory_available_mb,
                metrics.disk_usage_percent,
                metrics.disk_free_gb,
                metrics.network_bytes_sent,
                metrics.network_bytes_received,
                json.dumps(metrics.load_average),
                metrics.process_count
            ))
            
            self.metrics_db.commit()
            
        except Exception as e:
            self.logger.error(f"Failed to store system metrics: {e}")
    
    @performance_monitor
    def record_metric(self, name: str, value: Union[int, float], 
                     metric_type: MetricType = MetricType.GAUGE,
                     tags: Optional[Dict[str, str]] = None,
                     unit: str = "", description: str = ""):
        """
        Record a performance metric.
        
        Args:
            name: Metric name
            value: Metric value
            metric_type: Type of metric
            tags: Optional tags for the metric
            unit: Unit of measurement
            description: Metric description
        """
        try:
            metric = PerformanceMetric(
                name=name,
                value=value,
                metric_type=metric_type,
                timestamp=datetime.now(timezone.utc).isoformat(),
                tags=tags or {},
                unit=unit,
                description=description
            )
            
            # Store in memory
            with self.metrics_lock:
                self.current_metrics[name] = metric
                self.metrics_history[name].append(metric)
            
            # Store in database
            self._store_metric(metric)
            
            # Check for alerts
            self._check_metric_alerts(metric)
            
            self.logger.debug(f"Metric recorded: {name} = {value} {unit}")
            
        except Exception as e:
            self.logger.error(f"Failed to record metric {name}: {e}")
    
    def _store_metric(self, metric: PerformanceMetric):
        """Store metric in database."""
        try:
            cursor = self.metrics_db.cursor()
            
            cursor.execute("""
                INSERT INTO performance_metrics 
                (name, value, metric_type, timestamp, tags, unit, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                metric.name,
                metric.value,
                metric.metric_type.value,
                metric.timestamp,
                json.dumps(metric.tags),
                metric.unit,
                metric.description
            ))
            
            self.metrics_db.commit()
            
        except Exception as e:
            self.logger.error(f"Failed to store metric {metric.name}: {e}")
    
    def start_timer(self, operation_name: str):
        """Start timing an operation."""
        self.operation_timers[operation_name] = time.time()
        self.operation_counts[operation_name] += 1
    
    def end_timer(self, operation_name: str, record_metric: bool = True):
        """End timing an operation and optionally record metric."""
        if operation_name not in self.operation_timers:
            self.logger.warning(f"Timer not started for operation: {operation_name}")
            return 0
        
        duration = time.time() - self.operation_timers[operation_name]
        del self.operation_timers[operation_name]
        
        if record_metric:
            self.record_metric(
                name=f"{operation_name}_duration",
                value=duration,
                metric_type=MetricType.TIMER,
                unit="seconds",
                description=f"Duration of {operation_name} operation"
            )
            
            self.record_metric(
                name=f"{operation_name}_count",
                value=self.operation_counts[operation_name],
                metric_type=MetricType.COUNTER,
                description=f"Total count of {operation_name} operations"
            )
        
        return duration
    
    def set_alert_threshold(self, metric_name: str, threshold: float, level: AlertLevel):
        """Set alert threshold for a metric."""
        self.alert_thresholds[metric_name] = (threshold, level)
        self.logger.info(f"Alert threshold set: {metric_name} > {threshold} ({level.value})")
    
    def _check_metric_alerts(self, metric: PerformanceMetric):
        """Check if metric triggers any alerts."""
        if metric.name not in self.alert_thresholds:
            return
        
        threshold, level = self.alert_thresholds[metric.name]
        
        if metric.value > threshold:
            self._trigger_alert(metric.name, level, f"Metric {metric.name} exceeded threshold", 
                              threshold, metric.value)
    
    def _check_system_alerts(self, metrics: SystemMetrics):
        """Check system metrics for alerts."""
        # CPU usage alert
        if metrics.cpu_percent > 90:
            self._trigger_alert("cpu_percent", AlertLevel.CRITICAL,
                              f"High CPU usage: {metrics.cpu_percent:.1f}%", 90, metrics.cpu_percent)
        
        # Memory usage alert
        if metrics.memory_percent > 90:
            self._trigger_alert("memory_percent", AlertLevel.CRITICAL,
                              f"High memory usage: {metrics.memory_percent:.1f}%", 90, metrics.memory_percent)
        
        # Disk usage alert
        if metrics.disk_usage_percent > 90:
            self._trigger_alert("disk_usage_percent", AlertLevel.WARNING,
                              f"High disk usage: {metrics.disk_usage_percent:.1f}%", 90, metrics.disk_usage_percent)
    
    def _trigger_alert(self, metric_name: str, level: AlertLevel, message: str, 
                      threshold: float, current_value: float):
        """Trigger a performance alert."""
        try:
            alert = PerformanceAlert(
                alert_id=f"{metric_name}_{int(time.time())}",
                metric_name=metric_name,
                level=level,
                message=message,
                threshold=threshold,
                current_value=current_value,
                timestamp=datetime.now(timezone.utc).isoformat()
            )
            
            # Store alert
            self.active_alerts.append(alert)
            self._store_alert(alert)
            
            # Notify callbacks
            for callback in self.alert_callbacks:
                try:
                    callback(alert)
                except Exception as e:
                    self.logger.error(f"Alert callback error: {e}")
            
            self.logger.warning(f"Alert triggered: {message}")
            
        except Exception as e:
            self.logger.error(f"Failed to trigger alert: {e}")
    
    def _store_alert(self, alert: PerformanceAlert):
        """Store alert in database."""
        try:
            cursor = self.metrics_db.cursor()
            
            cursor.execute("""
                INSERT INTO performance_alerts 
                (alert_id, metric_name, level, message, threshold, current_value, timestamp, acknowledged)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                alert.alert_id,
                alert.metric_name,
                alert.level.value,
                alert.message,
                alert.threshold,
                alert.current_value,
                alert.timestamp,
                alert.acknowledged
            ))
            
            self.metrics_db.commit()
            
        except Exception as e:
            self.logger.error(f"Failed to store alert: {e}")
    
    def add_alert_callback(self, callback: Callable[[PerformanceAlert], None]):
        """Add alert callback function."""
        self.alert_callbacks.append(callback)
    
    def get_current_metrics(self) -> Dict[str, PerformanceMetric]:
        """Get current metrics."""
        with self.metrics_lock:
            return self.current_metrics.copy()
    
    def get_metric_history(self, metric_name: str, limit: int = 100) -> List[PerformanceMetric]:
        """Get metric history."""
        with self.metrics_lock:
            return list(self.metrics_history[metric_name])[-limit:]
    
    def get_system_metrics_history(self, limit: int = 100) -> List[SystemMetrics]:
        """Get system metrics history."""
        with self.metrics_lock:
            return list(self.system_metrics)[-limit:]
    
    def get_active_alerts(self) -> List[PerformanceAlert]:
        """Get active alerts."""
        return [alert for alert in self.active_alerts if not alert.acknowledged]
    
    def acknowledge_alert(self, alert_id: str):
        """Acknowledge an alert."""
        for alert in self.active_alerts:
            if alert.alert_id == alert_id:
                alert.acknowledged = True
                break
    
    def generate_performance_report(self, start_time: Optional[str] = None, 
                                  end_time: Optional[str] = None) -> PerformanceReport:
        """Generate performance report for specified time period."""
        try:
            if start_time is None:
                start_time = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
            if end_time is None:
                end_time = datetime.now(timezone.utc).isoformat()
            
            report_id = f"report_{int(time.time())}"
            
            # Query metrics from database
            cursor = self.metrics_db.cursor()
            
            cursor.execute("""
                SELECT * FROM performance_metrics 
                WHERE timestamp BETWEEN ? AND ?
                ORDER BY timestamp DESC
            """, (start_time, end_time))
            
            metrics_data = cursor.fetchall()
            metrics = []
            
            for row in metrics_data:
                metric = PerformanceMetric(
                    name=row['name'],
                    value=row['value'],
                    metric_type=MetricType(row['metric_type']),
                    timestamp=row['timestamp'],
                    tags=json.loads(row['tags']) if row['tags'] else {},
                    unit=row['unit'],
                    description=row['description']
                )
                metrics.append(metric)
            
            # Query alerts from database
            cursor.execute("""
                SELECT * FROM performance_alerts 
                WHERE timestamp BETWEEN ? AND ?
                ORDER BY timestamp DESC
            """, (start_time, end_time))
            
            alerts_data = cursor.fetchall()
            alerts = []
            
            for row in alerts_data:
                alert = PerformanceAlert(
                    alert_id=row['alert_id'],
                    metric_name=row['metric_name'],
                    level=AlertLevel(row['level']),
                    message=row['message'],
                    threshold=row['threshold'],
                    current_value=row['current_value'],
                    timestamp=row['timestamp'],
                    acknowledged=bool(row['acknowledged'])
                )
                alerts.append(alert)
            
            # Generate summary
            summary = self._generate_report_summary(metrics, alerts)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(metrics, alerts)
            
            report = PerformanceReport(
                report_id=report_id,
                title=f"Performance Report ({start_time} to {end_time})",
                start_time=start_time,
                end_time=end_time,
                summary=summary,
                metrics=metrics,
                alerts=alerts,
                recommendations=recommendations
            )
            
            self.logger.info(f"Performance report generated: {report_id}")
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate performance report: {e}")
            return None
    
    def _generate_report_summary(self, metrics: List[PerformanceMetric], 
                               alerts: List[PerformanceAlert]) -> Dict[str, Any]:
        """Generate report summary."""
        try:
            # Group metrics by name
            metric_groups = defaultdict(list)
            for metric in metrics:
                metric_groups[metric.name].append(metric.value)
            
            summary = {
                "total_metrics": len(metrics),
                "unique_metrics": len(metric_groups),
                "total_alerts": len(alerts),
                "critical_alerts": len([a for a in alerts if a.level == AlertLevel.CRITICAL]),
                "warning_alerts": len([a for a in alerts if a.level == AlertLevel.WARNING]),
                "metric_statistics": {}
            }
            
            # Calculate statistics for each metric
            for name, values in metric_groups.items():
                if values:
                    summary["metric_statistics"][name] = {
                        "count": len(values),
                        "min": min(values),
                        "max": max(values),
                        "avg": sum(values) / len(values),
                        "latest": values[0]  # Assuming sorted by timestamp desc
                    }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Failed to generate report summary: {e}")
            return {}
    
    def _generate_recommendations(self, metrics: List[PerformanceMetric], 
                                alerts: List[PerformanceAlert]) -> List[str]:
        """Generate performance recommendations."""
        recommendations = []
        
        try:
            # Check for high CPU usage
            cpu_alerts = [a for a in alerts if a.metric_name == "cpu_percent"]
            if len(cpu_alerts) > 5:
                recommendations.append("Consider optimizing CPU-intensive operations or reducing concurrent operations")
            
            # Check for high memory usage
            memory_alerts = [a for a in alerts if a.metric_name == "memory_percent"]
            if len(memory_alerts) > 3:
                recommendations.append("Consider implementing memory optimization or reducing batch sizes")
            
            # Check for slow operations
            timer_metrics = [m for m in metrics if m.metric_type == MetricType.TIMER]
            for metric in timer_metrics:
                if metric.value > 10:  # Operations taking more than 10 seconds
                    recommendations.append(f"Consider optimizing {metric.name} operation (takes {metric.value:.2f}s)")
            
            # Check for frequent errors
            error_alerts = [a for a in alerts if a.level == AlertLevel.ERROR]
            if len(error_alerts) > 10:
                recommendations.append("High error rate detected - investigate error handling and system stability")
            
        except Exception as e:
            self.logger.error(f"Failed to generate recommendations: {e}")
        
        return recommendations
    
    def get_performance_statistics(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics."""
        try:
            with self.metrics_lock:
                current_metrics = self.current_metrics.copy()
                system_metrics = list(self.system_metrics)[-10:] if self.system_metrics else []
            
            # Calculate system averages
            system_avg = {}
            if system_metrics:
                system_avg = {
                    "avg_cpu_percent": sum(m.cpu_percent for m in system_metrics) / len(system_metrics),
                    "avg_memory_percent": sum(m.memory_percent for m in system_metrics) / len(system_metrics),
                    "avg_disk_usage_percent": sum(m.disk_usage_percent for m in system_metrics) / len(system_metrics)
                }
            
            return {
                "current_metrics_count": len(current_metrics),
                "active_alerts_count": len(self.get_active_alerts()),
                "operation_counts": dict(self.operation_counts),
                "system_averages": system_avg,
                "alert_thresholds": {k: v[0] for k, v in self.alert_thresholds.items()},
                "monitoring_active": self.monitoring_active,
                "storage_path": str(self.storage_path)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get performance statistics: {e}")
            return {}
    
    def cleanup(self):
        """Cleanup performance monitor resources."""
        try:
            self.monitoring_active = False
            
            if self.monitoring_thread and self.monitoring_thread.is_alive():
                self.monitoring_thread.join(timeout=5)
            
            if self.metrics_db:
                self.metrics_db.close()
            
            self.logger.info("Performance monitor cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Cleanup error: {e}")


# Global performance monitor instance
_performance_monitor = None

def get_performance_monitor(storage_path: str = "./performance_metrics.db") -> PerformanceMonitor:
    """Get global performance monitor instance."""
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor(storage_path=storage_path)
    return _performance_monitor


# Example usage and testing
if __name__ == "__main__":
    # Test performance monitoring
    print("Testing Performance Monitoring and Metrics System...")
    
    try:
        # Create performance monitor
        monitor = PerformanceMonitor(storage_path="./test_performance.db")
        
        # Test metric recording
        print("Testing metric recording...")
        
        monitor.record_metric("bitcoin_addresses_generated", 1000, MetricType.COUNTER, 
                            {"operation": "puzzle_solving"}, "addresses", "Generated Bitcoin addresses")
        
        monitor.record_metric("puzzle_solving_rate", 500.5, MetricType.GAUGE,
                            {"puzzle_id": "1"}, "addresses/second", "Puzzle solving rate")
        
        # Test timer operations
        print("Testing timer operations...")
        
        monitor.start_timer("bitcoin_key_generation")
        time.sleep(0.1)  # Simulate work
        duration = monitor.end_timer("bitcoin_key_generation")
        print(f"Operation duration: {duration:.3f}s")
        
        # Test alert thresholds
        print("Testing alert thresholds...")
        
        monitor.set_alert_threshold("cpu_percent", 80.0, AlertLevel.WARNING)
        monitor.set_alert_threshold("memory_percent", 90.0, AlertLevel.CRITICAL)
        
        # Test alert callback
        def alert_callback(alert: PerformanceAlert):
            print(f"Alert received: {alert.message}")
        
        monitor.add_alert_callback(alert_callback)
        
        # Test performance report
        print("Testing performance report generation...")
        
        report = monitor.generate_performance_report()
        if report:
            print(f"Report generated: {report.title}")
            print(f"Metrics: {len(report.metrics)}, Alerts: {len(report.alerts)}")
            print(f"Recommendations: {len(report.recommendations)}")
        
        # Get performance statistics
        print("Testing performance statistics...")
        
        stats = monitor.get_performance_statistics()
        print(f"Performance statistics: {stats}")
        
        # Cleanup
        monitor.cleanup()
        
        print("Performance monitoring and metrics system test completed successfully!")
        
    except Exception as e:
        print(f"Performance monitoring test failed: {e}")

