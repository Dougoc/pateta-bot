"""
Registro de ferramentas MCP
Gerencia todas as ferramentas disponíveis no sistema
"""

import logging
from typing import Dict, List, Optional, Any
from .base_tool import BaseTool, ToolExecutionError, ToolValidationError

logger = logging.getLogger(__name__)


class ToolsRegistry:
    """Registro central de ferramentas MCP"""
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._cache: Dict[str, Any] = {}
        
    def register_tool(self, tool: BaseTool) -> None:
        """
        Registra uma nova ferramenta
        
        Args:
            tool: Instância da ferramenta a ser registrada
        """
        if not isinstance(tool, BaseTool):
            raise ValueError("Tool deve herdar de BaseTool")
            
        self._tools[tool.name] = tool
        logger.info(f"Ferramenta '{tool.name}' registrada")
        
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """
        Obtém uma ferramenta pelo nome
        
        Args:
            name: Nome da ferramenta
            
        Returns:
            Instância da ferramenta ou None se não encontrada
        """
        return self._tools.get(name)
        
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        Lista todas as ferramentas registradas
        
        Returns:
            Lista com informações de todas as ferramentas
        """
        return [tool.get_tool_info() for tool in self._tools.values()]
        
    async def execute_tool(self, name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa uma ferramenta específica
        
        Args:
            name: Nome da ferramenta
            params: Parâmetros para execução
            
        Returns:
            Resultado da execução da ferramenta
        """
        tool = self.get_tool(name)
        if not tool:
            raise ToolExecutionError(f"Ferramenta '{name}' não encontrada")
            
        # Validar parâmetros
        if not tool.validate_input(params):
            raise ToolValidationError(f"Parâmetros inválidos para ferramenta '{name}'")
            
        # Verificar cache
        cache_key = f"{name}:{hash(str(params))}"
        if cache_key in self._cache and tool.should_use_cache():
            logger.info(f"Usando cache para ferramenta '{name}'")
            return self._cache[cache_key]
            
        try:
            # Executar ferramenta
            result = await tool.execute(params)
            
            # Atualizar estatísticas
            tool.update_execution_stats()
            
            # Armazenar no cache
            self._cache[cache_key] = result
            
            logger.info(f"Ferramenta '{name}' executada com sucesso")
            return result
            
        except Exception as e:
            logger.error(f"Erro ao executar ferramenta '{name}': {e}")
            raise ToolExecutionError(f"Erro na execução da ferramenta '{name}': {str(e)}")
            
    def get_tool_descriptions(self) -> str:
        """
        Retorna descrições de todas as ferramentas para o prompt do Ollama
        
        Returns:
            String formatada com descrições das ferramentas
        """
        descriptions = []
        for tool in self._tools.values():
            desc = f"- {tool.name}: {tool.description}"
            if tool.get_parameters():
                params = [f"{p['name']}({p.get('type', 'string')})" for p in tool.get_parameters()]
                desc += f" Parâmetros: {', '.join(params)}"
            descriptions.append(desc)
            
        return "\n".join(descriptions)
        
    def detect_tool_needed(self, message: str) -> Optional[Dict[str, Any]]:
        """
        Detecta se uma mensagem precisa de uma ferramenta específica
        
        Args:
            message: Mensagem do usuário
            
        Returns:
            Dicionário com nome da ferramenta e parâmetros ou None
        """
        message_lower = message.lower()
        
        # Detectar ferramenta de notícias
        news_keywords = ['noticia', 'notícia', 'news', 'última', 'recente']
        if any(keyword in message_lower for keyword in news_keywords):
            return self._extract_news_params(message)
            
        # Detectar ferramenta de esportes
        sports_keywords = ['flamengo', 'futebol', 'esporte', 'time', 'jogo']
        if any(keyword in message_lower for keyword in sports_keywords):
            return self._extract_sports_params(message)
            
        # Detectar ferramenta de clima
        weather_keywords = ['clima', 'tempo', 'weather', 'temperatura', 'chuva']
        if any(keyword in message_lower for keyword in weather_keywords):
            return self._extract_weather_params(message)
            
        return None
        
    def _extract_news_params(self, message: str) -> Optional[Dict[str, Any]]:
        """Extrai parâmetros para ferramenta de notícias"""
        # Implementação básica - pode ser melhorada com NLP
        if 'flamengo' in message.lower():
            return {
                'tool': 'news_tool',
                'params': {'query': 'flamengo', 'limit': 3}
            }
        return {
            'tool': 'news_tool',
            'params': {'query': 'notícias', 'limit': 3}
        }
        
    def _extract_sports_params(self, message: str) -> Optional[Dict[str, Any]]:
        """Extrai parâmetros para ferramenta de esportes"""
        if 'flamengo' in message.lower():
            return {
                'tool': 'sports_tool',
                'params': {'team': 'flamengo', 'limit': 3}
            }
        return {
            'tool': 'sports_tool',
            'params': {'team': 'esportes', 'limit': 3}
        }
        
    def _extract_weather_params(self, message: str) -> Optional[Dict[str, Any]]:
        """Extrai parâmetros para ferramenta de clima"""
        # Assumir cidade padrão ou extrair da mensagem
        return {
            'tool': 'weather_tool',
            'params': {'city': 'Rio de Janeiro', 'country': 'BR'}
        }
        
    def clear_cache(self) -> None:
        """Limpa o cache de ferramentas"""
        self._cache.clear()
        logger.info("Cache de ferramentas limpo")
        
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do registro de ferramentas"""
        total_executions = sum(tool.execution_count for tool in self._tools.values())
        return {
            'total_tools': len(self._tools),
            'total_executions': total_executions,
            'cache_size': len(self._cache),
            'tools': [tool.get_tool_info() for tool in self._tools.values()]
        }


# Instância global do registro
tools_registry = ToolsRegistry()
