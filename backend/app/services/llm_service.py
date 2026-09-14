import os
import httpx
from typing import Optional


class LLMService:
    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")

    async def generate_with_groq(self, prompt: str, max_tokens: int = 2000) -> Optional[str]:
        """Generate using Groq API (FREE and fast!)"""
        if not self.groq_key or self.groq_key == "your-key-here":
            print("Groq: No API key found")
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.groq_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "openai/gpt-oss-20b",
                        "max_tokens": max_tokens,
                        "messages": [{"role": "user", "content": prompt}]
                    },
                    timeout=60.0
                )
                data = response.json()
                print("Groq response:", data)
                if "choices" in data:
                    return data["choices"][0]["message"]["content"]
                else:
                    print("Groq API error:", data)
                    return None
        except Exception as e:
            print("Groq API error:", str(e))
            return None

    async def generate_with_claude(self, prompt: str, max_tokens: int = 2000) -> Optional[str]:
        """Generate using Claude API"""
        if not self.anthropic_key or self.anthropic_key == "your-key-here":
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.anthropic_key,
                        "content-type": "application/json",
                        "anthropic-version": "2023-06-01"
                    },
                    json={
                        "model": "claude-3-haiku-20240307",
                        "max_tokens": max_tokens,
                        "messages": [{"role": "user", "content": prompt}]
                    },
                    timeout=60.0
                )
                data = response.json()
                if "content" in data:
                    return data["content"][0]["text"]
                else:
                    print("Claude API error:", data)
                    return None
        except Exception as e:
            print("Claude API error:", str(e))
            return None

    async def generate_with_openai(self, prompt: str, max_tokens: int = 2000) -> Optional[str]:
        """Generate using OpenAI API"""
        if not self.openai_key or self.openai_key == "your-key-here":
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.openai_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-3.5-turbo",
                        "max_tokens": max_tokens,
                        "messages": [{"role": "user", "content": prompt}]
                    },
                    timeout=60.0
                )
                data = response.json()
                if "choices" in data:
                    return data["choices"][0]["message"]["content"]
                else:
                    print("OpenAI API error:", data)
                    return None
        except Exception as e:
            print("OpenAI API error:", str(e))
            return None

    async def generate(self, prompt: str, max_tokens: int = 2000) -> str:
        """Generate text using available LLM (Groq > Claude > OpenAI > Local)"""
        
        # Try Groq first (FREE and fast!)
        result = await self.generate_with_groq(prompt, max_tokens)
        if result:
            return result
        
        # Try Claude
        result = await self.generate_with_claude(prompt, max_tokens)
        if result:
            return result
        
        # Try OpenAI
        result = await self.generate_with_openai(prompt, max_tokens)
        if result:
            return result
        
        # Fallback to local generation
        return self.generate_local(prompt)

    def generate_local(self, prompt: str) -> str:
        """Fallback: generate a basic report without external API."""
        return f"""# Research Report

## Summary
Based on the analysis of the provided sources, here are the key findings:

{prompt}

## Key Insights
- Multiple sources were analyzed to extract important entities and claims
- The knowledge graph shows connections between different topics
- Entity frequency analysis reveals the most mentioned subjects

## Conclusion
This report was generated from the ingested research data. For more detailed analysis, configure an LLM API key in the .env file.

---
*Generated by InsightGraph*
"""
