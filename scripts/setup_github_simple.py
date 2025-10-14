#!/usr/bin/env python3
"""
KeyHound Enhanced GitHub Project Management Automated Setup Script
Uses GitHub CLI (gh) - same as ScalpStorm
Requires: GitHub CLI (gh) installed and authenticated
"""

import subprocess
import json
import sys
import os
from datetime import datetime, timedelta

def run_command(command, capture_output=True):
    """Run a command and return the result."""
    try:
        if capture_output:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        else:
            subprocess.run(command, shell=True, check=True)
            return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Command failed: {command}")
        print(f"Error: {e.stderr}")
        return None

def check_gh_cli():
    """Check if GitHub CLI is installed and authenticated."""
    print("[CHECK] Checking GitHub CLI...")
    
    # Check if gh is installed
    if run_command("gh --version") is None:
        print("[ERROR] GitHub CLI not found. Please install it first:")
        print("   https://cli.github.com/")
        return False
    
    # Check if authenticated
    auth_status = run_command("gh auth status")
    if auth_status is None:
        print("[ERROR] Not authenticated with GitHub CLI. Please run:")
        print("   gh auth login")
        return False
    
    print("[SUCCESS] GitHub CLI is ready")
    return True

def create_labels(repo):
    """Create repository labels."""
    print("[INFO] Creating Repository Labels...")
    
    labels = [
        # Priority Labels
        ("priority: critical", "d73a4a", "Blocks development or critical functionality"),
        ("priority: high", "ff8c00", "Important for next release"),
        ("priority: medium", "fbca04", "Nice to have features"),
        ("priority: low", "28a745", "Future enhancement"),
        
        # Type Labels
        ("type: bug", "d73a4a", "Something is broken"),
        ("type: enhancement", "0075ca", "New feature or improvement"),
        ("type: refactor", "7057ff", "Code improvement without changing functionality"),
        ("type: documentation", "008672", "Documentation updates"),
        ("type: testing", "28a745", "Test related work"),
        ("type: deployment", "ff8c00", "Infrastructure and deployment"),
        
        # Component Labels
        ("component: core", "0075ca", "Core functionality and algorithms"),
        ("component: gpu", "7057ff", "GPU acceleration features"),
        ("component: web", "28a745", "Web interface and dashboard"),
        ("component: ml", "ff8c00", "Machine learning features"),
        ("component: deployment", "d73a4a", "Deployment configurations"),
        ("component: testing", "fbca04", "Test framework and test cases"),
        
        # Status Labels
        ("status: completed", "28a745", "Work is finished"),
        ("status: in-progress", "0075ca", "Currently being worked on"),
        ("status: blocked", "d73a4a", "Waiting for something"),
        ("status: needs-review", "fbca04", "Ready for review")
    ]
    
    for name, color, description in labels:
        command = f'gh label create "{name}" --color "{color}" --description "{description}" --repo {repo}'
        result = run_command(command)
        if result is None:
            print(f"[WARN] Label might already exist: {name}")
    
    print("[SUCCESS] Labels created successfully")

