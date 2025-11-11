from typing import List, Dict, Any

from loguru import logger


def perform_diarization(audio_path: str, hf_token: str | None) -> List[Dict[str, Any]]:
    """Optional diarization using pyannote. Returns empty list if unavailable."""
    if not hf_token:
        logger.warning("HF token not provided; skipping diarization")
        return []
    try:
        from pyannote.audio import Pipeline as DiarizationPipeline  # lazy import
        import torch

        pipeline = DiarizationPipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1", use_auth_token=hf_token
        )
        if torch.cuda.is_available():
            pipeline.to(torch.device("cuda"))
        diarization = pipeline(audio_path)
        segments: List[Dict[str, Any]] = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            segments.append(
                {
                    "speaker": speaker,
                    "start": float(turn.start),
                    "end": float(turn.end),
                    "duration": float(turn.end - turn.start),
                }
            )
        return segments
    except Exception as e:
        logger.warning(f"Diarization unavailable: {e}")
        return []


