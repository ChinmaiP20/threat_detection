# Execution Commands Guide

This document contains all the commands needed to execute the Audio Threat Detection application.

## Prerequisites

### 1. Install Python Dependencies

Navigate to the `audio-threat-detection` directory and install required packages:

```bash
cd "C:\Users\Chinmai Pore\OneDrive\Documents\audio-threat-detection"
pip install -r requirements.txt
```

Or install individually:
```bash
pip install faster-whisper==1.0.3
pip install pydub==0.25.1
pip install webrtcvad==2.0.10
pip install SpeechRecognition==3.10.4
pip install soundfile==0.12.1
pip install loguru==0.7.2
pip install deep-translator==1.11.4
pip install transformers==4.45.2
pip install pyannote.audio==3.1.1
pip install pyannote.core==5.0.0
pip install python-dotenv==1.0.1
pip install Flask==3.0.3
pip install flask-cors==4.0.1
```

**Note for NumPy**: Install based on your Python version:
- Python < 3.12: `pip install numpy==1.26.4`
- Python >= 3.12: `pip install "numpy>=2.1.0,<2.3"`

### 2. Install FFmpeg (Required for Audio Processing)

**Windows:**
1. Download FFmpeg from: https://ffmpeg.org/download.html
2. Extract and add to PATH, or use Chocolatey:
   ```powershell
   choco install ffmpeg
   ```
3. Verify installation:
   ```bash
   ffmpeg -version
   ffprobe -version
   ```

**Alternative Windows Installation:**
```powershell
# Using winget
winget install FFmpeg

# Or download portable version and add to PATH
```

### 3. HuggingFace Token (Optional - for Speaker Diarization)

If you want to use speaker diarization features:
1. Create a HuggingFace account: https://huggingface.co/
2. Generate an access token: https://huggingface.co/settings/tokens
3. Accept the model terms: https://huggingface.co/pyannote/speaker-diarization-3.1
4. Set environment variable:
   ```powershell
   $env:HF_TOKEN="your_token_here"
   ```

## Running the Application

### Method 1: Flask Web Application (Recommended)

Navigate to the `audio-threat-detection` directory:

```bash
cd "C:\Users\Chinmai Pore\OneDrive\Documents\audio-threat-detection"
python app.py
```

The server will start on `http://localhost:5000`

**Access the application:**
- Open your browser and go to: `http://localhost:5000`
- The web interface allows you to upload audio files and analyze them

**Stop the server:**
- Press `Ctrl+C` in the terminal

### Method 2: Using the Module Programmatically

You can import and use the modules directly in Python:

```python
from app.pipeline import comprehensive_analysis

# Analyze an audio file
results = comprehensive_analysis(
    audio_path="path/to/your/audio.mp3",
    hf_token="your_hf_token_here",  # Optional
    translate_to=("English", "en")  # Optional: ("Language Name", "lang_code")
)

print(f"Risk Level: {results['risk_level']}")
print(f"Risk Score: {results['risk_score']}")
print(f"Transcription: {results['transcription']}")
```

**Example script:**
```python
# analyze_audio.py
from app.pipeline import comprehensive_analysis
import json

results = comprehensive_analysis(
    audio_path="path/to/audio.mp3",
    hf_token=None,  # Set your token if needed
    translate_to=None  # Set ("English", "en") for translation
)

# Save results
with open("analysis_results.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"Analysis complete! Risk Level: {results['risk_level']}")
```

Run the script:
```bash
python analyze_audio.py
```

## Additional Commands

### Check Python Version
```bash
python --version
```

### Verify FFmpeg Installation
```bash
ffmpeg -version
ffprobe -version
```

### Check Installed Packages
```bash
pip list | findstr "whisper\|flask\|transformers\|pyannote"
```

### Run with Custom Port (Flask)
Modify `app.py` line 312 or set environment variable:
```powershell
$env:FLASK_PORT=8080
python app.py
```

### Run in Debug Mode
The Flask app already runs in debug mode by default. To disable:
```python
app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
```

## Troubleshooting

### FFmpeg Not Found
```bash
# Verify FFmpeg is in PATH
where ffmpeg
where ffprobe

# If not found, add FFmpeg to PATH or use full path
```

### Module Import Errors
```bash
# Ensure you're in the correct directory or install as package
cd "C:\Users\Chinmai Pore\OneDrive\Documents"
pip install -e .
```

### CUDA/GPU Issues
The application will automatically use CPU if CUDA is not available. To force CPU:
```python
# In transcription.py, modify:
self.model = WhisperModel(model_size, device="cpu")
```

### Memory Issues
For large audio files, use a smaller Whisper model:
```python
transcriber = Transcriber(model_size="tiny")  # or "base", "small", "medium", "large"
```

## Quick Start Summary

```bash
# 1. Install dependencies
cd "C:\Users\Chinmai Pore\OneDrive\Documents\audio-threat-detection"
pip install -r requirements.txt

# 2. Verify FFmpeg (must be installed separately)
ffmpeg -version

# 3. Run the application
python app.py

# 4. Open browser to http://localhost:5000
```

## API Endpoints (When Running Flask App)

- `GET /` - Web dashboard
- `GET /api/health` - Health check
- `POST /api/upload` - Upload audio file
- `POST /api/analyze` - Analyze uploaded audio
- `GET /api/progress/<analysis_id>` - Get analysis progress
- `GET /api/results/<analysis_id>` - Get analysis results
- `GET /api/keywords` - Get keywords/codewords/slang dictionaries
- `POST /api/keywords/add` - Add new keyword/codeword/slang
- `POST /api/keywords/delete` - Delete keyword/codeword/slang
- `GET /api/history` - Get analysis history
- `GET /api/report/<filename>` - Download report

