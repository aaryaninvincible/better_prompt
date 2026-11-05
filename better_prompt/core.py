"""
Core implementation of Better Prompt.
Transforms raw, ambiguous user requirements into rigorous, high-impact prompts.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any, List
import json
import os
import urllib.request
import urllib.error

from .detector import analyze_requirement, detect_language
from .templates import get_headers, DOMAIN_PERSONAS

class PromptFramework(str, Enum):
    STRUCTURED = "structured"
    CO_STAR = "co_star"
    CRISPE = "crispe"
    XML = "xml"

@dataclass
class PromptResult:
    raw_requirement: str
    enhanced_prompt: str
    detected_language: str
    target_language: str
    primary_domain: str
    framework: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "raw_requirement": self.raw_requirement,
            "enhanced_prompt": self.enhanced_prompt,
            "detected_language": self.detected_language,
            "target_language": self.target_language,
            "primary_domain": self.primary_domain,
            "framework": self.framework,
            "metadata": self.metadata,
        }

    def __str__(self) -> str:
        return self.enhanced_prompt

class BetterPrompt:
    """
    Main engine for analyzing requirements and generating high-performance prompts.
    """

    def __init__(self, ollama_host: str = "http://127.0.0.1:11434", default_model: str = "gemma4:12b"):
        self.ollama_host = os.environ.get("OLLAMA_HOST", ollama_host)
        self.default_model = os.environ.get("LOCAL_AGENT_MODEL", default_model)

    def enhance(
        self,
        requirement: str,
        target_language: Optional[str] = None,
        framework: str = "structured",
        use_ai: bool = False,
        model: Optional[str] = None,
        custom_instructions: Optional[str] = None
    ) -> PromptResult:
        """
        Transform a user requirement into a detailed, production-grade prompt.
        """
        analysis = analyze_requirement(requirement)
        detected_lang = analysis["language"]
        out_lang = target_language.lower() if target_language else detected_lang
        domain = analysis["primary_domain"]
        chosen_framework = framework.lower()

        # Generate base structured prompt
        if chosen_framework == "co_star":
            enhanced = self._build_co_star_prompt(requirement, analysis, out_lang, custom_instructions)
        elif chosen_framework == "crispe":
            enhanced = self._build_crispe_prompt(requirement, analysis, out_lang, custom_instructions)
        elif chosen_framework == "xml":
            enhanced = self._build_xml_prompt(requirement, analysis, out_lang, custom_instructions)
        else:
            enhanced = self._build_structured_prompt(requirement, analysis, out_lang, custom_instructions)

        # Optional AI refinement via local Ollama
        ai_meta = {"ai_enhanced": False}
        if use_ai:
            ai_output = self._call_local_gemma(
                requirement=requirement,
                draft_prompt=enhanced,
                target_lang=out_lang,
                model=model or self.default_model
            )
            if ai_output and not ai_output.startswith("[Error"):
                enhanced = ai_output
                ai_meta = {"ai_enhanced": True, "model": model or self.default_model}

        return PromptResult(
            raw_requirement=requirement,
            enhanced_prompt=enhanced,
            detected_language=detected_lang,
            target_language=out_lang,
            primary_domain=domain,
            framework=chosen_framework,
            metadata={**analysis, **ai_meta}
        )

    def _build_structured_prompt(
        self,
        requirement: str,
        analysis: Dict[str, Any],
        lang: str,
        custom_instructions: Optional[str]
    ) -> str:
        headers = get_headers(lang)
        domain = analysis["primary_domain"]
        persona_info = DOMAIN_PERSONAS.get(domain, DOMAIN_PERSONAS["general"])

        sections = [
            f"# System Directive: {persona_info['persona']}",
            "",
            f"## {headers['role']}",
            f"You are operating as an expert **{persona_info['persona']}**. "
            f"Maintain an authoritative, {persona_info['tone']} demeanor.",
            "",
            f"## {headers['context']}",
            f"The user has submitted the following requirement:\n> \"{requirement}\"",
            "",
            f"## {headers['objective']}",
            f"Analyze, solve, and execute the user's objective thoroughly. Provide complete, "
            f"production-grade outputs rather than conceptual outlines or placeholders.",
            "",
            f"## {headers['workflow']}",
            "1. **Deconstruct Scope**: Identify foundational components, data flow, and underlying logic.",
            "2. **Implement Solution**: Provide fully fleshed-out, clean, and well-structured deliverables.",
            "3. **Address Edge Cases**: Explicitly mitigate common pitfalls, vulnerabilities, and failure modes.",
            "4. **Deliver Verification**: Include practical testing or validation steps to confirm correctness.",
            "",
            f"## {headers['constraints']}",
            "- No lazy ellipsis or truncated placeholders (`// TODO`, `...`).",
            "- Adhere strictly to industry standard design patterns and security best practices.",
            "- Ensure all code, logic, or text is immediately executable and self-contained.",
        ]

        if custom_instructions:
            sections.extend([
                f"- User Custom Directive: {custom_instructions}"
            ])

        sections.extend([
            "",
            f"## {headers['output_format']}",
            persona_info["output_spec"],
            "",
            f"## {headers['evaluation']}",
            "- [ ] Does the solution completely fulfill the initial requirement without ambiguity?",
            "- [ ] Are all dependencies, edge cases, and configurations fully addressed?",
            "- [ ] Is the formatting clean, structured, and easy to read?"
        ])

        return "\n".join(sections)

    def _build_co_star_prompt(
        self,
        requirement: str,
        analysis: Dict[str, Any],
        lang: str,
        custom_instructions: Optional[str]
    ) -> str:
        domain = analysis["primary_domain"]
        persona_info = DOMAIN_PERSONAS.get(domain, DOMAIN_PERSONAS["general"])

        return (
            f"### Context (C)\n"
            f"User Goal: {requirement}\n"
            f"Domain Area: {domain.capitalize()}\n\n"
            f"### Objective (O)\n"
            f"Deliver an exhaustive, top-tier solution that fulfills the user requirement end-to-end.\n\n"
            f"### Style (S)\n"
            f"Professional, structured, rigorous, and {persona_info['tone']}.\n\n"
            f"### Tone (T)\n"
            f"Direct, authoritative, and helpful.\n\n"
            f"### Audience (A)\n"
            f"Developers, technical stakeholders, and end users seeking production quality.\n\n"
            f"### Response (R)\n"
            f"{persona_info['output_spec']}"
        )

    def _build_crispe_prompt(
        self,
        requirement: str,
        analysis: Dict[str, Any],
        lang: str,
        custom_instructions: Optional[str]
    ) -> str:
        domain = analysis["primary_domain"]
        persona_info = DOMAIN_PERSONAS.get(domain, DOMAIN_PERSONAS["general"])

        return (
            f"### Capacity & Role (CR)\n"
            f"Act as a {persona_info['persona']}.\n\n"
            f"### Insight (I)\n"
            f"Address the user's explicit and implicit needs based on: \"{requirement}\"\n\n"
            f"### Statement of Request (S)\n"
            f"Generate an end-to-end implementation with high precision.\n\n"
            f"### Persona & Personality (P)\n"
            f"Tone: {persona_info['tone']}.\n\n"
            f"### Experiment & Scope (E)\n"
            f"Provide fully verified steps, robust error handling, and zero placeholder code."
        )

    def _build_xml_prompt(
        self,
        requirement: str,
        analysis: Dict[str, Any],
        lang: str,
        custom_instructions: Optional[str]
    ) -> str:
        domain = analysis["primary_domain"]
        persona_info = DOMAIN_PERSONAS.get(domain, DOMAIN_PERSONAS["general"])

        return (
            f"<system>\n"
            f"  <role>{persona_info['persona']}</role>\n"
            f"  <style>{persona_info['tone']}</style>\n"
            f"</system>\n"
            f"<context>\n"
            f"  <requirement>{requirement}</requirement>\n"
            f"  <domain>{domain}</domain>\n"
            f"</context>\n"
            f"<instructions>\n"
            f"  <step>Analyze architecture and edge cases</step>\n"
            f"  <step>Produce production-ready, complete deliverable</step>\n"
            f"  <step>Provide validation/testing guidelines</step>\n"
            f"</instructions>\n"
            f"<output_format>\n"
            f"  {persona_info['output_spec']}\n"
            f"</output_format>"
        )

    def _call_local_gemma(self, requirement: str, draft_prompt: str, target_lang: str, model: str) -> Optional[str]:
        """
        Delegates prompt refinement to the local Gemma model via Ollama.
        """
        system_msg = (
            "You are an elite Prompt Engineer. Expand and optimize the given draft prompt into a masterpiece prompt. "
            f"The final prompt must be rendered in language: {target_lang}. "
            "Return ONLY the refined prompt text without conversational chatter."
        )
        prompt_body = f"User requirement: {requirement}\n\nDraft prompt:\n{draft_prompt}"

        payload = {
            "model": model,
            "prompt": prompt_body,
            "system": system_msg,
            "stream": False,
        }

        req = urllib.request.Request(
            f"{self.ollama_host}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("response", "").strip()
        except Exception as e:
            return f"[Error contacting local model: {e}]"

# Convenience alias
PromptEnhancer = BetterPrompt
