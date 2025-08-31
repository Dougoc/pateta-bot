import os, asyncio
from typing import Optional
from telegram import Update
from telegram.constants import ChatType
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALLOWED_CHAT_IDS = {cid.strip() for cid in os.getenv("ALLOWED_CHAT_IDS","").split(",") if cid.strip()}

assert BOT_TOKEN, "Defina BOT_TOKEN"
assert OPENAI_API_KEY, "Defina OPENAI_API_KEY"

client = OpenAI(api_key=OPENAI_API_KEY)

MODEL = "gpt-4o-mini"  # leve, barato e bom para chat
SYSTEM = (
    "Você é um assistente útil de um grupo de amigos no Telegram. "
    "Responda de forma objetiva, cite passos quando útil e não exponha chaves/segredos."
)

def _is_allowed(update: Update) -> bool:
    if not ALLOWED_CHAT_IDS:
        return True
    chat_id = str(update.effective_chat.id) if update.effective_chat else ""
    user_id = str(update.effective_user.id) if update.effective_user else ""
    return (chat_id in ALLOWED_CHAT_IDS) or (user_id in ALLOWED_CHAT_IDS)

async def _ask_llm(prompt: str, user: Optional[str]) -> str:
    # Mensagens no formato Chat Completions
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt if not user else f"[{user}] {prompt}"}
        ],
        temperature=0.2,
        max_tokens=800,
    )
    return resp.choices[0].message.content.strip()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_allowed(update):
        return
    await update.message.reply_text("Oi! Me use com /ask <pergunta> ou marcando @nome_do_bot no grupo.")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_allowed(update):
        return
    q = " ".join(context.args).strip()
    if not q:
        await update.message.reply_text("Uso: /ask <sua pergunta>")
        return
    await update.message.chat.send_action(action="typing")
    answer = await _ask_llm(q, update.effective_user.full_name if update.effective_user else None)
    await update.message.reply_text(answer, disable_web_page_preview=True)

async def on_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde quando for mencionado no grupo ou quando a mensagem começar com ! ou /ask."""
    if not _is_allowed(update):
        return
    msg = update.effective_message
    if not msg or not msg.text:
        return

    text = msg.text.strip()
    bot_username = (await context.bot.get_me()).username

    mentioned = f"@{bot_username}" in text
    starts_bang = text.startswith("!")
    if not (mentioned or starts_bang):
        return

    # Limpa a menção ou o prefixo "!"
    cleaned = text.replace(f"@{bot_username}", "").strip()
    if cleaned.startswith("!"):
        cleaned = cleaned[1:].strip()
    if not cleaned:
        return

    await msg.chat.send_action(action="typing")
    answer = await _ask_llm(cleaned, update.effective_user.full_name if update.effective_user else None)
    # Responde em thread (tópico) se existir, senão reply normal
    await msg.reply_text(answer, disable_web_page_preview=True)

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))

    # Em grupos: mencione @bot ou use "!"
    app.add_handler(MessageHandler(
        filters.TEXT & (filters.ChatType.GROUPS),
        on_group_message
    ))

    print("Bot rodando (polling). Ctrl+C para sair.")
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    asyncio.run(main())