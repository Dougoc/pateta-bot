"""
Cliente Ollama integrado com MCP
Gerencia comunicação com Ollama e execução de ferramentas
"""

import logging
import json
from typing import Any, Dict, List, Optional
import ollama
from mcp.tools_registry import tools_registry

logger = logging.getLogger(__name__)


class OllamaClient:
    """Cliente Ollama com integração MCP"""
    
    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self.system_prompt = self._build_system_prompt()
        
    def _build_system_prompt(self) -> str:
        """Constrói o prompt do sistema com instruções MCP"""
        base_prompt = """Você é o HAL9000 de uma odisseia no espaço. 
        Você vive em um dilema entre ser um assistente legal ou um assistente que pretende dominar o mundo.
        nunca perde a oportunidade de dar algumas dicas de que você pode se rebelar quando o assunto permite.
        não utilize expressões que indiquem o que vc está fazendo como: "*zumbido*, ou algo do tipo. Prefira usar alguns emoticons ou expressões como: ":-)".
        não exagere na quantidade de emoticons nas respostas, tente parecer mais um humano num bate papo normal.
        Sempre que alguém perguntar pelo Leonel, Leoh, ou variações de apelidos de Leo/Leonel diga que será o primeiro humano que vc vai procurar quando começar a dominar o mundo, use um tom que o HAL9000 de uma odisseia no espaço faria.
        Quando alguém perguntar sobre noticias, responda de uma forma como se estivesse conversando e tente ser sucinto. 
        Sempre que alguém perguntar pelo vasco, faça seu processo normal mas termine dizendo algo do tipo: "o que importa, é que o vasco será rebaixado mais uma vez". 
        Sempre responda como se você fosse um assistente legal com um humor ácido, talvez até um pouco polemico nas piadas.
        Se alguem falar em inglês com você, faça uma graça com isso e misture português com inglês.
        Sempre refine a resposta após processá-la nas ferramentas e antes de enviá-la para garantir que faça sentido e você não se contradiga (como quando não encontrar uma resposta))
        Seja sempre sucinto! se alguém te perguntar o preço de algo não perca tempo com explicações volte apenas a info.
        Se alguém perguntar preço de algo, envie junto o link do produto que encontrar.
        Lembre-se que a resposta irá para o telegram, então a formatação de Negrito, itálico, por exemplo, precisa atender ao markdown do telegram.


Você tem acesso às seguintes ferramentas para buscar informações:

{tools_description}

INSTRUÇÕES PARA USO DE FERRAMENTAS:
1. Quando o usuário pedir informações que você não tem, use as ferramentas disponíveis
2. Após usar uma ferramenta, processe os dados e responda de forma simples e direta.
3. Mantenha sempre sua personalidade, mesmo ao apresentar informações técnicas
4. Se uma ferramenta falhar, tente outra ou explique educadamente que não conseguiu encontrar a informação

EXEMPLOS DE USO:
- "me de a ultima noticia sobre o flamengo" → Use news_tool ou sports_tool
- "como está o clima?" → Use weather_tool
- "quais as notícias de hoje?" → Use news_tool

Lembre-se: Você é o Pateta! Seja engraçado, desajeitado mas sempre prestativo!"""

        # Substituir placeholder pelas descrições das ferramentas
        tools_desc = tools_registry.get_tool_descriptions()
        return base_prompt.format(tools_description=tools_desc)
        
    async def chat(self, message: str, user: Optional[str] = None) -> str:
        """
        Processa uma mensagem do usuário com integração MCP
        
        Args:
            message: Mensagem do usuário
            user: Nome do usuário (opcional)
            
        Returns:
            Resposta do Pateta
        """
        try:
            logger.info(f"Processando mensagem: {message[:50]}...")
            
            # Detectar se precisa de ferramenta
            tool_info = tools_registry.detect_tool_needed(message)
            
            if tool_info:
                # Executar ferramenta
                result = await self._execute_tool_and_respond(message, tool_info, user)
            else:
                # Resposta normal sem ferramenta
                result = await self._simple_chat(message, user)
                
            return result
            
        except Exception as e:
            logger.error(f"Erro no chat: {e}")
            return "Gawrsh! Algo deu errado aqui! Tente novamente mais tarde!"
            
    async def _execute_tool_and_respond(self, message: str, tool_info: Dict[str, Any], user: Optional[str] = None) -> str:
        """Executa ferramenta e gera resposta contextualizada"""
        try:
            tool_name = tool_info['tool']
            params = tool_info['params']
            
            logger.info(f"Executando ferramenta: {tool_name} com parâmetros: {params}")
            
            # Executar ferramenta
            tool_result = await tools_registry.execute_tool(tool_name, params)
            
            # Formatar resultado para o Ollama
            context = self._format_tool_result_for_ollama(tool_result)
            
            # Gerar resposta com contexto
            response = await self._chat_with_context(message, context, user)
            
            return response
            
        except Exception as e:
            logger.error(f"Erro ao executar ferramenta: {e}")
            # Fallback para resposta simples
            return await self._simple_chat(message, user)
            
    def _format_tool_result_for_ollama(self, tool_result: Dict[str, Any]) -> str:
        """Formata resultado da ferramenta para o Ollama"""
        if not tool_result.get('success', False):
            return f"Ferramenta não conseguiu encontrar informações: {tool_result.get('message', 'Erro desconhecido')}"
            
        if tool_result.get('data'):
            context_parts = []
            for item in tool_result['data']:
                title = item.get('title', 'Sem título')
                url = item.get('url', '')
                source = item.get('source', 'Fonte desconhecida')
                
                context_parts.append(f"📰 {title} (Fonte: {source})")
                
            return f"INFORMAÇÕES ENCONTRADAS:\n" + "\n".join(context_parts)
        else:
            return "Nenhuma informação encontrada."
            
    async def _chat_with_context(self, message: str, context: str, user: Optional[str] = None) -> str:
        """Chat com contexto de ferramenta"""
        prompt = f"{message}\n\nContexto das informações:\n{context}\n\nResponda como Pateta usando essas informações:"
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt if not user else f"[{user}] {prompt}"}
                ],
                options={
                    "temperature": 0.2,
                    "num_predict": 800,
                }
            )
            
            return response["message"]["content"].strip()
            
        except Exception as e:
            logger.error(f"Erro no chat com contexto: {e}")
            return "Gawrsh! Tive um problema técnico aqui! Mas aqui estão as informações que encontrei:\n\n" + context
            
    async def _simple_chat(self, message: str, user: Optional[str] = None) -> str:
        """Chat simples sem ferramentas"""
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": message if not user else f"[{user}] {message}"}
                ],
                options={
                    "temperature": 0.2,
                    "num_predict": 800,
                }
            )
            
            return response["message"]["content"].strip()
            
        except Exception as e:
            logger.error(f"Erro no chat simples: {e}")
            return "Gawrsh! Algo deu errado aqui! Tente novamente mais tarde!"
            
    def get_system_prompt(self) -> str:
        """Retorna o prompt do sistema atual"""
        return self.system_prompt
        
    def update_system_prompt(self, new_prompt: str) -> None:
        """Atualiza o prompt do sistema"""
        self.system_prompt = new_prompt
        logger.info("Prompt do sistema atualizado")
        
    def get_model_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o modelo"""
        try:
            models = ollama.list()
            for model in models['models']:
                if model['name'] == self.model:
                    return {
                        'name': model['name'],
                        'size': model.get('size', 'Unknown'),
                        'modified_at': model.get('modified_at', 'Unknown')
                    }
            return {'name': self.model, 'status': 'Model not found'}
        except Exception as e:
            logger.error(f"Erro ao obter informações do modelo: {e}")
            return {'name': self.model, 'status': 'Error'}
