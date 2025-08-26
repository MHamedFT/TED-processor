"""
Search service for TED talk content discovery using Tavily API.

Provides search query generation and execution functionality to find
related content and resources based on processed TED talk summaries.
"""

import json
import time
from typing import Dict, List, Any

from tavily import TavilyClient

from ai_services import get_openai_response
from config import config
from prompts import SEARCH_SYSTEM_MESSAGE


def get_tavily_search_results(queries: List[str]) -> Dict[int, Dict[str, Any]]:
    """Get search results with retry logic.
    
    Args:
        queries: List of search queries.
        
    Returns:
        Dictionary mapping query index to search results.
    """
    if not queries:
        print("No queries provided for search")
        return {}
        
    client = TavilyClient(api_key=config.TAVILY_API_KEY)
    results = {}
    
    for idx, query in enumerate(queries, 1):
        if not query.strip():
            continue
            
        results[idx] = {}
        results[idx]["query"] = query
        
        # Retry logic for search
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = client.search(query, max_results=config.MAX_SEARCH_RESULTS)["results"][0]
                results[idx]["url"] = response['url']
                results[idx]["content"] = response['content']
                break  # Success, exit retry loop
            except (IndexError, KeyError) as e:
                if attempt == max_retries - 1:  # Last attempt
                    print(f"Search failed for query '{query}' after {max_retries} attempts: {e}")
                    results[idx]["url"] = "N/A"
                    results[idx]["content"] = "Search failed"
                else:
                    time.sleep(1)  # Wait before retry
    
    return results


def generate_search_queries(speaker_name: str, title: str, summary: str) -> None:
    """Generate and execute search queries related to the TED talk content.
    
    Creates relevant search queries based on the talk summary and executes them
    using the Tavily search service to find related information and resources.
    
    Args:
        speaker_name: The speaker's name.
        title: The title of the talk.
        summary: The summary text.
        
    Raises:
        Handles JSON parsing errors gracefully and continues execution.
    """
    print(f"\033[94mGenerating queries...\033[0m")
    json_queries = get_openai_response(
        SEARCH_SYSTEM_MESSAGE, speaker_name, title, summary
    )
    
    try:
        list_of_queries = json.loads(json_queries)
        if not isinstance(list_of_queries, list):
            print("Invalid query format received from OpenAI")
            return
    except json.JSONDecodeError as e:
        print(f"Failed to parse search queries: {e}")
        return
        
    print(f"\033[94mGetting search results...\033[0m")
    query_results = get_tavily_search_results(list_of_queries)
    
    print("\n" + "="*config.TEXT_WIDTH)
    print("Search Results:".center(config.TEXT_WIDTH))
    print("="*config.TEXT_WIDTH)
    
    for result in query_results.values():
        print(f"Query: {result['query']}")
        print(f"URL: {result['url']}\n")
    
    print("="*config.TEXT_WIDTH)
