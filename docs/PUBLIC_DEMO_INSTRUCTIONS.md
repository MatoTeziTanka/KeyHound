# KeyHound Enhanced - Public Demo Instructions

## Quick Start

### 1. Start the Demo Server
```bash
# Windows (Easy)
scripts\start_public_demo.bat

# Or manually
python scripts/start_remote_stats.py --host 0.0.0.0 --port 8080 --update-interval 5
```

### 2. Access the Dashboard

#### Local Access
- **URL**: http://localhost:8080
- **Description**: Access from the same machine

#### Network Access
- **URL**: http://192.168.1.8:8080
- **Description**: Access from other devices on your network

#### External Access (Public)
- **URL**: http://YOUR_EXTERNAL_IP:8080
- **Requirements**:
  - Configure port forwarding on your router (port 8080)
  - Replace `YOUR_EXTERNAL_IP` with your actual external IP
  - Ensure firewall allows connections on port 8080

## Configuration

### Port Forwarding Setup
1. Access your router's admin panel (usually 192.168.1.1 or 192.168.0.1)
2. Find "Port Forwarding" or "Virtual Server" settings
3. Add a rule:
   - **External Port**: 8080
   - **Internal IP**: 192.168.1.8
   - **Internal Port**: 8080
   - **Protocol**: TCP

### Firewall Configuration
1. Windows Firewall:
   - Allow Python through firewall
   - Or create inbound rule for port 8080

2. Router Firewall:
   - Ensure port 8080 is open
   - Some routers have additional security settings

## Demo Features

### Real-time Statistics
- Live KeyHound performance metrics
- System resource monitoring
- Connection status indicators
- Historical performance charts

### Access Methods
- **Web Browser**: Any modern browser
- **Mobile**: Responsive design for phones/tablets
- **API**: REST endpoints for programmatic access

## Security Notes

### Demo Mode
- This is a demo server for testing
- Not recommended for production use
- No authentication required
- Data is not persistent

### Production Deployment
- Use HTTPS in production
- Implement authentication
- Add rate limiting
- Use environment variables for secrets

## Troubleshooting

### Cannot Access from External Network
1. Check port forwarding configuration
2. Verify firewall settings
3. Test with local network first
4. Check if ISP blocks incoming connections

### Connection Refused
1. Ensure server is running
2. Check if port is available
3. Verify firewall settings
4. Try a different port

### Performance Issues
1. Reduce update interval
2. Check system resources
3. Monitor network usage
4. Optimize server configuration

## Support

For issues or questions:
- Check the logs in the terminal
- Review firewall and router settings
- Test with local access first
- Ensure all dependencies are installed

---

**KeyHound Enhanced Public Demo** - Share your Bitcoin cryptography platform with the world!
