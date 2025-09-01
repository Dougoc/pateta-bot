#!/bin/bash

# Script para fazer deploy do código na Oracle Cloud VM
# Execute na sua máquina local

echo "🚀 Fazendo deploy do Pateta Bot para Oracle Cloud VM..."

# Verificar se o IP da VM foi fornecido
if [ -z "$1" ]; then
    echo "❌ Erro: Forneça o IP da VM"
    echo "Uso: ./deploy_oracle_cloud.sh <IP_DA_VM>"
    echo "Exemplo: ./deploy_oracle_cloud.sh 192.168.1.100"
    exit 1
fi

VM_IP=$1
SSH_USER="ubuntu"  # Ajuste se necessário

echo "📡 Conectando à VM: $VM_IP"

# Criar arquivo de configuração temporário
echo "⚙️ Criando arquivo de configuração..."
cat > .env.temp << EOF
BOT_TOKEN=
ALLOWED_CHAT_IDS=
EOF

# Fazer upload dos arquivos
echo "📤 Fazendo upload dos arquivos..."
scp main.py requirements.txt README.md .env.temp $SSH_USER@$VM_IP:/tmp/

# Executar comandos na VM
echo "🔧 Configurando na VM..."
ssh $SSH_USER@$VM_IP << 'EOF'
    # Parar o serviço se estiver rodando
    sudo systemctl stop pateta-bot 2>/dev/null || true
    
    # Copiar arquivos para o diretório do projeto
    sudo cp /tmp/main.py /opt/pateta-bot/
    sudo cp /tmp/requirements.txt /opt/pateta-bot/
    sudo cp /tmp/README.md /opt/pateta-bot/
    sudo cp /tmp/.env.temp /opt/pateta-bot/.env
    
    # Ajustar permissões
    sudo chown -R ubuntu:ubuntu /opt/pateta-bot/
    
    # Atualizar dependências
    cd /opt/pateta-bot
    source .venv/bin/activate
    pip install -r requirements.txt
    
    # Reiniciar serviço
    sudo systemctl restart pateta-bot
    
    # Verificar status
    sudo systemctl status pateta-bot --no-pager
EOF

# Limpar arquivo temporário
rm .env.temp

echo "✅ Deploy concluído!"
echo ""
echo "📋 Para verificar se está funcionando:"
echo "  ssh $SSH_USER@$VM_IP"
echo "  sudo journalctl -u pateta-bot -f"
echo ""
echo "🔧 Para configurar o bot:"
echo "  ssh $SSH_USER@$VM_IP"
echo "  sudo nano /opt/pateta-bot/.env"
echo "  sudo systemctl restart pateta-bot"
