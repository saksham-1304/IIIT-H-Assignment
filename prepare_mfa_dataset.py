"""
Prepare Dataset for Montreal Forced Aligner (MFA)
Organizes audio files and transcripts into MFA-required format.

MFA expects:
  mfa_data/
    audio1.wav
    audio1.lab (or .txt)
    audio2.wav
    audio2.lab
    ...
"""

import os
import shutil
from pathlib import Path

def prepare_mfa_data():
    """Prepare dataset in MFA-compatible format."""
    
    base_dir = Path(__file__).parent
    wav_dir = base_dir / "wav"
    transcript_dir = base_dir / "transcripts"
    mfa_dir = base_dir / "mfa_data"
    
    print("=" * 60)
    print("Preparing Dataset for MFA")
    print("=" * 60)
    
    # Create MFA directory
    if mfa_dir.exists():
        print(f"\n⚠ Directory '{mfa_dir}' already exists. Remove it? (y/n)")
        response = input().strip().lower()
        if response == 'y':
            shutil.rmtree(mfa_dir)
        else:
            print("Aborted.")
            return
    
    mfa_dir.mkdir(exist_ok=True)
    print(f"\n✓ Created directory: {mfa_dir}")
    
    # Get all wav files
    wav_files = sorted([f for f in os.listdir(wav_dir) if f.endswith('.wav')])
    
    processed = 0
    for wav_file in wav_files:
        basename = os.path.splitext(wav_file)[0]
        
        # Find transcript (handle both .txt and .TXT)
        txt_path_lower = transcript_dir / f"{basename}.txt"
        txt_path_upper = transcript_dir / f"{basename}.TXT"
        
        if txt_path_lower.exists():
            transcript_path = txt_path_lower
        elif txt_path_upper.exists():
            transcript_path = txt_path_upper
        else:
            print(f"⚠ No transcript found for {wav_file}, skipping...")
            continue
        
        # Copy audio file
        src_audio = wav_dir / wav_file
        dst_audio = mfa_dir / wav_file
        shutil.copy2(src_audio, dst_audio)
        
        # Copy and process transcript
        # MFA expects .lab or .txt files with the same basename
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript_content = f.read().strip()
        
        # Process based on file type
        if 'ISLE' in basename:
            # ISLE files: single line, already uppercase
            # Keep as-is for MFA
            processed_text = transcript_content
        else:
            # F2BJRLP files: multi-line transcripts
            # Combine into single line for MFA (remove extra whitespace)
            processed_text = ' '.join(transcript_content.split())
        
        # Save as .lab file (MFA standard) or .txt
        dst_transcript = mfa_dir / f"{basename}.lab"
        with open(dst_transcript, 'w', encoding='utf-8') as f:
            f.write(processed_text)
        
        print(f"✓ Processed: {basename}")
        processed += 1
    
    print(f"\n" + "=" * 60)
    print(f"✓ Successfully prepared {processed} file pairs")
    print(f"✓ Output directory: {mfa_dir}")
    print("=" * 60)
    
    print("""
Next Steps:
  1. Install MFA: conda install -c conda-forge montreal-forced-aligner
  2. Download dictionary: mfa model download dictionary english_us_arpa
  3. Download acoustic model: mfa model download acoustic english_us_arpa
  4. Run alignment:
     mfa align mfa_data/ english_us_arpa english_us_arpa output_textgrids/
    """)

if __name__ == "__main__":
    prepare_mfa_data()
