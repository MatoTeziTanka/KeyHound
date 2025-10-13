#!/usr/bin/env python3
"""
KeyHound Enhanced - Professional Deployment Script
Multi-environment deployment automation
"""

import os
import sys
import argparse
import subprocess
import yaml
from pathlib import Path

class KeyHoundDeployer:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.config_dir = self.base_dir / "config"
        self.scripts_dir = self.base_dir / "scripts"
        
    def deploy_docker(self, gpu=False, production=False):
        """Deploy using Docker"""
        print("🐳 Deploying KeyHound Enhanced with Docker...")
        print("=" * 50)
        
        # Check Docker
        if not self._check_docker():
            print("❌ Docker not found. Please install Docker first.")
            return False
        
        # Check GPU support if requested
        if gpu and not self._check_nvidia_docker():
            print("❌ NVIDIA Docker not found. Install nvidia-docker2 for GPU support.")
            return False
        
        # Build and start
        try:
            if gpu:
                print("🔥 Building GPU-enabled container...")
                subprocess.run([
                    "docker-compose", "build", 
                    "--build-arg", "TARGET=gpu"
                ], check=True)
            else:
                print("🔧 Building standard container...")
                subprocess.run(["docker-compose", "build"], check=True)
            
            print("🚀 Starting services...")
            subprocess.run(["docker-compose", "up", "-d"], check=True)
            
            print("✅ Docker deployment successful!")
            print("🌐 Web interface: http://localhost:5000")
            print("📊 Grafana: http://localhost:3000")
            print("📈 Prometheus: http://localhost:9090")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Docker deployment failed: {e}")
            return False
    
    def deploy_colab(self):
        """Generate Colab deployment instructions"""
        print("📓 Colab Deployment Instructions")
        print("=" * 40)
        
        colab_notebook = self.base_dir / "colab" / "KeyHound_Enhanced.ipynb"
        
        if not colab_notebook.exists():
            print("❌ Colab notebook not found!")
            return False
        
        print("✅ Colab notebook ready!")
        print("\n📋 Deployment Steps:")
        print("1. Open Google Colab")
        print("2. Upload the notebook: colab/KeyHound_Enhanced.ipynb")
        print("3. Select Runtime → T4 GPU or A100 GPU (Colab Pro)")
        print("4. Run all cells")
        print("5. Monitor progress in the dashboard")
        
        print(f"\n📁 Notebook location: {colab_notebook}")
        print("🚀 Expected performance:")
        print("   - T4 GPU: ~20,000 keys/second")
        print("   - A100 GPU: ~100,000+ keys/second")
        
        return True
    
    def deploy_local(self, gpu=False, config="development"):
        """Deploy locally"""
        print(f"🖥️ Deploying KeyHound Enhanced locally...")
        print("=" * 45)
        
        # Check Python
        if not self._check_python():
            print("❌ Python 3.8+ required")
            return False
        
        # Check dependencies
        if not self._check_dependencies():
            print("❌ Dependencies not installed. Run: pip install -r requirements.txt")
            return False
        
        # Check GPU if requested
        if gpu and not self._check_cuda():
            print("❌ CUDA not available. Install CUDA for GPU support.")
            return False
        
        # Run application
        try:
            config_file = f"config/{config}.yaml"
            cmd = ["python", "main.py", "--web"]
            
            if gpu:
                cmd.append("--gpu")
            
            cmd.extend(["--config", config_file])
            
            print(f"🚀 Starting KeyHound Enhanced...")
            print(f"⚙️ Config: {config_file}")
            print(f"🔥 GPU: {'Enabled' if gpu else 'Disabled'}")
            
            subprocess.run(cmd, cwd=self.base_dir)
            
        except KeyboardInterrupt:
            print("\n⏹️ Deployment stopped by user")
        except Exception as e:
            print(f"❌ Local deployment failed: {e}")
            return False
    
    def deploy_cloud(self, provider="gcp", region="us-central1-a"):
        """Deploy to cloud provider"""
        print(f"☁️ Deploying to {provider.upper()}...")
        print("=" * 30)
        
        if provider == "gcp":
            return self._deploy_gcp(region)
        elif provider == "aws":
            return self._deploy_aws(region)
        elif provider == "azure":
            return self._deploy_azure(region)
        else:
            print(f"❌ Unsupported cloud provider: {provider}")
            return False
    
    def _deploy_gcp(self, zone):
        """Deploy to Google Cloud Platform"""
        script_path = self.scripts_dir / "deploy_to_google_cloud.sh"
        
        if not script_path.exists():
            print("❌ GCP deployment script not found!")
            return False
        
        try:
            print(f"🚀 Deploying to GCP zone: {zone}")
            subprocess.run([
                "bash", str(script_path),
                "--zone", zone,
                "--gpu"
            ], check=True)
            
            print("✅ GCP deployment successful!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ GCP deployment failed: {e}")
            return False
    
    def _check_docker(self):
        """Check if Docker is available"""
        try:
            subprocess.run(["docker", "--version"], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _check_nvidia_docker(self):
        """Check if NVIDIA Docker is available"""
        try:
            subprocess.run(["docker", "run", "--rm", "--gpus", "all", 
                          "nvidia/cuda:11.8-base-ubuntu20.04", "nvidia-smi"],
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _check_python(self):
        """Check Python version"""
        return sys.version_info >= (3, 8)
    
    def _check_dependencies(self):
        """Check if dependencies are installed"""
        try:
            import torch
            import numpy
            import flask
            return True
        except ImportError:
            return False
    
    def _check_cuda(self):
        """Check if CUDA is available"""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False

def main():
    parser = argparse.ArgumentParser(
        description="KeyHound Enhanced - Professional Deployment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/deploy.py --docker                    # Docker deployment
  python scripts/deploy.py --docker --gpu              # Docker with GPU
  python scripts/deploy.py --colab                     # Colab instructions
  python scripts/deploy.py --local --gpu               # Local with GPU
  python scripts/deploy.py --cloud gcp                 # Cloud deployment
        """
    )
    
    # Deployment options
    parser.add_argument('--docker', action='store_true',
                       help='Deploy using Docker')
    parser.add_argument('--colab', action='store_true',
                       help='Generate Colab deployment instructions')
    parser.add_argument('--local', action='store_true',
                       help='Deploy locally')
    parser.add_argument('--cloud', choices=['gcp', 'aws', 'azure'],
                       help='Deploy to cloud provider')
    
    # Options
    parser.add_argument('--gpu', action='store_true',
                       help='Enable GPU support')
    parser.add_argument('--production', action='store_true',
                       help='Use production configuration')
    parser.add_argument('--region', default='us-central1-a',
                       help='Cloud region/zone')
    parser.add_argument('--config', default='development',
                       help='Configuration file')
    
    args = parser.parse_args()
    
    if not any([args.docker, args.colab, args.local, args.cloud]):
        parser.print_help()
        return
    
    deployer = KeyHoundDeployer()
    
    # Execute deployment
    success = False
    
    if args.docker:
        success = deployer.deploy_docker(gpu=args.gpu, production=args.production)
    elif args.colab:
        success = deployer.deploy_colab()
    elif args.local:
        success = deployer.deploy_local(gpu=args.gpu, config=args.config)
    elif args.cloud:
        success = deployer.deploy_cloud(provider=args.cloud, region=args.region)
    
    if success:
        print("\n🎉 Deployment completed successfully!")
        print("🚀 KeyHound Enhanced is ready for Bitcoin cryptography!")
    else:
        print("\n❌ Deployment failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
