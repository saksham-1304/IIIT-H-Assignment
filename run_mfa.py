"""
MFA Wrapper Script
Makes it easy to run MFA commands in the mfa_env conda environment
"""

import subprocess
import sys

def run_mfa_command(args):
    """Run an MFA command in the mfa_env environment."""
    command = ["conda", "run", "-n", "mfa_env", "mfa"] + args
    
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=False,
            text=True
        )
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Error running MFA command: {e}")
        return e.returncode
    except KeyboardInterrupt:
        print("\nCommand interrupted by user")
        return 130

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_mfa.py <mfa_arguments>")
        print("\nExamples:")
        print("  python run_mfa.py version")
        print("  python run_mfa.py model list acoustic")
        print("  python run_mfa.py align mfa_data/ english_us_arpa english_us_arpa output_textgrids/")
        sys.exit(1)
    
    exit_code = run_mfa_command(sys.argv[1:])
    sys.exit(exit_code)
