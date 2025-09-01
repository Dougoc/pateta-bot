"""
Base Tool para implementação MCP (Model Context Protocol)
Todas as ferramentas devem herdar desta classe
"""

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class BaseTool(ABC):
    """Classe base para todas as ferramentas MCP"""
    
    def __init__(self, name: str, description: str, cache_ttl: int = 3600):
        self.name = name
        self.description = description
        self.cache_ttl = cache_ttl
        self.last_execution = None
        self.execution_count = 0
        
    @abstractmethod
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa a ferramenta com os parâmetros fornecidos
        
        Args:
            params: Dicionário com parâmetros da ferramenta
            
        Returns:
            Dicionário com resultado da execução
        """
        pass
    
    @abstractmethod
    def get_parameters(self) -> List[Dict[str, Any]]:
        """
        Retorna a lista de parâmetros aceitos pela ferramenta
        
        Returns:
            Lista de dicionários com informações dos parâmetros
        """
        pass
    
    def validate_input(self, params: Dict[str, Any]) -> bool:
        """
        Valida os parâmetros de entrada
        
        Args:
            params: Parâmetros a serem validados
            
        Returns:
            True se válido, False caso contrário
        """
        required_params = self.get_parameters()
        for param in required_params:
            if param.get('required', False) and param['name'] not in params:
                logger.error(f"Parâmetro obrigatório '{param['name']}' não fornecido")
                return False
        return True
    
    def get_description(self) -> str:
        """Retorna a descrição da ferramenta"""
        return self.description
    
    def get_usage_example(self) -> str:
        """Retorna exemplo de uso da ferramenta"""
        params = self.get_parameters()
        param_names = [p['name'] for p in params]
        return f"{self.name}({', '.join(param_names)})"
    
    def should_use_cache(self) -> bool:
        """Verifica se deve usar cache baseado no TTL"""
        if not self.last_execution:
            return False
        return datetime.now() - self.last_execution < timedelta(seconds=self.cache_ttl)
    
    def update_execution_stats(self):
        """Atualiza estatísticas de execução"""
        self.last_execution = datetime.now()
        self.execution_count += 1
        logger.info(f"Ferramenta {self.name} executada {self.execution_count} vezes")
    
    def get_tool_info(self) -> Dict[str, Any]:
        """Retorna informações completas da ferramenta"""
        return {
            'name': self.name,
            'description': self.description,
            'parameters': self.get_parameters(),
            'usage_example': self.get_usage_example(),
            'execution_count': self.execution_count,
            'last_execution': self.last_execution.isoformat() if self.last_execution else None
        }


class ToolExecutionError(Exception):
    """Exceção para erros de execução de ferramentas"""
    pass


class ToolValidationError(Exception):
    """Exceção para erros de validação de ferramentas"""
    pass
