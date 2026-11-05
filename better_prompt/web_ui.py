"""
Lightweight Web Interface for Better Prompt.
Runs locally using Python standard library with zero external dependencies.
"""

import http.server
import socketserver
import json
import urllib.parse
import os
import sys

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from .core import BetterPrompt

DEFAULT_PORT = 8505
engine = BetterPrompt()

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Better Prompt — Multi-Language Prompt Engineering</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #090d16;
      --card-bg: #111827;
      --border: #1f293d;
      --accent: #6366f1;
      --accent-hover: #4f46e5;
      --text: #f3f4f6;
      --text-muted: #9ca3af;
      --code-bg: #0b0f19;
      --success: #10b981;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'Inter', sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 2.5rem 1rem;
    }
    .container {
      width: 100%;
      max-width: 900px;
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }
    header {
      text-align: center;
      margin-bottom: 0.5rem;
    }
    h1 {
      font-size: 2.2rem;
      font-weight: 700;
      background: linear-gradient(135deg, #a5b4fc, #6366f1, #38bdf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 0.5rem;
    }
    p.subtitle {
      color: var(--text-muted);
      font-size: 0.95rem;
    }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    }
    label {
      display: block;
      font-size: 0.85rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-bottom: 0.5rem;
    }
    textarea {
      width: 100%;
      height: 100px;
      background: var(--code-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.85rem;
      color: var(--text);
      font-size: 0.95rem;
      font-family: inherit;
      resize: vertical;
      outline: none;
      transition: border-color 0.2s;
    }
    textarea:focus {
      border-color: var(--accent);
    }
    .controls {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 1rem;
      margin-top: 1rem;
    }
    select, button {
      height: 42px;
      border-radius: 8px;
      font-size: 0.9rem;
      font-family: inherit;
      outline: none;
      transition: all 0.2s;
    }
    select {
      background: var(--code-bg);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 0 0.75rem;
      cursor: pointer;
    }
    button.btn-primary {
      background: linear-gradient(135deg, var(--accent), var(--accent-hover));
      color: #fff;
      font-weight: 600;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
    }
    button.btn-primary:hover {
      opacity: 0.95;
      transform: translateY(-1px);
    }
    .meta-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 0.75rem;
    }
    .badges {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
    .badge {
      font-size: 0.75rem;
      padding: 0.25rem 0.6rem;
      background: rgba(99, 102, 241, 0.15);
      border: 1px solid rgba(99, 102, 241, 0.3);
      color: #c7d2fe;
      border-radius: 6px;
      font-weight: 500;
    }
    .btn-copy {
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 0.35rem 0.75rem;
      border-radius: 6px;
      font-size: 0.8rem;
      cursor: pointer;
      transition: all 0.2s;
    }
    .btn-copy:hover {
      color: var(--text);
      border-color: var(--accent);
    }
    pre {
      background: var(--code-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.25rem;
      color: #e2e8f0;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.88rem;
      line-height: 1.6;
      white-space: pre-wrap;
      word-break: break-word;
      max-height: 480px;
      overflow-y: auto;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>Better Prompt</h1>
      <p class="subtitle">Turn raw, brief requests in any language into exhaustive, production-grade LLM prompts.</p>
    </header>

    <div class="card">
      <label for="req">Your Raw Requirement (Any Language)</label>
      <textarea id="req" placeholder="e.g. create a weather dashboard in react / मुझे एक टास्क मैनेजर ऐप बनाना है / crear una api con fastapi"></textarea>

      <div class="controls">
        <div>
          <label for="framework">Framework</label>
          <select id="framework">
            <option value="structured">Structured Directive</option>
            <option value="co_star">CO-STAR Framework</option>
            <option value="crispe">CRISPE Framework</option>
            <option value="xml">XML Architecture</option>
          </select>
        </div>
        <div>
          <label for="lang">Target Output Language</label>
          <select id="lang">
            <option value="">Auto-Detect / Match Input</option>
            <option value="en">English</option>
            <option value="hi">Hindi (हिंदी)</option>
            <option value="es">Spanish (Español)</option>
            <option value="fr">French (Français)</option>
            <option value="de">German (Deutsch)</option>
            <option value="zh">Chinese (中文)</option>
            <option value="ja">Japanese (日本語)</option>
          </select>
        </div>
        <div style="display: flex; flex-direction: column; justify-content: flex-end;">
          <button class="btn-primary" onclick="enhancePrompt()">Generate Prompt ⚡</button>
        </div>
      </div>
    </div>

    <div class="card" id="result-card" style="display: none;">
      <div class="meta-bar">
        <div class="badges" id="meta-badges"></div>
        <button class="btn-copy" id="copy-btn" onclick="copyOutput()">Copy Prompt</button>
      </div>
      <pre id="output-box"></pre>
    </div>
  </div>

  <script>
    async function enhancePrompt() {
      const req = document.getElementById('req').value.trim();
      if (!req) return;

      const framework = document.getElementById('framework').value;
      const lang = document.getElementById('lang').value;

      const resCard = document.getElementById('result-card');
      const outBox = document.getElementById('output-box');
      const badges = document.getElementById('meta-badges');

      outBox.textContent = "Analyzing requirement & generating high-impact prompt...";
      resCard.style.display = 'block';

      try {
        const resp = await fetch('/api/enhance', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ requirement: req, framework: framework, target_language: lang })
        });
        const data = await resp.json();

        badges.innerHTML = `
          <span class="badge">Language: ${data.detected_language.toUpperCase()} → ${data.target_language.toUpperCase()}</span>
          <span class="badge">Domain: ${data.primary_domain}</span>
          <span class="badge">Framework: ${data.framework}</span>
          <span class="badge">Complexity: ${data.metadata.complexity}</span>
        `;
        outBox.textContent = data.enhanced_prompt;
      } catch (err) {
        outBox.textContent = "Error: " + err;
      }
    }

    function copyOutput() {
      const text = document.getElementById('output-box').textContent;
      navigator.clipboard.writeText(text);
      const btn = document.getElementById('copy-btn');
      btn.textContent = "Copied! ✓";
      setTimeout(() => btn.textContent = "Copy Prompt", 2000);
    }
  </script>
</body>
</html>
"""

class PromptServerHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode("utf-8"))

    def do_POST(self):
        if self.path == "/api/enhance":
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(post_body)
                requirement = data.get("requirement", "")
                framework = data.get("framework", "structured")
                target_lang = data.get("target_language") or None

                result = engine.enhance(
                    requirement=requirement,
                    target_language=target_lang,
                    framework=framework
                )

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(result.to_dict(), ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Suppress spammy HTTP request logs
        return

def run_server(start_port=DEFAULT_PORT):
    for port in range(start_port, start_port + 20):
        try:
            httpd = socketserver.TCPServer(("", port), PromptServerHandler)
            print(f"\n==================================================")
            print(f" Better Prompt Web Interface is active!")
            print(f" URL: http://localhost:{port}")
            print(f"==================================================\n", flush=True)
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nShutting down server.")
            finally:
                httpd.server_close()
            return
        except OSError:
            continue
    print(f"Error: Could not bind to any port in range {start_port}-{start_port+20}")

if __name__ == "__main__":
    run_server()
