import json
import os
import re
from datetime import datetime
from typing import Dict, Any, Tuple

from loguru import logger


CUSTOM_KEYWORDS_FILE = "custom_threat_keywords.json"
CODEWORDS_FILE = "codewords_database.json"
SLANG_FILE = "slang_dictionary.json"
FEEDBACK_FILE = "keyword_feedback.json"


DEFAULT_CODEWORDS: Dict[str, Dict[str, Any]] = {
    "pop the balloon": {"real_meaning": "Execute target", "risk_score": 10, "category": "codeword"},
    "cut the cake": {"real_meaning": "Start operation", "risk_score": 8, "category": "codeword"},
}

DEFAULT_SLANG: Dict[str, str] = {
    "strapped": "armed with weapon",
    "heat": "gun/firearm",
}

THREAT_KEYWORDS: Dict[str, Dict[str, Any]] = {
    # Violence & Attack
    "kill": {"meaning": "Cause death", "risk_score": 10, "category": "violence"},
    "murder": {"meaning": "Unlawful killing", "risk_score": 10, "category": "violence"},
    "attack": {"meaning": "Violent act", "risk_score": 8, "category": "violence"},
    "assault": {"meaning": "Physical attack", "risk_score": 8, "category": "violence"},
    "shoot": {"meaning": "Fire weapon", "risk_score": 8, "category": "violence"},
    "stab": {"meaning": "Pierce with weapon", "risk_score": 9, "category": "violence"},
    "execute": {"meaning": "Carry out killing", "risk_score": 9, "category": "violence"},
    "assassinate": {"meaning": "Targeted killing", "risk_score": 10, "category": "violence"},
    "massacre": {"meaning": "Mass killing", "risk_score": 10, "category": "violence"},
    "slaughter": {"meaning": "Brutal killing", "risk_score": 9, "category": "violence"},
    
    # Weapons
    "bomb": {"meaning": "Explosive device", "risk_score": 9, "category": "weapon"},
    "explosive": {"meaning": "Blast material", "risk_score": 9, "category": "weapon"},
    "gun": {"meaning": "Firearm", "risk_score": 8, "category": "weapon"},
    "weapon": {"meaning": "Tool for harm", "risk_score": 7, "category": "weapon"},
    "rifle": {"meaning": "Long gun", "risk_score": 8, "category": "weapon"},
    "pistol": {"meaning": "Handgun", "risk_score": 8, "category": "weapon"},
    "grenade": {"meaning": "Hand explosive", "risk_score": 9, "category": "weapon"},
    "missile": {"meaning": "Projectile weapon", "risk_score": 9, "category": "weapon"},
    "detonator": {"meaning": "Trigger device", "risk_score": 9, "category": "weapon"},
    "ammunition": {"meaning": "Weapon supply", "risk_score": 7, "category": "weapon"},
    "firearm": {"meaning": "Gun weapon", "risk_score": 8, "category": "weapon"},
    
    # Terrorism
    "terror": {"meaning": "Acts causing fear", "risk_score": 9, "category": "terrorism"},
    "terrorist": {"meaning": "Violence actor", "risk_score": 9, "category": "terrorism"},
    "extremist": {"meaning": "Radical actor", "risk_score": 7, "category": "terrorism"},
    "radical": {"meaning": "Extreme ideology", "risk_score": 6, "category": "terrorism"},
    "jihad": {"meaning": "Holy war", "risk_score": 8, "category": "terrorism"},
    "martyr": {"meaning": "Death for cause", "risk_score": 8, "category": "terrorism"},
    "insurgent": {"meaning": "Rebel fighter", "risk_score": 7, "category": "terrorism"},
    "militant": {"meaning": "Armed fighter", "risk_score": 7, "category": "terrorism"},
    
    # Hostility
    "hostage": {"meaning": "Captive person", "risk_score": 8, "category": "hostility"},
    "kidnap": {"meaning": "Abduction", "risk_score": 9, "category": "hostility"},
    "ransom": {"meaning": "Payment for release", "risk_score": 7, "category": "hostility"},
    "threaten": {"meaning": "Express intent to harm", "risk_score": 7, "category": "hostility"},
    "threat": {"meaning": "Potential danger", "risk_score": 7, "category": "hostility"},
    "intimidate": {"meaning": "Cause fear", "risk_score": 6, "category": "hostility"},
    
    # Destruction
    "destroy": {"meaning": "Ruin completely", "risk_score": 7, "category": "destruction"},
    "sabotage": {"meaning": "Deliberate damage", "risk_score": 7, "category": "destruction"},
    "demolish": {"meaning": "Tear down", "risk_score": 7, "category": "destruction"},
    "explosion": {"meaning": "Destructive burst", "risk_score": 8, "category": "destruction"},
    "blast": {"meaning": "Explosive force", "risk_score": 8, "category": "destruction"},
    
    # Chemical/Biological
    "poison": {"meaning": "Toxic substance", "risk_score": 8, "category": "chemical"},
    "toxic": {"meaning": "Harmful substance", "risk_score": 7, "category": "chemical"},
    "chemical": {"meaning": "Hazardous agent", "risk_score": 8, "category": "chemical"},
    "biological": {"meaning": "Disease agent", "risk_score": 9, "category": "chemical"},
    "radiation": {"meaning": "Nuclear exposure", "risk_score": 9, "category": "chemical"},
    
    # Planning/Intent
    "plot": {"meaning": "Secret plan", "risk_score": 6, "category": "planning"},
    "conspire": {"meaning": "Plan together", "risk_score": 6, "category": "planning"},
    "ambush": {"meaning": "Surprise attack", "risk_score": 8, "category": "planning"},
    "infiltrate": {"meaning": "Secret entry", "risk_score": 6, "category": "planning"},
}


