"""
AI services for OpenAI API interactions.

This module provides cached AI services including:
- Chat completions for text processing
- Text-to-speech conversion
- Image generation using OpenAI image generators

All functions utilize LRU caching where applicable to optimize API usage.
"""

import requests
from functools import lru_cache

from openai import OpenAI

from config import config


@lru_cache(maxsize=config.CACHE_SIZE)
def get_openai_response(system_message: str, speaker: str, title: str, text: str) -> str:
    """Get OpenAI response.
    
    Args:
        system_message: The system message for the AI model.
        speaker: The speaker's name.
        title: The title of the talk.
        text: The text content to process.
        
    Returns:
        The AI model's response.
        
    Raises:
        ValueError: If OpenAI returns an empty response.
    """
    llm = OpenAI(api_key=config.OPENAI_API_KEY)
    response = llm.chat.completions.create(
        model=config.CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": f"Here is the text for TED Talk with the title {title} by {speaker}:\\n\\n" + text
            }
        ]
    )
    output = response.choices[0].message.content
    if output is None:
        raise ValueError(f"OpenAI returned empty response for {title}")
    
    return output


@lru_cache(maxsize=config.CACHE_SIZE)
def text_to_speech(text: str, path: str = config.AUDIO_PATH) -> None:
    """Convert text to speech using OpenAI's TTS API and save it as binary content.
    
    Args:
        text: The text (narrative) to convert to speech.
        path: The output file path where the audio will be saved.
    """
    llm = OpenAI(api_key=config.OPENAI_API_KEY)
    response = llm.audio.speech.create(
        model=config.TTS_MODEL,
        voice=config.TTS_VOICE,
        input=text,
    )
    with open(path, "wb") as f:
        f.write(response.content)


def image_generation(prompt: str, path: str = config.IMAGE_PATH) -> None:
    """Generate an image using OpenAI's API.
    
    Args:
        prompt: The visualization prompt for image generation.
        path: The output file path where the image will be saved.
              
    Raises:
        ValueError: If OpenAI returns an empty image response or no URL.
    """
    llm = OpenAI(api_key=config.OPENAI_API_KEY)
    response = llm.images.generate(
        model=config.IMAGE_MODEL,
        prompt=prompt,
        size=config.IMAGE_SIZE
    )
    if not response.data or not response.data[0].url:
        raise ValueError("OpenAI returned empty image response")    
    image_url = response.data[0].url

    request_response = requests.get(image_url)
    if request_response.status_code == 200:
        with open(path, "wb") as f:
            f.write(request_response.content)
    else:
        print(f"Failed to retrieve image from {image_url}")
