# Pateta Bot - Telegram Bot com Ollama Local

Um bot do Telegram que usa o Ollama (IA local) para responder perguntas e conversar com usuários.

## Configuração

### 1. Instalar Ollama
1. Instale o Ollama: `brew install ollama`
2. Inicie o servidor: `ollama serve`
3. Baixe o modelo: `ollama pull llama3.2`

### 2. Configurar variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
BOT_TOKEN=
ALLOWED_CHAT_IDS=
```

### 3. Instalar dependências
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Executar o bot
```bash
source .venv/bin/activate
python3 main.py
```

## Comandos

- `/start` - Inicia o bot
- `/ask <pergunta>` - Faz uma pergunta ao bot
- `@nome_do_bot <pergunta>` - Menciona o bot em grupos
- `!<pergunta>` - Usa exclamação em grupos

## Vantagens do Ollama Local

- ✅ **100% Gratuito** - Sem custos de API
- ✅ **Local** - Processa tudo no seu computador
- ✅ **Privacidade** - Dados não saem do seu PC
- ✅ **Sem limites** - Use quantas vezes quiser
- ✅ **Offline** - Funciona sem internet
- ✅ **Logs detalhados** - Fácil debug e monitoramento
