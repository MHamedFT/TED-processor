"""
Main module for TED Talk processing application.

This module serves as the entry point for the TED Talk processing pipeline,
which includes scraping TED talks, downloading transcripts, processing content
through AI transformations, and generating media content and further suggestions.

The application supports command-line arguments to specify which talk (newest, second newest, etc.) to process
and handles the entire workflow from data collection to content generation.
"""

import os
import argparse

from config import config
from ted_scraper import scrape_ted_talks, transcript_downloader
from content_processors import process_talk_content, generate_media_content
from search_service import generate_search_queries


def main():
    """
    Main function to orchestrate the TED talk processing pipeline.
    
    This function handles the complete workflow:
    1. Validates configuration settings
    2. Scrapes available TED talks
    3. Download and processe the selected talk's transcript
    4. Generates AI-processed content (summary, extract, narrative, visualization prompt)
    5. Creates media content (audio and visual)
    6. Generates and executes search queries and offers further suggestions
    
    Raises:
        Exception: Any error that occurs during the processing pipeline
    """
    try:
        # Ensure APIs are set
        config.validate()
        
        talks = scrape_ted_talks()
        
        os.makedirs(config.DATA_DIR, exist_ok=True)
        parser = argparse.ArgumentParser(description="TED Talk Transcript and Summary Generator")
        parser.add_argument(
            "--talk_number", type=int, default=1, help="The number of the TED talk to process"
        )
        args = parser.parse_args()
        talk_number = args.talk_number
        talk = talks[talk_number]
        url = talk["url"]
        speaker_name = talk["speaker"]
        title = talk["title"]
        print(f"\033[92mSelected Talk: {title} by {speaker_name} from {url}\033[0m")

        transcript = transcript_downloader(url)
        if transcript == "No transcript available.":
            print("\033[91mNo transcript available for this talk.\033[0m")
            return
        
        summary, extract, narrative, visualization_prompt = process_talk_content(speaker_name, title, transcript)
        generate_media_content(speaker_name, title, narrative, visualization_prompt)
        generate_search_queries(speaker_name, title, summary)
            
    except Exception as e:
        print(f"Error occurred: {e}")
        

if __name__ == "__main__":
    main()
