"""
Content processing pipeline functions for TED talk processing.

This module provides a complete pipeline for processing TED talk content through
various AI transformations including:
- Summary generation from transcript
- Extract creation from summary
- Narrative generation for audio content
- Visualization prompt generation for image creation
- Media content generation (audio and image)

The pipeline follows a sequential workflow where each step builds upon the previous output.
Note: Search query generation functionality has been moved to search_service.py
"""

import json
import textwrap
from typing import Tuple

from config import config
from prompts import (
    SUMMARY_SYSTEM_MESSAGE, 
    EXTRACT_SYSTEM_MESSAGE, 
    NARRATIVE_SYSTEM_MESSAGE, 
    IMAGE_SYSTEM_MESSAGE
)
from ai_services import get_openai_response, text_to_speech, image_generation


def process_talk_content(speaker_name: str, title: str, transcript: str) -> Tuple[str, str, str, str]:
    """Process TED talk content through AI transformations pipeline:
    
    1. Generate a concise summary from the full transcript
    2. Extract key insights and main points from the summary
    3. Create an engaging narrative suitable for audio presentation
    4. Generate a visualization prompt based on the summary

    Args:
        speaker_name: The speaker's name.
        title: The title of the talk.
        transcript: The full transcript text.
        
    Returns:
        Tuple containing (summary, extract, narrative, visualization_prompt).
    """
    
    # Step 1: Generate summary
    print(f"\033[94mGenerating summary...\033[0m")
    summary = get_openai_response(
        SUMMARY_SYSTEM_MESSAGE, speaker_name, title, transcript
    )
    
    print("="*config.TEXT_WIDTH)
    print("Summary:".center(config.TEXT_WIDTH))
    print("="*config.TEXT_WIDTH)
    print(textwrap.fill(summary, width=config.TEXT_WIDTH))
    print("="*config.TEXT_WIDTH)

    # Step 2: Generate extract
    print(f"\033[94mGenerating extract...\033[0m")
    extract = get_openai_response(
        EXTRACT_SYSTEM_MESSAGE, speaker_name, title, summary
    )
    
    print("="*config.TEXT_WIDTH)
    print("Extract:".center(config.TEXT_WIDTH))
    print("="*config.TEXT_WIDTH)
    print(textwrap.fill(extract, width=config.TEXT_WIDTH))
    print("="*config.TEXT_WIDTH)

    # Step 3: Generate narrative
    print(f"\033[94mGenerating narrative...\033[0m")
    narrative = get_openai_response(
        NARRATIVE_SYSTEM_MESSAGE, speaker_name, title, extract
    )
    
    print("="*config.TEXT_WIDTH)
    print("Narrative:".center(config.TEXT_WIDTH))
    print("="*config.TEXT_WIDTH)
    print(textwrap.fill(narrative, width=config.TEXT_WIDTH))
    print("="*config.TEXT_WIDTH)

    # Step 4: Generate visualization prompt
    print(f"\033[94mGenerating visualization prompt...\033[0m")
    visualization_prompt = get_openai_response(
        IMAGE_SYSTEM_MESSAGE, speaker_name, title, summary
    )
    
    print("="*config.TEXT_WIDTH)
    print("Visualization Prompt:".center(config.TEXT_WIDTH))
    print("="*config.TEXT_WIDTH)
    print(textwrap.fill(visualization_prompt, width=config.TEXT_WIDTH))
    print("="*config.TEXT_WIDTH)
    
    return summary, extract, narrative, visualization_prompt


def generate_media_content(speaker_name: str, title: str, narrative: str, visualization_prompt: str) -> None:
    """Generate multimedia content including audio and visual materials.
    
    1. Converts narrative text to speech audio file
    2. Creates an image based on the provided visualization prompt
    
    Args:
        speaker_name: The speaker's name.
        title: The title of the talk.
        narrative: The narrative text.
        visualization_prompt: The pre-generated visualization prompt for image creation.
    """
    
    # Generate audio
    print(f"\033[94mGenerating audio...\033[0m")
    text_to_speech(narrative)
    
    # Generate image
    try:
        print(f"\033[94mGenerating image...\033[0m")
        image_generation(visualization_prompt)
    except Exception as e:
        print(f"Image generation failed: {e}")
