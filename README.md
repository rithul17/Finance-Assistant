# AI-Powered Financial Analysis System

A comprehensive voice-to-voice financial analysis system that processes audio queries, performs multi-agent analysis using CrewAI, and returns synthesized audio responses with real-time stock market insights.

## Architecture

```
[User Audio Input] → [Streamlit Frontend]-> [FastAPI Backend]-> [Whisper STT] → [CrewAI Multi-Agent System] → [Edge TTS] → [Audio Response]
```

##  Installation & Setup

**USE PYTHON VERSION 3.10.13**
**pyenv install 3.10.13**
**pyenv local 3.10.13**

1. **Clone the repository**
```bash
git clone https://github.com/rithul17/Finance-Assistant
cd Finance-Assistant
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Environment Configuration**
use groq for faster inference
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
MODEL=groq/llama-3.3-70b-versatile
LITELLM_PROVIDER=groq
```

4. **Start the Backend**
```bash
cd backend/
uvicorn main:app --host 0.0.0.0 --port 8000 
```

5. **Start the Frontend**
```bash
cd frontend/
streamlit run app.py --server.port 8501

```

6. **Access the Application**
Open your browser to `http://localhost:8501`

### Agent Workflow
1. **Query Analysis Agent**: Extracts stock tickers and financial entities from user queries
2. **API Agent**: Retrieves real-time data from Yahoo Finance API
3. **Scraping Agent**: Gathers news and market sentiment from financial websites
4. **Retrieval Agent**: Selects relevant context from vector database using semantic search
5. **Analysis Agent**: Synthesizes all data sources into coherent financial insights
6. **Language Agent**: Converts analysis into concise 4-5 sentence summaries

##  Features

- **Voice-to-Voice Interface**: Complete hands-free interaction
- **Real-time Market Data**: Integration with Yahoo Finance API
- **News & Sentiment Analysis**: Web scraping for latest market news
- **Semantic Search**: Vector-based information retrieval
- **Multi-Agent Intelligence**: Specialized AI agents for different analysis tasks
- **Low Latency**: ~4 second average response time
- **Natural Language Output**: Conversational audio responses

##  Tech Stack

### Frontend
- **Streamlit**: Interactive web interface with audio recording capabilities

### Backend
- **FastAPI**: High-performance API server
- **Whisper Base**: Speech-to-text conversion
- **CrewAI**: Multi-agent orchestration framework
- **Edge TTS**: Text-to-speech synthesis (en-US-GuyNeural voice)

### AI & Data
- **Groq API**: LLM inference (llama-3.3-70b-versatile)
- **Pinecone**: Vector database for semantic search
- **Beautiful Soup**: Web scraping for news data
- **Yahoo Finance API**: Real-time market data

##  Prerequisites

- Python 3.8+
- Groq API key
- Yahoo Finance API access

##  Future Enhancements

### Planned Features
- **Advanced Web Scraping**: Migration to Hyperbrowser or Firecrawl for faster multi-site scraping
- **Error Handling**: Comprehensive fallback mechanisms for agent failures
- **Authentication**: User management and API key security
- **Caching**: Redis integration for frequently requested data
- **Multi-language Support**: Additional TTS voices and languages
