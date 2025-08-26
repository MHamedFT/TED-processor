"""
TED Talk Scraper and Transcript Processor

Provides web scraping functionality for TED talks and transcript downloading/processing.
Combines both talk discovery and content extraction in a unified module.
"""

import os
import time
from functools import lru_cache
from typing import Dict

import yt_dlp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from config import config


@lru_cache(maxsize=config.CACHE_SIZE)
def scrape_ted_talks() -> dict:
    """Scrape recent TED talks.
    
    Returns:
        dict: A dictionary of recent TED talks with their metadata.
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        talks_url = 'https://www.ted.com/talks'
        driver.get(talks_url)
        time.sleep(1)  # Wait for page to load
        
        video_containers = driver.find_elements(By.CSS_SELECTOR, 'div.xs-tui\\:col-span-1')

        talks = {}
        for idx, container in enumerate(video_containers, 1):
            try:
                # Extract the link from the <a> tag's href attribute
                link_element = container.find_element(By.TAG_NAME, 'a')
                link = link_element.get_attribute('href')

                # Extract the title from the <span> tag with the specific class
                title_element = container.find_element(By.CSS_SELECTOR, 'span.subheader2')
                title = title_element.text

                # Extract the speaker's name from the <p> tag with the specific class
                speaker_element = container.find_element(By.CSS_SELECTOR, 'p.text-textTertiary-onLight')
                speaker = speaker_element.text
                
                if link and title and speaker:
                    talks[idx] = {
                        'url': link,
                        'speaker': speaker.strip(),
                        'title': title.strip()
                    }
                
            except Exception as e:
                print(f"Failed to extract talk {idx}: {e}")
                continue

        return talks
        
    except Exception as e:
        raise e
    finally:
        if driver:
            driver.quit()


@lru_cache(maxsize=config.CACHE_SIZE)
def transcript_downloader(url: str, outtmpl: str = config.TRANSCRIPT_PATH) -> str:
    """Download transcript of a TED talk using yt-dlp.
    
    Args:
        url: The URL of the TED talk.
        outtmpl: The output template for the transcript file.
        
    Returns:
        The transcript text or an error message.
    """
    if not url or not url.strip():
        return "No transcript available."
        
    ydl_opts = {
        'writesubtitles': True,
        'skip_download': True,
        'subtitleslang': 'en',
        'outtmpl': outtmpl,
        'overwrites': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(url)
    except Exception as e:
        print(f"Failed to download transcript: {e}")
        return "No transcript available."

    file_path = f'{outtmpl}.en.vtt'
    if not os.path.exists(file_path):
        return "No transcript available."
    
    lines = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('WEBVTT') or '-->' in line:
                    continue
                else:
                    lines.append(line)
        os.remove(file_path)
        
        result = " ".join(lines)
        return result
        
    except Exception as e:
        print(f"Failed to process transcript file: {e}")
        if os.path.exists(file_path):
            os.remove(file_path)
        return "No transcript available."
