import os
from typing import Optional
from openai import OpenAI
from backend.config import settings

class GroqService:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.GROQ_MODEL
        self._client = None

    @property
    def client(self):
        if self._client is None and self.api_key:
            self._client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.groq.com/openai/v1"
            )
        return self._client

    def generate_text(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        # Refresh key in case settings was updated at runtime
        if not self.api_key:
            self.api_key = settings.GROQ_API_KEY
            self.model = settings.GROQ_MODEL

        if not self.api_key:
            print("[Groq Warning] No Groq API key provided. Returning fallback placeholder.")
            return "[No Groq API Key Configured]"

        try:
            messages = []
            if system_instruction:
                messages.append({"role": "system", "content": system_instruction})
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2,  # Low temperature for deterministic regulatory writing
                timeout=45.0
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[Error: Exception calling Groq API: {str(e)}]"

groq_service = GroqService()
