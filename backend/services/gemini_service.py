import httpx
from typing import Dict, Any, Optional
from backend.config import settings

class GeminiService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = settings.GEMINI_MODEL


    def generate_text(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        if not self.api_key:
            print("[Gemini Warning] No Gemini API key provided. Returning fallback placeholder.")
            return "[No Gemini API Key Configured]"

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        
        # Structure the payload per the Gemini API spec
        contents = [{
            "parts": [{"text": prompt}]
        }]
        
        data: Dict[str, Any] = {
            "contents": contents,
        }
        
        if system_instruction:
            data["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }

        try:
            response = httpx.post(url, json=data, timeout=45.0)
            if response.status_code == 200:
                res_data = response.json()
                candidates = res_data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
                return f"[Error: Unexpected Gemini API response structure: {response.text}]"
            else:
                return f"[Error calling Gemini API: {response.status_code} - {response.text}]"
        except Exception as e:
            return f"[Error: Exception calling Gemini API: {str(e)}]"

gemini_service = GeminiService()
