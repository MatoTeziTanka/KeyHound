#!/usr/bin/env python3
"""
KeyHound Enhanced - Deployment Verification Script
==================================================

Professional deployment verification for all supported environments:
- Docker & Docker Compose
- Google Colab
- Local Development
- Cloud Platforms (AWS, Azure, GCP)

This script systematically tests each deployment option to ensure
they work correctly for end users.

Author: KeyHound Enhanced Team
Version: 2.0.0
"""

import os
import sys
import subprocess
import yaml
import json
import time
import logging
import codecs
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Fix Windows Unicode encoding issues
if sys.platform == "win32":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('deployment_verification.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class DeploymentResult:
    """Results of deployment verification."""
    name: str
    status: str  # 'success', 'warning', 'error'
    message: str
    details: Dict
    duration: float

class DeploymentVerifier:
    """Comprehensive deployment verification system."""
    
    def __init__(self):
        self.results: List[DeploymentResult] = []
        self.start_time = time.time()
        
        # Get project root
        self.project_root = Path(__file__).parent.parent
        os.chdir(self.project_root)
        logger.info(f"Starting deployment verification from: {self.project_root}")
    
    def verify_docker_deployment(self) -> DeploymentResult:
        """Verify Docker deployment configuration."""
        logger.info("[DOCKER] Verifying Docker deployment...")
        start_time = time.time()
        
        try:
            # Check Dockerfile exists and is valid
            dockerfile_path = self.project_root / "deployments" / "docker" / "Dockerfile"
            if not dockerfile_path.exists():
                return DeploymentResult(
                    "Docker", "error", 
                    "Dockerfile not found", 
                    {"path": str(dockerfile_path)}, 
                    time.time() - start_time
                )
            
            # Validate Dockerfile syntax (basic check)
            with open(dockerfile_path, 'r') as f:
                dockerfile_content = f.read()
                
            required_stages = ["base", "dependencies", "application"]
            missing_stages = []
            for stage in required_stages:
                if f"FROM" not in dockerfile_content or f"AS {stage}" not in dockerfile_content:
                    missing_stages.append(stage)
            
            # Check docker-compose.yml
            compose_path = self.project_root / "deployments" / "docker" / "docker-compose.yml"
            if not compose_path.exists():
                return DeploymentResult(
                    "Docker Compose", "error",
                    "docker-compose.yml not found",
                    {"path": str(compose_path)},
                    time.time() - start_time
                )
            
            # Validate docker-compose syntax
            with open(compose_path, 'r') as f:
                compose_data = yaml.safe_load(f)
                
            required_services = ["keyhound-web", "redis", "postgres"]
            missing_services = []
            for service in required_services:
                if service not in compose_data.get('services', {}):
                    missing_services.append(service)
            
            # Check if Docker is available (optional)
            docker_available = False
            try:
                result = subprocess.run(['docker', '--version'], 
                                      capture_output=True, text=True, timeout=5)
                docker_available = result.returncode == 0
            except (subprocess.TimeoutExpired, FileNotFoundError):
                docker_available = False
            
            status = "success"
            message = "Docker deployment configuration valid"
            if missing_stages:
                status = "warning"
                message += f" (missing stages: {missing_stages})"
            if missing_services:
                status = "warning" 
                message += f" (missing services: {missing_services})"
            
            return DeploymentResult(
                "Docker", status, message,
                {
                    "dockerfile_exists": True,
                    "compose_exists": True,
                    "missing_stages": missing_stages,
                    "missing_services": missing_services,
                    "docker_available": docker_available
                },
                time.time() - start_time
            )
            
        except Exception as e:
            return DeploymentResult(
                "Docker", "error", f"Docker verification failed: {str(e)}",
                {"error": str(e)}, time.time() - start_time
            )
    
    def verify_colab_deployment(self) -> DeploymentResult:
        """Verify Google Colab deployment configuration."""
        logger.info("[COLAB] Verifying Google Colab deployment...")
        start_time = time.time()
        
        try:
            # Check Colab notebook exists
            notebook_path = self.project_root / "deployments" / "colab" / "KeyHound_Enhanced.ipynb"
            if not notebook_path.exists():
                return DeploymentResult(
                    "Google Colab", "error",
                    "Colab notebook not found",
                    {"path": str(notebook_path)},
                    time.time() - start_time
                )
            
            # Basic notebook validation (check if it's valid JSON)
            try:
                with open(notebook_path, 'r', encoding='utf-8') as f:
                    notebook_data = json.load(f)
                
                # Check for required cells
                cells = notebook_data.get('cells', [])
                required_keywords = ['KeyHound', 'setup', 'installation', 'dependencies']
                found_keywords = []
                
                for cell in cells:
                    if 'source' in cell:
                        cell_text = ''.join(cell['source']).lower()
                        for keyword in required_keywords:
                            if keyword.lower() in cell_text and keyword not in found_keywords:
                                found_keywords.append(keyword)
                
                status = "success" if len(found_keywords) >= 3 else "warning"
                message = f"Colab notebook valid (found keywords: {found_keywords})"
                
            except json.JSONDecodeError:
                status = "error"
                message = "Colab notebook is not valid JSON"
                notebook_data = None
            
            return DeploymentResult(
                "Google Colab", status, message,
                {
                    "notebook_exists": True,
                    "valid_json": status != "error",
                    "found_keywords": found_keywords if 'found_keywords' in locals() else [],
                    "cell_count": len(cells) if notebook_data else 0
                },
                time.time() - start_time
            )
            
        except Exception as e:
            return DeploymentResult(
                "Google Colab", "error", f"Colab verification failed: {str(e)}",
                {"error": str(e)}, time.time() - start_time
            )
    
    def verify_local_deployment(self) -> DeploymentResult:
        """Verify local development deployment."""
        logger.info("[LOCAL] Verifying local deployment...")
        start_time = time.time()
        
        try:
            # Check essential files
            essential_files = [
                "main.py",
                "requirements.txt", 
                "setup.py",
                "config/default.yaml",
                "core/simple_keyhound.py",
                "core/bitcoin_cryptography.py"
            ]
            
            missing_files = []
            for file_path in essential_files:
                full_path = self.project_root / file_path
                if not full_path.exists():
                    missing_files.append(file_path)
            
            # Test Python imports
            import_errors = []
            try:
                sys.path.insert(0, str(self.project_root))
                from core.simple_keyhound import SimpleKeyHound
                from core.bitcoin_cryptography import BitcoinCryptography
                from core.puzzle_data import BITCOIN_PUZZLES
            except ImportError as e:
                import_errors.append(str(e))
            
            # Test basic functionality
            functionality_works = False
            try:
                if not import_errors:
                    keyhound = SimpleKeyHound()
                    system_info = keyhound.get_system_info()
                    functionality_works = bool(system_info)
            except Exception as e:
                import_errors.append(f"Functionality test failed: {str(e)}")
            
            status = "success"
            message = "Local deployment ready"
            if missing_files:
                status = "error"
                message = f"Missing essential files: {missing_files}"
            elif import_errors:
                status = "warning"
                message = f"Import issues: {import_errors}"
            
            return DeploymentResult(
                "Local Development", status, message,
                {
                    "essential_files_missing": missing_files,
                    "import_errors": import_errors,
                    "functionality_works": functionality_works,
                    "python_version": sys.version
                },
                time.time() - start_time
            )
            
        except Exception as e:
            return DeploymentResult(
                "Local Development", "error", f"Local verification failed: {str(e)}",
                {"error": str(e)}, time.time() - start_time
            )
    
    def verify_cloud_deployments(self) -> List[DeploymentResult]:
        """Verify cloud deployment configurations."""
        logger.info("[CLOUD] Verifying cloud deployment configurations...")
        results = []
        
        cloud_platforms = ["aws", "azure", "gcp"]
        
        for platform in cloud_platforms:
            start_time = time.time()
            try:
                cloud_path = self.project_root / "deployments" / "cloud" / platform
                
                if not cloud_path.exists():
                    results.append(DeploymentResult(
                        f"Cloud {platform.upper()}", "warning",
                        f"Cloud deployment directory not found",
                        {"path": str(cloud_path)},
                        time.time() - start_time
                    ))
                    continue
                
                # Check for common cloud deployment files
                expected_files = {
                    "aws": ["Dockerfile", "docker-compose.yml", "terraform.tf"],
                    "azure": ["Dockerfile", "docker-compose.yml", "azure-pipelines.yml"],
                    "gcp": ["Dockerfile", "docker-compose.yml", "cloudbuild.yaml"]
                }
                
                files_found = []
                files_missing = []
                
                for expected_file in expected_files.get(platform, []):
                    file_path = cloud_path / expected_file
                    if file_path.exists():
                        files_found.append(expected_file)
                    else:
                        files_missing.append(expected_file)
                
                status = "success" if not files_missing else "warning"
                message = f"Cloud {platform.upper()} deployment configured"
                if files_missing:
                    message += f" (missing: {files_missing})"
                
                results.append(DeploymentResult(
                    f"Cloud {platform.upper()}", status, message,
                    {
                        "files_found": files_found,
                        "files_missing": files_missing,
                        "directory_exists": True
                    },
                    time.time() - start_time
                ))
                
            except Exception as e:
                results.append(DeploymentResult(
                    f"Cloud {platform.upper()}", "error",
                    f"Cloud {platform} verification failed: {str(e)}",
                    {"error": str(e)}, time.time() - start_time
                ))
        
        return results
    
    def verify_configurations(self) -> DeploymentResult:
        """Verify configuration files are valid."""
        logger.info("[CONFIG] Verifying configuration files...")
        start_time = time.time()
        
        try:
            config_files = [
                "config/default.yaml",
                "config/environments/production.yaml",
                "config/environments/docker.yaml",
                "config/environments/colab.yaml"
            ]
            
            invalid_configs = []
            valid_configs = []
            
            for config_file in config_files:
                config_path = self.project_root / config_file
                if not config_path.exists():
                    invalid_configs.append(f"{config_file} (not found)")
                    continue
                
                try:
                    with open(config_path, 'r') as f:
                        config_data = yaml.safe_load(f)
                    
                    # Basic validation
                    required_sections = ["app", "bitcoin", "performance"]
                    missing_sections = []
                    for section in required_sections:
                        if section not in config_data:
                            missing_sections.append(section)
                    
                    if missing_sections:
                        invalid_configs.append(f"{config_file} (missing sections: {missing_sections})")
                    else:
                        valid_configs.append(config_file)
                        
                except yaml.YAMLError as e:
                    invalid_configs.append(f"{config_file} (YAML error: {str(e)})")
            
            status = "success" if not invalid_configs else "warning"
            message = f"Configuration validation completed"
            if invalid_configs:
                message += f" (issues: {len(invalid_configs)})"
            
            return DeploymentResult(
                "Configuration Files", status, message,
                {
                    "valid_configs": valid_configs,
                    "invalid_configs": invalid_configs,
                    "total_checked": len(config_files)
                },
                time.time() - start_time
            )
            
        except Exception as e:
            return DeploymentResult(
                "Configuration Files", "error",
                f"Configuration verification failed: {str(e)}",
                {"error": str(e)}, time.time() - start_time
            )
    
    def run_verification(self) -> Dict:
        """Run complete deployment verification."""
        logger.info("[START] Starting comprehensive deployment verification...")
        logger.info("=" * 60)
        
        # Run all verifications
        self.results.append(self.verify_docker_deployment())
        self.results.append(self.verify_colab_deployment())
        self.results.append(self.verify_local_deployment())
        self.results.extend(self.verify_cloud_deployments())
        self.results.append(self.verify_configurations())
        
        # Generate summary
        total_time = time.time() - self.start_time
        summary = self.generate_summary(total_time)
        
        # Log results
        self.log_results()
        
        return summary
    
    def generate_summary(self, total_time: float) -> Dict:
        """Generate verification summary."""
        success_count = sum(1 for r in self.results if r.status == "success")
        warning_count = sum(1 for r in self.results if r.status == "warning")
        error_count = sum(1 for r in self.results if r.status == "error")
        
        overall_status = "success"
        if error_count > 0:
            overall_status = "error"
        elif warning_count > 0:
            overall_status = "warning"
        
        return {
            "overall_status": overall_status,
            "total_deployments": len(self.results),
            "successful": success_count,
            "warnings": warning_count,
            "errors": error_count,
            "total_time": total_time,
            "results": [
                {
                    "name": r.name,
                    "status": r.status,
                    "message": r.message,
                    "duration": r.duration
                }
                for r in self.results
            ]
        }
    
    def log_results(self):
        """Log verification results."""
        logger.info("\n" + "=" * 60)
        logger.info("[RESULTS] DEPLOYMENT VERIFICATION RESULTS")
        logger.info("=" * 60)
        
        for result in self.results:
            status_icon = {
                "success": "[SUCCESS]",
                "warning": "[WARNING]",
                "error": "[ERROR]"
            }.get(result.status, "[UNKNOWN]")
            
            logger.info(f"{status_icon} {result.name}: {result.message}")
            logger.info(f"   Duration: {result.duration:.2f}s")
            
            if result.details:
                logger.info(f"   Details: {json.dumps(result.details, indent=2)}")
        
        # Overall summary
        summary = self.generate_summary(time.time() - self.start_time)
        logger.info("\n" + "=" * 60)
        logger.info(f"[SUMMARY] {summary['successful']} successful, "
                   f"{summary['warnings']} warnings, {summary['errors']} errors")
        logger.info(f"[TIME] Total time: {summary['total_time']:.2f}s")
        logger.info("=" * 60)

def main():
    """Main entry point for deployment verification."""
    print("KeyHound Enhanced - Deployment Verification")
    print("=" * 50)
    
    verifier = DeploymentVerifier()
    summary = verifier.run_verification()
    
    # Exit with appropriate code
    if summary["overall_status"] == "error":
        sys.exit(1)
    elif summary["overall_status"] == "warning":
        sys.exit(2)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
