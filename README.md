# Assignment 1: Forced Alignment using Montreal Forced Aligner (MFA)

## 📋 Project Overview

This project implements a complete forced alignment pipeline using the Montreal Forced Aligner (MFA) to automatically match audio recordings with their corresponding text transcriptions at the word and phoneme level.

**Repository**: https://github.com/saksham-1304/IIIT-H-Assignment  
**Date**: November 7, 2025
<br>
**Report Link**: https://drive.google.com/file/d/1YdvBeMw_LqplqtHmt53RA9Jp1skTpjyj/view?usp=sharing

## 🎯 Objective

Set up and execute a complete forced alignment pipeline to understand how automatic alignment works between speech audio and phonetic transcription.

## 📁 Dataset Description

The dataset contains 6 audio files with corresponding transcripts:

### 1. Broadcast News Dataset (F2BJRLP series)
- **Files**: `F2BJRLP1`, `F2BJRLP2`, `F2BJRLP3`
- **Content**: Continuous speech, news broadcasts, formal narratives
- **Transcript format**: Multi-line paragraphs with natural punctuation
- **Duration**: Longer segments (typically several minutes)

### 2. ISLE Speech Dataset (ISLE_SESS series)
- **Files**: `ISLE_SESS0131_BLOCKD02_01_sprt1`, `ISLE_SESS0131_BLOCKD02_02_sprt1`, `ISLE_SESS0131_BLOCKD02_03_sprt1`
- **Content**: Minimal pair utterances (single short phrases)
- **Transcript format**: Single line, uppercase (e.g., "I SAID WHITE NOT BAIT")
- **Duration**: Short utterances (~1-3 seconds)

## 🛠️ Installation Instructions

### Step 1: Install Miniconda (Required)

1. Download Miniconda for Windows:
   - Visit: https://docs.conda.io/en/latest/miniconda.html
   - Download: **Miniconda3 Windows 64-bit** installer
   - Direct link: https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe

2. Run the installer:
   - ✅ **Important**: Check "Add Miniconda3 to my PATH environment variable"
   - Complete the installation
   - Restart PowerShell/Command Prompt

3. Verify installation:
   ```powershell
   conda --version
   ```
   Expected output: `conda 23.x.x` or similar

### Step 2: Install Montreal Forced Aligner

```powershell
# Update conda
conda update -n base -c defaults conda

# Install MFA
conda install -c conda-forge montreal-forced-aligner

# Verify MFA installation
mfa version
```

Expected output: `Montreal Forced Aligner version 2.x.x`

### Step 3: Download Pre-trained Models

```powershell
# Download English US pronunciation dictionary (ARPA format)
mfa model download dictionary english_us_arpa

# Download English US acoustic model
mfa model download acoustic english_us_arpa

# Verify downloaded models
mfa model list
```

You should see both `english_us_arpa` listed under dictionaries and acoustic models.

## 📊 Dataset Preparation

### Step 1: Validate Dataset

Run the validation script to ensure all audio files have corresponding transcripts:

```powershell
python validate_dataset.py
```

Expected output:
```
============================================================
MFA Dataset Validation
============================================================

✓ Found 6 audio files in 'wav/'

Paired Files (6):
  ✓ F2BJRLP1.wav → F2BJRLP1.TXT (203 chars)
  ✓ F2BJRLP2.wav → F2BJRLP2.TXT (285 chars)
  ✓ F2BJRLP3.wav → F2BJRLP3.TXT (312 chars)
  ✓ ISLE_SESS0131_BLOCKD02_01_sprt1.wav → ISLE_SESS0131_BLOCKD02_01_sprt1.txt (23 chars)
  ✓ ISLE_SESS0131_BLOCKD02_02_sprt1.wav → ISLE_SESS0131_BLOCKD02_02_sprt1.txt (23 chars)
  ✓ ISLE_SESS0131_BLOCKD02_03_sprt1.wav → ISLE_SESS0131_BLOCKD02_03_sprt1.txt (23 chars)

✅ All audio files have matching transcripts!
```

### Step 2: Prepare MFA Dataset

Convert transcripts to MFA-compatible format (`.lab` files):

```powershell
python prepare_mfa_dataset.py
```