def create_milestones(repo):
    """Create milestones with proper dates."""
    print("[INFO] Creating Milestones...")
    
    # Calculate dates
    today = datetime.now()
    week1 = today + timedelta(days=7)
    week2 = today + timedelta(days=14)
    month1 = today + timedelta(days=30)
    month3 = today + timedelta(days=90)
    
    milestones = [
        {
            "title": "v1.0.0 - Foundation Complete",
            "description": "Completed all structural improvements, file organization, and deployment setup",
            "due_date": today.strftime("%Y-%m-%dT23:59:59Z"),
            "state": "closed"
        },
        {
            "title": "v1.1.0 - GitHub Project Management",
            "description": "Complete GitHub project setup with automation, labels, and tracking",
            "due_date": week1.strftime("%Y-%m-%dT23:59:59Z")
        },
        {
            "title": "v1.2.0 - Documentation & Quality",
            "description": "Comprehensive documentation, user guides, and quality improvements",
            "due_date": week2.strftime("%Y-%m-%dT23:59:59Z")
        },
        {
            "title": "v1.3.0 - Performance Optimization",
            "description": "Performance improvements, monitoring, and optimization",
            "due_date": month1.strftime("%Y-%m-%dT23:59:59Z")
        },
        {
            "title": "v2.0.0 - Advanced Features",
            "description": "Advanced ML features, distributed computing, and enterprise capabilities",
            "due_date": month3.strftime("%Y-%m-%dT23:59:59Z")
        }
    ]
    
    milestone_numbers = []
    for milestone in milestones:
        if milestone.get("state") == "closed":
            command = f'''gh api repos/{repo}/milestones --method POST --field title="{milestone['title']}" --field description="{milestone['description']}" --field due_on="{milestone['due_date']}" --field state="closed"'''
        else:
            command = f'''gh api repos/{repo}/milestones --method POST --field title="{milestone['title']}" --field description="{milestone['description']}" --field due_on="{milestone['due_date']}"'''
        
        result = run_command(command)
        if result:
            milestone_data = json.loads(result)
            milestone_numbers.append(milestone_data['number'])
            print(f"[SUCCESS] Created milestone: {milestone['title']}")
    
    print("[SUCCESS] Milestones created successfully")
    return milestone_numbers

