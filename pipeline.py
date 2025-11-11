import os
from typing import Any, Dict, Optional, Tuple

from loguru import logger

from .audio_utils import ensure_mp3
from .threat_analysis import (
    detect_codewords,
    detect_slang,
    detect_threats,
    load_custom_keywords,
    load_slang_dictionary,
)
from .transcription import Transcriber


def translate_with_marian(text: str, lang_code: str) -> Optional[str]:
    try:
        from transformers import MarianMTModel, MarianTokenizer

        model_name = f"Helsinki-NLP/opus-mt-{lang_code}"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        max_len = 500
        sentences = text.split(".")
        chunks = []
        current = ""
        for s in sentences:
            if len(current) + len(s) < max_len:
                current += s + "."
            else:
                if current:
                    inputs = tokenizer(current, return_tensors="pt", padding=True)
                    translated = model.generate(**inputs)
                    chunks.append(tokenizer.decode(translated[0], skip_special_tokens=True))
                current = s + "."
        if current:
            inputs = tokenizer(current, return_tensors="pt", padding=True)
            translated = model.generate(**inputs)
            chunks.append(tokenizer.decode(translated[0], skip_special_tokens=True))
        return " ".join(chunks)
    except Exception as e:
        logger.warning(f"Translation failed: {e}")
        return None


def comprehensive_analysis(
    audio_path: str,
    hf_token: Optional[str] = None,
    translate_to: Optional[Tuple[str, str]] = None,
) -> Dict[str, Any]:
    logger.info(f"Analyzing: {audio_path}")
    mp3_path, _ = ensure_mp3(audio_path)

    # Diarization removed - set empty speakers list
    speakers = []

    # Use CPU to avoid CUDA/cuDNN issues
    # If you have working CUDA, you can change this to "auto" or "cuda"
    transcriber = Transcriber(model_size="base", device="cpu")
    transcript = transcriber.transcribe(mp3_path)
    text = transcript.get("text", "")

    translated_text = None
    if translate_to:
        _, lang_code = translate_to
        # Skip translation if language code is just "en" (English)
        if lang_code != "en":
            translated_text = translate_with_marian(text, lang_code)
        else:
            # If English is selected, just use the original text
            translated_text = text

    slang_dict = load_slang_dictionary()
    codewords_dict = load_custom_keywords()

    slang_found = detect_slang(text, slang_dict)
    codewords_found = detect_codewords(text, codewords_dict)
    threats = detect_threats(text)

    # Calculate risk scores properly
    keyword_risk = threats["total_risk"]
    codeword_risk = sum(c["risk_score"] * c["occurrences"] for c in codewords_found.values())
    total_risk = keyword_risk + codeword_risk

    # Use risk level from threats detection (which already includes proper categorization)
    # But adjust if codewords add significant risk
    base_risk_level = threats.get("risk_level", "SAFE")
    
    # Determine final risk level based on total risk
    if total_risk == 0:
        risk_level = "SAFE"
    elif total_risk < 20:
        risk_level = "LOW"
    elif total_risk < 50:
        risk_level = "MEDIUM"
    elif total_risk < 100:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"

    return {
        "transcription": text,
        "translation": translated_text,
        "speakers": speakers,
        "slang": slang_found,
        "codewords": codewords_found,
        "threats": threats,
        "risk_score": total_risk,
        "risk_level": risk_level,
        "keyword_risk": keyword_risk,
        "codeword_risk": codeword_risk,
    }


