#!/usr/bin/env python3
"""
Build script for Altum - Single-Image 3D Photo Generator
Handles virtual environment setup and dependency installation.
"""

import os
import sys
import subprocess
import platform
import argparse
from pathlib import Path


def run_command(cmd, description=None):
    """Run a shell command and report status."""
    if description:
        print(f"\n{'='*60}")
        print(f"  {description}")
        print('='*60)
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    
    if result.returncode != 0:
        print(f"\n❌ Error running: {' '.join(cmd)}")
        return False
    return True


def get_python_path(venv_path):
    """Get Python executable path for the venv."""
    if platform.system() == "Windows":
        return venv_path / "Scripts" / "python.exe"
    else:
        return venv_path / "bin" / "python"


def get_pip_path(venv_path):
    """Get pip executable path for the venv."""
    if platform.system() == "Windows":
        return venv_path / "Scripts" / "pip.exe"
    else:
        return venv_path / "bin" / "pip"


def setup_venv(venv_path):
    """Create virtual environment."""
    print("\n" + "="*60)
    print("  Creating Virtual Environment")
    print("="*60)
    
    if venv_path.exists():
        print(f"Virtual environment already exists at {venv_path}")
        return True
    
    print(f"Creating venv at: {venv_path}")
    result = subprocess.run(
        [sys.executable, "-m", "venv", str(venv_path)],
        cwd=PROJECT_ROOT
    )
    
    if result.returncode != 0:
        print("❌ Failed to create virtual environment")
        return False
    
    print("✓ Virtual environment created")
    return True


def upgrade_pip(pip_path):
    """Upgrade pip in the virtual environment."""
    print("\n" + "="*60)
    print("  Upgrading pip")
    print("="*60)
    
    cmd = [str(pip_path), "install", "--upgrade", "pip", "setuptools", "wheel"]
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    
    if result.returncode != 0:
        print("⚠ Warning: Failed to upgrade pip (continuing anyway)")
        return False
    
    print("✓ pip upgraded successfully")
    return True


def install_requirements(pip_path, requirements_file):
    """Install Python dependencies from requirements file."""
    if not requirements_file.exists():
        print(f"❌ Requirements file not found: {requirements_file}")
        return False
    
    print("\n" + "="*60)
    print("  Installing Dependencies")
    print("="*60)
    
    print(f"Installing from: {requirements_file}")
    cmd = [str(pip_path), "install", "-r", str(requirements_file)]
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    
    if result.returncode != 0:
        print("❌ Failed to install dependencies")
        return False
    
    print("✓ Dependencies installed successfully")
    return True


def run_tests(python_path):
    """Run tests if they exist."""
    print("\n" + "="*60)
    print("  Running Tests")
    print("="*60)
    
    tests_dir = PROJECT_ROOT / "tests"
    if not tests_dir.exists():
        print("No tests directory found, skipping tests")
        return True
    
    # Look for pytest
    cmd = [str(python_path), "-m", "pytest", str(tests_dir), "-v"]
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    
    if result.returncode != 0:
        print("⚠ Tests failed or pytest not installed")
        return False
    
    print("✓ All tests passed")
    return True


def print_completion_info(venv_path, python_path):
    """Print completion information."""
    print("\n" + "="*60)
    print("  Build Complete!")
    print("="*60)
    
    if platform.system() == "Windows":
        activate_cmd = f"{venv_path}\\Scripts\\activate"
    else:
        activate_cmd = f"source {venv_path}/bin/activate"
    
    print(f"\nVirtual environment created at: {venv_path}")
    print(f"\nTo activate the virtual environment:")
    print(f"  {activate_cmd}")
    
    print(f"\nTo run Altum:")
    print(f"  {python_path} -m src.app.main")
    
    print("\nOr directly:")
    if platform.system() == "Windows":
        print(f"  {venv_path}\\Scripts\\python -m src.app.main")
    else:
        print(f"  {venv_path}/bin/python -m src.app.main")


def main():
    """Main build function."""
    parser = argparse.ArgumentParser(
        description="Build script for Altum"
    )
    parser.add_argument(
        "--venv",
        default="venv",
        help="Virtual environment directory (default: venv)"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove existing virtual environment before creating new one"
    )
    parser.add_argument(
        "--no-test",
        action="store_true",
        help="Skip running tests"
    )
    
    args = parser.parse_args()
    
    venv_path = PROJECT_ROOT / args.venv
    python_path = get_python_path(venv_path)
    pip_path = get_pip_path(venv_path)
    requirements_file = PROJECT_ROOT / "requirements.txt"
    
    print("\n" + "="*60)
    print("  Altum Build Script")
    print("="*60)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Python Version: {sys.version}")
    print(f"Platform: {platform.system()}")
    
    # Clean if requested
    if args.clean and venv_path.exists():
        print(f"\nRemoving existing venv: {venv_path}")
        import shutil
        shutil.rmtree(venv_path)
    
    # Setup steps
    steps = [
        (setup_venv, (venv_path,)),
        (upgrade_pip, (pip_path,)),
        (install_requirements, (pip_path, requirements_file)),
    ]
    
    if not args.no_test:
        steps.append((run_tests, (python_path,)))
    
    # Execute steps
    for step, args_tuple in steps:
        if not step(*args_tuple):
            print("\n❌ Build failed!")
            return 1
    
    # Print completion info
    print_completion_info(venv_path, python_path)
    
    print("\n✓ Build completed successfully!")
    return 0


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).parent.resolve()
    sys.exit(main())