This script:
- Creates `mfa_data/` directory
- Copies audio files
- Converts transcripts to `.lab` format (single-line text)
- Handles multi-line F2BJRLP transcripts by joining them
- Preserves single-line ISLE transcripts

**Output structure**:
```
mfa_data/
  F2BJRLP1.wav
  F2BJRLP1.lab
  F2BJRLP2.wav
  F2BJRLP2.lab
  ...
```

## 🚀 Running Forced Alignment

### Execute MFA Alignment

```powershell
# Navigate to project directory (if not already there)
cd "C:\Users\HP\Downloads\Assignment\Assignment\IIIT-H-Assignment"

# Run forced alignment
mfa align mfa_data/ english_us_arpa english_us_arpa output_textgrids/
```

**Parameters**:
- `mfa_data/` - Input directory with audio and transcript files
- `english_us_arpa` - Pronunciation dictionary
- `english_us_arpa` - Acoustic model
- `output_textgrids/` - Output directory for TextGrid files

### Expected Output

The alignment process will:
1. Validate input files
2. Generate pronunciation variants
3. Perform acoustic alignment
4. Create TextGrid files in `output_textgrids/` directory

**Output files**:
```
output_textgrids/
  F2BJRLP1.TextGrid
  F2BJRLP2.TextGrid
  F2BJRLP3.TextGrid
  ISLE_SESS0131_BLOCKD02_01_sprt1.TextGrid
  ISLE_SESS0131_BLOCKD02_02_sprt1.TextGrid
  ISLE_SESS0131_BLOCKD02_03_sprt1.TextGrid
```

## 🔍 Inspecting Results

### Using Praat (Recommended)

1. **Download and Install Praat**:
   - Visit: https://www.fon.hum.uva.nl/praat/
   - Download the Windows version
   - Install and launch Praat

2. **Open TextGrid with Audio**:
   - In Praat: `Open` → `Read from file`
   - Select a `.wav` file from `wav/` directory
   - Select the corresponding `.TextGrid` file from `output_textgrids/`
   - Select both objects → `View & Edit`

3. **Analyze Alignment**:
   - **Words tier**: Shows start/end times for each word
   - **Phones tier**: Shows start/end times for each phoneme
   - Click on segments to play individual words/phonemes
   - Zoom in to examine phoneme boundaries

### Using Python Script

I've included an analysis script to programmatically inspect TextGrids:

```powershell
python analyze_textgrids.py
```

This script extracts and displays:
- Word boundaries and durations
- Phoneme boundaries and durations
- Alignment statistics

## 📝 Example Alignment Output

For the utterance: **"HELLO WORLD"**

**Word tier**:
```
0.00 – 0.45   HELLO
0.45 – 0.90   WORLD
```

**Phone tier**:
```
0.00 – 0.10   HH
0.10 – 0.25   AH
0.25 – 0.40   L
0.40 – 0.45   OW
0.45 – 0.55   W
0.55 – 0.70   ER
0.70 – 0.85   L
0.85 – 0.90   D
```

## 📊 Key Observations

### 1. Alignment Quality
- **F2BJRLP files**: Continuous speech with natural pauses, generally good alignment
- **ISLE files**: Short utterances with clear articulation, excellent alignment

### 2. Common Alignment Issues
- **Silence handling**: Leading/trailing silence sometimes included in word boundaries
- **Fast speech**: Rapid articulation can cause phoneme boundary merging
- **Background noise**: May affect boundary precision

### 3. Model Performance
- **english_us_arpa dictionary**: Comprehensive coverage of English phonemes
- **english_us_arpa acoustic model**: Trained on diverse speech data, performs well on both formal and conversational speech

## 📂 Project Structure