def _read_json(path: str, fallback):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return fallback
    return fallback


def _write_json(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_custom_keywords() -> Dict[str, Dict[str, Any]]:
    custom = _read_json(CUSTOM_KEYWORDS_FILE, {})
    THREAT_KEYWORDS.update(custom)
    return _read_json(CODEWORDS_FILE, DEFAULT_CODEWORDS)


def load_slang_dictionary() -> Dict[str, str]:
    return _read_json(SLANG_FILE, DEFAULT_SLANG)


def load_feedback() -> Dict[str, Any]:
    return _read_json(FEEDBACK_FILE, {"approved": [], "rejected": [], "modified": []})


def save_feedback(feedback: Dict[str, Any]) -> None:
    _write_json(FEEDBACK_FILE, feedback)


def record_feedback(entry: Dict[str, Any]) -> None:
    fb = load_feedback()
    fb.setdefault("events", []).append({**entry, "timestamp": datetime.now().isoformat()})
    save_feedback(fb)


def detect_slang(text: str, slang_dict: Dict[str, str]) -> Dict[str, Any]:
    text_lower = text.lower()
    found = {}
    for slang, meaning in slang_dict.items():
        pattern = r"\b" + re.escape(slang) + r"\b"
        matches = list(re.finditer(pattern, text_lower))
        if matches:
            contexts = []
            words = text.split()
            for m in matches:
                char_pos = m.start()
                word_idx = len(text[:char_pos].split())
                start = max(0, word_idx - 5)
                end = min(len(words), word_idx + 6)
                contexts.append(" ".join(words[start:end]))
            found[slang] = {"meaning": meaning, "occurrences": len(matches), "contexts": contexts}
    return found


def detect_codewords(text: str, codewords: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    text_lower = text.lower()
    found = {}
    for phrase, info in codewords.items():
        if phrase in text_lower:
            idx = 0
            contexts = []
            while True:
                idx = text_lower.find(phrase, idx)
                if idx == -1:
                    break
                words = text.split()
                char_to_word = 0
                word_idx = 0
                for i, w in enumerate(words):
                    char_to_word += len(w) + 1
                    if char_to_word > idx:
                        word_idx = i
                        break
                start = max(0, word_idx - 5)
                end = min(len(words), word_idx + 10)
                contexts.append(" ".join(words[start:end]))
                idx += len(phrase)
            if contexts:
                found[phrase] = {**info, "occurrences": len(contexts), "contexts": contexts}
    return found


def detect_threats(text: str) -> Dict[str, Any]:
    """Detect threat keywords and calculate risk scores with proper categorization."""
    words = text.lower().split()
    found = {}
    
    for i, w in enumerate(words):
        cleaned = re.sub(r"[^\w\s]", "", w).lower()
        if cleaned in THREAT_KEYWORDS:
            entry = found.setdefault(
                cleaned,
                {**THREAT_KEYWORDS[cleaned], "occurrences": 0, "contexts": []},
            )
            entry["occurrences"] += 1
            start = max(0, i - 5)
            end = min(len(words), i + 6)
            entry["contexts"].append(" ".join(words[start:end]))
    
    # Calculate total risk
    total_risk = sum(v["risk_score"] * v["occurrences"] for v in found.values())
    
    # Group by category
    categories = {}
    for word, info in found.items():
        cat = info["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((word, info))
    
    # Determine risk level
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
        "threats": found,
        "total_risk": total_risk,
        "risk_level": risk_level,
        "categories": categories,
    }


