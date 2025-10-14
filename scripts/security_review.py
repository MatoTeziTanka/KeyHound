#!/usr/bin/env python3
"""
KeyHound Enhanced - Security Review Script
==========================================

Comprehensive security analysis covering:
- API key protection and management
- Authentication mechanisms
- Data encryption and storage
- Input validation and sanitization
- Network security
- File permissions and access control
- Logging and monitoring
- Dependency security

Author: KeyHound Enhanced Security Team
Version: 2.0.0
"""

import os
import sys
import re
import json
import hashlib
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('security_review.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class SecurityIssue:
    """Represents a security issue found during review."""
    severity: str  # 'critical', 'high', 'medium', 'low', 'info'
    category: str  # 'authentication', 'encryption', 'validation', etc.
    file_path: str
    line_number: int
    description: str
    recommendation: str
    cwe_id: Optional[str] = None

class SecurityReviewer:
    """Comprehensive security review system."""
    
    def __init__(self):
        self.issues: List[SecurityIssue] = []
        self.project_root = Path(__file__).parent.parent
        os.chdir(self.project_root)
        
        # Security patterns to check
        self.secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'key\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'private_key\s*=\s*["\'][^"\']+["\']',
            r'gho_[a-zA-Z0-9]{36}',  # GitHub tokens
            r'sk-[a-zA-Z0-9]{48}',   # OpenAI keys
            r'AKIA[0-9A-Z]{16}',     # AWS access keys
        ]
        
        self.dangerous_functions = [
            'eval', 'exec', 'compile', '__import__',
            'subprocess.call', 'os.system', 'shell=True'
        ]
        
        self.sql_patterns = [
            r'SELECT.*FROM',
            r'INSERT.*INTO',
            r'UPDATE.*SET',
            r'DELETE.*FROM'
        ]
        
        logger.info(f"Starting security review from: {self.project_root}")
    
    def check_api_key_protection(self) -> List[SecurityIssue]:
        """Check for exposed API keys and secrets."""
        logger.info("[SECURITY] Checking API key protection...")
        issues = []
        
        # Check for hardcoded secrets in source files
        for py_file in self.project_root.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    for line_num, line in enumerate(lines, 1):
                        for pattern in self.secret_patterns:
                            if re.search(pattern, line, re.IGNORECASE):
                                # Skip if it's a placeholder or example
                                if any(placeholder in line.lower() for placeholder in 
                                      ['your_', 'example_', 'placeholder', 'change-this']):
                                    continue
                                    
                                issues.append(SecurityIssue(
                                    severity="high",
                                    category="authentication",
                                    file_path=str(py_file.relative_to(self.project_root)),
                                    line_number=line_num,
                                    description=f"Potential hardcoded secret found: {line.strip()[:100]}",
                                    recommendation="Use environment variables or secure configuration files",
                                    cwe_id="CWE-798"
                                ))
            except Exception as e:
                logger.warning(f"Could not read {py_file}: {e}")
        
        # Check for .env files that might contain secrets
        env_files = list(self.project_root.rglob(".env*"))
        for env_file in env_files:
            if env_file.name != ".env.example":
                issues.append(SecurityIssue(
                    severity="medium",
                    category="authentication",
                    file_path=str(env_file.relative_to(self.project_root)),
                    line_number=0,
                    description=f"Environment file found: {env_file.name}",
                    recommendation="Ensure .env files are in .gitignore and not committed",
                    cwe_id="CWE-200"
                ))
        
        return issues
    
    def check_input_validation(self) -> List[SecurityIssue]:
        """Check for input validation vulnerabilities."""
        logger.info("[SECURITY] Checking input validation...")
        issues = []
        
        for py_file in self.project_root.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    for line_num, line in enumerate(lines, 1):
                        # Check for dangerous functions
                        for func in self.dangerous_functions:
                            if func in line and not line.strip().startswith('#'):
                                issues.append(SecurityIssue(
                                    severity="high",
                                    category="validation",
                                    file_path=str(py_file.relative_to(self.project_root)),
                                    line_number=line_num,
                                    description=f"Dangerous function usage: {func}",
                                    recommendation="Use safer alternatives and validate all inputs",
                                    cwe_id="CWE-78"
                                ))
                        
                        # Check for SQL injection patterns
                        for sql_pattern in self.sql_patterns:
                            if re.search(sql_pattern, line, re.IGNORECASE):
                                if '?' not in line and '%s' not in line:
                                    issues.append(SecurityIssue(
                                        severity="medium",
                                        category="validation",
                                        file_path=str(py_file.relative_to(self.project_root)),
                                        line_number=line_num,
                                        description="Potential SQL injection vulnerability",
                                        recommendation="Use parameterized queries",
                                        cwe_id="CWE-89"
                                    ))
            except Exception as e:
                logger.warning(f"Could not read {py_file}: {e}")
        
        return issues
    
    def check_authentication_security(self) -> List[SecurityIssue]:
        """Check authentication and authorization mechanisms."""
        logger.info("[SECURITY] Checking authentication security...")
        issues = []
        
        # Check configuration files for security settings
        config_files = [
            "config/default.yaml",
            "config/environments/production.yaml",
            "config/environments/docker.yaml"
        ]
        
        for config_file in config_files:
            config_path = self.project_root / config_file
            if config_path.exists():
                try:
                    import yaml
                    with open(config_path, 'r') as f:
                        config = yaml.safe_load(f)
                    
                    # Check security settings
                    security = config.get('security', {})
                    
                    if not security.get('enable_authentication', False):
                        issues.append(SecurityIssue(
                            severity="medium",
                            category="authentication",
                            file_path=config_file,
                            line_number=0,
                            description="Authentication is disabled",
                            recommendation="Enable authentication for production deployments",
                            cwe_id="CWE-287"
                        ))
                    
                    session_timeout = security.get('session_timeout_minutes', 0)
                    if session_timeout > 120:  # More than 2 hours
                        issues.append(SecurityIssue(
                            severity="low",
                            category="authentication",
                            file_path=config_file,
                            line_number=0,
                            description=f"Long session timeout: {session_timeout} minutes",
                            recommendation="Consider shorter session timeouts for better security",
                            cwe_id="CWE-613"
                        ))
                    
                    # Check for weak secret keys
                    web_config = config.get('web', {})
                    secret_key = web_config.get('secret_key', '')
                    if 'change-in-production' in secret_key.lower() or 'default' in secret_key.lower():
                        issues.append(SecurityIssue(
                            severity="high",
                            category="authentication",
                            file_path=config_file,
                            line_number=0,
                            description="Default or placeholder secret key detected",
                            recommendation="Use a strong, unique secret key in production",
                            cwe_id="CWE-798"
                        ))
                
                except Exception as e:
                    logger.warning(f"Could not parse {config_file}: {e}")
        
        return issues
    
    def check_encryption_and_storage(self) -> List[SecurityIssue]:
        """Check encryption and data storage security."""
        logger.info("[SECURITY] Checking encryption and storage...")
        issues = []
        
        # Check configuration files for encryption settings
        config_files = [
            "config/default.yaml",
            "config/environments/production.yaml",
            "config/environments/docker.yaml"
        ]
        
        for config_file in config_files:
            config_path = self.project_root / config_file
            if config_path.exists():
                try:
                    import yaml
                    with open(config_path, 'r') as f:
                        config = yaml.safe_load(f)
                    
                    # Check results encryption
                    results = config.get('results', {})
                    if not results.get('encryption_enabled', False):
                        issues.append(SecurityIssue(
                            severity="medium",
                            category="encryption",
                            file_path=config_file,
                            line_number=0,
                            description="Results encryption is disabled",
                            recommendation="Enable encryption for sensitive data storage",
                            cwe_id="CWE-311"
                        ))
                    
                    # Check database security
                    database = config.get('database', {})
                    if database.get('type') == 'sqlite' and 'password' not in str(database):
                        # SQLite without password protection
                        issues.append(SecurityIssue(
                            severity="low",
                            category="encryption",
                            file_path=config_file,
                            line_number=0,
                            description="SQLite database without password protection",
                            recommendation="Consider using PostgreSQL with authentication or encrypt SQLite",
                            cwe_id="CWE-311"
                        ))
                
                except Exception as e:
                    logger.warning(f"Could not parse {config_file}: {e}")
        
        return issues
    
    def check_file_permissions(self) -> List[SecurityIssue]:
        """Check file permissions and access control."""
        logger.info("[SECURITY] Checking file permissions...")
        issues = []
        
        # Check for world-writable files
        try:
            result = subprocess.run(['find', '.', '-type', 'f', '-perm', '777'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0 and result.stdout.strip():
                for file_path in result.stdout.strip().split('\n'):
                    if file_path:
                        issues.append(SecurityIssue(
                            severity="medium",
                            category="access_control",
                            file_path=file_path,
                            line_number=0,
                            description="World-writable file detected",
                            recommendation="Restrict file permissions to necessary users only",
                            cwe_id="CWE-276"
                        ))
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # Windows or find not available
            pass
        
        # Check for sensitive files that might be readable
        sensitive_files = ['.env', 'api_keys.env', 'config/production.yaml']
        for sensitive_file in sensitive_files:
            file_path = self.project_root / sensitive_file
            if file_path.exists():
                try:
                    # Check if file is readable by others (simplified check)
                    stat = file_path.stat()
                    # This is a basic check - in production, use proper permission checking
                    if stat.st_mode & 0o044:  # Group or other read
                        issues.append(SecurityIssue(
                            severity="medium",
                            category="access_control",
                            file_path=sensitive_file,
                            line_number=0,
                            description="Sensitive file may be readable by others",
                            recommendation="Restrict file permissions to owner only (600)",
                            cwe_id="CWE-276"
                        ))
                except Exception:
                    pass
        
        return issues
    
    def check_dependencies(self) -> List[SecurityIssue]:
        """Check for vulnerable dependencies."""
        logger.info("[SECURITY] Checking dependencies...")
        issues = []
        
        # Check requirements.txt for known vulnerable packages
        requirements_file = self.project_root / "requirements.txt"
        if requirements_file.exists():
            try:
                with open(requirements_file, 'r') as f:
                    requirements = f.read()
                
                # Check for packages without version pins
                unpinned_packages = []
                for line in requirements.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#') and '==' not in line and '>=' not in line:
                        package_name = line.split()[0].split('>')[0].split('<')[0]
                        unpinned_packages.append(package_name)
                
                if unpinned_packages:
                    issues.append(SecurityIssue(
                        severity="medium",
                        category="dependencies",
                        file_path="requirements.txt",
                        line_number=0,
                        description=f"Unpinned dependencies: {', '.join(unpinned_packages)}",
                        recommendation="Pin all dependency versions for reproducible builds",
                        cwe_id="CWE-1104"
                    ))
                
                # Check for known vulnerable packages (basic check)
                vulnerable_packages = {
                    'flask': '0.12.3',  # Example - check actual vulnerabilities
                    'requests': '2.25.1'
                }
                
                for package, version in vulnerable_packages.items():
                    if package in requirements.lower():
                        issues.append(SecurityIssue(
                            severity="info",
                            category="dependencies",
                            file_path="requirements.txt",
                            line_number=0,
                            description=f"Package {package} may have known vulnerabilities",
                            recommendation=f"Check for security updates and use latest secure version",
                            cwe_id="CWE-1104"
                        ))
            
            except Exception as e:
                logger.warning(f"Could not read requirements.txt: {e}")
        
        return issues
    
    def check_logging_security(self) -> List[SecurityIssue]:
        """Check logging and monitoring security."""
        logger.info("[SECURITY] Checking logging security...")
        issues = []
        
        # Check for sensitive data in logs
        for py_file in self.project_root.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    for line_num, line in enumerate(lines, 1):
                        # Check for logging of sensitive data
                        if 'logger.' in line or 'logging.' in line:
                            if any(sensitive in line.lower() for sensitive in 
                                  ['password', 'secret', 'key', 'token', 'private_key']):
                                issues.append(SecurityIssue(
                                    severity="medium",
                                    category="logging",
                                    file_path=str(py_file.relative_to(self.project_root)),
                                    line_number=line_num,
                                    description="Potential logging of sensitive data",
                                    recommendation="Avoid logging sensitive information or mask it",
                                    cwe_id="CWE-532"
                                ))
            except Exception as e:
                logger.warning(f"Could not read {py_file}: {e}")
        
        return issues
    
    def run_security_review(self) -> Dict:
        """Run comprehensive security review."""
        logger.info("Starting comprehensive security review...")
        logger.info("=" * 60)
        
        # Run all security checks
        self.issues.extend(self.check_api_key_protection())
        self.issues.extend(self.check_input_validation())
        self.issues.extend(self.check_authentication_security())
        self.issues.extend(self.check_encryption_and_storage())
        self.issues.extend(self.check_file_permissions())
        self.issues.extend(self.check_dependencies())
        self.issues.extend(self.check_logging_security())
        
        # Generate summary
        summary = self.generate_summary()
        
        # Log results
        self.log_results()
        
        return summary
    
    def generate_summary(self) -> Dict:
        """Generate security review summary."""
        severity_counts = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'info': 0
        }
        
        category_counts = {}
        
        for issue in self.issues:
            severity_counts[issue.severity] += 1
            category_counts[issue.category] = category_counts.get(issue.category, 0) + 1
        
        overall_severity = "secure"
        if severity_counts['critical'] > 0 or severity_counts['high'] > 3:
            overall_severity = "critical"
        elif severity_counts['high'] > 0 or severity_counts['medium'] > 5:
            overall_severity = "high"
        elif severity_counts['medium'] > 0 or severity_counts['low'] > 10:
            overall_severity = "medium"
        elif severity_counts['low'] > 0:
            overall_severity = "low"
        
        return {
            "overall_severity": overall_severity,
            "total_issues": len(self.issues),
            "severity_breakdown": severity_counts,
            "category_breakdown": category_counts,
            "issues": [
                {
                    "severity": issue.severity,
                    "category": issue.category,
                    "file": issue.file_path,
                    "line": issue.line_number,
                    "description": issue.description,
                    "recommendation": issue.recommendation,
                    "cwe_id": issue.cwe_id
                }
                for issue in self.issues
            ]
        }
    
    def log_results(self):
        """Log security review results."""
        logger.info("\n" + "=" * 60)
        logger.info("SECURITY REVIEW RESULTS")
        logger.info("=" * 60)
        
        summary = self.generate_summary()
        
        # Log summary
        logger.info(f"Overall Security Status: {summary['overall_severity'].upper()}")
        logger.info(f"Total Issues Found: {summary['total_issues']}")
        logger.info(f"Severity Breakdown: {summary['severity_breakdown']}")
        logger.info(f"Category Breakdown: {summary['category_breakdown']}")
        
        # Log issues by severity
        for severity in ['critical', 'high', 'medium', 'low', 'info']:
            issues_of_severity = [i for i in self.issues if i.severity == severity]
            if issues_of_severity:
                logger.info(f"\n{severity.upper()} ISSUES ({len(issues_of_severity)}):")
                for issue in issues_of_severity:
                    logger.info(f"  [{issue.category}] {issue.file_path}:{issue.line_number}")
                    logger.info(f"    {issue.description}")
                    logger.info(f"    Recommendation: {issue.recommendation}")
                    if issue.cwe_id:
                        logger.info(f"    CWE: {issue.cwe_id}")
        
        logger.info("\n" + "=" * 60)

def main():
    """Main entry point for security review."""
    print("KeyHound Enhanced - Security Review")
    print("=" * 50)
    
    reviewer = SecurityReviewer()
    summary = reviewer.run_security_review()
    
    # Exit with appropriate code
    if summary["overall_severity"] in ["critical", "high"]:
        sys.exit(1)
    elif summary["overall_severity"] == "medium":
        sys.exit(2)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
