# Audio Threat Detection System - Complete Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [System Architecture](#system-architecture)
4. [Installation Guide](#installation-guide)
5. [Usage Instructions](#usage-instructions)
6. [Threat Detection System](#threat-detection-system)
7. [Scoring Methodology](#scoring-methodology)
8. [API Documentation](#api-documentation)
9. [File Structure](#file-structure)
10. [Configuration](#configuration)
11. [Troubleshooting](#troubleshooting)
12. [Development Guide](#development-guide)

---

## Project Overview

The **Audio Threat Detection System** is an advanced audio analysis platform designed to detect potential security threats in audio recordings. The system uses state-of-the-art speech recognition, natural language processing, and threat detection algorithms to analyze audio content and identify potentially dangerous keywords, codewords, and slang terms.

### Key Capabilities
- **Real-time Audio Transcription**: Converts speech to text using Whisper AI
- **Multi-language Support**: Supports transcription and translation in 11+ languages
- **Threat Keyword Detection**: Identifies 50+ threat keywords across 6 categories
- **Codeword Detection**: Detects hidden meanings and coded language
- **Slang Translation**: Identifies and translates slang terms
- **Risk Scoring**: Calculates comprehensive threat risk scores
- **Web-based Interface**: User-friendly dashboard for analysis and reporting

---

## Features

### Core Features

1. **Audio Processing**
   - Supports multiple audio formats (MP3, WAV, M4A, OGG, FLAC, MP4, AVI, MOV)
   - Automatic format conversion to MP3 (CBR 128k, 16kHz mono)
   - Audio duration calculation

2. **Speech Recognition**
   - Powered by Faster Whisper (OpenAI Whisper implementation)
   - Automatic language detection
   - High-accuracy transcription
   - CPU-based processing (avoids CUDA/cuDNN issues)

3. **Threat Detection**
   - **50+ Threat Keywords** across 6 categories:
     - Violence & Attack (10 keywords)
     - Weapons (11 keywords)
     - Terrorism (8 keywords)
     - Hostility (6 keywords)
     - Destruction (5 keywords)
     - Chemical/Biological (5 keywords)
     - Planning/Intent (4 keywords)
   - Context-aware detection
   - Occurrence counting
   - Risk score calculation

4. **Codeword Detection**
   - Custom codeword database
   - Hidden meaning identification
   - Context extraction
   - Risk scoring per codeword

5. **Slang Detection**
   - Slang dictionary support
   - Meaning translation
   - Occurrence tracking

6. **Translation**
   - Multi-language translation support
   - 11 supported languages:
     - English, Spanish, French, German, Hindi
     - Chinese, Arabic, Russian, Portuguese
     - Japanese, Italian
   - Optional translation feature

7. **Risk Assessment**
   - Comprehensive risk scoring
   - Risk level classification:
     - **SAFE**: 0 risk points
     - **LOW**: 1-19 risk points
     - **MEDIUM**: 20-49 risk points
     - **HIGH**: 50-99 risk points
     - **CRITICAL**: 100+ risk points

8. **Web Dashboard**
   - Modern, responsive UI
   - Real-time progress tracking
   - Detailed results visualization
   - Export capabilities
   - Keyword management interface

---

## System Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Web Dashboard                        │
│              (Flask Web Application)                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Analysis Pipeline                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Audio Utils  │→ │Transcription │→ │Threat Analysis│  │
│  │ (FFmpeg)    │  │ (Whisper)    │  │ (NLP)        │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│         │                  │                  │         │
│         └──────────────────┴──────────────────┘         │
│                          │                               │
│                          ▼                               │
│              ┌───────────────────────┐                   │
│              │  Risk Calculation     │                   │
│              │  & Scoring Engine    │                   │
│              └───────────────────────┘                   │
└─────────────────────────────────────────────────────────┘
```

### Technology Stack

- **Backend Framework**: Flask 3.0.3
- **Speech Recognition**: Faster Whisper 1.0.3
- **Audio Processing**: FFmpeg, pydub
- **NLP**: Custom threat detection algorithms
- **Translation**: Transformers (MarianMT), deep-translator
- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **Logging**: Loguru

### Data Flow

1. **Upload**: User uploads audio file via web interface
2. **Conversion**: Audio converted to MP3 format (if needed)
3. **Transcription**: Audio transcribed to text using Whisper
4. **Analysis**: Text analyzed for threats, codewords, and slang
5. **Scoring**: Risk scores calculated based on detected threats
6. **Display**: Results displayed in web dashboard
7. **Export**: Results can be exported as JSON reports

---

## Installation Guide

### Prerequisites

- **Python**: 3.8 or higher (tested with Python 3.13)
- **FFmpeg**: Required for audio processing
- **Operating System**: Windows, Linux, or macOS

### Step 1: Install Python Dependencies

Navigate to the project directory and install required packages:

```bash
cd "C:\Users\Chinmai Pore\OneDrive\Documents\audio-threat-detection"
pip install -r requirements.txt
```

**Required Packages:**
- `faster-whisper==1.0.3` - Speech recognition
- `pydub==0.25.1` - Audio manipulation
- `loguru==0.7.2` - Logging
- `deep-translator==1.11.4` - Translation
- `transformers==4.45.2` - ML models
- `Flask==3.0.3` - Web framework
- `flask-cors==4.0.1` - CORS support

**Note for NumPy**: Install based on your Python version:
- Python < 3.12: `pip install numpy==1.26.4`
- Python >= 3.12: `pip install "numpy>=2.1.0,<2.3"`

### Step 2: Install FFmpeg

**Windows:**
```powershell
# Option 1: Using Chocolatey
choco install ffmpeg

# Option 2: Using winget
winget install FFmpeg

# Option 3: Manual installation
# Download from https://ffmpeg.org/download.html
# Extract and add to PATH
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Verify Installation:**
```bash
ffmpeg -version
ffprobe -version
```

### Step 3: Verify Installation

```bash
# Check Python version
python --version

# Verify packages
pip list | findstr "whisper flask transformers"

# Test FFmpeg
ffmpeg -version
```

---

## Usage Instructions

### Starting the Application

1. **Navigate to the project directory:**
   ```bash
   cd "C:\Users\Chinmai Pore\OneDrive\Documents\audio-threat-detection"
   ```

2. **Start the Flask server:**
   ```bash
   python app.py
   ```

3. **Access the web interface:**
   - Open your browser
   - Navigate to: `http://localhost:5000`

### Using the Web Interface

#### Upload Audio File

1. **Method 1: Drag & Drop**
   - Drag an audio file onto the upload area
   - File will be automatically selected

2. **Method 2: Browse**
   - Click "Select File" button
   - Choose audio file from file dialog

3. **Method 3: File Path**
   - Enter full file path in the text field
   - Example: `C:\Users\Documents\audio.mp3`

#### Configure Analysis Options

1. **Translation** (Optional):
   - Select target language from dropdown
   - Choose "No Translation" to skip translation
   - English option available (uses original text)

2. **Analysis Features**:
   - Threat Detection: Always enabled
   - Code Word Detection: Always enabled
   - Slang Translation: Always enabled
   - Request Human Feedback: Optional

#### Start Analysis

1. Click **"Start Analysis"** button
2. Monitor progress in the progress bar
3. Wait for analysis to complete (may take several minutes for long audio)
4. View results in the "Analysis Results" tab

#### View Results

Results are organized into tabs:

1. **Transcription**: Full text transcription
2. **Threats**: Detected threat keywords grouped by category
3. **Code Words**: Detected codewords with hidden meanings
4. **Slang**: Detected slang terms with translations

#### Export Results

- Click **"Export Full Report"** button
- Report saved as JSON file in `reports/` directory
- Includes all analysis data and metadata

---

## Threat Detection System

### Threat Categories

#### 1. Violence & Attack (10 keywords)
- **Keywords**: kill, murder, attack, assault, shoot, stab, execute, assassinate, massacre, slaughter
- **Risk Scores**: 8-10 per keyword
- **Purpose**: Detect direct threats of violence

#### 2. Weapons (11 keywords)
- **Keywords**: bomb, explosive, gun, weapon, rifle, pistol, grenade, missile, detonator, ammunition, firearm
- **Risk Scores**: 7-9 per keyword
- **Purpose**: Identify weapon-related threats

#### 3. Terrorism (8 keywords)
- **Keywords**: terror, terrorist, extremist, radical, jihad, martyr, insurgent, militant
- **Risk Scores**: 6-9 per keyword
- **Purpose**: Detect terrorism-related language

#### 4. Hostility (6 keywords)
- **Keywords**: hostage, kidnap, ransom, threaten, threat, intimidate
- **Risk Scores**: 6-9 per keyword
- **Purpose**: Identify hostile intentions

#### 5. Destruction (5 keywords)
- **Keywords**: destroy, sabotage, demolish, explosion, blast
- **Risk Scores**: 7-8 per keyword
- **Purpose**: Detect destruction-related threats

#### 6. Chemical/Biological (5 keywords)
- **Keywords**: poison, toxic, chemical, biological, radiation
- **Risk Scores**: 7-9 per keyword
- **Purpose**: Identify chemical/biological threats

#### 7. Planning/Intent (4 keywords)
- **Keywords**: plot, conspire, ambush, infiltrate
- **Risk Scores**: 6-8 per keyword
- **Purpose**: Detect planning activities

### Detection Process

1. **Text Normalization**: Convert text to lowercase, remove punctuation
2. **Word Matching**: Match cleaned words against threat keyword database
3. **Context Extraction**: Capture 5 words before and after each match
4. **Occurrence Counting**: Count how many times each keyword appears
5. **Risk Calculation**: Multiply risk_score × occurrences for each keyword
6. **Categorization**: Group threats by category for reporting

### Custom Keywords

Users can add custom threat keywords via the web interface:

1. Click **"Manage Keywords"** button
2. Select **"Threat Keywords"** tab
3. Fill in keyword details:
   - Keyword: The word/phrase to detect
   - Meaning: Description of the threat
   - Risk Score: 1-10 (higher = more dangerous)
   - Category: violence, weapon, terrorism, etc.
4. Click **"Add Keyword"**

Custom keywords are saved to `custom_threat_keywords.json` and loaded automatically.

---

## Scoring Methodology

### Risk Score Calculation

The system calculates risk scores using the following formula:

```
Total Risk Score = Keyword Risk + Codeword Risk

Where:
- Keyword Risk = Σ(risk_score × occurrences) for all threat keywords
- Codeword Risk = Σ(risk_score × occurrences) for all codewords
```

### Risk Level Classification

| Risk Level | Score Range | Description |
|------------|-------------|-------------|
| **SAFE** | 0 | No threats detected |
| **LOW** | 1-19 | Minimal threat indicators |
| **MEDIUM** | 20-49 | Moderate threat level |
| **HIGH** | 50-99 | Significant threat detected |
| **CRITICAL** | 100+ | Severe threat requiring immediate attention |

### Example Calculation

**Scenario**: Audio contains:
- "kill" (risk_score: 10) appears 2 times = 20 points
- "bomb" (risk_score: 9) appears 1 time = 9 points
- "attack" (risk_score: 8) appears 3 times = 24 points
- Codeword "pop the balloon" (risk_score: 10) appears 1 time = 10 points

**Total Risk Score**: 20 + 9 + 24 + 10 = **63 points**
**Risk Level**: **HIGH** (50-99 range)

### Scoring Factors

1. **Keyword Severity**: Higher risk_score keywords contribute more
2. **Frequency**: Multiple occurrences increase total risk
3. **Context**: Context helps determine if threat is serious
4. **Codewords**: Hidden threats add to overall risk

---

## API Documentation

### REST API Endpoints

#### Health Check
```
GET /api/health
```
**Response:**
```json
{
  "status": "ok",
  "analysis_module": true,
  "timestamp": "2025-11-06T22:55:00"
}
```

#### Upload Audio File
```
POST /api/upload
Content-Type: multipart/form-data

Body: audio file
```
**Response:**
```json
{
  "success": true,
  "filename": "20251106_225538_audio.mp3",
  "filepath": "uploads/20251106_225538_audio.mp3",
  "size": 1024000
}
```

#### Start Analysis
```
POST /api/analyze
Content-Type: application/json

Body:
{
  "filepath": "uploads/audio.mp3",
  "translation": "es",
  "request_feedback": false
}
```
**Response:**
```json
{
  "success": true,
  "analysis_id": "20251106_225539_121073",
  "message": "Analysis started"
}
```

#### Get Progress
```
GET /api/progress/<analysis_id>
```
**Response:**
```json
{
  "status": "processing",
  "progress": 50,
  "stage": "Transcription complete, analyzing threats..."
}
```

#### Get Results
```
GET /api/results/<analysis_id>
```
**Response:**
```json
{
  "transcription": "Full transcribed text...",
  "translation": "Translated text (if requested)...",
  "speakers": [],
  "slang": {},
  "codewords": {},
  "threats": {
    "threats": {...},
    "total_risk": 63,
    "risk_level": "HIGH",
    "categories": {...}
  },
  "risk_score": 63,
  "risk_level": "HIGH",
  "keyword_risk": 53,
  "codeword_risk": 10
}
```

#### Get Keywords
```
GET /api/keywords
```
**Response:**
```json
{
  "keywords": {...},
  "codewords": {...},
  "slang": {...},
  "counts": {
    "keywords": 50,
    "codewords": 2,
    "slang": 2
  }
}
```

#### Add Keyword
```
POST /api/keywords/add
Content-Type: application/json

Body:
{
  "type": "keyword",
  "word": "threat",
  "meaning": "Potential danger",
  "risk_score": 7,
  "category": "hostility"
}
```

#### Delete Keyword
```
POST /api/keywords/delete
Content-Type: application/json

Body:
{
  "type": "keyword",
  "keyword": "threat"
}
```

#### Get History
```
GET /api/history
```
**Response:**
```json
{
  "success": true,
  "reports": [
    {
      "filename": "report_20251106_184724.json",
      "created": "2025-11-06T18:47:24",
      "size": 10240
    }
  ],
  "count": 1
}
```

#### Download Report
```
GET /api/report/<filename>
```
**Response:** JSON file download

---

## File Structure

```
audio-threat-detection/
├── app.py                          # Flask web application
├── threat_analysis_module.py       # Bridge module for app package
├── requirements.txt                # Python dependencies
├── uploads/                        # Uploaded audio files
├── reports/                        # Analysis reports (JSON)
├── templates/
│   └── dashboard.html              # Web dashboard HTML
├── static/
│   └── dashboard.js               # Frontend JavaScript
└── ...

app/
├── __init__.py                     # Package initialization
├── pipeline.py                     # Main analysis pipeline
├── transcription.py                # Speech recognition module
├── threat_analysis.py              # Threat detection engine
├── audio_utils.py                  # Audio processing utilities
├── diarization.py                  # Speaker diarization (disabled)
└── PROJECT_DOCUMENTATION.md       # This file
```

### Key Files Explained

- **`app.py`**: Flask web server, handles HTTP requests, manages analysis jobs
- **`pipeline.py`**: Core analysis logic, orchestrates transcription and threat detection
- **`threat_analysis.py`**: Threat keyword database and detection algorithms
- **`transcription.py`**: Whisper model wrapper for speech-to-text
- **`audio_utils.py`**: FFmpeg integration for audio conversion
- **`dashboard.html`**: Web interface markup
- **`dashboard.js`**: Frontend logic and API communication

---

## Configuration

### Environment Variables

#### HuggingFace Token (Optional)
```powershell
# For future speaker diarization features
$env:HF_TOKEN="your_huggingface_token_here"
```

#### Flask Port (Optional)
```powershell
# Change default port from 5000
$env:FLASK_PORT=8080
```

### Configuration Files

#### Custom Keywords
- **File**: `custom_threat_keywords.json`
- **Format**: JSON dictionary
- **Example**:
```json
{
  "custom_threat": {
    "meaning": "Custom threat description",
    "risk_score": 8,
    "category": "violence"
  }
}
```

#### Codewords Database
- **File**: `codewords_database.json`
- **Format**: JSON dictionary
- **Example**:
```json
{
  "pop the balloon": {
    "real_meaning": "Execute target",
    "risk_score": 10,
    "category": "codeword"
  }
}
```

#### Slang Dictionary
- **File**: `slang_dictionary.json`
- **Format**: JSON dictionary
- **Example**:
```json
{
  "strapped": "armed with weapon",
  "heat": "gun/firearm"
}
```

### Model Configuration

#### Whisper Model Size
Edit `pipeline.py`:
```python
transcriber = Transcriber(model_size="base")  # Options: tiny, base, small, medium, large
```

#### Device Selection
Edit `pipeline.py`:
```python
transcriber = Transcriber(model_size="base", device="cpu")  # Options: cpu, cuda, auto
```

---

## Troubleshooting

### Common Issues

#### 1. FFmpeg Not Found
**Error**: `ffmpeg not found. Please install ffmpeg and ensure it is on PATH.`

**Solution**:
- Install FFmpeg (see Installation Guide)
- Add FFmpeg to system PATH
- Verify: `ffmpeg -version`

#### 2. CUDA/cuDNN Errors
**Error**: `Could not locate cudnn_ops64_9.dll`

**Solution**:
- System automatically falls back to CPU
- No action needed - CPU mode works reliably
- For GPU acceleration, install proper CUDA toolkit and cuDNN

#### 3. Module Import Errors
**Error**: `ModuleNotFoundError: No module named 'app'`

**Solution**:
- Ensure you're running from `audio-threat-detection` directory
- Check that `app` package is in parent directory
- Verify Python path includes parent directory

#### 4. Analysis Module Unavailable
**Error**: `Analysis module not available`

**Solution**:
- Check that `threat_analysis_module.py` exists
- Verify `app` package is accessible
- Check import errors in console output

#### 5. Transcription Hangs
**Error**: Progress stuck at 20-30%

**Solution**:
- Transcription takes time for long audio files
- Check console for actual progress
- Ensure CPU has sufficient resources
- Try smaller audio files first

#### 6. Port Already in Use
**Error**: `Address already in use`

**Solution**:
```bash
# Windows: Find and kill process using port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or change port in app.py
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Performance Optimization

#### For Faster Transcription
1. Use smaller Whisper model: `model_size="tiny"` or `"base"`
2. Split long audio files into shorter segments
3. Use GPU if available (requires CUDA setup)

#### For Better Accuracy
1. Use larger Whisper model: `model_size="medium"` or `"large"`
2. Ensure good audio quality (clear speech, minimal noise)
3. Use appropriate sample rate (16kHz recommended)

---

## Development Guide

### Adding New Threat Keywords

1. **Edit `threat_analysis.py`**:
```python
THREAT_KEYWORDS: Dict[str, Dict[str, Any]] = {
    # ... existing keywords ...
    "new_threat": {
        "meaning": "Description of threat",
        "risk_score": 8,
        "category": "violence"  # or weapon, terrorism, etc.
    },
}
```

2. **Or use Web Interface**:
   - Go to "Manage Keywords" → "Threat Keywords"
   - Add keyword via form

### Adding New Categories

1. **Update `threat_analysis.py`**:
   - Add keywords with new category name
   - Category will be automatically detected

2. **Update UI** (optional):
   - Modify `dashboard.js` to handle new category display

### Extending Translation Support

1. **Edit `threat_analysis_module.py`**:
```python
SUPPORTED_LANGUAGES: Dict[str, Tuple[str, str]] = {
    # ... existing languages ...
    "11": ("New Language", "en-xx"),  # Replace xx with language code
}
```

2. **Update `dashboard.html`**:
   - Add option to translation dropdown

### Customizing Risk Scoring

Edit `pipeline.py`:
```python
# Modify risk level thresholds
if total_risk == 0:
    risk_level = "SAFE"
elif total_risk < 30:  # Changed from 20
    risk_level = "LOW"
# ... etc.
```

### Adding New Analysis Features

1. **Create analysis function** in `threat_analysis.py` or new module
2. **Call from `pipeline.py`** in `comprehensive_analysis()`
3. **Add to return dictionary**
4. **Update UI** to display results

---

## Security Considerations

### Data Privacy
- Audio files are stored locally in `uploads/` directory
- Transcripts and analysis results stored in `reports/` directory
- No data is sent to external services (except translation APIs)
- Consider implementing file cleanup policies

### Access Control
- Currently no authentication required
- Consider adding authentication for production use
- Restrict file upload sizes (currently 500MB max)

### Threat Detection Limitations
- Keyword-based detection may produce false positives
- Context is important - review results carefully
- Not a substitute for human analysis
- Use as a screening tool, not final decision maker

---

## Future Enhancements

### Planned Features
1. **Speaker Diarization**: Re-enable with proper CUDA setup
2. **Emotion Analysis**: AI-powered emotion detection
3. **Sentiment Analysis**: Advanced sentiment scoring
4. **Sarcasm Detection**: Identify non-literal threats
5. **Real-time Analysis**: Stream audio processing
6. **Batch Processing**: Analyze multiple files
7. **User Authentication**: Secure access control
8. **Database Integration**: Store results in database
9. **API Rate Limiting**: Prevent abuse
10. **Advanced Reporting**: PDF reports, charts, graphs

### Contributing
- Follow PEP 8 style guide
- Add docstrings to functions
- Test changes thoroughly
- Update documentation

---

## License & Credits

### Technologies Used
- **Faster Whisper**: OpenAI Whisper implementation
- **Flask**: Web framework
- **FFmpeg**: Audio processing
- **Transformers**: Hugging Face transformers library
- **Tailwind CSS**: UI styling

### Acknowledgments
- OpenAI for Whisper model
- Hugging Face for model hosting
- FFmpeg team for audio tools

---

## Support & Contact

For issues, questions, or contributions:
1. Check Troubleshooting section
2. Review error messages in console
3. Check log files for detailed errors
4. Verify all dependencies are installed

---

## Version History

### Version 1.0 (Current)
- Initial release
- Basic threat detection
- Web dashboard
- Multi-language support
- Comprehensive keyword database

---

**Last Updated**: November 6, 2025
**Version**: 1.0
**Status**: Production Ready

