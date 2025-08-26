# TED Talk AI Processor

An intelligent Python application that automatically discovers, processes, and enriches TED talks using OpenAI's APIs. The application scrapes recent TED talks, downloads transcripts, and generates comprehensive AI-powered content including summaries, audio narratives, visualizations, and curated research links.

## Features

- **Automated TED Talk Discovery**: Scrapes the latest TED talks from ted.com
- **Transcript Processing**: Downloads and processes talk transcripts
- **AI-Powered Content Generation**:
  - Detailed summaries with all key points
  - Concise paragraph-length extracts
  - Audio narratives explaining the talk summary
  - Abstract visualizations generated from talk themes
  - Curated search queries and research links for further reading
- **Configurable AI Models**: Support for different OpenAI models (GPT-4, DALL-E, TTS)
- **Command-Line Interface**: Easy talk selection and processing

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd TED
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment configuration**:
   ```bash
   cp .env.example .env
   ```

4. **Configure API keys in `.env`**:
   - `OPENAI_API_KEY`: **Required** for AI processing (summary, audio, image generation)
   - `TAVILY_API_KEY`: **Required** for web search functionality

## Usage

### Basic Usage

Process the most recent TED talk:
```bash
python src/main.py
```

Process a specific talk (by position in recent talks list):
```bash
python src/main.py --talk_number 3
```

### Output

The application generates the following content in the `media/` directory:
- **Text content**: Summary and extract saved as text files
- **Audio file**: `narrative.mp3` - AI-generated narration in high quality
- **Image file**: `artwork.png` - Abstract artistic visualization
- **Research links**: Curated URLs for further exploration

## Configuration

The application is highly configurable through environment variables in `.env`:

### Model Configuration
- `CHAT_MODEL`: OpenAI chat model (default: `gpt-5`)
- `TTS_MODEL`: Text-to-speech model (default: `tts-1-hd`)
- `TTS_VOICE`: Voice selection (default: `alloy`)
- `IMAGE_MODEL`: Image generation model (default: `dall-e-3`)
- `IMAGE_SIZE`: Generated image dimensions (default: `1792x1024`)

### File and Directory Settings
- `DATA_DIR`: Output directory for generated content (default: `media`)

### Search and Display
- `MAX_SEARCH_RESULTS`: Number of search results per query (default: `1`)
- `SEARCH_QUERIES_COUNT`: Number of search queries to generate (default: `5`)
- `TEXT_WIDTH`: Text wrapping width for output (default: `80`)

### Performance
- `CACHE_SIZE`: LRU cache size for scraping results (default: `10`)

## Project Structure

```
src/
├── main.py                 # Main application entry point and CLI
├── config.py              # Configuration management and validation
├── ted_scraper.py         # TED talk scraping and transcript downloading
├── content_processors.py  # AI content processing pipeline
├── ai_services.py         # OpenAI API integration services
├── search_service.py      # Web search and link generation
├── prompts.py            # AI prompt templates
└── main.ipynb            # Jupyter notebook for interactive development

media/                     # Generated content output directory
├── narrative.mp3         # AI-generated audio narration (high quality)
├── artwork.png           # Abstract artistic visualization
└── transcript            # Downloaded transcript text

archive/                   # Development history and experiments
requirements.txt          # Python dependencies
.env.example              # Environment configuration template
```

## Dependencies

- **openai**: OpenAI API integration for GPT, DALL-E, and TTS
- **selenium**: Web scraping for TED talk discovery
- **yt-dlp**: Video/transcript downloading capabilities
- **tavily-python**: Web search API integration
- **python-dotenv**: Environment variable management
- **requests**: HTTP client for API calls

## Requirements

- Python 3.8+
- Chrome/Chromium browser (for web scraping)
- OpenAI API key with access to GPT, DALL-E, and TTS services
- Tavily API key for web search functionality

## Error Handling

The application includes comprehensive error handling for:
- Missing API keys and configuration validation
- Network connectivity issues during scraping
- Transcript availability validation
- API rate limiting and service errors