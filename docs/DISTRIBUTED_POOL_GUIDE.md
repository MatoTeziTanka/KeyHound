# KeyHound Enhanced - Distributed Pool Guide

## 🌍 Community-Powered Bitcoin Puzzle Solving

The KeyHound Enhanced Distributed Pool is a revolutionary community-driven system that allows anyone to contribute their computing power to solve Bitcoin puzzles and earn fair rewards based on their hardware performance.

## 🎯 How It Works

### Pool Structure
- **Pool Owner (You)**: Receives 40% of any found Bitcoin
- **Key Finder**: Receives 20% bonus for finding the private key
- **Community**: Receives 40% distributed fairly based on hardware performance

### Fair Reward Distribution
- **Hardware Performance Scoring**: 1-minute and 1-hour tests determine your contribution level
- **Multi-Device Support**: Run on multiple devices (phones, PCs, servers) for higher rewards
- **Performance Tracking**: Weekly cycles with hourly adjustments for optimal fairness
- **Secure Key Delivery**: Only the pool owner receives found private keys

## 🚀 Quick Start

### For Pool Owner (You)

1. **Start the Pool Server**:
   ```bash
   python scripts/start_distributed_pool.py --server --pool-owner YOUR_POOL_ID
   ```

2. **Access the Dashboard**:
   - Open: `http://localhost:8080/api/pool_dashboard`
   - Monitor participants, performance, and found keys

3. **Share with Community**:
   - Share the dashboard URL
   - Participants can join automatically

### For Community Participants

1. **Download KeyHound Enhanced**:
   ```bash
   git clone https://github.com/sethpizzaboy/KeyHound
   cd KeyHound
   pip install -r requirements.txt
   ```

2. **Join the Pool**:
   ```bash
   python scripts/start_distributed_pool.py --client --user-id YOUR_USER_ID --server-url POOL_SERVER_URL
   ```

3. **Automatic Setup**:
   - Hardware performance test runs automatically
   - Your reward percentage is calculated
   - Work assignments begin immediately

## 🔧 Hardware Performance Scoring

### Performance Test Phases

#### Phase 1: Quick Assessment (1 minute)
- **Private Key Generation**: Tests CPU performance
- **Address Generation**: Tests Bitcoin cryptography
- **Puzzle Solving**: Tests overall solving capability

#### Phase 2: Comprehensive Analysis (1 hour)
- **Extended Performance Tests**: More accurate scoring
- **Memory Stress Testing**: Evaluates sustained performance
- **Power Efficiency**: Rewards efficient devices

### Scoring Factors

1. **Base Hardware Score**:
   - CPU cores × frequency
   - RAM capacity
   - GPU count and memory
   - Device type (server/PC/mobile)

2. **Performance Score**:
   - Operations per second across all tests
   - Consistency across test runs
   - Sustained performance over time

3. **Efficiency Score**:
   - Performance per watt consumed
   - Mobile devices get efficiency bonus
   - Battery-powered devices get efficiency consideration

4. **Power Score**:
   - Sustained performance over time
   - Consistency across different workloads
   - Reliability factor

### Reward Percentage Calculation

- **Minimum**: 0.1% of found Bitcoin
- **Maximum**: 5.0% of found Bitcoin
- **Multi-Device Bonus**: Up to 2x for multiple devices
- **Performance Scaling**: Linear scaling based on combined score

## 📊 Performance Tracking Cycles

### Weekly Performance Cycles

1. **1 Hour**: Initial performance assessment
2. **6 Hours**: Early performance validation
3. **12 Hours**: Mid-day performance check
4. **18 Hours**: Evening performance review
5. **24 Hours**: Daily performance summary
6. **48 Hours**: Two-day performance analysis
7. **96 Hours**: Four-day performance evaluation
8. **1 Week**: Weekly performance reset with carryover

### Performance Adjustments

- **Upward Adjustments**: Better performance increases reward percentage
- **Downward Adjustments**: Poor performance decreases reward percentage
- **Carryover**: Previous week's best percentage is maintained
- **Fair Reset**: New weekly cycle starts with latest performance