```
IIIT-H-Assignment/
│
context and instructions
│
├── wav/                          # Original audio files (6 files)
│   ├── F2BJRLP1.wav
│   ├── F2BJRLP2.wav
│   ├── F2BJRLP3.wav
│   ├── ISLE_SESS0131_BLOCKD02_01_sprt1.wav
│   ├── ISLE_SESS0131_BLOCKD02_02_sprt1.wav
│   └── ISLE_SESS0131_BLOCKD02_03_sprt1.wav
│
├── transcripts/                  # Original transcripts (6 files)
│   ├── F2BJRLP1.TXT
│   ├── F2BJRLP2.TXT
│   ├── F2BJRLP3.TXT
│   ├── ISLE_SESS0131_BLOCKD02_01_sprt1.txt
│   ├── ISLE_SESS0131_BLOCKD02_02_sprt1.txt
│   └── ISLE_SESS0131_BLOCKD02_03_sprt1.txt
│
├── mfa_data/                     # MFA-formatted dataset
│   ├── [audio].wav + .lab files (6 pairs)
│
├── output_textgrids/             # Generated TextGrid files
│   ├── [audio].TextGrid (6 files)
│   └── alignment_analysis.csv
│
├── validate_dataset.py           # Dataset validation script
├── prepare_mfa_dataset.py        # MFA dataset preparation script
├── analyze_textgrids.py          # TextGrid analysis script
├── run_mfa.py                    # Automated alignment pipeline
│
├── Assignment1.pdf               # Assignment requirements
├── README.md                     # This file
└── .gitignore                    # Git ignore patterns
```

## 🎓 What is Forced Alignment?

Forced alignment is an automated process that:

1. **Takes as input**:
   - Audio recording of speech
   - Text transcript of what was said

2. **Produces as output**:
   - Precise timestamps for when each word starts and ends
   - Precise timestamps for when each phoneme starts and ends

3. **How it works**:
   - Uses a pronunciation dictionary to convert words to phonemes
   - Uses an acoustic model trained on speech data
   - Applies Viterbi algorithm to find optimal alignment
   - Generates TextGrid files with boundary annotations

## 🔧 Automation Script

For convenience, use the automated pipeline script:

```powershell
python run_mfa.py
```

This script runs the entire pipeline:

1. Validates dataset
2. Prepares MFA data
3. Runs forced alignment
4. Analyzes results

## 📦 Requirements

- **Python**: 3.8 or higher
- **Conda**: Miniconda or Anaconda
- **MFA**: Montreal Forced Aligner 2.x
- **Praat**: For visualization (optional but recommended)

### Python Dependencies

```
textgrid==1.6.0  # For TextGrid parsing
scipy>=1.9.0     # For audio file handling
```

Install with:
```powershell
pip install textgrid scipy
```

## 🏆 Extra Credit Opportunities

### 1. Train Custom Dictionary

Use MFA's G2P (Grapheme-to-Phoneme) model to generate a custom dictionary:

```powershell
mfa g2p english_us_arpa mfa_data/ custom_dict.txt
mfa align mfa_data/ custom_dict.txt english_us_arpa output_textgrids_custom/
```

### 2. Compare Multiple Acoustic Models

Try different acoustic models and compare alignment quality:

```powershell
# Download alternative model
mfa model download acoustic english_mfa

# Run alignment with different model
mfa align mfa_data/ english_us_arpa english_mfa output_textgrids_mfa/
```

### 3. Automated Pipeline

The `run_mfa.py` script provides full automation with error handling and logging.

## 🐛 Troubleshooting

### Issue: "conda command not found"

- **Solution**: Restart PowerShell or add conda to PATH manually
- Check: `C:\Users\[YourUsername]\miniconda3\Scripts` should be in PATH

### Issue: MFA alignment fails

- **Solution**: Check that `.lab` files contain valid text
- Verify models are downloaded: `mfa model list`
- Check audio files are valid WAV format (16-bit PCM recommended)

### Issue: Poor alignment quality

- **Solution**:
  - Check transcript accuracy
  - Ensure audio quality is good
  - Try different acoustic models
  - Consider training custom dictionary

## 📧 Submission

- **GitHub Repository**: [IIIT-H-Assignment](https://github.com/saksham-1304/IIIT-H-Assignment)
- **Outputs**: All TextGrid files in `output_textgrids/`

Ensure all links are publicly accessible for evaluation.

## 📚 Resources

- [MFA Documentation](https://montreal-forced-aligner.readthedocs.io/)
- [Praat Software](https://www.fon.hum.uva.nl/praat/)
- [TextGrid Format Guide](https://www.fon.hum.uva.nl/praat/manual/TextGrid_file_formats.html)

## 👤 Author

**Saksham**  
GitHub: [saksham-1304](https://github.com/saksham-1304)

## 📄 License

This project is for educational purposes as part of IIIT Hyderabad coursework.

---

**Last Updated**: November 7, 2025
