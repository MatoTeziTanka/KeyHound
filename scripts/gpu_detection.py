#!/usr/bin/env python3
"""
GPU Detection and Setup Script for KeyHound Enhanced
Diagnoses GPU availability and provides setup instructions.
"""

import sys
import subprocess
import platform

def check_nvidia_driver():
    """Check if NVIDIA drivers are installed."""
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] NVIDIA drivers installed")
            print("Driver info:")
            for line in result.stdout.split('\n')[:5]:
                if line.strip():
                    print(f"  {line}")
            return True
        else:
            print("[FAIL] NVIDIA drivers not found")
            return False
    except FileNotFoundError:
        print("[FAIL] nvidia-smi not found - NVIDIA drivers not installed")
        return False

def check_cuda_toolkit():
    """Check if CUDA toolkit is installed."""
    try:
        result = subprocess.run(['nvcc', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] CUDA toolkit installed")
            for line in result.stdout.split('\n'):
                if 'release' in line.lower():
                    print(f"  {line.strip()}")
            return True
        else:
            print("[FAIL] CUDA toolkit not found")
            return False
    except FileNotFoundError:
        print("[FAIL] nvcc not found - CUDA toolkit not installed")
        return False

def check_python_gpu_libraries():
    """Check if Python GPU libraries are installed."""
    libraries = {
        'cupy': 'CuPy (CUDA Python)',
        'torch': 'PyTorch',
        'numba': 'Numba',
        'numpy': 'NumPy'
    }
    
    results = {}
    for lib, name in libraries.items():
        try:
            module = __import__(lib)
            version = getattr(module, '__version__', 'unknown')
            print(f"[OK] {name}: {version}")
            
            # Special checks for GPU libraries
            if lib == 'cupy':
                try:
                    import cupy as cp
                    device_count = cp.cuda.runtime.getDeviceCount()
                    print(f"  GPU devices detected: {device_count}")
                    if device_count > 0:
                        props = cp.cuda.runtime.getDeviceProperties(0)
                        print(f"  GPU 0: {props['name'].decode('utf-8')}")
                        print(f"  Memory: {props['totalGlobalMem'] / (1024**3):.1f} GB")
                except Exception as e:
                    print(f"  GPU access error: {e}")
            
            elif lib == 'torch':
                try:
                    import torch
                    if torch.cuda.is_available():
                        print(f"  CUDA available: {torch.cuda.device_count()} devices")
                        for i in range(torch.cuda.device_count()):
                            print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
                    else:
                        print(f"  CUDA not available in PyTorch")
                except Exception as e:
                    print(f"  PyTorch CUDA error: {e}")
            
            results[lib] = True
        except ImportError:
            print(f"[FAIL] {name}: Not installed")
            results[lib] = False
    
    return results

def provide_setup_instructions(nvidia_ok, cuda_ok, missing_libs):
    """Provide setup instructions for missing components."""
    print("\n" + "="*60)
    print("SETUP INSTRUCTIONS")
    print("="*60)
    
    if not nvidia_ok:
        print("\n[SETUP] Install NVIDIA Drivers:")
        if platform.system() == "Windows":
            print("  1. Go to: https://www.nvidia.com/drivers")
            print("  2. Download and install latest drivers")
            print("  3. Restart your computer")
        else:
            print("  1. sudo apt update")
            print("  2. sudo apt install nvidia-driver-470")
            print("  3. sudo reboot")
    
    if not cuda_ok:
        print("\n[SETUP] Install CUDA Toolkit:")
        if platform.system() == "Windows":
            print("  1. Go to: https://developer.nvidia.com/cuda-downloads")
            print("  2. Download CUDA 11.8 or 12.x for Windows")
            print("  3. Run the installer")
        else:
            print("  1. wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run")
            print("  2. sudo sh cuda_11.8.0_520.61.05_linux.run")
    
    if missing_libs:
        print("\n[SETUP] Install Python GPU Libraries:")
        print("  pip install cupy-cuda11x  # For CUDA 11.x")
        print("  pip install cupy-cuda12x  # For CUDA 12.x")
        print("  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
        print("  pip install numba[cuda]")

def main():
    """Main GPU detection and diagnosis."""
    print("="*60)
    print("KeyHound Enhanced - GPU Detection & Setup")
    print("="*60)
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print()
    
    # Check NVIDIA drivers
    print("[CHECK] Checking NVIDIA Drivers...")
    nvidia_ok = check_nvidia_driver()
    print()
    
    # Check CUDA toolkit
    print("[CHECK] Checking CUDA Toolkit...")
    cuda_ok = check_cuda_toolkit()
    print()
    
    # Check Python GPU libraries
    print("[CHECK] Checking Python GPU Libraries...")
    lib_results = check_python_gpu_libraries()
    print()
    
    # Summary
    print("="*60)
    print("DIAGNOSIS SUMMARY")
    print("="*60)
    
    gpu_ready = nvidia_ok and cuda_ok and lib_results.get('cupy', False)
    
    if gpu_ready:
        print("[SUCCESS] GPU ACCELERATION READY!")
        print("[OK] All components installed and working")
        print("[OK] You can use: python main.py --puzzle 40 --gpu")
        print()
        print("Expected performance:")
        print("  CPU: ~3,590 keys/sec")
        print("  GPU: ~50,000-100,000+ keys/sec (10-30x faster!)")
    else:
        print("[ERROR] GPU ACCELERATION NOT READY")
        print("Missing components:")
        if not nvidia_ok:
            print("  [FAIL] NVIDIA drivers")
        if not cuda_ok:
            print("  [FAIL] CUDA toolkit")
        if not lib_results.get('cupy', False):
            print("  [FAIL] CuPy library")
        
        # Provide setup instructions
        provide_setup_instructions(nvidia_ok, cuda_ok, not lib_results.get('cupy', False))
        
        print("\n[INFO] ALTERNATIVE: Use Google Colab")
        print("  1. Go to: https://colab.research.google.com/")
        print("  2. Enable GPU: Runtime -> Change runtime type -> GPU")
        print("  3. Clone KeyHound and install dependencies")
        print("  4. Run GPU-accelerated KeyHound immediately!")
    
    return 0 if gpu_ready else 1

if __name__ == '__main__':
    sys.exit(main())