## 🔐 Security Features

### Secure Key Delivery

1. **Encryption**: All found private keys are encrypted for pool owner only
2. **Metadata Tracking**: Full audit trail of key discovery
3. **Secure Transmission**: Encrypted communication channels
4. **No Key Exposure**: Participants never see private keys

### Pool Integrity

1. **Device Registration**: Unique device IDs prevent duplicate accounts
2. **Performance Validation**: Anti-cheat measures in performance tests
3. **Work Verification**: Cryptographic proof of work completion
4. **Audit Logging**: Complete transaction and activity logs

## 🌐 Multi-Platform Support

### Supported Devices

- **Desktop PCs**: Windows, macOS, Linux
- **Gaming PCs**: High-performance hardware with GPUs
- **Laptops**: Portable computing power
- **Mobile Devices**: Android, iOS (limited performance)
- **Servers**: Cloud instances, dedicated servers
- **Raspberry Pi**: ARM-based devices

### Device Type Considerations

- **Servers**: Highest performance, best rewards
- **Gaming PCs**: High performance with GPU acceleration
- **Desktop PCs**: Good performance for consistent rewards
- **Laptops**: Moderate performance, battery consideration
- **Mobile Devices**: Lower performance but efficiency bonus

## 📈 Pool Statistics Dashboard

### Real-Time Monitoring

- **Total Participants**: Current pool size
- **Active Participants**: Currently working participants
- **Keys Found**: Total successful puzzle solutions
- **Rewards Distributed**: Total Bitcoin distributed
- **Performance Leaderboard**: Top performers by score

### Individual Statistics

- **Your Rank**: Position among all participants
- **Your Reward Percentage**: Current reward share
- **Work Contributed**: Puzzles solved or attempted
- **Device Performance**: Hardware score and efficiency
- **Multi-Device Bonus**: Additional devices and their contributions

## 🛠️ Advanced Configuration

### Pool Server Configuration

```bash
python scripts/start_distributed_pool.py --server \
  --host 0.0.0.0 \
  --port 8080 \
  --pool-owner YOUR_POOL_ID \
  --debug
```

### Pool Client Configuration

```bash
python scripts/start_distributed_pool.py --client \
  --user-id YOUR_USER_ID \
  --device-name "My Gaming PC" \
  --server-url http://pool.example.com:8080
```

### Running Both Server and Client

```bash
python scripts/start_distributed_pool.py --both \
  --user-id YOUR_USER_ID \
  --pool-owner YOUR_POOL_ID
```

## 🔄 API Endpoints

### Pool Server API

- `GET /api/health` - Health check
- `POST /api/register` - Register new participant
- `POST /api/request_work` - Request puzzle work
- `POST /api/submit_key` - Submit found private key
- `POST /api/heartbeat` - Send activity heartbeat
- `GET /api/stats` - Get pool statistics
- `GET /api/participants` - Get participant list
- `GET /api/found_keys` - Get found keys (metadata only)
- `GET /api/pool_dashboard` - Pool dashboard page

### Example API Usage

```python
import requests

# Register participant
response = requests.post('http://pool.example.com:8080/api/register', json={
    'user_id': 'alice',
    'device_name': 'Gaming PC',
    'hardware_specs': {...},
    'performance_tests': [...],
    'hardware_score': {...}
})

# Request work
response = requests.post('http://pool.example.com:8080/api/request_work', json={
    'user_id': 'alice',
    'device_id': 'device_123',
    'capabilities': {
        'max_puzzle_bits': 66,
        'preferred_work_size': 1000000
    }
})

# Submit found key
response = requests.post('http://pool.example.com:8080/api/submit_key', json={
    'user_id': 'alice',
    'device_id': 'device_123',
    'puzzle_id': 'puzzle_66',
    'private_key': 'found_private_key',
    'public_key': 'derived_public_key',
    'address': 'bitcoin_address'
})
```

## 🎯 Reward Examples

