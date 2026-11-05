"""
CLI interface for Better Prompt.
"""

import sys
import argparse
import json

# Ensure cross-platform UTF-8 handling on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from .core import BetterPrompt, PromptFramework

def main():
    parser = argparse.ArgumentParser(
        prog="better-prompt",
        description="Better Prompt: Multi-language intelligent prompt engineering tool"
    )
    parser.add_argument("requirement", nargs="?", default="", help="Raw requirement in any language")
    parser.add_argument("-l", "--lang", help="Target output language code (e.g. en, hi, es, fr, de, ja, zh)")
    parser.add_argument("-f", "--framework", choices=["structured", "co_star", "crispe", "xml"], default="structured", help="Prompt structure framework")
    parser.add_argument("-o", "--output", help="Save the enhanced prompt to a file")
    parser.add_argument("--ai", action="store_true", help="Enhance further using local offline Gemma model via Ollama")
    parser.add_argument("-m", "--model", help="Specify local Ollama model (default: gemma4:12b)")
    parser.add_argument("-j", "--json", action="store_true", help="Output full analysis metadata as JSON")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive terminal mode")

    args = parser.parse_args()

    engine = BetterPrompt()

    if args.interactive or not args.requirement:
        print("=== Better Prompt: Multi-Language Prompt Generator ===")
        print("Enter your requirement in any language (or 'exit' to quit):")
        try:
            req = input("\nRequirement > ").strip()
            if not req or req.lower() in ["exit", "quit"]:
                sys.exit(0)
            args.requirement = req
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            sys.exit(0)

    result = engine.enhance(
        requirement=args.requirement,
        target_language=args.lang,
        framework=args.framework,
        use_ai=args.ai,
        model=args.model
    )

    if args.json:
        output_str = json.dumps(result.to_dict(), indent=2, ensure_ascii=False)
    else:
        output_str = result.enhanced_prompt

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_str)
        print(f"Enhanced prompt saved to: {args.output}")
    else:
        print("\n" + "="*50)
        print(f"Detected: {result.detected_language} | Target: {result.target_language} | Domain: {result.primary_domain} | Framework: {result.framework}")
        print("="*50 + "\n")
        print(output_str)

if __name__ == "__main__":
    main()
