"""LLM provider abstraction layer.

Supports Anthropic Claude, OpenAI, and OpenRouter (OpenAI-compatible).
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class LLMConfig:
    """Configuration for LLM provider."""

    provider: str = "anthropic"  # "anthropic", "openai", or "openrouter"
    model: str = "claude-sonnet-4-20250514"
    api_key: str = ""
    base_url: str = ""  # custom base URL (auto-set for openrouter)
    max_tokens: int = 8192
    temperature: float = 0.3

    def __post_init__(self):
        if not self.api_key:
            env_keys = {
                "anthropic": "ANTHROPIC_API_KEY",
                "openai": "OPENAI_API_KEY",
                "openrouter": "OPENROUTER_API_KEY",
            }
            self.api_key = os.environ.get(env_keys.get(self.provider, ""), "")

        if self.provider == "openrouter" and not self.base_url:
            self.base_url = "https://openrouter.ai/api/v1"


@dataclass
class UsageTracker:
    """Tracks API token usage and estimated costs."""

    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_calls: int = 0
    cost_per_input_token: float = 0.0  # set based on model
    cost_per_output_token: float = 0.0

    @property
    def estimated_cost(self) -> float:
        return (
            self.total_input_tokens * self.cost_per_input_token
            + self.total_output_tokens * self.cost_per_output_token
        )

    def record(self, input_tokens: int, output_tokens: int):
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_calls += 1

    def summary(self) -> str:
        return (
            f"API calls: {self.total_calls} | "
            f"Tokens: {self.total_input_tokens:,} in + {self.total_output_tokens:,} out | "
            f"Est. cost: ${self.estimated_cost:.4f}"
        )


class LLMClient:
    """Unified LLM client for research tasks."""

    def __init__(self, config: LLMConfig | None = None):
        self.config = config or LLMConfig()
        self._client: Any = None
        self.usage = UsageTracker()

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
            elif self.config.provider in ("openai", "openrouter"):
                try:
                    from openai import AsyncOpenAI
                    kwargs: dict[str, Any] = {"api_key": self.config.api_key}
                    if self.config.base_url:
                        kwargs["base_url"] = self.config.base_url
                    self._client = AsyncOpenAI(**kwargs)
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
            api_kwargs: dict[str, Any] = {
                "model": self.config.model,
                "max_tokens": tokens,
                "temperature": temp,
                "messages": messages,
            }
            if system:
                api_kwargs["system"] = system
            response = await client.messages.create(**api_kwargs)
            self.usage.record(
                response.usage.input_tokens, response.usage.output_tokens
            )
            return response.content[0].text

        elif self.config.provider in ("openai", "openrouter"):
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            api_kwargs = {
                "model": self.config.model,
                "messages": messages,
                "max_tokens": tokens,
                "temperature": temp,
            }
            response = await client.chat.completions.create(**api_kwargs)

            # Track usage
            if response.usage:
                self.usage.record(
                    response.usage.prompt_tokens or 0,
                    response.usage.completion_tokens or 0,
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
