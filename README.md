#  Audio Threat Detection System

> AI-Powered Audio Analysis with Speaker Identification, Multilingual Translation, Threat Detection, and Human-in-the-Loop Feedback

---

##  Table of Contents

- [Overview](#overview)
- [Features](#features)
- [AI Models Used](#ai-models-used)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [Output Files](#output-files)
- [Human Feedback System](#human-feedback-system)
- [Translation Support](#translation-support)
- [Troubleshooting](#troubleshooting)
- [Performance Benchmarks](#performance-benchmarks)

---

##  Overview

The **Audio Threat Detection System** is a comprehensive AI-powered tool designed to analyze audio files for potential threats, suspicious language, codewords, and emotional indicators. It combines multiple state-of-the-art machine learning models to provide a full threat assessment with human review capabilities.

### What It Does
- Converts audio from any format to MP3
- Identifies and separates multiple speakers
- Transcribes speech with automatic language detection
- Translates transcriptions into 10+ languages
- Detects threat keywords, slang, and codewords
- Analyzes emotion, sentiment, toxicity, and sarcasm
- Provides a human-in-the-loop feedback interface
- Generates detailed JSON and text reports

---

##  Features

| Feature | Description |
|---------|-------------|
| 🎤 Audio Conversion | Supports MP3, WAV, M4A, FLAC, OGG, MP4, AVI, MOV |
| 👥 Speaker Diarization | Identifies and separates unique speakers |
| 📝 Transcription | Multilingual speech-to-text via Whisper |
| 🌍 Translation | Translate to 10 languages (Spanish, French, Hindi, etc.) |
| ⚠️ Threat Detection | 50+ built-in threat keywords across 7 categories |
| 🕵️ Codeword Detection | Detects innocent phrases with hidden meanings |
| 🗣️ Slang Detection | 14+ built-in criminal/gang slang terms |
| 😊 Emotion Analysis | Detects 7 emotions (joy, anger, fear, sadness, etc.) |
| 💭 Sentiment Analysis | Positive, Neutral, Negative classification |
| ☣️ Toxicity Detection | 6 toxicity categories via BERT |
| 🎭 Sarcasm Detection | Reduces false positives from sarcastic content |
| 🧑‍💻 Human Feedback | Approve, reject, or modify detected keywords |
| 📊 Report Generation | JSON + Text reports with full analysis |
| 🖥️ Web Dashboard | Browser-based frontend with Flask API |

---

## 🤖 AI Models Used

| Model | Purpose | Size | Parameters |
|-------|---------|------|------------|
| `openai/whisper-large-v3` | Speech-to-Text & Translation | 3.0 GB | 1.55B |
| `j-hartmann/emotion-english-distilroberta-base` | Emotion Detection | 255 MB | 82M |
| `cardiffnlp/twitter-roberta-base-sentiment-latest` | Sentiment Analysis | 500 MB | 125M |
| `unitary/toxic-bert` | Toxicity Detection | 440 MB | 110M |
| `helinivan/english-sarcasm-detector` | Sarcasm Detection | 440 MB | 110M |
| `pyannote/speaker-diarization-3.1` | Speaker Diarization | 230 MB | ~20M |
| `Helsinki-NLP/opus-mt-{lang}` | Translation (per language) | 300 MB | 77M |

**Total storage (without translation):** ~4.9 GB  
**Total storage (with all 10 languages):** ~7.9 GB

---

## 💻 System Requirements

### Minimum
- **OS:** Windows 10 / Ubuntu 20.04 / macOS 11
- **CPU:** Intel i5 / AMD Ryzen 5
- **RAM:** 8 GB
- **Storage:** 10 GB free disk space
- **Python:** 3.8 or higher
- **Internet:** Required for first-time model downloads

### Recommended
- **CPU:** Intel i7 / AMD Ryzen 7
- **RAM:** 16 GB
- **GPU:** NVIDIA RTX 3060 (6 GB VRAM) or better
- **Storage:** 15 GB free SSD space

### Optimal
- **CPU:** Intel i9 / AMD Ryzen 9
- **RAM:** 32 GB
- **GPU:** NVIDIA RTX 4080 (12 GB VRAM) or better
- **Storage:** 20 GB free NVMe SSD

---

## 🔧 Installation

### Step 1: Clone or Download the Project
```bash
git clone https://github.com/yourname/audio-threat-detection.git
cd audio-threat-detection
```

### Step 2: Create a Virtual Environment (Recommended)
```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
# Core ML packages
pip install torch transformers soundfile librosa noisereduce pydub

# Speaker diarization
pip install pyannote.audio

# Translation support
pip install sentencepiece sacremoses

# Web interface
pip install flask flask-cors

# Additional utilities
pip install numpy scipy
```

### Step 4: Install FFmpeg (Required for Audio Conversion)

**Windows (using Chocolatey):**
```bash
choco install ffmpeg
```

**Windows (manual):**
1. Download from https://www.gyan.dev/ffmpeg/builds/
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to system PATH

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

### Step 5: Create Project Directories
```bash
mkdir uploads reports templates analysis_reports
```

---

##  Project Structure

```
audio-threat-detection/
│
├── threat_analysis.py              # Main analysis module
├── app.py                          # Flask web server
├── README.md                       # This file
│
├── templates/
│   └── dashboard.html              # Web dashboard UI
│
├── uploads/                        # Uploaded audio files
├── reports/                        # Web-generated reports
├── analysis_reports/               # CLI-generated reports
│
├── custom_threat_keywords.json     # User-added threat keywords
├── codewords_database.json         # Codewords/phrases database
├── slang_dictionary.json           # Slang terms dictionary
└── keyword_feedback.json           # Human feedback history
```

---

##  Configuration

### 1. Set HuggingFace Token

Speaker diarization requires a HuggingFace token. Get yours at https://huggingface.co/settings/tokens

In `threat_analysis.py`:
```python
HF_TOKEN = "hf_your_actual_token_here"
```

Also accept the diarization model terms at:
- https://huggingface.co/pyannote/speaker-diarization-3.1
- https://huggingface.co/pyannote/segmentation-3.0

### 2. Change Whisper Model (Optional)

To use a smaller/faster model, edit `threat_analysis.py`:
```python
# Options (smallest to largest):
MODEL_NAME = "openai/whisper-tiny"    # 75 MB  - Fastest
MODEL_NAME = "openai/whisper-base"    # 145 MB - Fast
MODEL_NAME = "openai/whisper-small"   # 483 MB - Balanced
MODEL_NAME = "openai/whisper-medium"  # 1.5 GB - Good
MODEL_NAME = "openai/whisper-large-v3" # 3 GB  - Best (default)
```

---

##  Usage

### Option A: Command-Line Interface

```bash
python threat_analysis.py
```

**Main Menu:**
```
  AUDIO THREAT DETECTION SYSTEM - MAIN MENU
================================================================================
1. Analyze Audio File (with Human Feedback)
2. Analyze Audio File (No Feedback - Auto Mode)
3. Add Custom Threat Keyword
4. Add Codeword/Phrase
5. Add Slang Term
6. View Databases
7. View Feedback History
8. Exit
```

**Example Analysis:**
```bash
# Select 1 → Enter file path → Select translation language

Enter audio file path: C:\audio\sample.mp3

TRANSLATION OPTIONS
1. Spanish   6. Arabic
2. French    7. Russian
3. German    8. Portuguese
4. Hindi     9. Japanese
5. Chinese  10. Italian
0. Skip Translation

Select language: 4   ← Translates to Hindi
```

### Option B: Web Dashboard

```bash
# Start the Flask server
python app.py

# Open browser
http://localhost:5000
```

**Web Dashboard Tabs:**
- **Analyze Audio** - Upload and analyze files
- **Manage Keywords** - Add threat keywords via UI
- **Manage Codewords** - Add codewords via UI
- **Manage Slang** - Add slang terms via UI
- **View Results** - See analysis results with charts

---

##  Output Files

### JSON Report (`threat_report_TIMESTAMP.json`)
```json
{
    "transcription": "Full transcribed text...",
    "translation": "Translated text (if selected)...",
    "translated_language": "Hindi",
    "speakers": [
        {"speaker": "SPEAKER_00", "start": 0.0, "end": 45.2, "duration": 45.2}
    ],
    "slang": {
        "strapped": {"meaning": "armed with weapon", "occurrences": 1}
    },
    "codewords": {
        "pop the balloon": {"real_meaning": "Execute target", "risk_score": 10}
    },
    "threats": {
        "threats": {"attack": {"risk_score": 8, "occurrences": 2}},
        "total_risk": 16
    },
    "emotions": [{"label": "anger", "score": 0.82}],
    "sentiments": [{"label": "Negative", "score": 0.75}],
    "sarcasm": {"average_score": 0.15, "sarcastic_sentences": []},
    "risk_score": 28.5,
    "risk_level": "LOW"
}
```

### Risk Levels

| Level | Score Range | Description |
|-------|-------------|-------------|
| ✅ SAFE | 0 | No threats detected |
| ⚠️ LOW | 1 - 19 | Minor indicators |
| ⚠️⚠️ MEDIUM | 20 - 49 | Moderate concern |
| ⚠️⚠️⚠️ HIGH | 50 - 99 | Significant threat |
| 🚨 CRITICAL | 100+ | Immediate attention required |

---

## 🧑‍💻 Human Feedback System

When using **Option 1 (Analysis with Feedback)**, you are prompted to review each detection:

```
HUMAN FEEDBACK REQUEST
================================================================================
Detected threat keyword: 'attack'
Meaning: Violent act
Risk Score: 8
Context: "...we need to attack this problem head-on..."

Options:
1. Approve - Add to permanent database
2. Reject  - False positive, remove from detection
3. Modify  - Change risk score or meaning
4. Skip    - Keep for this analysis only
```

| Option | Effect |
|--------|--------|
| Approve | Saves to permanent database for future analyses |
| Reject | Excludes from future detections, logs reason |
| Modify | Updates risk score or meaning before saving |
| Skip | Uses for current analysis only, not saved |

All feedback is saved to `keyword_feedback.json` and viewable via **Menu Option 7**.

---

##  Translation Support

Supported target languages:

| # | Language | Model |
|---|----------|-------|
| 1 | Spanish | opus-mt-en-es |
| 2 | French | opus-mt-en-fr |
| 3 | German | opus-mt-en-de |
| 4 | Hindi | opus-mt-en-hi |
| 5 | Chinese | opus-mt-en-zh |
| 6 | Arabic | opus-mt-en-ar |
| 7 | Russian | opus-mt-en-ru |
| 8 | Portuguese | opus-mt-en-pt |
| 9 | Japanese | opus-mt-en-jap |
| 10 | Italian | opus-mt-en-it |

Translation models are downloaded (~300 MB each) only when first used.

---

##  Threat Categories

### Built-in Threat Keywords (14 default, expandable)

| Category | Examples |
|----------|---------|
| Violence | kill, murder, attack, assault, shoot |
| Weapon | bomb, explosive, gun, weapon |
| Terrorism | terror, terrorist, hostage |
| Hostility | kidnap, threat |

### Built-in Codewords (10 default, expandable)

| Phrase | Hidden Meaning |
|--------|---------------|
| "pop the balloon" | Execute target |
| "cut the cake" | Start operation |
| "clean the house" | Eliminate evidence |
| "take out the trash" | Remove target |
| "light the candles" | Start the plan |

### Built-in Slang (14 default, expandable)

| Slang | Meaning |
|-------|---------|
| strapped | armed with weapon |
| cap | shoot |
| smoke | kill |
| drill | attack/shoot |
| slide | go attack someone |

---

## 🛠️ Troubleshooting

### FFmpeg Not Found
```bash
# Windows
choco install ffmpeg

# Verify installation
ffmpeg -version
```

### CUDA/GPU Not Detected
```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# Install CUDA-enabled PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Diarization Authentication Error
```
# Ensure you have:
# 1. Valid HF_TOKEN in threat_analysis.py
# 2. Accepted model terms at huggingface.co/pyannote/speaker-diarization-3.1
```

### Out of Memory Error
```python
# Use smaller Whisper model
MODEL_NAME = "openai/whisper-base"

# Or disable diarization
speakers = []
```

### Port Already in Use (Web Server)
```python
# In app.py, change port:
app.run(debug=True, host='0.0.0.0', port=5001)
```

---

# Performance Benchmarks

### Processing Time (5-minute audio file)

| Hardware | Transcription | Full Pipeline |
|----------|--------------|---------------|
| CPU (i5) | 12-15 min | 20-25 min |
| CPU (i7) | 8-12 min | 15-20 min |
| GPU RTX 3060 | 2-3 min | 4-6 min |
| GPU RTX 4090 | 1-2 min | 2-3 min |

### Memory Usage During Analysis

| Task | CPU RAM | GPU VRAM |
|------|---------|----------|
| Whisper | 4-6 GB | 6-8 GB |
| Emotion | 500 MB | 1 GB |
| Sentiment | 800 MB | 1.5 GB |
| Diarization | 2-3 GB | 3-4 GB |
| **Peak Total** | **~8-12 GB** | **~10-15 GB** |

---

##  Dependencies

```
torch
transformers
soundfile
librosa
noisereduce
pydub
pyannote.audio
sentencepiece
sacremoses
flask
flask-cors
numpy
scipy
```

Install all at once:
```bash
pip install torch transformers soundfile librosa noisereduce pydub pyannote.audio sentencepiece sacremoses flask flask-cors numpy scipy
```

---

##  License

This project is for educational and research purposes only.  
All AI models used are open-source and available on Hugging Face.

---

# Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) - Speech recognition
- [PyAnnote Audio](https://github.com/pyannote/pyannote-audio) - Speaker diarization
- [HuggingFace Transformers](https://huggingface.co/transformers) - Model hosting and inference
- [Helsinki-NLP](https://huggingface.co/Helsinki-NLP) - MarianMT translation models

---

