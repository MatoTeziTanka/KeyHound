#!/usr/bin/env python3
"""
Advanced Memory Optimization Module for KeyHound Enhanced

This module provides comprehensive memory optimization for large key spaces
including memory pooling, streaming processing, and intelligent caching.

Features:
- Memory pooling for efficient allocation/deallocation
- Streaming processing for large datasets
- Intelligent caching with LRU and memory-aware eviction
- Memory monitoring and profiling
- Garbage collection optimization
- Memory-mapped file processing
- Batch processing with memory constraints

Legendary Code Quality Standards:
- Comprehensive error handling and logging
- Type hints for all functions and methods
- Detailed documentation and examples
- Performance optimization and monitoring
- Security best practices implementation
"""

import gc
import os
import sys
import time
import threading
import weakref
from typing import Optional, Dict, Any, List, Tuple, Union, Iterator, Callable
from dataclasses import dataclass, field
from collections import OrderedDict, deque
import mmap
import array
import numpy as np
import psutil
from pathlib import Path

# Import KeyHound modules
from error_handling import KeyHoundLogger, error_handler, performance_monitor

# Configure logging
logger = KeyHoundLogger("MemoryOptimization")


@dataclass
class MemoryStats:
    """Memory statistics for monitoring."""
    total_memory: int
    available_memory: int
    used_memory: int
    memory_percent: float
    cached_memory: int
    swap_memory: int
    timestamp: float


@dataclass
class MemoryPool:
    """Memory pool configuration."""
    pool_size: int
    chunk_size: int
    max_chunks: int
    pre_allocate: bool = True
    auto_grow: bool = True