### Example Scenarios

#### Scenario 1: Single Device User
- **Device**: Gaming PC with RTX 3080
- **Performance Score**: 2,500
- **Reward Percentage**: 2.5%
- **If 1 BTC Found**: Receives 0.025 BTC (2.5%)

#### Scenario 2: Multi-Device User
- **Devices**: Gaming PC + 2 Phones + Laptop
- **Combined Performance**: 3,200
- **Multi-Device Bonus**: 1.6x
- **Adjusted Score**: 5,120
- **Reward Percentage**: 5.0% (capped)
- **If 1 BTC Found**: Receives 0.05 BTC (5%)

#### Scenario 3: Server Owner
- **Device**: Dedicated Server with 32 CPU cores
- **Performance Score**: 4,800
- **Reward Percentage**: 4.8%
- **If 1 BTC Found**: Receives 0.048 BTC (4.8%)

### Pool Owner Rewards

- **Pool Owner Share**: 40% of any found Bitcoin
- **Key Finder Bonus**: 20% of any found Bitcoin
- **Community Pool**: 40% distributed among all participants

## 🚨 Important Notes

### Legal and Ethical Considerations

1. **Legal Compliance**: Ensure Bitcoin puzzle solving is legal in your jurisdiction
2. **Tax Implications**: Bitcoin rewards may be taxable income
3. **Responsible Participation**: Don't overload your devices
4. **Fair Play**: No cheating or manipulation of performance tests

### Technical Considerations

1. **Internet Connection**: Stable connection required for pool participation
2. **Device Temperature**: Monitor device temperature during intensive work
3. **Power Consumption**: Consider electricity costs vs. potential rewards
4. **Backup Plans**: Keep your pool owner keys secure and backed up

### Security Best Practices

1. **Secure Keys**: Use hardware wallets for pool owner keys
2. **Network Security**: Use VPN if connecting from public networks
3. **Device Security**: Keep devices updated and secure
4. **Backup Strategies**: Regular backups of important data

## 🆘 Troubleshooting

### Common Issues

#### Client Connection Issues
```bash
# Check server connectivity
curl http://pool.example.com:8080/api/health

# Verify client configuration
python scripts/start_distributed_pool.py --client --user-id test --server-url http://localhost:8080
```

#### Performance Test Failures
```bash
# Run hardware test manually
python pool/hardware_scorer.py

# Check system requirements
python -c "import psutil; print(f'CPU: {psutil.cpu_count()}, RAM: {psutil.virtual_memory().total / (1024**3):.1f} GB')"
```

#### Pool Server Issues
```bash
# Check server logs
python scripts/start_distributed_pool.py --server --debug

# Verify port availability
netstat -an | grep 8080
```

### Getting Help

1. **Check Logs**: Review application logs for error details
2. **Test Components**: Run individual components separately
3. **Verify Dependencies**: Ensure all required packages are installed
4. **Network Issues**: Check firewall and network connectivity

## 🌟 Future Enhancements

### Planned Features

- **GPU Acceleration**: Enhanced GPU support for better performance
- **Mobile Apps**: Native mobile applications for pool participation
- **Advanced Analytics**: Detailed performance analytics and insights
- **Automated Payouts**: Automatic Bitcoin distribution to participants
- **Pool Federation**: Multiple pool coordination and load balancing

### Community Contributions

- **Performance Optimizations**: Community-driven performance improvements
- **New Platforms**: Support for additional hardware platforms
- **Feature Requests**: Community-driven feature development
- **Bug Reports**: Help improve the system reliability

---

## 🎉 Join the Revolution!

The KeyHound Enhanced Distributed Pool represents the future of collaborative cryptocurrency puzzle solving. By combining the computing power of the community, we can tackle challenges that would be impossible for individual users while ensuring fair and transparent reward distribution.

**Start your journey today and be part of the next generation of Bitcoin puzzle solving!**

---

*KeyHound Enhanced - Distributed Pool System*  
*Community-Powered Bitcoin Cryptography* 🚀
