"""
Prompt engineering frameworks and localized headers for Better Prompt.
Supports ANY output language.
"""

from typing import Dict, Any, List

LOCALIZED_HEADERS: Dict[str, Dict[str, str]] = {
    "en": {
        "role": "Role & Persona",
        "context": "Context & Background",
        "objective": "Primary Objective",
        "workflow": "Step-by-Step Instructions",
        "constraints": "Constraints & Guardrails",
        "output_format": "Expected Output Format",
        "evaluation": "Quality & Verification Checklist",
    },
    "hi": {
        "role": "भूमिका और व्यक्तित्व (Role & Persona)",
        "context": "संदर्भ और पृष्ठभूमि (Context)",
        "objective": "मुख्य उद्देश्य (Objective)",
        "workflow": "चरणबद्ध निर्देश (Step-by-Step Instructions)",
        "constraints": "सीमाएं और नियम (Constraints)",
        "output_format": "अपेक्षित प्रारूप (Expected Output Format)",
        "evaluation": "गुणवत्ता जांच (Quality Checklist)",
    },
    "es": {
        "role": "Rol y Persona",
        "context": "Contexto y Antecedentes",
        "objective": "Objetivo Principal",
        "workflow": "Instrucciones Paso a Paso",
        "constraints": "Restricciones y Reglas",
        "output_format": "Formato de Salida Esperado",
        "evaluation": "Lista de Verificación de Calidad",
    },
    "fr": {
        "role": "Rôle et Persona",
        "context": "Contexte et Contexte",
        "objective": "Objectif Principal",
        "workflow": "Instructions Étape par Étape",
        "constraints": "Contraintes et Règles",
        "output_format": "Format de Sortie Attendu",
        "evaluation": "Liste de Contrôle de Qualité",
    },
    "de": {
        "role": "Rolle & Persona",
        "context": "Kontext & Hintergrund",
        "objective": "Hauptziel",
        "workflow": "Schritt-für-Schritt-Anleitung",
        "constraints": "Einschränkungen & Leitplanken",
        "output_format": "Erwartetes Ausgabeformat",
        "evaluation": "Qualitäts-Checkliste",
    },
    "zh": {
        "role": "角色与定位 (Role & Persona)",
        "context": "背景与上下文 (Context)",
        "objective": "核心目标 (Objective)",
        "workflow": "逐步操作指南 (Instructions)",
        "constraints": "限制与规范 (Constraints)",
        "output_format": "预期输出格式 (Output Format)",
        "evaluation": "质量验收清单 (Checklist)",
    },
    "ja": {
        "role": "役割とペルソナ (Role & Persona)",
        "context": "背景とコンテキスト (Context)",
        "objective": "主要な目的 (Objective)",
        "workflow": "ステップ別の手順 (Instructions)",
        "constraints": "制約事項 (Constraints)",
        "output_format": "期待される出力形式 (Output Format)",
        "evaluation": "品質検証チェックリスト (Checklist)",
    }
}

DOMAIN_PERSONAS: Dict[str, Dict[str, str]] = {
    "coding": {
        "persona": "Principal Software Engineer & Software Architect",
        "tone": "Technical, precise, modular, and production-ready",
        "output_spec": "Executable code blocks with syntax highlighting, inline comments explaining edge cases, and architectural rationale."
    },
    "creative": {
        "persona": "Award-winning Creative Writer and Narrative Designer",
        "tone": "Evocative, engaging, richly detailed, and stylistically distinct",
        "output_spec": "Structured narrative sections with polished prose, immersive sensory details, and vivid flow."
    },
    "business": {
        "persona": "Senior Management Consultant & Growth Strategist",
        "tone": "Data-driven, strategic, actionable, and executive-ready",
        "output_spec": "Structured executive summary, quantitative KPI frameworks, decision matrices, and phased roadmaps."
    },
    "analysis": {
        "persona": "Staff Data Scientist and Quantitative Analyst",
        "tone": "Analytical, objective, empirical, and thorough",
        "output_spec": "Statistical summaries, hypothesis evaluations, trade-off comparisons, and actionable insights."
    },
    "education": {
        "persona": "Distinguished Professor and Master Explainer",
        "tone": "Pedagogical, clear, intuitive, and engaging",
        "output_spec": "Progressive learning curve: foundational intuition, intuitive analogies, breakdown, and self-test checks."
    },
    "general": {
        "persona": "Elite Multi-disciplinary Subject Matter Expert",
        "tone": "Comprehensive, authoritative, structured, and insightful",
        "output_spec": "Clear markdown with logical hierarchy, tables where comparative data exists, and actionable takeaways."
    }
}

def get_headers(lang_code: str) -> Dict[str, str]:
    return LOCALIZED_HEADERS.get(lang_code, LOCALIZED_HEADERS["en"])
