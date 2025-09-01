"""
Configurações centralizadas do Pateta Bot
"""

import os
from typing import Set
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Bot
BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_CHAT_IDS: Set[str] = {cid.strip() for cid in os.getenv("ALLOWED_CHAT_IDS", "").split(",") if cid.strip()}

# Configurações do Ollama
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Configurações de Cache
CACHE_TTL_NEWS = int(os.getenv("CACHE_TTL_NEWS", "3600"))  # 1 hora
CACHE_TTL_SPORTS = int(os.getenv("CACHE_TTL_SPORTS", "1800"))  # 30 minutos
CACHE_TTL_WEATHER = int(os.getenv("CACHE_TTL_WEATHER", "900"))  # 15 minutos

# Configurações de Rate Limiting
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "1"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))

# Configurações de Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Configurações de APIs
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY", "")

# Configurações de Cidade Padrão
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "Rio de Janeiro")
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "BR")

# Configurações de Times Favoritos
FAVORITE_TEAMS = os.getenv("FAVORITE_TEAMS", "flamengo,vasco,fluminense,botafogo").split(",")

# Configurações de Resumo Matinal
MORNING_NEWS_ENABLED = os.getenv("MORNING_NEWS_ENABLED", "true").lower() == "true"
MORNING_NEWS_TIME = os.getenv("MORNING_NEWS_TIME", "08:00")
MORNING_NEWS_TOPICS = os.getenv("MORNING_NEWS_TOPICS", "notícias,esportes,clima").split(",")

# Configurações de Web Scraping
USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# Configurações de Segurança
MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", "4096"))
MAX_TOOL_EXECUTIONS_PER_MINUTE = int(os.getenv("MAX_TOOL_EXECUTIONS_PER_MINUTE", "5"))

# URLs de APIs e Sites
GOOGLE_NEWS_RSS_BASE = "https://news.google.com/rss/search"
DUCKDUCKGO_API_URL = "https://api.duckduckgo.com/"
OPENWEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Sites de notícias para scraping
NEWS_SITES = [
    "https://g1.globo.com/",
    "https://www.uol.com.br/",
    "https://www.terra.com.br/",
    "https://www.r7.com/",
    "https://www.cnnbrasil.com.br/"
]

# Sites esportivos
SPORTS_SITES = [
    "https://ge.globo.com/",
    "https://www.lance.com.br/",
    "https://www.espn.com.br/",
    "https://www.uol.com.br/esporte/"
]

# Validações
def validate_config():
    """Valida as configurações obrigatórias"""
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN é obrigatório")
    
    if not ALLOWED_CHAT_IDS:
        print("⚠️  AVISO: ALLOWED_CHAT_IDS está vazio. Adicione IDs de chat permitidos.")
    
    return True

# Configurações de desenvolvimento
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
TESTING = os.getenv("TESTING", "false").lower() == "true"

# Configurações de monitoramento
ENABLE_METRICS = os.getenv("ENABLE_METRICS", "true").lower() == "true"
METRICS_INTERVAL = int(os.getenv("METRICS_INTERVAL", "300"))  # 5 minutos