class MemoryOptimizer:
    """
    Advanced memory optimization system for KeyHound Enhanced.
    
    Provides intelligent memory management for large-scale Bitcoin cryptographic
    operations with memory pooling, streaming processing, and intelligent caching.
    """
    
    def __init__(self, max_memory_mb: int = 1024, enable_monitoring: bool = True):
        """
        Initialize memory optimizer.
        
        Args:
            max_memory_mb: Maximum memory usage in MB
            enable_monitoring: Enable memory monitoring
        """
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.enable_monitoring = enable_monitoring
        self.logger = logger
        
        # Memory pools
        self.memory_pools: Dict[str, MemoryPool] = {}
        self.pooled_arrays: Dict[str, deque] = {}
        
        # Caching system
        self.cache = OrderedDict()
        self.cache_stats = {"hits": 0, "misses": 0, "evictions": 0}
        self.max_cache_size = self.max_memory_bytes // 4  # 25% for cache
        
        # Streaming processing
        self.streaming_enabled = True
        self.stream_chunk_size = 1024 * 1024  # 1MB chunks
        
        # Memory monitoring
        self.memory_stats: List[MemoryStats] = []
        self.monitoring_thread = None
        self.monitoring_active = False
        
        # Weak references for automatic cleanup
        self.weak_refs: List[weakref.ref] = []
        
        # Initialize memory pools
        self._initialize_memory_pools()
        
        # Start monitoring if enabled
        if self.enable_monitoring:
            self._start_monitoring()
        
        self.logger.info(f"Memory optimizer initialized with {max_memory_mb}MB limit")
    
    def _initialize_memory_pools(self):
        """Initialize memory pools for common data types."""
        # Pool for Bitcoin private keys (32 bytes each)
        self.memory_pools["private_keys"] = MemoryPool(
            pool_size=1024 * 1024,  # 1MB
            chunk_size=32,
            max_chunks=32768,
            pre_allocate=True
        )
        
        # Pool for Bitcoin addresses (25 bytes each)
        self.memory_pools["addresses"] = MemoryPool(
            pool_size=512 * 1024,  # 512KB
            chunk_size=25,
            max_chunks=20480,
            pre_allocate=True
        )
        
        # Pool for hash values (32 bytes each)
        self.memory_pools["hashes"] = MemoryPool(
            pool_size=2 * 1024 * 1024,  # 2MB
            chunk_size=32,
            max_chunks=65536,
            pre_allocate=True
        )
        
        # Initialize pooled arrays
        for pool_name, pool_config in self.memory_pools.items():
            self.pooled_arrays[pool_name] = deque()
            if pool_config.pre_allocate:
                self._pre_allocate_pool(pool_name, pool_config)
    
    def _pre_allocate_pool(self, pool_name: str, pool_config: MemoryPool):
        """Pre-allocate memory pool."""
        try:
            for _ in range(min(pool_config.max_chunks, 1000)):  # Limit pre-allocation
                chunk = bytearray(pool_config.chunk_size)
                self.pooled_arrays[pool_name].append(chunk)
            
            self.logger.debug(f"Pre-allocated {len(self.pooled_arrays[pool_name])} chunks for {pool_name}")
            
        except MemoryError as e:
            self.logger.warning(f"Memory allocation failed for {pool_name}: {e}")
    
    def get_pooled_array(self, pool_name: str, size: int = None) -> bytearray:
        """
        Get a pooled array from memory pool.
        
        Args:
            pool_name: Name of the memory pool
            size: Size of the array (default: pool chunk size)
            
        Returns:
            Pooled bytearray
        """
        if pool_name not in self.pooled_arrays:
            raise ValueError(f"Unknown pool: {pool_name}")
        
        pool_config = self.memory_pools[pool_name]
        chunk_size = size or pool_config.chunk_size
        
        # Try to get from pool
        if self.pooled_arrays[pool_name]:
            chunk = self.pooled_arrays[pool_name].popleft()
            if len(chunk) >= chunk_size:
                return chunk[:chunk_size]  # Truncate if needed
            else:
                # Return to pool and allocate new
                self.pooled_arrays[pool_name].append(chunk)
        
        # Allocate new chunk
        try:
            return bytearray(chunk_size)
        except MemoryError as e:
            self.logger.error(f"Memory allocation failed: {e}")
            raise
    
    def return_pooled_array(self, pool_name: str, chunk: bytearray):
        """
        Return a pooled array to memory pool.
        
        Args:
            pool_name: Name of the memory pool
            chunk: Array to return
        """
        if pool_name not in self.pooled_arrays:
            return
        
        pool_config = self.memory_pools[pool_name]
        
        # Check if we can return to pool
        if (len(self.pooled_arrays[pool_name]) < pool_config.max_chunks and
            len(chunk) <= pool_config.chunk_size):
            
            # Clear and resize if needed
            chunk[:] = b'\x00' * len(chunk)
            if len(chunk) < pool_config.chunk_size:
                chunk.extend(b'\x00' * (pool_config.chunk_size - len(chunk)))
            
            self.pooled_arrays[pool_name].append(chunk)
    
    @performance_monitor
    def cache_get(self, key: str) -> Any:
        """Get value from cache."""
        if key in self.cache:
            # Move to end (most recently used)
            value = self.cache.pop(key)
            self.cache[key] = value
            self.cache_stats["hits"] += 1
            return value
        
        self.cache_stats["misses"] += 1
        return None
    
    @performance_monitor
    def cache_set(self, key: str, value: Any, size_bytes: int = None):
        """
        Set value in cache with size tracking.
        
        Args:
            key: Cache key
            value: Value to cache
            size_bytes: Size in bytes (for memory tracking)
        """
        # Estimate size if not provided
        if size_bytes is None:
            if hasattr(value, '__sizeof__'):
                size_bytes = sys.getsizeof(value)
            else:
                size_bytes = 1024  # Default estimate
        
        # Evict if cache is too large
        while (len(self.cache) > 0 and 
               self._get_cache_memory_usage() + size_bytes > self.max_cache_size):
            self._evict_lru()
        
        # Add to cache
        self.cache[key] = value
        
        # Track with weak reference for cleanup
        if hasattr(value, '__weakref__'):
            self.weak_refs.append(weakref.ref(value))
    
    def _evict_lru(self):
        """Evict least recently used item from cache."""
        if self.cache:
            key, value = self.cache.popitem(last=False)
            self.cache_stats["evictions"] += 1
            self.logger.debug(f"Evicted cache item: {key}")
    
    def _get_cache_memory_usage(self) -> int:
        """Get approximate memory usage of cache."""
        total_size = 0
        for key, value in self.cache.items():
            total_size += sys.getsizeof(key) + sys.getsizeof(value)
        return total_size
    
    @performance_monitor
    def stream_process_keys(self, key_range: Tuple[int, int], 
                          process_func: Callable[[int], Any],
                          chunk_size: int = None) -> Iterator[Any]:
        """
        Stream process keys in chunks to minimize memory usage.
        
        Args:
            key_range: Tuple of (start, end) key range
            process_func: Function to process each key
            chunk_size: Size of each chunk
            
        Yields:
            Processed results
        """
        start_key, end_key = key_range
        chunk_size = chunk_size or self.stream_chunk_size
        
        self.logger.info(f"Stream processing keys {start_key} to {end_key} in chunks of {chunk_size}")
        
        current_key = start_key
        while current_key < end_key:
            # Calculate chunk bounds
            chunk_end = min(current_key + chunk_size, end_key)
            
            # Process chunk
            chunk_results = []
            for key in range(current_key, chunk_end):
                try:
                    result = process_func(key)
                    if result:
                        chunk_results.append(result)
                except Exception as e:
                    self.logger.warning(f"Error processing key {key}: {e}")
            
            # Yield results
            for result in chunk_results:
                yield result
            
            # Clean up chunk
            chunk_results.clear()
            gc.collect()
            
            # Check memory usage
            if self._is_memory_pressure():
                self.logger.warning("Memory pressure detected, forcing garbage collection")
                gc.collect()
                time.sleep(0.1)  # Brief pause
            
            current_key = chunk_end
    
    def _is_memory_pressure(self) -> bool:
        """Check if system is under memory pressure."""
        memory = psutil.virtual_memory()
        return memory.percent > 85  # 85% memory usage threshold
    
    @performance_monitor
    def memory_mapped_file(self, filepath: str, mode: str = 'r') -> mmap.mmap:
        """
        Create memory-mapped file for large data processing.
        
        Args:
            filepath: Path to file
            mode: File mode ('r', 'w', 'a')
            
        Returns:
            Memory-mapped file object
        """
        try:
            with open(filepath, mode + 'b') as f:
                mmap_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ if mode == 'r' else mmap.ACCESS_WRITE)
            
            self.logger.info(f"Created memory-mapped file: {filepath}")
            return mmap_file
            
        except Exception as e:
            self.logger.error(f"Failed to create memory-mapped file {filepath}: {e}")
            raise
    
    def _start_monitoring(self):
        """Start memory monitoring thread."""
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitor_memory, daemon=True)
        self.monitoring_thread.start()
        
        self.logger.info("Memory monitoring started")
    
    def _monitor_memory(self):
        """Monitor memory usage in background thread."""
        while self.monitoring_active:
            try:
                memory = psutil.virtual_memory()
                swap = psutil.swap_memory()
                
                stats = MemoryStats(
                    total_memory=memory.total,
                    available_memory=memory.available,
                    used_memory=memory.used,
                    memory_percent=memory.percent,
                    cached_memory=getattr(memory, 'cached', 0),
                    swap_memory=swap.used,
                    timestamp=time.time()
                )
                
                self.memory_stats.append(stats)
                
                # Keep only last 1000 measurements
                if len(self.memory_stats) > 1000:
                    self.memory_stats = self.memory_stats[-1000:]
                
                # Log high memory usage
                if memory.percent > 90:
                    self.logger.warning(f"High memory usage: {memory.percent:.1f}%")
                
                time.sleep(5)  # Monitor every 5 seconds
                
            except Exception as e:
                self.logger.error(f"Memory monitoring error: {e}")
                time.sleep(10)  # Wait longer on error
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get comprehensive memory statistics."""
        memory = psutil.virtual_memory()
        
        return {
            "current_memory": {
                "total_gb": memory.total / (1024**3),
                "available_gb": memory.available / (1024**3),
                "used_gb": memory.used / (1024**3),
                "percent": memory.percent
            },
            "cache_stats": self.cache_stats.copy(),
            "memory_pools": {
                name: {
                    "allocated_chunks": len(pooled_arrays),
                    "pool_size_mb": pool.pool_size / (1024*1024),
                    "chunk_size": pool.chunk_size
                }
                for name, pool in self.memory_pools.items()
                for pooled_arrays in [self.pooled_arrays[name]]
            },
            "optimization_limits": {
                "max_memory_mb": self.max_memory_bytes / (1024*1024),
                "max_cache_size_mb": self.max_cache_size / (1024*1024)
            }
        }
    
    def optimize_memory(self):
        """Perform memory optimization operations."""
        self.logger.info("Performing memory optimization...")
        
        # Clear cache if memory pressure
        if self._is_memory_pressure():
            self.cache.clear()
            self.cache_stats["evictions"] += len(self.cache)
            self.logger.info("Cleared cache due to memory pressure")
        
        # Force garbage collection
        collected = gc.collect()
        self.logger.info(f"Garbage collection freed {collected} objects")
        
        # Compact memory pools
        for pool_name in self.pooled_arrays:
            pool = self.pooled_arrays[pool_name]
            if len(pool) > 1000:  # Keep only 1000 chunks per pool
                excess = len(pool) - 1000
                for _ in range(excess):
                    pool.popleft()
        
        # Clear weak references
        self.weak_refs = [ref for ref in self.weak_refs if ref() is not None]
    
    def cleanup(self):
        """Cleanup memory optimizer resources."""
        self.logger.info("Cleaning up memory optimizer...")
        
        # Stop monitoring
        self.monitoring_active = False
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5)
        
        # Clear pools and cache
        for pool in self.pooled_arrays.values():
            pool.clear()
        
        self.cache.clear()
        self.weak_refs.clear()
        
        # Final garbage collection
        gc.collect()
        
        self.logger.info("Memory optimizer cleanup completed")


class StreamingKeyProcessor:
    """
    Streaming key processor for large-scale Bitcoin key operations.
    
    Processes keys in streaming fashion to minimize memory usage while
    maintaining high performance through intelligent batching and caching.
    """
    
    def __init__(self, memory_optimizer: MemoryOptimizer, batch_size: int = 10000):
        """
        Initialize streaming key processor.
        
        Args:
            memory_optimizer: Memory optimizer instance
            batch_size: Batch size for processing
        """
        self.memory_optimizer = memory_optimizer
        self.batch_size = batch_size
        self.logger = logger
        
        # Processing statistics
        self.stats = {
            "keys_processed": 0,
            "batches_processed": 0,
            "processing_time": 0,
            "memory_usage": 0
        }
    
    @performance_monitor
    def process_key_range(self, start_key: int, end_key: int, 
                         process_func: Callable[[int], Any]) -> Iterator[Any]:
        """
        Process a range of keys in streaming fashion.
        
        Args:
            start_key: Starting key value
            end_key: Ending key value
            process_func: Function to process each key
            
        Yields:
            Processed results
        """
        total_keys = end_key - start_key
        self.logger.info(f"Streaming processing {total_keys:,} keys from {start_key} to {end_key}")
        
        start_time = time.time()
        
        # Process in batches
        for batch_start in range(start_key, end_key, self.batch_size):
            batch_end = min(batch_start + self.batch_size, end_key)
            
            # Process batch
            batch_results = self._process_batch(batch_start, batch_end, process_func)
            
            # Yield results
            for result in batch_results:
                yield result
            
            # Update statistics
            batch_size = batch_end - batch_start
            self.stats["keys_processed"] += batch_size
            self.stats["batches_processed"] += 1
            
            # Memory optimization
            if self.stats["batches_processed"] % 10 == 0:
                self.memory_optimizer.optimize_memory()
        
        # Final statistics
        self.stats["processing_time"] = time.time() - start_time
        self.stats["memory_usage"] = psutil.virtual_memory().used
        
        self.logger.info(f"Streaming processing completed: {self.stats['keys_processed']:,} keys in {self.stats['processing_time']:.2f}s")
    
    def _process_batch(self, batch_start: int, batch_end: int, 
                      process_func: Callable[[int], Any]) -> List[Any]:
        """Process a batch of keys."""
        batch_results = []
        
        for key in range(batch_start, batch_end):
            try:
                result = process_func(key)
                if result:
                    batch_results.append(result)
            except Exception as e:
                self.logger.warning(f"Error processing key {key}: {e}")
        
        return batch_results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics."""
        if self.stats["processing_time"] > 0:
            keys_per_second = self.stats["keys_processed"] / self.stats["processing_time"]
        else:
            keys_per_second = 0
        
        return {
            **self.stats,
            "keys_per_second": keys_per_second,
            "memory_optimizer_stats": self.memory_optimizer.get_memory_stats()
        }


