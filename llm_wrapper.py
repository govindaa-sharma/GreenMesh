import os, json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SIMULATE_IF_NO_KEY = True


class LLM:
    def __init__(self, provider="gemini", model="gemini-2.5-flash"):
        self.provider = provider
        self.model = model
        self.key = GEMINI_API_KEY

        if self.key:
            genai.configure(api_key=self.key)
            self.client = genai.GenerativeModel(model)
        else:
            self.client = None

    def call(self, prompt, max_tokens=300, temperature=0.0):
        """
        Returns a dict with 'text'. If Gemini gives empty response,
        fallback to simulated deterministic output.
        """
        if not self.key:
            if SIMULATE_IF_NO_KEY:
                return {"text": self._simulate(prompt)}
            raise RuntimeError("No GEMINI_API_KEY found.")

        try:
            print("[LLM] Calling Gemini API...")
            response = self.client.generate_content(
                prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens
                }
            )

            # Try to extract the response text robustly
            text = ""
            if hasattr(response, "text") and response.text:
                text = response.text.strip()
            elif hasattr(response, "candidates") and response.candidates:
                # candidate may exist but have empty parts
                parts = getattr(response.candidates[0].content, "parts", [])
                if parts and hasattr(parts[0], "text"):
                    text = parts[0].text.strip()

            # Gemini sometimes returns empty content → handle that
            if not text or text.lower() in ["", "null", "none"]:
                print("[LLM] Empty or blocked response — using simulation.")
                text = self._simulate(prompt)

            print("[LLM] Gemini responded.")
            return {"text": text}

        except Exception as e:
            print(f"[LLM] Gemini ERROR: {e}")
            return {"text": self._simulate(prompt)}

    def _simulate(self, prompt):
        """Local deterministic fallback when Gemini fails or key missing."""
        if "fusion" in prompt.lower():
            return '{"zones": {"zoneA": {"avg_water":2.8},"zoneB":{"avg_garbage":96}}}'
        if "plan" in prompt.lower() or "planner" in prompt.lower():
            return '{"plans":[{"id":"p1","name":"alert_and_dispatch","cost":100,"time_min":30,"confidence":0.9,"rationale":["water > threshold"]},{"id":"p2","name":"monitor","cost":10,"time_min":120,"confidence":0.6,"rationale":["uncertain data"]}]}'
        if "safety" in prompt.lower():
            return '{"verified": true, "flags":[]}'
        if "audit" in prompt.lower() or "explain" in prompt.lower():
            return '{"explain":"Planner chose p1 because water > threshold; expected to reduce risk by 60%","signature":"sim-sign"}'
        return "OK"