def create_completed_issues(repo, milestone_numbers):
    """Create issues for completed work."""
    print("[INFO] Creating Completed Issues...")
    
    completed_issues = [
        {
            "title": "[REFACTOR] Eliminate redundant file structure - flatten keyhound package",
            "body": """## Structural Improvement

### Problem
The original structure had redundant nested keyhound/keyhound/ directories, making imports complex and the structure confusing.

### Solution
Flattened the package structure to eliminate redundant naming:
- Moved all modules from keyhound/keyhound/ to root level
- Simplified imports from 'from keyhound.module import' to 'from module import'
- Maintained clean organization with proper __init__.py files

### Impact
- Simplified imports and module structure
- Industry-standard Python project layout
- Easier navigation and maintenance
- Cleaner entry point (main.py)

### Commits
- a3dc7e4 - MAJOR RESTRUCTURE: Flatten keyhound package to root level""",
            "labels": "type: refactor,priority: high,component: core,status: completed"
        },
        {
            "title": "[REFACTOR] Remove duplicate files and clean codebase",
            "body": """## Codebase Cleanup

### Problem
Multiple duplicate files existed causing confusion and maintenance issues:
- Duplicate requirements.txt files
- Duplicate test files
- Duplicate validation files
- Duplicate structure files

### Solution
Systematically removed all duplicates:
- Kept only working requirements.txt (removed non-existent packages)
- Consolidated test files (kept simple_functionality_test.py)
- Removed duplicate validation scripts
- Eliminated redundant structure files

### Impact
- Clean, maintainable codebase
- No confusion about which files to use
- Reduced repository size
- Single source of truth for each file type

### Commits
- f4ae95e - Remove duplicate requirements files
- da490b6 - Remove duplicate test files
- af2dcc3 - Remove duplicate validation files
- 0aa7e81 - Remove duplicate optimal structure files""",
            "labels": "type: refactor,priority: high,component: core,status: completed"
        },
        {
            "title": "[REFACTOR] Optimize file organization and eliminate duplicates",
            "body": """## File Organization Optimization

### Problem
Files were scattered and some duplicates remained:
- Config files in multiple locations
- Deployment files duplicated
- Test files in wrong locations
- Root directory cluttered

### Solution
Organized everything properly:
- Moved docker.yaml to config/environments/
- Removed duplicate Dockerfile and docker-compose.yml from root
- Moved test files to tests/ directory
- Moved scripts to scripts/ directory
- Clean root directory with only essential files

### Impact
- Professional project structure
- Clear file organization
- No duplicate files
- Easy navigation and maintenance

### Commits
- d892488 - Perfect file structure organization""",
            "labels": "type: refactor,priority: medium,component: deployment,status: completed"
        },
        {
            "title": "[BUG] Fix import path issues after structural changes",
            "body": """## Import Path Resolution

### Problem
After structural changes, import paths were broken:
- Modules couldn't find each other
- Relative imports were incorrect
- Absolute imports were outdated
- Import errors in multiple files

### Solution
Fixed all import paths systematically:
- Updated all 'from src.module import' to relative imports
- Fixed 'from keyhound.module import' to 'from .module import'
- Corrected cross-module imports
- Ensured all modules can import each other

### Impact
- All imports working correctly
- No module import errors
- Clean relative import structure
- Maintainable import system

### Commits
- a6cfea1 - All file paths corrected after reorganization""",
            "labels": "type: bug,priority: high,component: core,status: completed"
        },
        {
            "title": "[CRITICAL] Restore accidentally deleted keyhound package",
            "body": """## Critical Recovery

### Problem
During cleanup, the core keyhound_enhanced.py file was accidentally deleted, breaking the main functionality.

### Solution
Recreated the core file with all original functionality:
- Restored core/keyhound_enhanced.py with complete implementation
- Updated imports to match new structure
- Maintained all original features and functionality
- Ensured compatibility with new organization

### Impact
- Core functionality restored
- Application working again
- All features available
- No data loss

### Commits
- 6de179c - Restore accidentally deleted keyhound package""",
            "labels": "type: bug,priority: critical,component: core,status: completed"
        },
        {
            "title": "[DEPLOYMENT] Implement enterprise deployment strategy",
            "body": """## Enterprise Deployment Infrastructure

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
- Production-ready deployments
- Multi-environment support
- Scalable infrastructure
- Professional deployment process

### Commits
- f7b9622 - Complete enterprise deployment strategy""",
            "labels": "type: deployment,priority: high,component: deployment,status: completed"
        }
    ]
    
    issue_numbers = []
    for issue in completed_issues:
        command = f'''gh issue create --title "{issue['title']}" --body "{issue['body']}" --label "{issue['labels']}" --milestone {milestone_numbers[0]} --repo {repo}'''
        result = run_command(command)
        if result:
            print(f"[SUCCESS] Created completed issue: {issue['title']}")
            
            # Extract issue number from the result (handle different output formats)
            try:
                if '#' in result:
                    issue_number = result.split('#')[1].split()[0]
                else:
                    # Try to extract from URL format
                    issue_number = result.split('/')[-1]
                
                issue_numbers.append(issue_number)
                
                # Close the issue as completed
                close_command = f'gh issue close {issue_number} --repo {repo} --comment "Completed in commits listed above"'
                run_command(close_command)
                print(f"[SUCCESS] Closed issue #{issue_number} as completed")
            except:
                print(f"[WARN] Could not parse issue number from: {result}")
                # Try to close by searching for the issue
                search_command = f'gh issue list --repo {repo} --search "{issue["title"][:50]}" --json number --jq ".[0].number"'
                issue_number = run_command(search_command)
                if issue_number:
                    close_command = f'gh issue close {issue_number} --repo {repo} --comment "Completed in commits listed above"'
                    run_command(close_command)
                    print(f"[SUCCESS] Closed issue #{issue_number} as completed")
    
    print("[SUCCESS] Completed issues created and closed")
    return issue_numbers

