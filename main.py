"""
Pateta Bot - Bot do Telegram com integração MCP
"""

import os
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Importações da nova estrutura
from config.settings import BOT_TOKEN, ALLOWED_CHAT_IDS, validate_config
from core.ollama_client import OllamaClient
from mcp.tools_registry import tools_registry
from mcp.news_tool import NewsTool

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Instância global do cliente Ollama
ollama_client = None
mcp_initialized = False

def _is_allowed(chat_id: int, user_id: int) -> bool:
    """Verifica se o usuário está autorizado"""
    chat_id_str = str(chat_id)
    user_id_str = str(user_id)
    
    logger.info(f"Chat ID: {chat_id_str}, User ID: {user_id_str}, Allowed: {chat_id_str in ALLOWED_CHAT_IDS}")
    
    # Adicionar ID específico do usuário

    
    return chat_id_str in ALLOWED_CHAT_IDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para comando /start"""
    if not _is_allowed(update.effective_chat.id, update.effective_user.id):
        return
        
    logger.info(f"Comando /start recebido de {update.effective_user.first_name}")
    
    welcome_message = """Gawrsh! Olá! Eu sou o Pateta! 🤪

Estou aqui para conversar com você e buscar informações quando precisar!

Comandos disponíveis:
/start - Esta mensagem
/ask [pergunta] - Faça uma pergunta para mim
/news [assunto] - Buscar notícias (em breve!)
/sports [time] - Notícias esportivas (em breve!)
/weather [cidade] - Clima atual (em breve!)

Exemplos:
/ask como você está?
/ask me conte uma piada
/news flamengo
/sports flamengo
/weather Rio de Janeiro

Lembre-se: Eu sou o Pateta, então posso ser um pouco desajeitado, mas sempre prestativo! 😄"""

    await update.message.reply_text(welcome_message)

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para comando /ask"""
    global mcp_initialized, ollama_client
    
    if not _is_allowed(update.effective_chat.id, update.effective_user.id):
        return
        
    user_name = update.effective_user.first_name
    logger.info(f"Comando /ask recebido de {user_name}")
    
    # Inicializar MCP se necessário
    if not mcp_initialized:
        await setup_mcp_tools()
        mcp_initialized = True
    
    # Extrair pergunta do comando
    if not context.args:
        await update.message.reply_text("Gawrsh! Você precisa fazer uma pergunta! Tente: /ask como você está?")
        return
        
    question = " ".join(context.args)
    logger.info(f"Pergunta: {question}")
    
    # Mostrar que está digitando
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Processar com Ollama + MCP
        answer = await ollama_client.chat(question, user_name)
        
        await update.message.reply_text(answer)
        
    except Exception as e:
        logger.error(f"Erro ao processar pergunta: {e}")
        await update.message.reply_text("Gawrsh! Tive um problema técnico aqui! Tente novamente mais tarde!")

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para comando /news"""
    if not _is_allowed(update.effective_chat.id, update.effective_user.id):
        return
        
    user_name = update.effective_user.first_name
    logger.info(f"Comando /news recebido de {user_name}")
    
    # Extrair assunto do comando
    if not context.args:
        query = "notícias"
    else:
        query = " ".join(context.args)
    
    logger.info(f"Buscando notícias sobre: {query}")
    
    # Mostrar que está digitando
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Usar ferramenta de notícias
        news_tool = tools_registry.get_tool("news_tool")
        if news_tool:
            result = await news_tool.execute({"query": query, "limit": 3})
            
            if result.get('success') and result.get('data'):
                news_text = "📰 **Últimas Notícias:**\n\n"
                for i, item in enumerate(result['data'][:3], 1):
                    title = item.get('title', 'Sem título')
                    source = item.get('source', 'Fonte desconhecida')
                    news_text += f"{i}. {title}\n   📍 {source}\n\n"
                
                await update.message.reply_text(news_text, parse_mode='Markdown')
            else:
                await update.message.reply_text("Gawrsh! Não consegui encontrar notícias sobre isso!")
        else:
            await update.message.reply_text("Gawrsh! A ferramenta de notícias não está disponível!")
            
    except Exception as e:
        logger.error(f"Erro ao buscar notícias: {e}")
        await update.message.reply_text("Gawrsh! Tive um problema técnico aqui! Tente novamente mais tarde!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para mensagens de texto"""
    global mcp_initialized, ollama_client
    
    if not _is_allowed(update.effective_chat.id, update.effective_user.id):
        return
        
    user_name = update.effective_user.first_name
    message_text = update.message.text
    
    logger.info(f"Mensagem recebida de {user_name}: {message_text[:50]}...")
    
    # Inicializar MCP se necessário
    if not mcp_initialized:
        await setup_mcp_tools()
        mcp_initialized = True
    
    # Mostrar que está digitando
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Processar com Ollama + MCP
        answer = await ollama_client.chat(message_text, user_name)
        
        await update.message.reply_text(answer)
        
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}")
        await update.message.reply_text("Gawrsh! Tive um problema técnico aqui! Tente novamente mais tarde!")

async def setup_mcp_tools():
    """Configura as ferramentas MCP"""
    global ollama_client
    
    logger.info("Configurando ferramentas MCP...")
    
    # Registrar ferramentas
    news_tool = NewsTool()
    tools_registry.register_tool(news_tool)
    
    # Inicializar cliente Ollama
    ollama_client = OllamaClient()
    
    logger.info("Ferramentas MCP configuradas!")

def main():
    """Função principal"""
    # Validar configurações
    try:
        validate_config()
    except ValueError as e:
        logger.error(f"Erro de configuração: {e}")
        return
    
    logger.info("Iniciando bot...")
    
    # Criar aplicação
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Adicionar handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Bot rodando (polling). Ctrl+C para sair.")
    
    # Executar bot
    app.run_polling()

if __name__ == "__main__":
    main()