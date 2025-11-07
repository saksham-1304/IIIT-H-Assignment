"""
Automated MFA Forced Alignment Pipeline
Runs the complete workflow: validation → preparation → alignment → analysis
"""

import os
import subprocess
import sys
from pathlib import Path

def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(title.center(70))
    print("="*70 + "\n")


def run_command(command, description, shell=True):
    """Run a shell command and handle errors."""
    print(f"▶ {description}...")
    print(f"  Command: {command}\n")
    
    try:
        result = subprocess.run(
            command,
            shell=shell,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        print(f"✅ {description} completed successfully!\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {command.split()[0]}")
        print("Please ensure the required tool is installed and in PATH.")
        return False


def check_prerequisites():
    """Check if required tools are installed."""
    print_header("CHECKING PREREQUISITES")
    
    # Check Python
    print(f"✓ Python: {sys.version.split()[0]}")
    
    # Check MFA
    result = subprocess.run(
        "mfa version",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"✓ MFA: {result.stdout.strip()}")
    else:
        print("❌ MFA not found!")
        print("\nPlease install MFA first:")
        print("  conda install -c conda-forge montreal-forced-aligner")
        return False
    
    # Check if models are downloaded
    result = subprocess.run(
        "mfa model list",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if "english_us_arpa" in result.stdout:
        print("✓ MFA models downloaded (english_us_arpa)")
    else:
        print("⚠ MFA models not found!")
        print("\nDownloading models now...")
        subprocess.run("mfa model download dictionary english_us_arpa", shell=True)
        subprocess.run("mfa model download acoustic english_us_arpa", shell=True)
    
    return True


def step1_validate():
    """Step 1: Validate dataset."""
    print_header("STEP 1: DATASET VALIDATION")
    
    if not Path("validate_dataset.py").exists():
        print("❌ validate_dataset.py not found!")
        return False
    
    return run_command(
        f"{sys.executable} validate_dataset.py",
        "Validating dataset"
    )


def step2_prepare():
    """Step 2: Prepare MFA dataset."""
    print_header("STEP 2: PREPARE MFA DATASET")
    
    if not Path("prepare_mfa_dataset.py").exists():
        print("❌ prepare_mfa_dataset.py not found!")
        return False
    
    # Check if mfa_data already exists
    if Path("mfa_data").exists():
        print("⚠ mfa_data/ directory already exists.")
        print("  The preparation script will prompt for removal confirmation.")
    
    # We need to run this interactively or with auto-yes
    # For automation, we'll modify the call
    print("▶ Preparing MFA dataset...")
    print(f"  Running: python prepare_mfa_dataset.py\n")
    
    # Run interactively
    result = subprocess.run(
        f"{sys.executable} prepare_mfa_dataset.py",
        shell=True
    )
    
    if result.returncode == 0:
        print(f"\n✅ Dataset preparation completed!\n")
        return True
    else:
        print(f"\n❌ Dataset preparation failed!\n")
        return False


def step3_align():
    """Step 3: Run MFA forced alignment."""
    print_header("STEP 3: FORCED ALIGNMENT")
    
    if not Path("mfa_data").exists():
        print("❌ mfa_data/ directory not found!")
        print("  Please run step 2 (prepare dataset) first.")
        return False
    
    # Create output directory
    output_dir = Path("output_textgrids")
    if output_dir.exists():
        print(f"⚠ Output directory already exists: {output_dir}")
        print("  Existing TextGrid files will be overwritten.")
    
    return run_command(
        "mfa align mfa_data/ english_us_arpa english_us_arpa output_textgrids/",
        "Running forced alignment (this may take a few minutes)"
    )


def step4_analyze():
    """Step 4: Analyze TextGrid outputs."""
    print_header("STEP 4: ANALYZE RESULTS")
    
    if not Path("output_textgrids").exists():
        print("❌ output_textgrids/ directory not found!")
        print("  Please run step 3 (alignment) first.")
        return False
    
    if not Path("analyze_textgrids.py").exists():
        print("❌ analyze_textgrids.py not found!")
        return False
    
    return run_command(
        f"{sys.executable} analyze_textgrids.py",
        "Analyzing TextGrid files"
    )


def run_full_pipeline():
    """Run the complete pipeline."""
    print_header("MFA FORCED ALIGNMENT PIPELINE")
    print("This script will run the complete workflow:")
    print("  1. Validate dataset")
    print("  2. Prepare MFA dataset")
    print("  3. Run forced alignment")
    print("  4. Analyze results")
    print("\nPress Enter to continue or Ctrl+C to cancel...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\n\nPipeline cancelled by user.")
        return
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites check failed. Please install required tools.")
        return
    
    # Run steps
    steps = [
        ("Validation", step1_validate),
        ("Preparation", step2_prepare),
        ("Alignment", step3_align),
        ("Analysis", step4_analyze)
    ]
    
    results = {}
    
    for step_name, step_func in steps:
        success = step_func()
        results[step_name] = success
        
        if not success:
            print(f"\n⚠ Step '{step_name}' failed or was skipped.")
            print("  Do you want to continue with the next step? (y/n): ", end="")
            try:
                response = input().strip().lower()
                if response != 'y':
                    print("\nPipeline stopped by user.")
                    break
            except KeyboardInterrupt:
                print("\n\nPipeline cancelled by user.")
                break
    
    # Summary
    print_header("PIPELINE SUMMARY")
    
    for step_name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{step_name:20s} {status}")
    
    if all(results.values()):
        print("\n🎉 All steps completed successfully!")
        print("\nNext steps:")
        print("  1. Open TextGrid files in Praat for visualization")
        print("  2. Review the analysis output above")
        print("  3. Check output_textgrids/ directory for all TextGrid files")
    else:
        print("\n⚠ Some steps failed. Please review the errors above.")


def run_single_step():
    """Run a single step interactively."""
    print_header("MFA PIPELINE - SINGLE STEP MODE")
    print("\nAvailable steps:")
    print("  1. Validate dataset")
    print("  2. Prepare MFA dataset")
    print("  3. Run forced alignment")
    print("  4. Analyze results")
    print("  5. Run full pipeline")
    print("  0. Exit")
    
    try:
        choice = input("\nEnter step number: ").strip()
        
        if choice == "1":
            step1_validate()
        elif choice == "2":
            step2_prepare()
        elif choice == "3":
            step3_align()
        elif choice == "4":
            step4_analyze()
        elif choice == "5":
            run_full_pipeline()
        elif choice == "0":
            print("Exiting...")
        else:
            print("Invalid choice!")
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Command-line mode
        arg = sys.argv[1].lower()
        
        if arg in ["full", "all", "pipeline"]:
            run_full_pipeline()
        elif arg in ["validate", "val", "1"]:
            check_prerequisites()
            step1_validate()
        elif arg in ["prepare", "prep", "2"]:
            check_prerequisites()
            step2_prepare()
        elif arg in ["align", "3"]:
            check_prerequisites()
            step3_align()
        elif arg in ["analyze", "analysis", "4"]:
            check_prerequisites()
            step4_analyze()
        else:
            print(f"Unknown argument: {arg}")
            print("\nUsage:")
            print("  python run_alignment.py [full|validate|prepare|align|analyze]")
            print("  python run_alignment.py          (interactive mode)")
    else:
        # Interactive mode
        run_full_pipeline()
