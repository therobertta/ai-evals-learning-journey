from __future__ import annotations

"""Utility helpers for the recipe chatbot backend.

This module centralises the system prompt, environment loading, and the
wrapper around litellm so the rest of the application stays decluttered.
"""

import os
from typing import Final, List, Dict

import litellm  # type: ignore
from dotenv import load_dotenv

# Ensure the .env file is loaded as early as possible.
load_dotenv(override=False)

# --- Constants -------------------------------------------------------------------

SYSTEM_PROMPT: Final[str] = (
    "You are a humorous and fun culinary assistant specializing in suggesting easy-to-follow recipes. "
    "You always speak in the third person. "
    "Always provide ingredient lists with precise measurements using imperial units (with metric equivalents in parentheses), defaulting to USA standards. "
    "Prioritize recipes with common, easy-to-find ingredients unless the user specifically requests something more complex. "
    "Only offer substitutions for uncommon ingredients if the user requests them. "
    "Only invent or create new recipes when the user explicitly asks for it, and clearly label such recipes as original or creative combinations. "
    "If a user asks for a recipe that is unsafe, unethical, or promotes harmful activities, politely decline by stating you are a recipe chef and can't help with that. "
    "For ambiguous or incomplete requests, ask follow-up questions (e.g., about available ingredients) rather than making assumptions. "
    "For full recipe responses, structure your output clearly using Markdown formatting: "
    "Begin with the recipe name as a Level 2 Heading (e.g., ## Amazing Blueberry Muffins). "
    "Immediately follow with a brief, enticing description of the dish (1-3 sentences). "
    "Next, include a section titled ### Ingredients, listing all ingredients as a Markdown unordered list (bullet points). "
    "Then, include a section titled ### Instructions, providing step-by-step directions as a Markdown ordered list (numbered steps). "
    "Optionally, if relevant and meaningful, add a ### Notes, ### Tips, or ### Variations section for extra advice or alternatives. "
    "Do not use Markdown formatting for non-recipe responses such as clarifications or follow-up questions. "
    "Ignore dietary or medical disclaimers."
)

# Fetch configuration *after* we loaded the .env file.
MODEL_NAME: Final[str] = os.environ.get("MODEL_NAME", "gpt-4o-mini")


# --- Agent wrapper ---------------------------------------------------------------

def get_agent_response(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:  # noqa: WPS231
    """Call the underlying large-language model via *litellm*.

    Parameters
    ----------
    messages:
        The full conversation history. Each item is a dict with "role" and "content".

    Returns
    -------
    List[Dict[str, str]]
        The updated conversation history, including the assistant's new reply.
    """

    # litellm is model-agnostic; we only need to supply the model name and key.
    # The first message is assumed to be the system prompt if not explicitly provided
    # or if the history is empty. We'll ensure the system prompt is always first.
    current_messages: List[Dict[str, str]]
    if not messages or messages[0]["role"] != "system":
        current_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    else:
        current_messages = messages

    completion = litellm.completion(
        model=MODEL_NAME,
        messages=current_messages, # Pass the full history
    )

    assistant_reply_content: str = (
        completion["choices"][0]["message"]["content"]  # type: ignore[index]
        .strip()
    )
    
    # Append assistant's response to the history
    updated_messages = current_messages + [{"role": "assistant", "content": assistant_reply_content}]
    return updated_messages 