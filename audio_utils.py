import os
import subprocess
import tempfile
from pathlib import Path
from typing import Tuple

from loguru import logger


def ensure_mp3(input_path: str | os.PathLike[str]) -> Tuple[str, bool]:
    """
    Ensure the audio file is converted to MP3 (CBR 128k, 16kHz mono).

    Returns (mp3_path, created_new_file)
    """
    input_path = str(input_path)
    ext = Path(input_path).suffix.lower()
    if ext == ".mp3":
        return input_path, False

    tmp_dir = tempfile.mkdtemp(prefix="audio_convert_")
    output_path = str(Path(tmp_dir) / (Path(input_path).stem + ".mp3"))

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-ac",
        "1",
        "-ar",
        "16000",
        "-b:a",
        "128k",
        output_path,
    ]

    try:
        logger.debug(f"Running ffmpeg: {' '.join(cmd)}")
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError as e:
        raise RuntimeError(
            "ffmpeg not found. Please install ffmpeg and ensure it is on PATH."
        ) from e
    except subprocess.CalledProcessError as e:
        logger.error(e.stderr.decode(errors="ignore"))
        raise RuntimeError("ffmpeg conversion failed") from e

    return output_path, True


def get_duration_seconds(audio_path: str | os.PathLike[str]) -> float:
    """Return duration in seconds using ffprobe."""
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(audio_path),
    ]
    try:
        out = subprocess.check_output(cmd)
        return float(out.decode().strip())
    except Exception:
        return 0.0


