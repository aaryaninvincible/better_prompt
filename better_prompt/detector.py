"""
Detector and analyzer for multi-language user requirements.
Analyzes intent, domain, language, and implicit constraints.
"""

import re
import unicodedata
from typing import Dict, Any, List

# Unicode script ranges for multi-language detection
SCRIPT_RANGES = {
    "hi": ("DEVANAGARI", "Hindi"),
    "zh": ("CJK UNIFIED IDEOGRAPH", "Chinese"),
    "ja": ("HIRAGANA", "Japanese"),
    "ko": ("HANGUL", "Korean"),
    "ar": ("ARABIC", "Arabic"),
    "ru": ("CYRILLIC", "Russian"),
}

# Domain keyword markers across multiple languages
DOMAIN_KEYWORDS = {
    "coding": [
        "code", "app", "function", "api", "database", "python", "javascript", "react", "vue", "angular",
        "svelte", "pinia", "redux", "next", "nuxt", "tailwind", "css", "html", "node", "express",
        "fastapi", "django", "flask", "docker", "kubernetes", "bug", "script", "backend", "frontend",
        "sql", "program", "class", "algorithm", "auth", "authentication", "jwt", "token", "service",
        "server", "endpoint", "microservice", "cart", "ecommerce", "e-commerce",
        "कोड", "ऐप", "प्रोग्राम", "फंक्शन", "código", "aplicación", "función", "programme"
    ],
    "creative": [
        "story", "poem", "essay", "article", "blog", "write", "creative", "fiction",
        "कहानी", "कविता", "लेख", "historia", "poema", "redactar", "écrire", "histoire"
    ],
    "business": [
        "marketing", "business", "plan", "pitch", "sales", "finance", "strategy", "proposal",
        "व्यापार", "रणनीति", "negocio", "estrategia", "ventas", "stratégie", "vente"
    ],
    "analysis": [
        "analyze", "data", "metrics", "chart", "insights", "evaluation", "compare",
        "विश्लेषण", "डेटा", "analizar", "datos", "analyser", "données"
    ],
    "education": [
        "explain", "teach", "learn", "concept", "guide", "tutorial", "summary",
        "समझाओ", "सीखो", "explicar", "enseñar", "tutoriel", "cours"
    ]
}

def detect_language(text: str) -> str:
    """
    Detect the primary language of the input text using script inspection and common stopwords.
    Returns language code: 'en', 'hi', 'es', 'fr', 'zh', 'ja', 'ru', 'ar', etc.
    """
    if not text or not text.strip():
        return "en"

    # Check non-Latin Unicode scripts first
    script_counts: Dict[str, int] = {}
    for char in text:
        if char.isalpha():
            name = unicodedata.name(char, "")
            for code, (script_prefix, _) in SCRIPT_RANGES.items():
                if script_prefix in name:
                    script_counts[code] = script_counts.get(code, 0) + 1

    if script_counts:
        best_script = max(script_counts.items(), key=lambda x: x[1])
        if best_script[1] > 2:
            return best_script[0]

    # Latin-based language stopword heuristics
    lower = text.lower()
    spanish_markers = [" para ", " como ", " hacer ", " crear ", " quiero ", " con ", " por qué "]
    french_markers = [" pour ", " comment ", " faire ", " créer ", " avec ", " pourquoi ", " dans "]
    german_markers = [" für ", " wie ", " machen ", " erstellen ", " mit ", " warum ", " nicht "]

    if any(m in lower for m in spanish_markers):
        return "es"
    if any(m in lower for m in french_markers):
        return "fr"
    if any(m in lower for m in german_markers):
        return "de"

    return "en"

def analyze_requirement(text: str) -> Dict[str, Any]:
    """
    Analyze the raw requirement string into structured intent dimensions.
    """
    text_clean = text.strip()
    lang = detect_language(text_clean)
    lower = text_clean.lower()

    # Determine domain
    matched_domains: List[str] = []
    for domain, kws in DOMAIN_KEYWORDS.items():
        if any(kw in lower for kw in kws):
            matched_domains.append(domain)

    primary_domain = matched_domains[0] if matched_domains else "general"

    # Complexity heuristic
    word_count = len(text_clean.split())
    if word_count < 6:
        complexity = "brief"
    elif word_count < 25:
        complexity = "moderate"
    else:
        complexity = "detailed"

    # Check for technical constraints
    has_constraints = any(token in lower for token in [
        "must", "never", "only", "without", "should not", "limit", "ना", "बिना", "sin", "sans"
    ])

    return {
        "raw": text_clean,
        "language": lang,
        "primary_domain": primary_domain,
        "domains": matched_domains,
        "complexity": complexity,
        "word_count": word_count,
        "has_constraints": has_constraints,
    }