# Global memory optimizer instance
_memory_optimizer = None

def get_memory_optimizer(max_memory_mb: int = 1024) -> MemoryOptimizer:
    """Get global memory optimizer instance."""
    global _memory_optimizer
    if _memory_optimizer is None:
        _memory_optimizer = MemoryOptimizer(max_memory_mb=max_memory_mb)
    return _memory_optimizer


# Example usage and testing
if __name__ == "__main__":
    # Test memory optimization
    print("Testing Memory Optimization Module...")
    
    try:
        # Create memory optimizer
        memory_opt = MemoryOptimizer(max_memory_mb=512)
        
        # Test memory pooling
        print("Testing memory pooling...")
        private_key = memory_opt.get_pooled_array("private_keys")
        memory_opt.return_pooled_array("private_keys", private_key)
        print("Memory pooling test passed")
        
        # Test caching
        print("Testing caching...")
        memory_opt.cache_set("test_key", "test_value")
        cached_value = memory_opt.cache_get("test_key")
        print(f"Cached value: {cached_value}")
        
        # Test streaming processing
        print("Testing streaming processing...")
        def test_process_func(key):
            return key * 2 if key % 1000 == 0 else None
        
        results = list(memory_opt.stream_process_keys((0, 10000), test_process_func))
        print(f"Streaming processing results: {len(results)} items")
        
        # Get memory statistics
        stats = memory_opt.get_memory_stats()
        print(f"Memory statistics: {stats}")
        
        # Cleanup
        memory_opt.cleanup()
        
        print("Memory optimization module test completed successfully!")
        
    except Exception as e:
        print(f"Memory optimization test failed: {e}")
