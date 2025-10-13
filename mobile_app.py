#!/usr/bin/env python3
"""
Advanced Mobile App Companion for KeyHound Enhanced

This module provides comprehensive mobile app capabilities for KeyHound Enhanced,
enabling mobile monitoring, control, and management of Bitcoin cryptographic operations.

Features:
- Mobile-responsive web interface optimized for touch devices
- Progressive Web App (PWA) capabilities with offline support
- Real-time notifications and alerts for mobile devices
- Touch-optimized controls for puzzle solving and monitoring
- Mobile-specific performance optimizations
- Offline data synchronization and caching
- Mobile push notifications via service workers
- Cross-platform compatibility (iOS, Android, Web)
- Mobile-optimized charts and visualizations
- Gesture-based navigation and controls

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
import hashlib
import base64
from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from enum import Enum
import threading
import logging

# Web framework imports
try:
    from flask import Flask, render_template, jsonify, request, session, redirect, url_for, send_file
    from flask_socketio import SocketIO, emit, join_room, leave_room
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    Flask = None
    SocketIO = None

# Import KeyHound modules
from error_handling import KeyHoundLogger, error_handler, performance_monitor
from keyhound_enhanced import KeyHoundEnhanced
from web_interface import KeyHoundWebInterface, WebConfig

# Configure logging
logger = KeyHoundLogger("MobileApp")


class MobilePlatform(Enum):
    """Mobile platform enumeration."""
    IOS = "ios"
    ANDROID = "android"
    WEB = "web"
    PWA = "pwa"


class NotificationType(Enum):
    """Notification type enumeration."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    PUZZLE_SOLVED = "puzzle_solved"
    BENCHMARK_COMPLETE = "benchmark_complete"
    SYSTEM_ALERT = "system_alert"


@dataclass
class MobileConfig:
    """Mobile app configuration."""
    app_name: str = "KeyHound Mobile"
    version: str = "1.0.0"
    pwa_enabled: bool = True
    offline_support: bool = True
    push_notifications: bool = True
    touch_optimized: bool = True
    theme: str = "dark"
    auto_refresh_interval: int = 5
    max_offline_data_mb: int = 50


@dataclass
class MobileNotification:
    """Mobile notification data structure."""
    notification_id: str
    type: NotificationType
    title: str
    message: str
    timestamp: str
    data: Dict[str, Any] = None
    read: bool = False
    priority: int = 0


