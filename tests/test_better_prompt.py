"""
Comprehensive unit test suite for better_prompt.
Tests multi-language detection, requirement analysis, and prompt generation frameworks.
"""

import unittest
import sys
import os

# Add parent directory to path so better_prompt can be imported directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from better_prompt.detector import detect_language, analyze_requirement
from better_prompt.templates import get_headers, DOMAIN_PERSONAS
from better_prompt.core import BetterPrompt, PromptResult, PromptFramework

class TestBetterPromptLanguageDetection(unittest.TestCase):
    """Test multi-language script and stopword detection."""

    def test_detect_language_english(self):
        text = "Create a modern weather dashboard using React and Tailwind"
        self.assertEqual(detect_language(text), "en")

    def test_detect_language_hindi(self):
        text = "मुझे एक अच्छा सा कैलकुलेटर ऐप बनाना है पाइथन में"
        self.assertEqual(detect_language(text), "hi")

    def test_detect_language_spanish(self):
        text = "Quiero crear una aplicación para gestionar mis tareas diarias con React"
        self.assertEqual(detect_language(text), "es")

    def test_detect_language_french(self):
        text = "Comment créer une application pour gérer les utilisateurs avec FastAPI"
        self.assertEqual(detect_language(text), "fr")

    def test_detect_language_chinese(self):
        text = "帮我写一个基于Python的爬虫程序，抓取天气数据"
        self.assertEqual(detect_language(text), "zh")

    def test_detect_language_empty(self):
        self.assertEqual(detect_language(""), "en")
        self.assertEqual(detect_language("   "), "en")


class TestBetterPromptRequirementAnalysis(unittest.TestCase):
    """Test requirement decomposition, domain classification, and complexity."""

    def test_analyze_requirement_coding_domain(self):
        text = "Write a python script to connect to a postgresql database and run queries"
        analysis = analyze_requirement(text)
        self.assertEqual(analysis["language"], "en")
        self.assertEqual(analysis["primary_domain"], "coding")
        self.assertIn("coding", analysis["domains"])
        self.assertEqual(analysis["complexity"], "moderate")

    def test_analyze_requirement_creative_domain(self):
        text = "Write a fantasy story about a clockmaker who discovers time magic"
        analysis = analyze_requirement(text)
        self.assertEqual(analysis["primary_domain"], "creative")

    def test_analyze_requirement_business_domain(self):
        text = "Create a strategic business plan and marketing pitch for a SaaS startup"
        analysis = analyze_requirement(text)
        self.assertEqual(analysis["primary_domain"], "business")

    def test_analyze_requirement_brief_complexity(self):
        text = "make weather app"
        analysis = analyze_requirement(text)
        self.assertEqual(analysis["complexity"], "brief")
        self.assertLess(analysis["word_count"], 6)

    def test_analyze_requirement_constraints(self):
        text = "Build a REST API in nodejs without using express and must include auth"
        analysis = analyze_requirement(text)
        self.assertTrue(analysis["has_constraints"])


class TestBetterPromptFrameworks(unittest.TestCase):
    """Test all prompt engineering frameworks and outputs."""

    def setUp(self):
        self.engine = BetterPrompt()

    def test_structured_framework(self):
        req = "Build an authentication service with JWT and refresh tokens"
        result = self.engine.enhance(req, framework="structured")

        self.assertIsInstance(result, PromptResult)
        self.assertEqual(result.framework, "structured")
        self.assertEqual(result.primary_domain, "coding")
        self.assertIn("System Directive:", result.enhanced_prompt)
        self.assertIn("Role & Persona", result.enhanced_prompt)
        self.assertIn("Primary Objective", result.enhanced_prompt)
        self.assertIn("Constraints & Guardrails", result.enhanced_prompt)
        self.assertIn("Expected Output Format", result.enhanced_prompt)
        self.assertIn(req, result.enhanced_prompt)

    def test_co_star_framework(self):
        req = "Analyze quarterly churn metrics for an e-commerce platform"
        result = self.engine.enhance(req, framework="co_star")

        self.assertEqual(result.framework, "co_star")
        self.assertIn("Context (C)", result.enhanced_prompt)
        self.assertIn("Objective (O)", result.enhanced_prompt)
        self.assertIn("Style (S)", result.enhanced_prompt)
        self.assertIn("Tone (T)", result.enhanced_prompt)
        self.assertIn("Audience (A)", result.enhanced_prompt)
        self.assertIn("Response (R)", result.enhanced_prompt)

    def test_crispe_framework(self):
        req = "Explain quantum computing to high school students"
        result = self.engine.enhance(req, framework="crispe")

        self.assertEqual(result.framework, "crispe")
        self.assertIn("Capacity & Role (CR)", result.enhanced_prompt)
        self.assertIn("Insight (I)", result.enhanced_prompt)
        self.assertIn("Statement of Request (S)", result.enhanced_prompt)
        self.assertIn("Persona & Personality (P)", result.enhanced_prompt)
        self.assertIn("Experiment & Scope (E)", result.enhanced_prompt)

    def test_xml_framework(self):
        req = "Design a scalable rate limiter algorithm in Go"
        result = self.engine.enhance(req, framework="xml")

        self.assertEqual(result.framework, "xml")
        self.assertIn("<system>", result.enhanced_prompt)
        self.assertIn("<context>", result.enhanced_prompt)
        self.assertIn("<instructions>", result.enhanced_prompt)
        self.assertIn("<output_format>", result.enhanced_prompt)

    def test_target_language_override(self):
        req = "Create a task manager"
        result_hi = self.engine.enhance(req, target_language="hi")
        self.assertEqual(result_hi.target_language, "hi")
        # Localized Hindi headers should be present
        self.assertIn("भूमिका और व्यक्तित्व", result_hi.enhanced_prompt)
        self.assertIn("मुख्य उद्देश्य", result_hi.enhanced_prompt)

        result_es = self.engine.enhance(req, target_language="es")
        self.assertEqual(result_es.target_language, "es")
        self.assertIn("Objetivo Principal", result_es.enhanced_prompt)

    def test_custom_instructions_integration(self):
        req = "Write a blog post about artificial intelligence"
        custom = "Target audience is senior executives, keep it under 800 words"
        result = self.engine.enhance(req, custom_instructions=custom)
        self.assertIn(custom, result.enhanced_prompt)

    def test_prompt_result_serialization(self):
        req = "Test serialization"
        result = self.engine.enhance(req)
        d = result.to_dict()
        self.assertEqual(d["raw_requirement"], req)
        self.assertIn("enhanced_prompt", d)
        self.assertIn("detected_language", d)
        self.assertEqual(str(result), result.enhanced_prompt)

if __name__ == "__main__":
    unittest.main()
