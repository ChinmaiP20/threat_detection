from typing import List, Dict, Any, Optional

from faster_whisper import WhisperModel
from loguru import logger
from deep_translator import GoogleTranslator


class Transcriber:
    def __init__(self, model_size: str = "base", device: str = "auto") -> None:
        # Check if CUDA is available and working, otherwise force CPU
        actual_device = self._get_safe_device(device)
        logger.info(f"Initializing WhisperModel with device: {actual_device} (requested: {device})")
        self.model = WhisperModel(model_size, device=actual_device)
    
    def _get_safe_device(self, requested_device: str) -> str:
        """Determine safe device to use, falling back to CPU if CUDA has issues."""
        if requested_device == "cpu":
            return "cpu"
        
        # Try to detect CUDA availability
        try:
            import torch
            if torch.cuda.is_available():
                # Try to create a simple tensor to test if CUDA actually works
                try:
                    test_tensor = torch.zeros(1).cuda()
                    del test_tensor
                    torch.cuda.empty_cache()
                    logger.info("CUDA is available and working")
                    return requested_device if requested_device != "auto" else "cuda"
                except Exception as e:
                    logger.warning(f"CUDA is available but not working properly: {e}. Falling back to CPU.")
                    return "cpu"
            else:
                logger.info("CUDA is not available, using CPU")
                return "cpu"
        except ImportError:
            logger.info("PyTorch not available, using CPU")
            return "cpu"
        except Exception as e:
            logger.warning(f"Error checking CUDA: {e}. Falling back to CPU.")
            return "cpu"

    def _translate(self, text: str, source: Optional[str], target: str) -> str:
        try:
            translator = GoogleTranslator(source=source or "auto", target=target)
            return translator.translate(text)
        except Exception:
            return text

    def transcribe(self, audio_path: str, translate_to: Optional[str] = None) -> Dict[str, Any]:
        segments_info: List[Dict[str, Any]] = []
        logger.info(f"Transcribing {audio_path}")
        segments, info = self.model.transcribe(audio_path, vad_filter=True)
        for seg in segments:
            segments_info.append(
                {
                    "start": float(seg.start),
                    "end": float(seg.end),
                    "text": seg.text.strip(),
                }
            )

        full_text = " ".join(s["text"] for s in segments_info).strip()
        result: Dict[str, Any] = {
            "language": info.language,
            "duration": float(info.duration),
            "segments": segments_info,
            "text": full_text,
        }

        if translate_to:
            translated_segments: List[Dict[str, Any]] = []
            for s in segments_info:
                translated_text = self._translate(s["text"], source=info.language, target=translate_to)
                translated_segments.append({**s, "translated_text": translated_text})
            result["segments"] = translated_segments
            result["translated_text"] = self._translate(full_text, source=info.language, target=translate_to)
            result["target_language"] = translate_to

        return result


