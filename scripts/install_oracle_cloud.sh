#!/bin/bash

# Script de instalação para Oracle Cloud VM
# Execute como: sudo bash install_oracle_cloud.sh

echo "🚀 Instalando Pateta Bot na Oracle Cloud VM..."

# Atualizar sistema
echo "📦 Atualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependências do sistema
echo "🔧 Instalando dependências..."
sudo apt install -y python3 python3-pip python3-venv curl wget git

# Instalar Ollama
echo "🤖 Instalando Ollama..."
curl -fsSL https://ollama.ai/install.sh | sh

# Iniciar Ollama como serviço
echo "🔄 Configurando Ollama como serviço..."
sudo systemctl enable ollama
sudo systemctl start ollama

# Aguardar Ollama inicializar
echo "⏳ Aguardando Ollama inicializar..."
sleep 10

# Baixar modelo
echo "📥 Baixando modelo llama3.2..."
ollama pull llama3.2

# Criar diretório do projeto
echo "📁 Criando diretório do projeto..."
mkdir -p /opt/pateta-bot
cd /opt/pateta-bot

# Criar virtualenv
echo "🐍 Criando ambiente virtual..."
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências Python
echo "📦 Instalando dependências Python..."
pip install --upgrade pip
pip install python-telegram-bot==21.6 ollama==0.5.3 tqdm==4.66.5 python-dotenv==1.1.1

# Criar arquivo de configuração
echo "⚙️ Criando arquivo de configuração..."
cat > .env << EOF
BOT_TOKEN=
ALLOWED_CHAT_IDS=
EOF

# Criar script de inicialização
echo "🔄 Criando script de inicialização..."
cat > start_bot.sh << 'EOF'
#!/bin/bash
cd /opt/pateta-bot
source .venv/bin/activate
python3 main.py
EOF

chmod +x start_bot.sh

# Criar serviço systemd
echo "🔧 Criando serviço systemd..."
sudo tee /etc/systemd/system/pateta-bot.service > /dev/null << EOF
[Unit]
Description=Pateta Bot Telegram
After=network.target ollama.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/pateta-bot
Environment=PATH=/opt/pateta-bot/.venv/bin
ExecStart=/opt/pateta-bot/.venv/bin/python3 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Habilitar e iniciar serviço
echo "🚀 Habilitando e iniciando serviço..."
sudo systemctl daemon-reload
sudo systemctl enable pateta-bot
sudo systemctl start pateta-bot

echo "✅ Instalação concluída!"
echo ""
echo "📋 Comandos úteis:"
echo "  Verificar status: sudo systemctl status pateta-bot"
echo "  Ver logs: sudo journalctl -u pateta-bot -f"
echo "  Reiniciar: sudo systemctl restart pateta-bot"
echo "  Parar: sudo systemctl stop pateta-bot"
echo ""
echo "🔧 Para configurar o bot:"
echo "  1. Edite o arquivo .env: nano /opt/pateta-bot/.env"
echo "  2. Adicione seu BOT_TOKEN e ALLOWED_CHAT_IDS"
echo "  3. Reinicie o serviço: sudo systemctl restart pateta-bot"
