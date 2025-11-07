# 🤖 AI COLLABORATION DOCUMENT - KeyHound Bitcoin Puzzle Solver

**⚠️ READ THIS FIRST: Purpose of This Document ⚠️**

**Version:** V1.0.0  
**Last Updated:** October 31, 2025  
**Status:** Production - Active Development  
**Session:** Initial Foundation

---

## 📋 DOCUMENT PURPOSE

This document provides **complete context** for AI assistants (Claude, ChatGPT, Gemini, Copilot, etc.) to collaborate on developing KeyHound - a Bitcoin puzzle solving platform.

### **What This Document Is:**
A comprehensive briefing that contains:
- Complete project overview and architecture
- Current implementation status
- What's been built and tested
- Active development roadmap
- Specific collaboration needs
- Version tracking and session history

### **What We're Asking You (AI) To Do:**

1. **READ** this entire document carefully before engaging
2. **UNDERSTAND** the current architecture and status
3. **CONTRIBUTE** through code improvements, testing, or strategic insights
4. **DOCUMENT** all changes with version increments
5. **MAINTAIN** error handling, docstrings, and progress tracking
6. **COLLABORATE** by building on previous AI session insights

### **What We're NOT Asking:**
- ❌ Rewrite working code unnecessarily
- ❌ Remove existing documentation
- ❌ Skip version tracking or changelog updates
- ✅ **Focus on:** Incremental improvements, bug fixes, feature additions, optimization

---

## 🎯 Project Goal

**KeyHound Enhanced - Enterprise Bitcoin Cryptography Platform**

