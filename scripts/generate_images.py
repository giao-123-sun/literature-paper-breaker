#!/usr/bin/env python3
"""Generate promotional images using Gemini 3.1 Flash Image via OpenRouter.

Uses google/gemini-3.1-flash-image-preview (Nano Banana 2) for image generation
and google/gemini-3.1-flash-lite-preview for lightweight text tasks.

Usage:
    export OPENROUTER_API_KEY="sk-or-v1-..."
    python scripts/generate_images.py [--output-dir OUTPUT_DIR] [--only TASK]

Tasks:
    pipeline    - Generate pipeline architecture diagram
    integrity   - Generate data integrity comparison infographic
    showcase    - Generate paper showcase image
    social      - Generate social media promotional images
    all         - Generate all images (default)
"""

import argparse
import asyncio
import base64
import json
import logging
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("image_gen")

# --- Model configuration ---

IMAGE_MODEL = "google/gemini-3.1-flash-image-preview"  # Nano Banana 2
LITE_MODEL = "google/gemini-3.1-flash-lite-preview"  # Cheap text tasks


async def get_client():
    """Create OpenRouter client."""
    from openai import AsyncOpenAI

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        print("ERROR: Set OPENROUTER_API_KEY environment variable")
        sys.exit(1)

    return AsyncOpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )


async def generate_image(client, prompt: str, filename: str, output_dir: str) -> str | None:
    """Generate an image using Gemini 3.1 Flash Image via OpenRouter.

    Returns the saved file path, or None on failure.
    """
    logger.info(f"Generating: {filename}")
    logger.info(f"  Prompt: {prompt[:100]}...")

    try:
        response = await client.chat.completions.create(
            model=IMAGE_MODEL,
            messages=[
                {"role": "user", "content": prompt},
            ],
            max_tokens=4096,
            extra_body={
                "modalities": ["image", "text"],
            },
        )

        content = response.choices[0].message.content or ""

        # Extract base64 image data from response
        # Gemini returns images as data URLs: data:image/png;base64,...
        image_data = _extract_base64_image(content)

        if image_data:
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(image_data))
            logger.info(f"  Saved: {filepath}")
            return filepath
        else:
            # Response was text-only, save the text for debugging
            text_path = os.path.join(output_dir, f"{filename}.response.txt")
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.warning(f"  No image in response. Text saved to {text_path}")
            return None

    except Exception as e:
        logger.error(f"  Failed: {e}")
        return None


def _extract_base64_image(content: str) -> str | None:
    """Extract base64 image data from response content.

    Handles multiple formats:
    - data:image/png;base64,<data>
    - data:image/jpeg;base64,<data>
    - Inline base64 blocks
    """
    # Try data URL format first
    match = re.search(r"data:image/(?:png|jpeg|webp);base64,([A-Za-z0-9+/=\s]+)", content)
    if match:
        return match.group(1).replace("\n", "").replace(" ", "")

    # Try raw base64 block (long alphanumeric string)
    match = re.search(r"([A-Za-z0-9+/]{100,}={0,2})", content)
    if match:
        return match.group(1)

    return None