class KeyHoundMobileApp:
    """
    Advanced mobile app companion for KeyHound Enhanced.
    
    Provides comprehensive mobile capabilities for monitoring, control,
    and management of Bitcoin cryptographic operations.
    """
    
    def __init__(self, keyhound: KeyHoundEnhanced, mobile_config: MobileConfig,
                 web_interface: Optional[KeyHoundWebInterface] = None):
        """
        Initialize mobile app companion.
        
        Args:
            keyhound: KeyHoundEnhanced instance
            mobile_config: Mobile app configuration
            web_interface: Optional existing web interface
        """
        if not FLASK_AVAILABLE:
            raise ImportError("Flask and Flask-SocketIO are required for mobile app")
        
        self.keyhound = keyhound
        self.mobile_config = mobile_config
        self.logger = logger
        
        # Mobile-specific components
        self.mobile_app = None
        self.mobile_socketio = None
        self.notifications: List[MobileNotification] = []
        self.offline_data: Dict[str, Any] = {}
        self.service_worker_registered = False
        
        # Web interface integration
        self.web_interface = web_interface
        
        # Mobile-specific routes and handlers
        self._setup_mobile_app()
        self._setup_mobile_routes()
        self._setup_mobile_socketio()
        
        # Background tasks
        self.background_thread = None
        self.running = False
        
        self.logger.info(f"Mobile app companion initialized: {mobile_config.app_name}")
    
    def _setup_mobile_app(self):
        """Setup mobile app Flask instance."""
        try:
            self.mobile_app = Flask(__name__)
            self.mobile_app.config['SECRET_KEY'] = f"keyhound-mobile-{int(time.time())}"
            
            # Mobile-specific configuration
            self.mobile_app.config['MOBILE_OPTIMIZED'] = True
            self.mobile_app.config['TOUCH_FRIENDLY'] = True
            
            self.logger.info("Mobile app Flask instance created")
            
        except Exception as e:
            self.logger.error(f"Mobile app setup failed: {e}")
            raise
    
    def _setup_mobile_routes(self):
        """Setup mobile-specific routes."""
        
        @self.mobile_app.route('/mobile')
        def mobile_dashboard():
            """Mobile dashboard page."""
            return render_template('mobile_dashboard.html', config=self.mobile_config)
        
        @self.mobile_app.route('/mobile/pwa')
        def pwa_dashboard():
            """PWA dashboard page."""
            return render_template('pwa_dashboard.html', config=self.mobile_config)
        
        @self.mobile_app.route('/mobile/manifest.json')
        def mobile_manifest():
            """PWA manifest file."""
            manifest = {
                "name": self.mobile_config.app_name,
                "short_name": "KeyHound",
                "version": self.mobile_config.version,
                "description": "KeyHound Enhanced Mobile Companion",
                "start_url": "/mobile/pwa",
                "display": "standalone",
                "background_color": "#1a1a1a",
                "theme_color": "#667eea",
                "orientation": "portrait",
                "icons": [
                    {
                        "src": "/static/icons/icon-192.png",
                        "sizes": "192x192",
                        "type": "image/png"
                    },
                    {
                        "src": "/static/icons/icon-512.png",
                        "sizes": "512x512",
                        "type": "image/png"
                    }
                ],
                "categories": ["productivity", "utilities", "finance"],
                "screenshots": [
                    {
                        "src": "/static/screenshots/mobile-dashboard.png",
                        "sizes": "750x1334",
                        "type": "image/png"
                    }
                ]
            }
            return jsonify(manifest)
        
        @self.mobile_app.route('/mobile/sw.js')
        def service_worker():
            """Service worker for PWA capabilities."""
            sw_code = self._generate_service_worker()
            return sw_code, 200, {'Content-Type': 'application/javascript'}
        
        @self.mobile_app.route('/mobile/api/notifications')
        def api_notifications():
            """Get mobile notifications."""
            try:
                unread_count = len([n for n in self.notifications if not n.read])
                return jsonify({
                    "notifications": [asdict(n) for n in self.notifications[-20:]],  # Last 20
                    "unread_count": unread_count,
                    "total_count": len(self.notifications)
                })
            except Exception as e:
                self.logger.error(f"Notifications API error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.mobile_app.route('/mobile/api/notifications/<notification_id>/read', methods=['POST'])
        def api_mark_notification_read(notification_id: str):
            """Mark notification as read."""
            try:
                for notification in self.notifications:
                    if notification.notification_id == notification_id:
                        notification.read = True
                        break
                
                return jsonify({"success": True})
            except Exception as e:
                self.logger.error(f"Mark notification read error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.mobile_app.route('/mobile/api/offline-data')
        def api_offline_data():
            """Get offline data for mobile app."""
            try:
                # Include essential data for offline use
                offline_data = {
                    "system_status": self._get_basic_system_status(),
                    "recent_results": self._get_recent_results_offline(),
                    "notifications": [asdict(n) for n in self.notifications[-10:]],
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                
                return jsonify(offline_data)
            except Exception as e:
                self.logger.error(f"Offline data API error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.mobile_app.route('/mobile/api/quick-action', methods=['POST'])
        def api_quick_action():
            """Handle quick actions from mobile app."""
            try:
                data = request.get_json()
                action = data.get('action')
                
                if action == 'start_puzzle_solving':
                    puzzle_id = data.get('puzzle_id', 1)
                    return self._handle_quick_puzzle_solving(puzzle_id)
                
                elif action == 'start_brainwallet_test':
                    target_address = data.get('target_address')
                    return self._handle_quick_brainwallet_test(target_address)
                
                elif action == 'get_status':
                    return self._handle_quick_status_check()
                
                else:
                    return jsonify({"error": "Unknown action"}), 400
                    
            except Exception as e:
                self.logger.error(f"Quick action API error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.mobile_app.route('/mobile/api/touch-optimized')
        def api_touch_optimized():
            """Get touch-optimized interface data."""
            try:
                touch_data = {
                    "large_buttons": True,
                    "swipe_navigation": True,
                    "touch_targets": {
                        "min_size": 44,  # iOS recommended minimum
                        "spacing": 8
                    },
                    "gestures": {
                        "swipe_left": "next_page",
                        "swipe_right": "previous_page",
                        "pull_to_refresh": "refresh_data",
                        "long_press": "context_menu"
                    },
                    "haptic_feedback": True,
                    "voice_commands": False  # Could be enabled for accessibility
                }
                
                return jsonify(touch_data)
            except Exception as e:
                self.logger.error(f"Touch optimized API error: {e}")
                return jsonify({"error": str(e)}), 500
    
    def _setup_mobile_socketio(self):
        """Setup mobile-specific SocketIO handlers."""
        try:
            self.mobile_socketio = SocketIO(self.mobile_app, cors_allowed_origins="*")
            
            @self.mobile_socketio.on('mobile_connect')
            def handle_mobile_connect():
                """Handle mobile client connection."""
                session_id = request.sid
                
                # Send initial mobile data
                initial_data = {
                    "app_name": self.mobile_config.app_name,
                    "version": self.mobile_config.version,
                    "notifications": len(self.notifications),
                    "system_status": self._get_basic_system_status()
                }
                
                emit('mobile_initial_data', initial_data)
                
                # Join mobile room
                join_room('mobile_clients')
                
                self.logger.info(f"Mobile client connected: {session_id}")
            
            @self.mobile_socketio.on('mobile_disconnect')
            def handle_mobile_disconnect():
                """Handle mobile client disconnection."""
                session_id = request.sid
                leave_room('mobile_clients')
                
                self.logger.info(f"Mobile client disconnected: {session_id}")
            
            @self.mobile_socketio.on('mobile_notification_subscribe')
            def handle_notification_subscribe():
                """Handle mobile notification subscription."""
                join_room('mobile_notifications')
                self.logger.info("Mobile client subscribed to notifications")
            
            @self.mobile_socketio.on('mobile_swipe_action')
            def handle_swipe_action(data):
                """Handle mobile swipe gestures."""
                direction = data.get('direction')
                
                if direction == 'left':
                    emit('mobile_navigate', {'action': 'next_page'})
                elif direction == 'right':
                    emit('mobile_navigate', {'action': 'previous_page'})
                elif direction == 'up':
                    emit('mobile_refresh', {'action': 'pull_to_refresh'})
                
                self.logger.debug(f"Mobile swipe action: {direction}")
            
            @self.mobile_socketio.on('mobile_long_press')
            def handle_long_press(data):
                """Handle mobile long press gestures."""
                element = data.get('element')
                
                emit('mobile_context_menu', {
                    'element': element,
                    'actions': ['copy', 'share', 'bookmark']
                })
                
                self.logger.debug(f"Mobile long press on: {element}")
            
            self.logger.info("Mobile SocketIO handlers setup completed")
            
        except Exception as e:
            self.logger.error(f"Mobile SocketIO setup failed: {e}")
            raise
    
    def _generate_service_worker(self) -> str:
        """Generate service worker code for PWA capabilities."""
        sw_code = """
const CACHE_NAME = 'keyhound-mobile-v1';
const OFFLINE_URL = '/mobile/offline';

const urlsToCache = [
    '/mobile/pwa',
    '/static/css/mobile.css',
    '/static/js/mobile.js',
    '/mobile/manifest.json'
];

// Install service worker
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => cache.addAll(urlsToCache))
    );
});

// Fetch event
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                // Return cached version or fetch from network
                return response || fetch(event.request);
            })
    );
});

// Background sync for offline actions
self.addEventListener('sync', (event) => {
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

// Push notifications
self.addEventListener('push', (event) => {
    const options = {
        body: event.data ? event.data.text() : 'KeyHound notification',
        icon: '/static/icons/icon-192.png',
        badge: '/static/icons/badge-72.png',
        vibrate: [100, 50, 100],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        },
        actions: [
            {
                action: 'explore',
                title: 'View Details',
                icon: '/static/icons/checkmark.png'
            },
            {
                action: 'close',
                title: 'Close',
                icon: '/static/icons/xmark.png'
            }
        ]
    };

    event.waitUntil(
        self.registration.showNotification('KeyHound Enhanced', options)
    );
});

// Notification click
self.addEventListener('notificationclick', (event) => {
    event.notification.close();

    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('/mobile/pwa')
        );
    }
});

async function doBackgroundSync() {
    // Sync offline data when connection is restored
    try {
        const response = await fetch('/mobile/api/offline-data');
        const data = await response.json();
        
        // Update local storage with synced data
        localStorage.setItem('keyhound_offline_data', JSON.stringify(data));
        
        console.log('Background sync completed');
    } catch (error) {
        console.error('Background sync failed:', error);
    }
}
"""
        return sw_code
    
    def _get_basic_system_status(self) -> Dict[str, Any]:
        """Get basic system status for mobile app."""
        try:
            return {
                "status": "running",
                "found_keys": len(self.keyhound.found_keys),
                "gpu_enabled": self.keyhound.use_gpu,
                "thread_count": self.keyhound.num_threads,
                "uptime": time.time() - (self.keyhound.start_time or time.time()),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            self.logger.error(f"Basic system status error: {e}")
            return {"status": "error", "error": str(e)}
    
    def _get_recent_results_offline(self) -> List[Dict[str, Any]]:
        """Get recent results for offline mobile access."""
        try:
            if self.keyhound.result_persistence:
                results = self.keyhound.result_persistence.list_results(limit=5)
                return [asdict(result) for result in results]
            else:
                return []
        except Exception as e:
            self.logger.error(f"Recent results offline error: {e}")
            return []
    
    def _handle_quick_puzzle_solving(self, puzzle_id: int) -> Dict[str, Any]:
        """Handle quick puzzle solving from mobile."""
        try:
            # Start puzzle solving in background
            def solve_puzzle():
                try:
                    result = self.keyhound.solve_bitcoin_puzzle_streaming(puzzle_id, max_keys=100000)
                    
                    # Send notification
                    self.send_mobile_notification(
                        NotificationType.PUZZLE_SOLVED,
                        f"Puzzle {puzzle_id} Result",
                        f"Puzzle solving completed: {'Solution found' if result else 'No solution found'}"
                    )
                    
                except Exception as e:
                    self.send_mobile_notification(
                        NotificationType.ERROR,
                        "Puzzle Solving Error",
                        f"Error solving puzzle {puzzle_id}: {str(e)}"
                    )
            
            thread = threading.Thread(target=solve_puzzle, daemon=True)
            thread.start()
            
            return {
                "success": True,
                "message": f"Puzzle solving started for puzzle {puzzle_id}",
                "estimated_time": "5-10 minutes"
            }
            
        except Exception as e:
            self.logger.error(f"Quick puzzle solving error: {e}")
            return {"success": False, "error": str(e)}
    
    def _handle_quick_brainwallet_test(self, target_address: str) -> Dict[str, Any]:
        """Handle quick brainwallet test from mobile."""
        try:
            if not target_address:
                return {"success": False, "error": "Target address required"}
            
            # Start brainwallet test in background
            def test_brainwallet():
                try:
                    result = self.keyhound.brainwallet_security_test(target_address, max_patterns=5000)
                    
                    # Send notification
                    self.send_mobile_notification(
                        NotificationType.SUCCESS,
                        "Brainwallet Test Complete",
                        f"Found {len(result) if result else 0} matches for {target_address[:10]}..."
                    )
                    
                except Exception as e:
                    self.send_mobile_notification(
                        NotificationType.ERROR,
                        "Brainwallet Test Error",
                        f"Error testing {target_address[:10]}...: {str(e)}"
                    )
            
            thread = threading.Thread(target=test_brainwallet, daemon=True)
            thread.start()
            
            return {
                "success": True,
                "message": f"Brainwallet test started for {target_address[:10]}...",
                "estimated_time": "2-5 minutes"
            }
            
        except Exception as e:
            self.logger.error(f"Quick brainwallet test error: {e}")
            return {"success": False, "error": str(e)}
    
    def _handle_quick_status_check(self) -> Dict[str, Any]:
        """Handle quick status check from mobile."""
        try:
            status = self._get_basic_system_status()
            
            # Add mobile-specific status
            status.update({
                "mobile_app_version": self.mobile_config.version,
                "pwa_enabled": self.mobile_config.pwa_enabled,
                "notifications_count": len(self.notifications),
                "offline_data_size": len(str(self.offline_data))
            })
            
            return {"success": True, "status": status}
            
        except Exception as e:
            self.logger.error(f"Quick status check error: {e}")
            return {"success": False, "error": str(e)}
    
    def send_mobile_notification(self, notification_type: NotificationType, 
                               title: str, message: str, data: Dict[str, Any] = None):
        """
        Send mobile notification.
        
        Args:
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            data: Additional notification data
        """
        try:
            notification_id = f"mobile_{int(time.time() * 1000)}"
            
            notification = MobileNotification(
                notification_id=notification_id,
                type=notification_type,
                title=title,
                message=message,
                timestamp=datetime.now(timezone.utc).isoformat(),
                data=data or {},
                priority=self._get_notification_priority(notification_type)
            )
            
            self.notifications.append(notification)
            
            # Keep only last 100 notifications
            if len(self.notifications) > 100:
                self.notifications = self.notifications[-100:]
            
            # Send via SocketIO to mobile clients
            if self.mobile_socketio:
                self.mobile_socketio.emit('mobile_notification', asdict(notification), room='mobile_notifications')
            
            self.logger.info(f"Mobile notification sent: {title}")
            
        except Exception as e:
            self.logger.error(f"Mobile notification send error: {e}")
    
    def _get_notification_priority(self, notification_type: NotificationType) -> int:
        """Get notification priority based on type."""
        priority_map = {
            NotificationType.ERROR: 3,
            NotificationType.WARNING: 2,
            NotificationType.PUZZLE_SOLVED: 3,
            NotificationType.BENCHMARK_COMPLETE: 2,
            NotificationType.SYSTEM_ALERT: 3,
            NotificationType.SUCCESS: 1,
            NotificationType.INFO: 0
        }
        return priority_map.get(notification_type, 0)
    
    def start_mobile_app(self, host: str = "0.0.0.0", port: int = 5001):
        """Start mobile app server."""
        try:
            self.running = True
            
            self.logger.info(f"Starting mobile app on {host}:{port}")
            
            self.mobile_socketio.run(
                self.mobile_app,
                host=host,
                port=port,
                debug=False
            )
            
        except Exception as e:
            self.logger.error(f"Mobile app start error: {e}")
            raise
    
    def stop_mobile_app(self):
        """Stop mobile app server."""
        self.running = False
        self.logger.info("Mobile app stopped")
    
    def get_mobile_statistics(self) -> Dict[str, Any]:
        """Get mobile app statistics."""
        try:
            return {
                "app_name": self.mobile_config.app_name,
                "version": self.mobile_config.version,
                "pwa_enabled": self.mobile_config.pwa_enabled,
                "notifications_total": len(self.notifications),
                "notifications_unread": len([n for n in self.notifications if not n.read]),
                "offline_data_entries": len(self.offline_data),
                "service_worker_registered": self.service_worker_registered,
                "touch_optimized": self.mobile_config.touch_optimized,
                "push_notifications_enabled": self.mobile_config.push_notifications
            }
        except Exception as e:
            self.logger.error(f"Mobile statistics error: {e}")
            return {}


def create_mobile_app(keyhound: KeyHoundEnhanced, 
                     mobile_config: Optional[MobileConfig] = None) -> KeyHoundMobileApp:
    """Create mobile app companion instance."""
    if mobile_config is None:
        mobile_config = MobileConfig()
    
    return KeyHoundMobileApp(keyhound, mobile_config)


# Example usage and testing
if __name__ == "__main__":
    # Test mobile app
    print("Testing KeyHound Mobile App Companion...")
    
    try:
        # Create KeyHound instance
        keyhound = KeyHoundEnhanced(use_gpu=False, verbose=True)
        
        # Create mobile app
        mobile_config = MobileConfig(
            app_name="KeyHound Mobile Test",
            version="1.0.0",
            pwa_enabled=True,
            theme="dark"
        )
        
        mobile_app = create_mobile_app(keyhound, mobile_config)
        
        print("Mobile app companion created successfully")
        print(f"Access mobile interface at: http://localhost:5001/mobile")
        print(f"Access PWA interface at: http://localhost:5001/mobile/pwa")
        print("Press Ctrl+C to stop")
        
        # Start mobile app
        mobile_app.start_mobile_app(host="127.0.0.1", port=5001)
        
    except Exception as e:
        print(f"Mobile app test failed: {e}")