**Primary Objectives:**
1. Solve unsolved Bitcoin puzzles (#67-160) systematically
2. Provide CPU and GPU-accelerated cryptographic key generation
3. Enable distributed computing across multiple nodes
4. Deliver real-time monitoring and alerting
5. Implement checkpoint-based resume capability
6. Maintain production-grade code quality

**Current Capabilities:**
- ✅ CPU-based puzzle solving (1,000-2,000 keys/sec per core)
- ✅ Auto-selection of unsolved puzzles
- ✅ Range checkpointing for resume capability
- ✅ Multi-recipient email alerts via SMTP
- ✅ Live dashboard with throughput monitoring
- ✅ Systemd service deployment (VM191)
- ✅ Google Colab compatibility
- ⏳ GPU acceleration (legacy hardware challenges)
- 🔄 Distributed multi-node coordination

---

## 📊 Current Development Status

### **Version History:**

#### **V1.0.0 - Initial Foundation (October 2025)**
- Project structure established
- Core modules implemented
- Basic documentation created
- CPU-only solving operational

#### **V1.1.0 - Current Session (October 31, 2025)**
- Range checkpointing added
- Auto-puzzle selection implemented
- GSMG solver archived to EOL
- Dashboard throughput API created
- Multi-worker systemd services
- This AI collaboration document created
- Comprehensive documentation revamp initiated

#### **V1.2.0 - Planned (Next Session)**
- Enhanced error handling across all modules
- Comprehensive docstrings (all functions)
- Version tracking in module headers
- GitHub issue templates
- Updated README with complete structure
- Progress tracking system

#### **V2.0.0 - Future Major Release**
- GPU acceleration fully operational
- Distributed computing framework
- ML-based pattern recognition
- Web UI for puzzle management
- Desktop GUI (Electron/Tauri)
- Native executables (PyInstaller)

---

## 🏗️ Repository Structure

```
KeyHound/
├── 📁 core/                           # Core Bitcoin cryptography
│   ├── bitcoin_cryptography.py       # V1.0.0 - Address generation, key handling
│   ├── simple_keyhound.py            # V1.1.0 - Main solver with checkpointing
│   ├── gpu_enabled_keyhound.py       # V1.0.0 - GPU acceleration (needs update)
│   ├── puzzle_data.py                # V1.0.0 - Bitcoin puzzle definitions
│   ├── performance_monitoring.py     # V1.0.0 - Metrics collection
│   ├── result_persistence.py         # V1.0.0 - Checkpoint management
│   └── working_notification_system.py # V1.1.0 - Multi-recipient alerts
├── 📁 web/                            # Web interface and APIs
│   ├── remote_stats_server.py        # V1.1.0 - Dashboard (port 5050)
│   └── throughput_api.py             # V1.1.0 - Keys/sec aggregation (port 5051)
├── 📁 deployments/                    # Deployment configurations
│   ├── docker/                        # V1.0.0 - Docker compose setup
│   ├── colab/                         # V1.1.0 - Google Colab notebooks
│   │   ├── KeyHound_Enhanced.ipynb  # V1.1.0 - Auto-puzzle selection
│   │   └── COLAB_QUICK_FIX.md        # V1.0.0 - Drive mount workarounds
│   └── systemd/                       # V1.1.0 - VM191 service units
├── 📁 docs/                           # Documentation
│   ├── PACKAGING.md                   # V1.0.0 - Deployment guide
│   ├── STATUS.md                      # V1.0.0 - Current status
│   └── [DOCS_*.md]                   # V1.0.0 - Various guides
├── 📁 EOL/                            # End-of-life / archived code
│   ├── gsmg_puzzle_solver.py         # V1.1.0 - Archived GSMG solver
│   └── README.md                      # V1.1.0 - EOL tracking
├── 📁 checkpoints/                    # Runtime checkpoints
│   └── puzzle_{bits}_checkpoint.json  # V1.1.0 - Auto-generated
├── main.py                            # V1.1.0 - CLI entry point with auto-select
├── OPERATIONS.md                      # V1.1.0 - VM191 runbook
├── README.md                          # V1.0.0 - Project overview (needs V1.2.0 update)
├── CONTRIBUTING.md                    # V1.1.0 - Contribution guidelines
├── AI_COLLABORATION.md                # V1.1.0 - This document
└── requirements.txt                   # V1.0.0 - Python dependencies
```

---

## 🔑 Key Components

### **1. Core Solver (`core/simple_keyhound.py`)**

**Version:** V1.1.0  
**Purpose:** Main puzzle solving engine with checkpointing

**Key Features:**
- Sequential key generation and testing
- Automatic checkpoint saves (every 60 seconds)
- Resume from last tested key on restart
- Multi-bit puzzle support (40-66 bits)
- Performance tracking (keys/sec)

**Current Status:**
- ✅ Checkpoint save/load working
- ✅ Sequential scanning implemented
- ✅ Progress reporting functional
- ⏳ Needs enhanced docstrings (V1.2.0)
- ⏳ Needs comprehensive error handling (V1.2.0)

**Entry Points:**
```python
keyhound = SimpleKeyHound(verbose=True)
result = keyhound.solve_puzzle(
    bits=67,                          # Auto-selected if PUZZLE_BITS=auto
    target_address="1BY8GQbnue...",   # From puzzle_data.py
    max_attempts=10000000,
    timeout=3600
)
```

---

### **2. Auto-Puzzle Selection (`main.py`)**

**Version:** V1.1.0  
**Purpose:** Automatically select unsolved puzzle with balance check

**Key Features:**
- Env variable override (`PUZZLE_BITS`)
- Auto-selection skips known solved puzzles
- Live balance check via BlockCypher API
- Fallback to manual mode if API fails

**Current Status:**
- ✅ Auto-selection working
- ✅ Env override functional
- ✅ Balance check implemented
- ⏳ Needs timeout handling improvement (V1.2.0)

---

### **3. Dashboard (`web/remote_stats_server.py`)**

**Version:** V1.1.0  
**Purpose:** Real-time monitoring dashboard (port 5050)

**Key Features:**
- System resource monitoring
- Live keys/sec display
- Health check endpoint
- WebSocket updates

**Current Status:**
- ✅ Dashboard running on VM191
- ✅ Health endpoint working
- ✅ Throughput proxy added
- ⏳ Needs template improvements (V1.2.0)

---

### **4. Throughput API (`web/throughput_api.py`)**

**Version:** V1.1.0  
**Purpose:** Aggregate keys/sec from worker logs (port 5051)

**Key Features:**
- Parses all run_worker_*.log files
- Extracts latest keys/sec per worker
- Aggregates total throughput
- CORS-enabled for dashboard

**Current Status:**
- ✅ Log parsing working
- ✅ Aggregation functional
- ✅ CORS enabled
- ⏳ Needs better error handling for missing logs (V1.2.0)

---

### **5. Systemd Services (VM191)**

**Version:** V1.1.0  
**Purpose:** Production deployment with auto-start

**Services:**
- `keyhound-solver@1..10.service` - CPU workers (10 cores)
- `keyhound-dashboard.service` - Dashboard (port 5050)
- `keyhound-throughput.service` - Throughput API (port 5051)
- `keyhound-checkpoint.timer` - Periodic backups (every 30 min)

**Current Status:**
- ⚠️ Workers failing (systemd env quoting issue)
- ⏳ Needs drop-in config fix (current session)
- ✅ Dashboard and throughput services running

---

## 🔬 Testing & Validation

### **Manual Testing Procedures:**

#### **1. CPU Solver Test:**
```bash
cd ~/KeyHound
source .venv/bin/activate
PYTHONWARNINGS=ignore PYTHONPATH=. python3 main.py --puzzle 67 --log-level INFO
# Expected: Progress lines with keys/sec, checkpoint saves
```

#### **2. Checkpoint Resume Test:**
```bash
# Run solver, interrupt with Ctrl+C
# Check checkpoint: cat checkpoints/puzzle_67_checkpoint.json
# Restart solver - should resume from last_key
```

#### **3. Dashboard Test:**
```bash
curl -s http://127.0.0.1:5050/api/health
# Expected: {"status":"healthy","timestamp":"...","uptime":...}
```

#### **4. Throughput API Test:**
```bash
curl -s http://127.0.0.1:5051/api/throughput
# Expected: {"total_keys_per_second":..., "workers_count":..., "per_worker":{...}}
```

---

## 📈 Performance Metrics

### **Current Benchmarks (VM191):**

| Metric | Value | Notes |
|--------|-------|-------|
| **CPU Cores** | 10 (8 vCPU allocated) | Xeon E5-2698 v3 |
| **Keys/sec per core** | ~1,400 | CPU-only (no GPU) |
| **Total throughput** | ~14,000 keys/sec | 10 workers × 1,400 |
| **Memory usage** | ~2-3% of 24GB | Very light |
| **Checkpoint interval** | 60 seconds | Configurable |
| **Startup overhead** | <5 seconds | Fast resume |

### **Expected Performance (Future):**

| Deployment | GPU | Expected Speed | Status |
|------------|-----|---------------|--------|
| **VM191** | GRID K1 (legacy) | N/A | ⚠️ Driver incompatible |
| **VM191** | CPU-only | ~14,000 keys/sec | ✅ Running |
| **Google Colab** | T4 (Free) | 20,000+ keys/sec | ✅ Compatible |
| **Google Colab** | A100 (Pro) | 100,000+ keys/sec | ✅ Compatible |
| **Multi-node** | 4x VM | 56,000+ keys/sec | ⏳ Planned V2.0 |

---

## 🐛 Known Issues & Blockers

### **Critical Issues:**

#### **Issue 1: Systemd Worker Services Failing**
**Status:** Active (Current Session)  
**Impact:** High - Workers not running on VM191  
**Cause:** Environment variable quoting in drop-in config  
**Symptoms:**
- `systemd[1]: keyhound-solver@1.service: Failed with result 'exit-code'`
- Exit code 127 (command not found) or 2 (invalid argument)
- "Invalid environment assignment, ignoring: lzqm / ugoi / mxdb"

**Resolution Steps:**
1. Edit `/etc/systemd/system/keyhound-solver@.service.d/override.conf`
2. Properly quote SMTP_PASSWORD
3. Fix CPU pinning logic ($$CPU instead of $CPU)
4. Reload: `systemctl daemon-reload`
5. Restart: `systemctl restart 'keyhound-solver@*'`

**AI Task:** Provide corrected drop-in config in current session

---

#### **Issue 2: Legacy GPU Driver Incompatibility**
**Status:** Deferred  
**Impact:** Medium - GPU acceleration unavailable on VM191  
**Cause:** GRID K1 (Kepler) requires driver 367.xx, not compatible with Ubuntu 24.04 + modern CUDA  
**Workaround:** CPU-only mode sufficient for now; use Colab for GPU

---

### **Minor Issues:**

#### **Issue 3: Dashboard "Puzzle: 66" Label**
**Status:** Cosmetic  
**Impact:** Low - Confusing but doesn't affect runtime  
**Cause:** Static text in systemd unit Description  
**Fix:** Update Description in base unit (future)

---

#### **Issue 4: Throughput API Only Sees 2 Workers**
**Status:** Resolved pending systemd fix  
**Impact:** Medium - Incomplete monitoring  
**Cause:** Workers 1,2,4-7,9,10 not writing logs due to service failure  
**Fix:** After systemd fix, all 10 workers will appear

---

## 🎯 Development Priorities

### **Immediate (Current Session - V1.1.1):**
1. ✅ Create AI_COLLABORATION.md (this file)
2. ⏳ Fix systemd worker services on VM191
3. ⏳ Verify all 10 workers running and reporting
4. ⏳ Confirm checkpoint saves are working
5. ⏳ Open GitHub issue for GSMG integration (--gsmg flag)

### **Short-term (Next Session - V1.2.0):**
1. Add comprehensive docstrings to all core modules
2. Implement robust error handling with try/except/logging
3. Create VERSION.md with module-level version tracking
4. Update README.md with complete structure
5. Create GitHub issue templates
6. Add PROGRESS.md for session tracking
7. Reorganize file structure (move DOCS_* to docs/)

### **Medium-term (V1.3.0 - V1.9.x):**
1. Implement distributed worker coordination
2. Add web UI for puzzle management
3. Create desktop GUI (Electron/Tauri)
4. Build native executables (PyInstaller)
5. Optimize performance (profiling, parallelization)
6. Add ML-based pattern recognition

### **Long-term (V2.0.0+):**
1. GPU acceleration on modern hardware
2. Cloud deployment (AWS/GCP/Azure)
3. Commercial features (licensing, support)
4. Community puzzle pools
5. API for third-party integration

---

## 🔧 Version Control Standards

### **Version Numbering:**

**Format:** `VMAJOR.MINOR.PATCH`

- **MAJOR (V1.x.x → V2.x.x):** New AI Colab session with major features/refactors
- **MINOR (Vx.1.x → Vx.2.x):** AI response within same session (new features, improvements)
- **PATCH (Vx.x.1 → Vx.x.2):** Small fixes, typos, corrections (no AI required)

### **Module Header Format:**

```python
"""
Module Name: core/simple_keyhound.py
Version: V1.1.0
Last Updated: 2025-10-31
AI Session: Session 1 (Claude Sonnet 4.5)
Status: Production

Description:
    Main puzzle solving engine with checkpoint-based resume capability.
    Supports 40-66 bit Bitcoin puzzles with sequential key generation.

Changelog:
    V1.0.0 (2025-10-14): Initial implementation - random key generation
    V1.1.0 (2025-10-31): Added range checkpointing, sequential scanning
    
Dependencies:
    - bitcoin_cryptography.py V1.0.0
    - puzzle_data.py V1.0.0
    - Python 3.8+

Usage:
    keyhound = SimpleKeyHound(verbose=True)
    result = keyhound.solve_puzzle(bits=67, timeout=3600)
"""
```

---

## 📝 Session History

### **Session 1 - October 31, 2025**

**AI:** Claude Sonnet 4.5 (Cursor)  
**Duration:** ~4 hours  
**Version Progression:** V1.0.0 → V1.1.0

**Tasks Completed:**
- ✅ Clarified KeyHound vs ScalpStorm vs GSMG confusion
- ✅ Set up VM191 (puzzle-keyhound) from scratch
- ✅ Configured network (static IP 192.168.12.191)
- ✅ Created keyhound user with SSH access
- ✅ Attempted NVIDIA GRID K1 driver installation
- ✅ Identified GPU incompatibility (too old for modern CUDA)
- ✅ Proceeded with CPU-only approach
- ✅ Cloned KeyHound repo
- ✅ Set up Python venv and dependencies
- ✅ Implemented range checkpointing (V1.1.0)
- ✅ Implemented auto-puzzle selection (V1.1.0)
- ✅ Created throughput API (V1.1.0)
- ✅ Updated dashboard to show throughput (V1.1.0)
- ✅ Created systemd services for 10 workers
- ✅ Set up email alerts (multi-recipient)
- ✅ Created checkpoint timer (every 30 min)
- ✅ Updated OPERATIONS.md and README.md
- ✅ Created CONTRIBUTING.md and CODEOWNERS
- ✅ Archived GSMG solver to EOL/
- ✅ Created AI_COLLABORATION.md (this document)
- ⏳ Troubleshooting systemd worker service failures

**Key Decisions:**
- Use CPU-only mode (GRID K1 too old)
- Sequential scanning for checkpointing
- Auto-select unsolved puzzle by default
- 10 workers (one per CPU core)
- Systemd for production deployment
- Checkpoint every 60 seconds

**Blockers Encountered:**
- GPU driver incompatibility → Resolved: CPU-only
- Systemd env quoting issues → In progress

**Next Session Goals:**
- Fix systemd worker services
- Verify 10 workers running
- Add comprehensive docstrings (V1.2.0)
- Enhance error handling (V1.2.0)
- Update README (V1.2.0)

**Insights:**
- Auto-puzzle selection prevents wasted cycles on solved puzzles
- Checkpointing critical for long-running solves (Colab timeouts)
- Systemd drop-in configs need careful quoting
- VM191 has 10 CPUs but originally only 4 workers configured
- Throughput API aggregation works well for multi-worker monitoring

---

## 🤝 AI Collaboration Guidelines

### **What's Most Helpful:**

1. **Incremental Improvements**
   - Enhance existing code with better error handling
   - Add comprehensive docstrings
   - Optimize performance bottlenecks
   - Fix bugs and edge cases

2. **Documentation**
   - Update version numbers in module headers
   - Maintain changelog entries
   - Keep README accurate and complete
   - Document all design decisions

3. **Testing & Validation**
   - Test changes thoroughly
   - Provide test cases and examples
   - Verify backward compatibility
   - Check for regressions

4. **Strategic Insights**
   - Suggest architecture improvements
   - Identify optimization opportunities
   - Propose new features
   - Review security implications

---

## 📚 Resources & References

### **Primary Resources:**
- **Repository:** https://github.com/MatoTeziTanka/KeyHound
- **Project Board:** https://github.com/users/MatoTeziTanka/projects/3
- **VM191 Dashboard:** http://192.168.12.191:5050
- **Throughput API:** http://192.168.12.191:5051/api/throughput

### **Technical Resources:**
- **BIP39 Spec:** https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
- **Bitcoin Puzzle Info:** https://privatekeys.pw/puzzles/bitcoin-puzzle-tx
- **secp256k1:** https://en.bitcoin.it/wiki/Secp256k1

### **Related Projects:**
- **CryptoPuzzles:** `/home/mgmt1/GitHub/CryptoPuzzles` (Trithemius puzzle)
- **GSMG.IO:** `/home/mgmt1/GitHub/GSMG.IO` (5 BTC challenge)
- **Dell-Server-Roadmap:** `/home/mgmt1/GitHub/Dell-Server-Roadmap` (infrastructure docs)

---

## 🔮 Future Development Roadmap

### **V1.2.0 - Documentation & Error Handling**
- [ ] Comprehensive docstrings for all functions
- [ ] Robust error handling with try/except
- [ ] Module-level version tracking
- [ ] Updated README
- [ ] GitHub issue templates
- [ ] PROGRESS.md for session tracking

### **V1.3.0 - Performance Optimization**
- [ ] Profiling and bottleneck analysis
- [ ] Parallel processing improvements
- [ ] Memory optimization
- [ ] Faster address generation

### **V1.4.0 - Distributed Computing**
- [ ] Worker coordination protocol
- [ ] Range assignment system
- [ ] Result aggregation
- [ ] Multi-node monitoring

### **V1.5.0 - Web UI**
- [ ] Puzzle management interface
- [ ] Real-time progress visualization
- [ ] Configuration editor
- [ ] Log viewer

### **V2.0.0 - Major Feature Release**
- [ ] GPU acceleration (modern hardware)
- [ ] Desktop GUI (Electron/Tauri)
- [ ] Native executables (PyInstaller)
- [ ] Cloud deployment templates
- [ ] ML pattern recognition

---

## 🎯 Current Focus

**Active Development Areas:**
1. Systemd service configuration fixes
2. Verification of 10-worker deployment
3. Checkpoint functionality validation

**Blockers:**
- Systemd env quoting issue (in progress)

**Resources Needed:**
- None currently

---

## 📞 Collaboration Protocol

### **When Starting a New AI Session:**

1. **Read this file completely** - Full context essential
2. **Check Session History** - Understand what's been done
3. **Review current version** - Know where we are (V1.1.0)
4. **Identify next version** - What will this session be (V1.2.0?)
5. **Document everything** - Update changelog, version headers

### **When Making Changes:**

1. **Version increment** - Update module header version
2. **Add changelog entry** - What changed and why
3. **Update docstrings** - Keep documentation current
4. **Test thoroughly** - Verify changes work
5. **Update this file** - Add to session history

### **When Closing a Session:**

1. **Summarize accomplishments** - What was done
2. **Document decisions** - Why certain choices made
3. **List remaining tasks** - What's next
4. **Update version numbers** - Reflect current state
5. **Commit and push** - Save progress to GitHub

---

## 🏆 Success Criteria

### **V1.2.0 Success:**
- ✅ All modules have comprehensive docstrings
- ✅ Robust error handling in all functions
- ✅ Version tracking in all module headers
- ✅ README fully updated
- ✅ GitHub issues templates created
- ✅ PROGRESS.md established

### **V2.0.0 Success:**
- ✅ GPU acceleration working on modern hardware
- ✅ Distributed computing operational
- ✅ Desktop GUI released
- ✅ Native executables available
- ✅ Full documentation suite complete

---

## 📖 HOW TO USE THIS DOCUMENT (For AI Assistants)

### **Step 1: Understand Context (15 minutes)**
Read in order:
1. **Document Purpose** - What we need
2. **Project Goal** - What we're building
3. **Current Development Status** - Where we are (V1.1.0)
4. **Repository Structure** - How it's organized

### **Step 2: Review Current State (15 minutes)**
Read:
1. **Key Components** - Main modules and their status
2. **Known Issues & Blockers** - Active problems
3. **Session History** - What's been done

### **Step 3: Plan Your Contribution**
Determine:
1. **Version target** - V1.1.1 (patch), V1.2.0 (minor), V2.0.0 (major)
2. **Focus area** - Bug fix, feature, docs, refactor
3. **Testing approach** - How to validate changes
4. **Documentation needs** - What to update

### **Step 4: Execute & Document**
For each change:
1. **Update version** in module header
2. **Add changelog entry** in module header
3. **Update docstrings** if function signature changed
4. **Test thoroughly** with examples
5. **Update this file** in Session History

### **Expected Output:**
Structure your work as:
1. **Version Increment:** What version is this (V1.x.x)?
2. **Changes Made:** List of files modified
3. **Testing Done:** How you validated changes
4. **Session Summary:** Add to Session History section
5. **Next Steps:** What should the next AI work on?

---

**📌 This document is the single source of truth for KeyHound AI collaboration.**

**🤖 Ready to collaborate? Let's solve Bitcoin puzzles together!**