async def lite_generate(client, prompt: str, system: str = "") -> str:
    """Use Gemini Flash Lite for cheap text tasks."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model=LITE_MODEL,
        messages=messages,
        max_tokens=500,
        temperature=0.1,
    )
    return response.choices[0].message.content or ""


# --- Image generation prompts ---
# Tips from Google Developers Blog:
# - Describe the scene, don't just list keywords
# - Use photographic/cinematic language for composition control
# - For infographics: specify topic, audience, title placement, data/context
# - Gemini pulls from real-world knowledge for more accurate diagrams

PROMPTS = {
    "pipeline": {
        "filename": "pipeline_architecture.png",
        "prompt": (
            "Create a clean, modern horizontal infographic showing an AI research pipeline "
            "with exactly 7 steps flowing from left to right. "
            "Each step is a rounded rectangle with a small icon inside: "
            "1) 'Literature Search' (magnifying glass icon), "
            "2) 'Literature Review' (open book icon), "
            "3) 'Gap Analysis' (puzzle piece icon), "
            "4) 'Hypothesis Generation' (lightbulb icon), "
            "5) 'Paper Outline' (document list icon), "
            "6) 'Paper Writing' (fountain pen icon), "
            "7) 'Peer Review' (checkmark shield icon). "
            "Connect steps with sleek arrows. "
            "Below each step, show the data source or tool used in small text: "
            "Step 1 shows 'OpenAlex / Semantic Scholar / CrossRef / CORE / CText'. "
            "Step 2-7 show 'LLM (DeepSeek / Claude / Gemini)'. "
            "Use a gradient color scheme from deep blue (step 1) to violet (step 7) "
            "on a clean white background. "
            "Title at the top: 'Literature Paper Breaker — Research Pipeline'. "
            "Subtitle: 'AI-Powered Humanities & Social Science Research Automation'. "
            "Style: minimalist, professional, academic. "
            "Wide format, 1200x600 aspect ratio."
        ),
    },
    "integrity": {
        "filename": "data_integrity_comparison.png",
        "prompt": (
            "Create a side-by-side comparison infographic with the title "
            "'Data Integrity: Why It Matters' at the top. "
            "LEFT side (labeled 'Other AI Tools', with a red X icon and red border): "
            "Show a mock paper excerpt that reads: "
            "'Our survey of 473 respondents revealed that 73.2% believe AI threatens creative industries "
            "(p < 0.001, CI: 69.1-77.3).' "
            "Below it, a red warning label: 'FABRICATED — No survey was actually conducted'. "
            "RIGHT side (labeled 'Literature Paper Breaker', with a green checkmark and green border): "
            "Show a mock paper excerpt that reads: "
            "'This study proposes a survey protocol targeting 60 university students to examine attitudes "
            "toward AI in creative fields. The instrument includes 25 Likert-scale items...' "
            "Below it, a green label: 'HONEST — Clearly states this is a research protocol, not fabricated results'. "
            "Bottom of the image: 'We never fabricate empirical data. When research needs human subjects, "
            "we write a proper research protocol.' "
            "Style: clean, academic, infographic. White background with subtle gray grid. "
            "Wide format, 1200x800 aspect ratio."
        ),
    },
    "showcase": {
        "filename": "paper_showcase.png",
        "prompt": (
            "Create a professional showcase image displaying three academic paper covers arranged "
            "in a slightly overlapping fan layout, tilted at elegant angles. "
            "Paper 1 (front, largest): Title 'LLMs as Cultural Agents: How AI-Generated Text Reshapes "
            "Collective Memory in the Digital Public Sphere', journal 'Sociology', language 'English'. "
            "Paper 2 (middle): Title in Chinese characters '数字孪生与非物质文化遗产保护', "
            "journal 'Anthropology', language 'Chinese'. "
            "Paper 3 (back): Title 'The Algorithmic Flaneur: Psychogeography and AI-Mediated Urban Experience', "
            "journal 'Philosophy', language 'English'. "
            "Each paper shows a clean academic header with title, abstract preview (blurred), "
            "and a 'Generated by Literature Paper Breaker' watermark. "
            "Background: soft gradient from light blue to white. "
            "Bottom text: '3 papers generated in under $1 total API cost'. "
            "Style: professional, elegant, academic publishing aesthetic. "
            "Wide format, 1200x800 aspect ratio."
        ),
    },
    "social_twitter": {
        "filename": "social_twitter_banner.png",
        "prompt": (
            "Create a Twitter/X header banner image for an open source project. "
            "Left side: A stylized illustration of a stack of academic books being transformed "
            "into a glowing digital document by AI, with subtle circuit-board patterns. "
            "Right side text, large and bold: 'Literature Paper Breaker'. "
            "Below in smaller text: 'AI Research Pipeline for Humanities & Social Sciences'. "
            "Below that: 'Open Source | Multi-Database | Peer Review Simulation'. "
            "Color scheme: deep navy blue background with cyan/teal accents and white text. "
            "Style: modern tech, clean, professional. "
            "Exact dimensions: 1500x500 aspect ratio (Twitter header size)."
        ),
    },
    "social_card": {
        "filename": "social_share_card.png",
        "prompt": (
            "Create a social media share card (Open Graph style) for a GitHub project. "
            "Top section: Project logo area with text 'LPB' in a modern geometric font. "
            "Center: Large text reading 'The First AI Research Pipeline for Humanities & Social Sciences'. "
            "Below center: Three feature pills/badges: "
            "'5 Academic Databases' | 'Full Pipeline Automation' | 'Simulated Peer Review'. "
            "Bottom: 'github.com/... | MIT License | Python 3.10+'. "
            "Color scheme: white background, dark text, accent colors in teal and violet. "
            "Small icons of books, magnifying glass, and lightbulb scattered decoratively. "
            "Style: clean, modern, GitHub project card aesthetic. "
            "Dimensions: 1200x630 aspect ratio (OG image standard)."
        ),
    },
}


async def generate_prompt_suggestions(client, task: str) -> str:
    """Use Gemini Lite to suggest improvements to a prompt before generating."""
    return await lite_generate(
        client,
        prompt=(
            f"I want to generate a {task} image for an academic research tool called "
            "'Literature Paper Breaker'. Suggest 3 visual style keywords that would make "
            "this image look professional and academic. Reply with just the 3 keywords, "
            "comma-separated."
        ),
        system="You are a graphic design assistant. Be concise.",
    )


async def run_task(client, task_name: str, output_dir: str) -> dict:
    """Run a single image generation task."""
    if task_name not in PROMPTS:
        logger.error(f"Unknown task: {task_name}")
        return {"task": task_name, "status": "error", "error": "Unknown task"}

    task = PROMPTS[task_name]

    # Use Lite model to get style suggestions
    suggestions = await generate_prompt_suggestions(client, task_name)
    logger.info(f"  Style suggestions from Lite model: {suggestions}")

    # Generate the image
    result = await generate_image(
        client, task["prompt"], task["filename"], output_dir
    )

    return {
        "task": task_name,
        "status": "success" if result else "no_image",
        "file": result,
        "style_hints": suggestions,
    }


async def main():
    parser = argparse.ArgumentParser(description="Generate promotional images for LPB")
    parser.add_argument(
        "--output-dir",
        default="output/images",
        help="Output directory for generated images",
    )
    parser.add_argument(
        "--only",
        choices=list(PROMPTS.keys()) + ["all"],
        default="all",
        help="Which image(s) to generate",
    )
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    client = await get_client()

    tasks = list(PROMPTS.keys()) if args.only == "all" else [args.only]

    logger.info(f"Image Generation — {len(tasks)} task(s)")
    logger.info(f"Image model: {IMAGE_MODEL}")
    logger.info(f"Lite model:  {LITE_MODEL}")
    logger.info(f"Output dir:  {args.output_dir}")

    results = []
    start = time.time()

    for task_name in tasks:
        result = await run_task(client, task_name, args.output_dir)
        results.append(result)

    elapsed = time.time() - start

    # Summary
    logger.info(f"\n{'='*50}")
    logger.info("RESULTS")
    logger.info(f"{'='*50}")
    success = sum(1 for r in results if r["status"] == "success")
    for r in results:
        icon = "OK" if r["status"] == "success" else "NO_IMG" if r["status"] == "no_image" else "ERR"
        logger.info(f"  [{icon}] {r['task']}: {r.get('file', r.get('error', 'N/A'))}")
    logger.info(f"\n  {success}/{len(results)} images generated in {elapsed:.1f}s")

    # Save manifest
    manifest_path = os.path.join(args.output_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    logger.info(f"  Manifest saved: {manifest_path}")

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
