#!/usr/bin/env python3
"""
Add User Tutorials Task to GitHub Project
"""

import subprocess
import json
import sys
import os
from pathlib import Path

def load_api_keys():
    """Load API keys from CursorAI directory."""
    cursorai_path = Path(__file__).parent.parent.parent / "CursorAI" / "api_keys.env"
    
    if not cursorai_path.exists():
        print("[ERROR] API keys file not found at:", cursorai_path)
        return None
    
    api_keys = {}
    with open(cursorai_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                api_keys[key] = value
    
    return api_keys

def create_user_tutorials_issue(repo, github_token):
    """Create user tutorials issue using GitHub API."""
    print("[INFO] Creating User Tutorials Issue using API...")
    
    import requests
    
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    issue_data = {
        "title": "[DOCUMENTATION] Create comprehensive user tutorials and guides",
        "body": """## User Tutorials and Guides

### Goal
Create comprehensive user tutorials to improve user experience and make KeyHound Enhanced accessible to users of all skill levels.

### Tasks
- Create beginner-friendly installation guide
- Write step-by-step puzzle solving tutorials
- Create brainwallet testing walkthrough
- Add web interface usage guide
- Create deployment tutorials for different environments
- Add troubleshooting guide with common issues
- Create video tutorials (optional)
- Add interactive examples and demos

### Tutorials Needed
1. **Getting Started Tutorial**
   - Installation on different platforms
   - Basic configuration
   - First puzzle solve

2. **Puzzle Solving Tutorial**
   - Understanding Bitcoin puzzles
   - Choosing puzzle difficulty
   - Monitoring progress
   - Interpreting results

3. **Brainwallet Testing Tutorial**
   - Setting up brainwallet tests
   - Understanding patterns
   - Security recommendations

4. **Web Interface Tutorial**
   - Dashboard navigation
   - Real-time monitoring
   - Configuration management

5. **Deployment Tutorials**
   - Docker deployment
   - Google Colab setup
   - Cloud deployment
   - Local development

6. **Advanced Features Tutorial**
   - GPU acceleration setup
   - Distributed computing
   - Performance optimization

### Acceptance Criteria
- Clear, step-by-step instructions
- Screenshots and examples
- Beginner to advanced progression
- Cross-platform compatibility
- Error handling and troubleshooting
- Interactive elements where possible

### Priority
Low - Important for user experience but not blocking core functionality

### Target Milestone
v1.2.0 - Documentation & Quality""",
        "labels": ["type: documentation", "priority: low", "component: core", "status: needs-review"]
    }
    
    url = f"https://api.github.com/repos/{repo}/issues"
    
    response = requests.post(url, headers=headers, json=issue_data)
    if response.status_code == 201:
        issue_data = response.json()
        issue_number = issue_data["number"]
        print(f"[SUCCESS] Created user tutorials issue: {issue_data['title']}")
        print(f"[INFO] Issue number: #{issue_number}")
        print(f"[INFO] Issue URL: {issue_data['html_url']}")
        return issue_number
    else:
        print(f"[ERROR] Failed to create issue: {response.text}")
        return None

def main():
    """Main function to add user tutorials task."""
    print("Adding User Tutorials Task to GitHub Project")
    print("===========================================")
    
    # Load API keys
    api_keys = load_api_keys()
    if not api_keys:
        print("[ERROR] Could not load API keys")
        return
    
    github_token = api_keys.get('GITHUB_TOKEN')
    if not github_token:
        print("[ERROR] GitHub token not found in API keys")
        return
    
    print(f"[SUCCESS] Loaded GitHub token: {github_token[:8]}...")
    
    repo = "sethpizzaboy/KeyHound"
    
    # Create user tutorials issue
    issue_number = create_user_tutorials_issue(repo, github_token)
    
    if issue_number:
        print("\n[SUCCESS] User Tutorials Task Added!")
        print("=================================")
        print(f"✅ Issue created: #{issue_number}")
        print(f"✅ Priority: Low")
        print(f"✅ Labels: documentation, priority: low, component: core")
        print(f"✅ Status: needs-review")
        print(f"✅ Target Milestone: v1.2.0 - Documentation & Quality")
        print("\nNext steps:")
        print(f"1. Visit: https://github.com/{repo}/issues/{issue_number}")
        print(f"2. Add to project board: https://github.com/{repo}/projects/3")
        print("3. Move to appropriate column (Backlog or To Do)")
    else:
        print("[ERROR] Failed to create user tutorials task")

if __name__ == "__main__":
    main()
