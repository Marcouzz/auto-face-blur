
# Auto Face Blur

**Auto Face Blur** is a simple and secure web tool that processes uploaded videos to automatically blur faces and remove all metadata (such as device, time, and location). After processing, the video is ready for safe download and sharing.

## Features
- Automatic face detection and blurring in videos
- Removal of all video metadata
- Simple web interface for upload, status checking, and download
- Supports common video formats

## Requirements
- Python 3.10 or higher
- [ffmpeg](https://ffmpeg.org/) installed and available in your system PATH

## Installation & Setup

### 1. Clone the project
```bash
git clone https://github.com/Marcouzz/auto-face-blur.git
cd auto-face-blur
````

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

* **Windows (cmd):**

```bash
venv\Scripts\activate
```

* **Windows (PowerShell):**

```bash
venv\Scripts\Activate.ps1
```

* **Linux / Mac:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the web server

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Open your browser at `http://localhost:8000`.

## Usage

1. Open the main page in your browser
2. Upload your video
3. Check the processing status
4. Download the anonymized video once processing is complete

## Project Structure

* `app.py` → Main FastAPI application
* `processor.py` → Video processing and face blurring logic
* `static/` → HTML, CSS, and frontend assets
* `tmp/` → Temporary folder for storing videos during processing

## Notes

* Make sure **ffmpeg** is installed and accessible in PATH
* Temporary files in `tmp/` are removed after processing
* Suitable for local testing or small servers; use a queue or database for multiple simultaneous tasks in production
