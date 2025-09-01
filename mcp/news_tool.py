"""
Ferramenta de Notícias MCP
Busca notícias usando Google News RSS e web scraping
"""

import asyncio
import logging
import re
from typing import Any, Dict, List
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup

from .base_tool import BaseTool, ToolExecutionError

logger = logging.getLogger(__name__)


class NewsTool(BaseTool):
    """Ferramenta para buscar notícias"""
    
    def __init__(self):
        super().__init__(
            name="news_tool",
            description="Busca notícias recentes sobre um assunto ou cidade",
            cache_ttl=3600  # 1 hora
        )
        self.session = None
        
    def get_parameters(self) -> List[Dict[str, Any]]:
        """Retorna parâmetros aceitos pela ferramenta"""
        return [
            {
                'name': 'query',
                'type': 'string',
                'required': True,
                'description': 'Termo de busca para notícias'
            },
            {
                'name': 'limit',
                'type': 'integer',
                'required': False,
                'default': 3,
                'description': 'Número máximo de notícias (1-10)'
            },
            {
                'name': 'language',
                'type': 'string',
                'required': False,
                'default': 'pt',
                'description': 'Idioma das notícias (pt, en, es)'
            }
        ]
        
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Executa a busca de notícias"""
        try:
            # Validar e processar parâmetros
            query = params.get('query', '').strip()
            limit = min(max(params.get('limit', 3), 1), 10)
            language = params.get('language', 'pt')
            
            if not query:
                raise ToolExecutionError("Query não pode estar vazia")
                
            logger.info(f"Buscando notícias para: '{query}' (limite: {limit})")
            
            # Inicializar sessão HTTP se necessário
            if not self.session:
                self.session = aiohttp.ClientSession()
                
            # Buscar notícias
            news_items = await self._fetch_news(query, limit, language)
            
            if not news_items:
                return {
                    'success': False,
                    'message': f"Nenhuma notícia encontrada para '{query}'",
                    'data': []
                }
                
            return {
                'success': True,
                'query': query,
                'count': len(news_items),
                'data': news_items,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro ao buscar notícias: {e}")
            raise ToolExecutionError(f"Erro na busca de notícias: {str(e)}")
            
    async def _fetch_news(self, query: str, limit: int, language: str) -> List[Dict[str, Any]]:
        """Busca notícias de múltiplas fontes"""
        news_items = []
        
        # Tentar Google News RSS primeiro
        try:
            rss_news = await self._fetch_google_news_rss(query, limit, language)
            news_items.extend(rss_news)
        except Exception as e:
            logger.warning(f"Erro ao buscar Google News RSS: {e}")
            
        # Se não conseguiu RSS, tentar DuckDuckGo
        if len(news_items) < limit:
            try:
                ddg_news = await self._fetch_duckduckgo_news(query, limit - len(news_items))
                news_items.extend(ddg_news)
            except Exception as e:
                logger.warning(f"Erro ao buscar DuckDuckGo: {e}")
                
        # Se ainda não tem notícias suficientes, tentar web scraping
        if len(news_items) < limit:
            try:
                scraped_news = await self._scrape_news_sites(query, limit - len(news_items))
                news_items.extend(scraped_news)
            except Exception as e:
                logger.warning(f"Erro ao fazer web scraping: {e}")
                
        return news_items[:limit]
        
    async def _fetch_google_news_rss(self, query: str, limit: int, language: str) -> List[Dict[str, Any]]:
        """Busca notícias via Google News RSS"""
        # Google News RSS URL
        encoded_query = query.replace(' ', '+')
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl={language}&gl=BR&ceid=BR:pt-419"
        
        try:
            async with self.session.get(rss_url, timeout=10) as response:
                if response.status != 200:
                    raise Exception(f"HTTP {response.status}")
                    
                content = await response.text()
                return self._parse_rss_feed(content, limit)
                
        except Exception as e:
            logger.error(f"Erro ao buscar RSS: {e}")
            raise
            
    def _parse_rss_feed(self, content: str, limit: int) -> List[Dict[str, Any]]:
        """Parse RSS feed XML"""
        try:
            soup = BeautifulSoup(content, 'xml')
            items = soup.find_all('item')[:limit]
            
            news_items = []
            for item in items:
                title = item.find('title')
                link = item.find('link')
                pub_date = item.find('pubDate')
                
                if title and link:
                    news_items.append({
                        'title': title.get_text().strip(),
                        'url': link.get_text().strip(),
                        'published': pub_date.get_text().strip() if pub_date else None,
                        'source': 'Google News RSS'
                    })
                    
            return news_items
            
        except Exception as e:
            logger.error(f"Erro ao parsear RSS: {e}")
            return []
            
    async def _fetch_duckduckgo_news(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Busca notícias via DuckDuckGo Instant Answer"""
        # DuckDuckGo Instant Answer API
        api_url = f"https://api.duckduckgo.com/"
        params = {
            'q': f"{query} news",
            'format': 'json',
            'no_html': '1',
            'skip_disambig': '1'
        }
        
        try:
            async with self.session.get(api_url, params=params, timeout=10) as response:
                if response.status != 200:
                    raise Exception(f"HTTP {response.status}")
                    
                data = await response.json()
                
                news_items = []
                if 'AbstractURL' in data and data['AbstractURL']:
                    news_items.append({
                        'title': data.get('Abstract', 'Notícia encontrada'),
                        'url': data['AbstractURL'],
                        'published': None,
                        'source': 'DuckDuckGo'
                    })
                    
                return news_items[:limit]
                
        except Exception as e:
            logger.error(f"Erro ao buscar DuckDuckGo: {e}")
            return []
            
    async def _scrape_news_sites(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Web scraping de sites de notícias"""
        # Lista de sites para tentar
        news_sites = [
            'https://g1.globo.com/',
            'https://www.uol.com.br/',
            'https://www.terra.com.br/'
        ]
        
        news_items = []
        
        for site in news_sites:
            if len(news_items) >= limit:
                break
                
            try:
                site_news = await self._scrape_site(site, query)
                news_items.extend(site_news)
            except Exception as e:
                logger.warning(f"Erro ao fazer scraping de {site}: {e}")
                continue
                
        return news_items[:limit]
        
    async def _scrape_site(self, site_url: str, query: str) -> List[Dict[str, Any]]:
        """Faz scraping de um site específico"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            async with self.session.get(site_url, headers=headers, timeout=10) as response:
                if response.status != 200:
                    return []
                    
                content = await response.text()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Buscar links de notícias (implementação básica)
                news_links = soup.find_all('a', href=True)
                
                news_items = []
                for link in news_links:
                    if len(news_items) >= 2:  # Máximo 2 por site
                        break
                        
                    href = link.get('href', '')
                    title = link.get_text().strip()
                    
                    # Verificar se parece ser uma notícia
                    if self._is_news_link(href, title, query):
                        news_items.append({
                            'title': title,
                            'url': href if href.startswith('http') else f"{site_url.rstrip('/')}{href}",
                            'published': None,
                            'source': site_url
                        })
                        
                return news_items
                
        except Exception as e:
            logger.error(f"Erro ao fazer scraping de {site_url}: {e}")
            return []
            
    def _is_news_link(self, href: str, title: str, query: str) -> bool:
        """Verifica se um link parece ser uma notícia relevante"""
        # Palavras-chave que indicam notícias
        news_keywords = ['noticia', 'notícia', 'news', 'reportagem', 'materia', 'matéria']
        
        # Verificar se contém palavras-chave de notícias
        has_news_keyword = any(keyword in title.lower() for keyword in news_keywords)
        
        # Verificar se contém a query
        has_query = query.lower() in title.lower()
        
        # Verificar se o link parece ser de notícia
        is_news_url = any(keyword in href.lower() for keyword in news_keywords)
        
        return (has_news_keyword or has_query) and len(title) > 10
        
    async def cleanup(self):
        """Limpa recursos da ferramenta"""
        if self.session:
            await self.session.close()
            self.session = None
            
    def __del__(self):
        """Destrutor para garantir limpeza"""
        if hasattr(self, 'session') and self.session:
            try:
                asyncio.create_task(self.session.close())
            except:
                pass
