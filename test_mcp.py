"""
Script de teste para verificar funcionamento do MCP
"""

import asyncio
import logging
from mcp.tools_registry import tools_registry
from mcp.news_tool import NewsTool
from core.ollama_client import OllamaClient

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_news_tool():
    """Testa a ferramenta de notícias"""
    print("🔍 Testando ferramenta de notícias...")
    
    # Registrar ferramenta
    news_tool = NewsTool()
    tools_registry.register_tool(news_tool)
    
    # Testar busca
    try:
        result = await news_tool.execute({"query": "flamengo", "limit": 2})
        print(f"✅ Resultado: {result}")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

async def test_ollama_integration():
    """Testa integração com Ollama"""
    print("🤖 Testando integração com Ollama...")
    
    try:
        client = OllamaClient()
        
        # Testar detecção de ferramenta
        tool_info = tools_registry.detect_tool_needed("me de a ultima noticia sobre o flamengo")
        print(f"🔍 Detecção de ferramenta: {tool_info}")
        
        # Testar chat simples
        response = await client.chat("Olá, como você está?", "Teste")
        print(f"💬 Resposta: {response[:100]}...")
        
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

async def test_tools_registry():
    """Testa o registro de ferramentas"""
    print("📋 Testando registro de ferramentas...")
    
    try:
        # Listar ferramentas
        tools = tools_registry.list_tools()
        print(f"✅ Ferramentas registradas: {len(tools)}")
        
        # Obter descrições
        descriptions = tools_registry.get_tool_descriptions()
        print(f"📝 Descrições: {descriptions}")
        
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

async def main():
    """Função principal de teste"""
    print("🚀 Iniciando testes MCP...")
    
    tests = [
        test_tools_registry,
        test_news_tool,
        test_ollama_integration
    ]
    
    results = []
    for test in tests:
        try:
            result = await test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erro no teste: {e}")
            results.append(False)
    
    # Resumo
    print("\n📊 Resumo dos testes:")
    print(f"✅ Passou: {sum(results)}/{len(results)}")
    print(f"❌ Falhou: {len(results) - sum(results)}/{len(results)}")
    
    if all(results):
        print("🎉 Todos os testes passaram!")
    else:
        print("⚠️  Alguns testes falharam!")

if __name__ == "__main__":
    asyncio.run(main())
