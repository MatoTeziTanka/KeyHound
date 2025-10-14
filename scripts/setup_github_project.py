#!/usr/bin/env python3
"""
GitHub Project Setup Automation Script
Automates the creation of GitHub projects, labels, milestones, and issues
"""

import os
import sys
import json
import requests
from pathlib import Path

class GitHubProjectSetup:
    def __init__(self, token, repo_owner, repo_name):
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def create_labels(self):
        """Create all necessary labels"""
        labels = [
            # Priority Labels
            {"name": "priority: critical", "color": "d73a4a", "description": "Blocks development or critical functionality"},
            {"name": "priority: high", "color": "ff8c00", "description": "Important for next release"},
            {"name": "priority: medium", "color": "fbca04", "description": "Nice to have features"},
            {"name": "priority: low", "color": "28a745", "description": "Future enhancement"},
            
            # Type Labels
            {"name": "type: bug", "color": "d73a4a", "description": "Something is broken"},
            {"name": "type: enhancement", "color": "0075ca", "description": "New feature or improvement"},
            {"name": "type: refactor", "color": "7057ff", "description": "Code improvement without changing functionality"},
            {"name": "type: documentation", "color": "008672", "description": "Documentation updates"},
            {"name": "type: testing", "color": "28a745", "description": "Test related work"},
            {"name": "type: deployment", "color": "ff8c00", "description": "Infrastructure and deployment"},
            
            # Component Labels
            {"name": "component: core", "color": "0075ca", "description": "Core functionality and algorithms"},
            {"name": "component: gpu", "color": "7057ff", "description": "GPU acceleration features"},
            {"name": "component: web", "color": "28a745", "description": "Web interface and dashboard"},
            {"name": "component: ml", "color": "ff8c00", "description": "Machine learning features"},
            {"name": "component: deployment", "color": "d73a4a", "description": "Deployment configurations"},
            {"name": "component: testing", "color": "fbca04", "description": "Test framework and test cases"},
            
            # Status Labels
            {"name": "status: completed", "color": "28a745", "description": "Work is finished"},
            {"name": "status: in-progress", "color": "0075ca", "description": "Currently being worked on"},
            {"name": "status: blocked", "color": "d73a4a", "description": "Waiting for something"},
            {"name": "status: needs-review", "color": "fbca04", "description": "Ready for review"}
        ]
        
        url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/labels"
        
        for label in labels:
            response = requests.post(url, headers=self.headers, json=label)
            if response.status_code == 201:
                print(f"✅ Created label: {label['name']}")
            elif response.status_code == 422:
                print(f"⚠️  Label already exists: {label['name']}")
            else:
                print(f"❌ Failed to create label {label['name']}: {response.text}")
    
    def create_milestones(self):
        """Create project milestones"""
        milestones = [
            {
                "title": "v1.0.0 - Foundation Complete",
                "description": "Completed all structural improvements, file organization, and deployment setup",
                "state": "closed"
            },
            {
                "title": "v1.1.0 - GitHub Project Management",
                "description": "Complete GitHub project setup with automation, labels, and tracking",
                "due_on": "2025-01-20T23:59:59Z"
            },
            {
                "title": "v1.2.0 - Documentation & Quality",
                "description": "Comprehensive documentation, user guides, and quality improvements",
                "due_on": "2025-01-27T23:59:59Z"
            },
            {
                "title": "v1.3.0 - Performance Optimization",
                "description": "Performance improvements, monitoring, and optimization",
                "due_on": "2025-02-13T23:59:59Z"
            },
            {
                "title": "v2.0.0 - Advanced Features",
                "description": "Advanced ML features, distributed computing, and enterprise capabilities",
                "due_on": "2025-04-13T23:59:59Z"
            }
        ]
        
        url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/milestones"
        
        for milestone in milestones:
            response = requests.post(url, headers=self.headers, json=milestone)
            if response.status_code == 201:
                print(f"✅ Created milestone: {milestone['title']}")
            else:
                print(f"❌ Failed to create milestone {milestone['title']}: {response.text}")
    
    def create_completed_issues(self):
        """Create issues for completed work"""
        completed_issues = [
            {
                "title": "[REFACTOR] Eliminate redundant file structure - flatten keyhound package",
                "body": """## 🏗️ Structural Improvement

### Problem
The original structure had redundant nested `keyhound/keyhound/` directories, making imports complex and the structure confusing.

### Solution
Flattened the package structure to eliminate redundant naming:
- Moved all modules from `keyhound/keyhound/` to root level
- Simplified imports from `from keyhound.module import` to `from module import`
- Maintained clean organization with proper `__init__.py` files

### Impact
- ✅ Simplified imports and module structure
- ✅ Industry-standard Python project layout
- ✅ Easier navigation and maintenance
- ✅ Cleaner entry point (`main.py`)

### Commits
- `a3dc7e4` - MAJOR RESTRUCTURE: Flatten keyhound package to root level""",
                "labels": ["type: refactor", "priority: high", "component: core", "status: completed"]
            },
            {
                "title": "[REFACTOR] Remove duplicate files and clean codebase",
                "body": """## 🧹 Codebase Cleanup

### Problem
Multiple duplicate files existed causing confusion and maintenance issues:
- Duplicate requirements.txt files
- Duplicate test files
- Duplicate validation files
- Duplicate structure files

### Solution
Systematically removed all duplicates:
- Kept only working `requirements.txt` (removed non-existent packages)
- Consolidated test files (kept `simple_functionality_test.py`)
- Removed duplicate validation scripts
- Eliminated redundant structure files

### Impact
- ✅ Clean, maintainable codebase
- ✅ No confusion about which files to use
- ✅ Reduced repository size
- ✅ Single source of truth for each file type

### Commits
- `f4ae95e` - Remove duplicate requirements files
- `da490b6` - Remove duplicate test files
- `af2dcc3` - Remove duplicate validation files
- `0aa7e81` - Remove duplicate optimal structure files""",
                "labels": ["type: refactor", "priority: high", "component: core", "status: completed"]
            },
            {
                "title": "[REFACTOR] Optimize file organization and eliminate duplicates",
                "body": """## 📁 File Organization Optimization

### Problem
Files were scattered and some duplicates remained:
- Config files in multiple locations
- Deployment files duplicated
- Test files in wrong locations
- Root directory cluttered

### Solution
Organized everything properly:
- Moved `docker.yaml` to `config/environments/`
- Removed duplicate `Dockerfile` and `docker-compose.yml` from root
- Moved test files to `tests/` directory
- Moved scripts to `scripts/` directory
- Clean root directory with only essential files

### Impact
- ✅ Professional project structure
- ✅ Clear file organization
- ✅ No duplicate files
- ✅ Easy navigation and maintenance

### Commits
- `d892488` - Perfect file structure organization""",
                "labels": ["type: refactor", "priority: medium", "component: deployment", "status: completed"]
            },
            {
                "title": "[BUG] Fix import path issues after structural changes",
                "body": """## 🔧 Import Path Resolution

### Problem
After structural changes, import paths were broken:
- Modules couldn't find each other
- Relative imports were incorrect
- Absolute imports were outdated
- Import errors in multiple files

### Solution
Fixed all import paths systematically:
- Updated all `from src.module import` to relative imports
- Fixed `from keyhound.module import` to `from .module import`
- Corrected cross-module imports
- Ensured all modules can import each other

### Impact
- ✅ All imports working correctly
- ✅ No module import errors
- ✅ Clean relative import structure
- ✅ Maintainable import system

### Commits
- `a6cfea1` - All file paths corrected after reorganization""",
                "labels": ["type: bug", "priority: high", "component: core", "status: completed"]
            },
            {
                "title": "[CRITICAL] Restore accidentally deleted keyhound package",
                "body": """## 🚨 Critical Recovery

### Problem
During cleanup, the core `keyhound_enhanced.py` file was accidentally deleted, breaking the main functionality.

### Solution
Recreated the core file with all original functionality:
- Restored `core/keyhound_enhanced.py` with complete implementation
- Updated imports to match new structure
- Maintained all original features and functionality
- Ensured compatibility with new organization

### Impact
- ✅ Core functionality restored
- ✅ Application working again
- ✅ All features available
- ✅ No data loss

### Commits
- `6de179c` - Restore accidentally deleted keyhound package""",
                "labels": ["type: bug", "priority: critical", "component: core", "status: completed"]
            },
            {
                "title": "[DEPLOYMENT] Implement enterprise deployment strategy",
                "body": """## 🚀 Enterprise Deployment Infrastructure

### Problem
No comprehensive deployment strategy for different environments and use cases.

### Solution
Implemented complete enterprise deployment strategy:
- Multi-environment configurations (production, docker, colab)
- Docker containerization with multi-stage builds
- Google Colab notebook deployment
- Cloud deployment configurations (AWS, Azure, GCP)
- Environment-specific configurations
- Professional deployment documentation

### Impact
- ✅ Production-ready deployments
- ✅ Multi-environment support
- ✅ Scalable infrastructure
- ✅ Professional deployment process

### Commits
- `f7b9622` - Complete enterprise deployment strategy""",
                "labels": ["type: deployment", "priority: high", "component: deployment", "status: completed"]
            }
        ]
        
        url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues"
        
        for issue in completed_issues:
            response = requests.post(url, headers=self.headers, json=issue)
            if response.status_code == 201:
                issue_number = response.json()["number"]
                print(f"✅ Created issue: {issue['title']}")
                
                # Close the issue as completed
                close_url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_number}"
                close_response = requests.patch(close_url, headers=self.headers, json={"state": "closed"})
                if close_response.status_code == 200:
                    print(f"✅ Closed issue #{issue_number} as completed")
            else:
                print(f"❌ Failed to create issue {issue['title']}: {response.text}")
    
    def create_future_issues(self):
        """Create issues for future work"""
        future_issues = [
            {
                "title": "[DEPLOYMENT] Set up GitHub Actions CI/CD pipeline",
                "body": """## 🤖 CI/CD Automation

### Goal
Implement automated continuous integration and deployment pipeline using GitHub Actions.

### Tasks
- [ ] Configure automated testing on every commit
- [ ] Set up code quality checks (linting, formatting)
- [ ] Implement security scanning
- [ ] Create automated Docker builds
- [ ] Set up deployment automation
- [ ] Configure performance testing

### Acceptance Criteria
- [ ] Tests run automatically on PRs
- [ ] Code quality gates prevent bad merges
- [ ] Security vulnerabilities detected automatically
- [ ] Docker images built and pushed automatically
- [ ] Deployment happens automatically on main branch

### Priority
High - Essential for maintaining code quality and deployment reliability.""",
                "labels": ["type: deployment", "priority: high", "component: deployment", "status: in-progress"]
            },
            {
                "title": "[TESTING] Add comprehensive test coverage",
                "body": """## 🧪 Test Coverage Enhancement

### Goal
Achieve comprehensive test coverage across all components.

### Tasks
- [ ] Increase unit test coverage to 90%+
- [ ] Add integration tests for core functionality
- [ ] Implement performance benchmarks
- [ ] Add end-to-end testing
- [ ] Create test data fixtures
- [ ] Set up automated test reporting

### Acceptance Criteria
- [ ] 90%+ code coverage across all modules
- [ ] All critical paths have integration tests
- [ ] Performance benchmarks established
- [ ] Tests run in CI/CD pipeline
- [ ] Test results reported automatically

### Priority
High - Essential for code quality and reliability.""",
                "labels": ["type: testing", "priority: high", "component: testing", "status: needs-review"]
            },
            {
                "title": "[DOCUMENTATION] Create comprehensive user documentation",
                "body": """## 📚 Documentation Enhancement

### Goal
Create comprehensive documentation for users and developers.

### Tasks
- [ ] Complete API documentation
- [ ] Create user tutorials and guides
- [ ] Write developer contribution guide
- [ ] Add deployment documentation
- [ ] Create troubleshooting guide
- [ ] Add code examples and demos

### Acceptance Criteria
- [ ] Complete API reference with examples
- [ ] Step-by-step user tutorials
- [ ] Clear contribution guidelines
- [ ] Comprehensive deployment guide
- [ ] Troubleshooting documentation
- [ ] Working code examples

### Priority
Medium - Important for user adoption and developer onboarding.""",
                "labels": ["type: documentation", "priority: medium", "status: needs-review"]
            }
        ]
        
        url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues"
        
        for issue in future_issues:
            response = requests.post(url, headers=self.headers, json=issue)
            if response.status_code == 201:
                print(f"✅ Created future issue: {issue['title']}")
            else:
                print(f"❌ Failed to create issue {issue['title']}: {response.text}")

def main():
    print("🚀 KeyHound Enhanced - GitHub Project Setup Automation")
    print("=" * 60)
    
    # Get GitHub token
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("❌ Please set GITHUB_TOKEN environment variable")
        print("Get your token from: https://github.com/settings/tokens")
        print("Required scopes: repo, project, issues")
        sys.exit(1)
    
    # Repository information
    repo_owner = "sethpizzaboy"
    repo_name = "KeyHound"
    
    print(f"📁 Repository: {repo_owner}/{repo_name}")
    print(f"🔑 Token: {'*' * (len(token) - 4)}{token[-4:]}")
    print()
    
    setup = GitHubProjectSetup(token, repo_owner, repo_name)
    
    print("🏷️  Creating labels...")
    setup.create_labels()
    print()
    
    print("🎯 Creating milestones...")
    setup.create_milestones()
    print()
    
    print("✅ Creating completed issues...")
    setup.create_completed_issues()
    print()
    
    print("📋 Creating future issues...")
    setup.create_future_issues()
    print()
    
    print("🎉 GitHub project setup complete!")
    print(f"View your project: https://github.com/{repo_owner}/{repo_name}")

if __name__ == "__main__":
    main()
