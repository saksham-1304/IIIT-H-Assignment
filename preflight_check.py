"""
Pre-Flight Check Script
Verifies that your environment is ready to run MFA alignment
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(title):
    """Print formatted header."""
    print("\n" + "="*70)
    print(title.center(70))
    print("="*70 + "\n")

def check_python():
    """Check Python version."""
    version = sys.version.split()[0]
    major, minor = map(int, version.split('.')[:2])
    
    if major >= 3 and minor >= 7:
        print(f"✅ Python {version} (OK)")
        return True
    else:
        print(f"❌ Python {version} (Need 3.7+)")
        return False

def check_command(command, name, min_version=None):
    """Check if a command exists and optionally verify version."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            output = result.stdout.strip()
            print(f"✅ {name}: {output}")
            return True
        else:
            print(f"❌ {name}: Not found or error")
            return False
    except subprocess.TimeoutExpired:
        print(f"⚠️  {name}: Command timed out")
        return False
    except FileNotFoundError:
        print(f"❌ {name}: Command not found")
        return False

def check_directory(path, name, should_exist=True):
    """Check if a directory exists."""
    path = Path(path)
    exists = path.exists() and path.is_dir()
    
    if should_exist:
        if exists:
            count = len(list(path.iterdir()))
            print(f"✅ {name}: Found ({count} items)")
            return True
        else:
            print(f"❌ {name}: Not found at {path}")
            return False
    else:
        if exists:
            print(f"⚠️  {name}: Already exists (will be overwritten)")
            return True
        else:
            print(f"✅ {name}: Ready to create")
            return True

def check_files(directory, pattern, name, expected_count=None):
    """Check for specific files in a directory."""
    path = Path(directory)
    
    if not path.exists():
        print(f"❌ {name}: Directory not found")
        return False
    
    files = list(path.glob(pattern))
    count = len(files)
    
    if expected_count:
        if count == expected_count:
            print(f"✅ {name}: Found {count}/{expected_count} files")
            return True
        else:
            print(f"❌ {name}: Found {count}/{expected_count} files")
            return False
    else:
        print(f"{'✅' if count > 0 else '❌'} {name}: Found {count} files")
        return count > 0

def check_mfa_models():
    """Check if MFA models are downloaded."""
    try:
        result = subprocess.run(
            "mfa model list",
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        output = result.stdout
        
        has_dict = "english_us_arpa" in output and "dictionary" in output.lower()
        has_acoustic = "english_us_arpa" in output and "acoustic" in output.lower()
        
        if has_dict and has_acoustic:
            print("✅ MFA Models: Both dictionary and acoustic models found")
            return True
        elif has_dict:
            print("⚠️  MFA Models: Dictionary found, acoustic model missing")
            return False
        elif has_acoustic:
            print("⚠️  MFA Models: Acoustic model found, dictionary missing")
            return False
        else:
            print("❌ MFA Models: Not found")
            return False
    except Exception as e:
        print(f"❌ MFA Models: Error checking ({e})")
        return False

def check_scripts():
    """Check if required scripts exist."""
    base_dir = Path(__file__).parent
    scripts = [
        "validate_dataset.py",
        "prepare_mfa_dataset.py",
        "analyze_textgrids.py",
        "run_alignment.py"
    ]
    
    all_found = True
    for script in scripts:
        path = base_dir / script
        if path.exists():
            print(f"✅ Script: {script}")
        else:
            print(f"❌ Script: {script} not found")
            all_found = False
    
    return all_found

def main():
    """Run all checks."""
    print_header("MFA ASSIGNMENT PRE-FLIGHT CHECK")
    
    results = {}
    
    # Check Python
    print("--- Python Environment ---")
    results['python'] = check_python()
    
    # Check required tools
    print("\n--- Required Tools ---")
    results['conda'] = check_command("conda --version", "Conda")
    results['mfa'] = check_command("mfa version", "MFA")
    
    # Check MFA models
    print("\n--- MFA Models ---")
    results['models'] = check_mfa_models()
    
    # Check directories
    print("\n--- Project Directories ---")
    base_dir = Path(__file__).parent
    results['wav_dir'] = check_directory(base_dir / "wav", "wav/")
    results['transcripts_dir'] = check_directory(base_dir / "transcripts", "transcripts/")
    results['mfa_data_dir'] = check_directory(base_dir / "mfa_data", "mfa_data/", should_exist=False)
    results['output_dir'] = check_directory(base_dir / "output_textgrids", "output_textgrids/", should_exist=False)
    
    # Check files
    print("\n--- Dataset Files ---")
    results['wav_files'] = check_files("wav", "*.wav", "Audio files", expected_count=6)
    results['transcript_files'] = check_files("transcripts", "*.txt", "Transcript files (.txt)", expected_count=3)
    results['transcript_files_upper'] = check_files("transcripts", "*.TXT", "Transcript files (.TXT)", expected_count=3)
    
    # Check if mfa_data is prepared
    if (base_dir / "mfa_data").exists():
        print("\n--- MFA Data (Already Prepared) ---")
        check_files("mfa_data", "*.wav", "MFA audio files", expected_count=6)
        check_files("mfa_data", "*.lab", "MFA label files", expected_count=6)
    
    # Check scripts
    print("\n--- Python Scripts ---")
    results['scripts'] = check_scripts()
    
    # Summary
    print_header("SUMMARY")
    
    critical_checks = ['python', 'conda', 'mfa', 'models', 'wav_dir', 'transcripts_dir', 'wav_files']
    critical_passed = all(results.get(key, False) for key in critical_checks)
    
    if critical_passed:
        print("✅ ALL CRITICAL CHECKS PASSED!")
        print("\nYou are ready to run the alignment pipeline.")
        print("\nNext steps:")
        print("  1. Run: python run_alignment.py")
        print("  2. Or follow QUICK_START.md")
    else:
        print("⚠️  SOME CRITICAL CHECKS FAILED")
        print("\nPlease address the issues marked with ❌ above.")
        print("\nCommon solutions:")
        
        if not results.get('conda', True):
            print("\n  • Install Miniconda:")
            print("    https://docs.conda.io/en/latest/miniconda.html")
        
        if not results.get('mfa', True):
            print("\n  • Install MFA:")
            print("    conda install -c conda-forge montreal-forced-aligner")
        
        if not results.get('models', True):
            print("\n  • Download MFA models:")
            print("    mfa model download dictionary english_us_arpa")
            print("    mfa model download acoustic english_us_arpa")
        
        if not results.get('wav_files', True) or not results.get('transcripts_dir', True):
            print("\n  • Ensure wav/ and transcripts/ directories contain all 6 files")
    
    # Additional recommendations
    print("\n--- Optional Recommendations ---")
    
    try:
        result = subprocess.run("praat --version", shell=True, capture_output=True, timeout=3)
        if result.returncode == 0:
            print("✅ Praat is installed (for visualization)")
        else:
            print("⚠️  Praat not found (recommended for inspecting results)")
            print("   Download from: https://www.fon.hum.uva.nl/praat/")
    except:
        print("⚠️  Praat not found (recommended for inspecting results)")
        print("   Download from: https://www.fon.hum.uva.nl/praat/")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
