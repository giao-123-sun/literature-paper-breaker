"""LLM provider abstraction layer.

Supports Anthropic Claude and OpenAI models.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any


@dataclass
class LLMConfig:
    """Configuration for LLM provider."""

    provider: str = "anthropic"  # "anthropic" or "openai"
    model: str = "claude-sonnet-4-20250514"
    api_key: str = ""
    max_tokens: int = 8192
    temperature: float = 0.3

    def __post_init__(self):
        if not self.api_key:
            if self.provider == "anthropic":
                self.api_key = os.environ.get("ANTHROPIC_API_KEY", "")
            elif self.provider == "openai":
                self.api_key = os.environ.get("OPENAI_API_KEY", "")


class LLMClient:
    """Unified LLM client for research tasks."""

    def __init__(self, config: LLMConfig | None = None):
        self.config = config or LLMConfig()
        self._client: Any = None

    async def _get_client(self) -> Any:
        if self._client is None:
            if self.config.provider == "anthropic":
                try:
                    import anthropic
                    self._client = anthropic.AsyncAnthropic(api_key=self.config.api_key)
                except ImportError:
                    raise ImportError(
                        "anthropic package not installed. Run: pip install anthropic"
                    )
            elif self.config.provider == "openai":
                try:
                    from openai import AsyncOpenAI
                    self._client = AsyncOpenAI(api_key=self.config.api_key)
                except ImportError:
                    raise ImportError(
                        "openai package not installed. Run: pip install openai"
                    )
        return self._client

    async def generate(
        self,
        prompt: str,
        *,
        system: str = "",
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """Generate text from LLM."""
        client = await self._get_client()
        temp = temperature if temperature is not None else self.config.temperature
        tokens = max_tokens or self.config.max_tokens

        if self.config.provider == "anthropic":
            messages = [{"role": "user", "content": prompt}]
            kwargs: dict[str, Any] = {
                "model": self.config.model,
                "max_tokens": tokens,
                "temperature": temp,
                "messages": messages,
            }
            if system:
                kwargs["system"] = system
            response = await client.messages.create(**kwargs)
            return response.content[0].text

        elif self.config.provider == "openai":
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            response = await client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                max_tokens=tokens,
                temperature=temp,
            )
            return response.choices[0].message.content or ""

        raise ValueError(f"Unknown provider: {self.config.provider}")

    async def generate_structured(
        self,
        prompt: str,
        *,
        system: str = "",
        temperature: float | None = None,
    ) -> str:
        """Generate structured output (JSON) from LLM."""
        structured_prompt = (
            f"{prompt}\n\n"
            "IMPORTANT: Respond ONLY with valid JSON. No markdown, no explanation."
        )
        return await self.generate(
            structured_prompt,
            system=system,
            temperature=temperature or 0.1,
        )

    async def close(self) -> None:
        if self._client and hasattr(self._client, "close"):
            await self._client.close()