def create_future_issues(repo, milestone_numbers):
    """Create issues for future work."""
    print("[INFO] Creating Future Issues...")
    
    future_issues = [
        {
            "title": "[DEPLOYMENT] Set up GitHub Actions CI/CD pipeline",
            "body": """## CI/CD Automation

### Goal
Implement automated continuous integration and deployment pipeline using GitHub Actions.

### Tasks
- Configure automated testing on every commit
- Set up code quality checks (linting, formatting)
- Implement security scanning
- Create automated Docker builds
- Set up deployment automation
- Configure performance testing

### Acceptance Criteria
- Tests run automatically on PRs
- Code quality gates prevent bad merges
- Security vulnerabilities detected automatically
- Docker images built and pushed automatically
- Deployment happens automatically on main branch

### Priority
High - Essential for maintaining code quality and deployment reliability.""",
            "labels": "type: deployment,priority: high,component: deployment,status: in-progress",
            "milestone": milestone_numbers[1]
        },
        {
            "title": "[TESTING] Add comprehensive test coverage",
            "body": """## Test Coverage Enhancement

### Goal
Achieve comprehensive test coverage across all components.

### Tasks
- Increase unit test coverage to 90%+
- Add integration tests for core functionality
- Implement performance benchmarks
- Add end-to-end testing
- Create test data fixtures
- Set up automated test reporting

### Acceptance Criteria
- 90%+ code coverage across all modules
- All critical paths have integration tests
- Performance benchmarks established
- Tests run in CI/CD pipeline
- Test results reported automatically

### Priority
High - Essential for code quality and reliability.""",
            "labels": "type: testing,priority: high,component: testing,status: needs-review",
            "milestone": milestone_numbers[1]
        },
        {
            "title": "[DOCUMENTATION] Create comprehensive user documentation",
            "body": """## Documentation Enhancement

### Goal
Create comprehensive documentation for users and developers.

### Tasks
- Complete API documentation
- Create user tutorials and guides
- Write developer contribution guide
- Add deployment documentation
- Create troubleshooting guide
- Add code examples and demos

### Acceptance Criteria
- Complete API reference with examples
- Step-by-step user tutorials
- Clear contribution guidelines
- Comprehensive deployment guide
- Troubleshooting documentation
- Working code examples

### Priority
Medium - Important for user adoption and developer onboarding.""",
            "labels": "type: documentation,priority: medium,status: needs-review",
            "milestone": milestone_numbers[2]
        }
    ]
    
    for issue in future_issues:
        command = f'''gh issue create --title "{issue['title']}" --body "{issue['body']}" --label "{issue['labels']}" --milestone {issue['milestone']} --repo {repo}'''
        result = run_command(command)
        if result:
            print(f"[SUCCESS] Created future issue: {issue['title']}")
    
    print("[SUCCESS] Future issues created")

def main():
    """Main function to set up GitHub project management."""
    print("KeyHound Enhanced GitHub Project Management Setup")
    print("=================================================")
    
    repo = "sethpizzaboy/KeyHound"
    
    # Check prerequisites
    if not check_gh_cli():
        sys.exit(1)
    
    # Create labels
    create_labels(repo)
    print()
    
    # Create milestones
    milestone_numbers = create_milestones(repo)
    if not milestone_numbers:
        print("[ERROR] Failed to create milestones")
        sys.exit(1)
    print()
    
    # Create completed issues
    completed_issue_numbers = create_completed_issues(repo, milestone_numbers)
    print()
    
    # Create future issues
    create_future_issues(repo, milestone_numbers)
    print()
    
    print("KeyHound Enhanced GitHub Project Setup Complete!")
    print("================================================")
    print("[SUCCESS] Labels created (20 labels)")
    print("[SUCCESS] Milestones created (5 milestones)")
    print("[SUCCESS] Completed issues created and closed (6 issues)")
    print("[SUCCESS] Future issues created (3 issues)")
    print()
    print("Next steps:")
    print(f"1. Visit your project: https://github.com/{repo}/projects/3")
    print("2. Add the created issues to your project board")
    print("3. Set up automation rules (optional)")
    print()
    print("Summary:")
    print("- Repository: sethpizzaboy/KeyHound")
    print("- Labels: 20 labels added")
    print("- Milestones: 5 milestones with proper dates")
    print("- Completed Issues: 6 issues (closed)")
    print("- Future Issues: 3 issues (open)")
    print("- All using GitHub CLI (same as ScalpStorm)")

if __name__ == "__main__":
    main()
