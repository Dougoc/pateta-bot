# Pateta Bot - Deploy na Oracle Cloud

Guia completo para instalar e executar o Pateta Bot em uma VM da Oracle Cloud.

## 📋 Pré-requisitos

- ✅ Conta Oracle Cloud (OCI)
- ✅ VM Ubuntu 20.04+ criada
- ✅ IP público da VM
- ✅ Chave SSH configurada
- ✅ Porta 22 (SSH) liberada no Security List

## 🚀 Instalação Automática

### 1. Conectar na VM
```bash
ssh ubuntu@<IP_DA_SUA_VM>
```

### 2. Executar script de instalação
```bash
# Baixar o script
wget https://raw.githubusercontent.com/seu-usuario/pateta-bot/main/install_oracle_cloud.sh

# Executar como root
sudo bash install_oracle_cloud.sh
```

### 3. Configurar o bot
```bash
# Editar configuração
sudo nano /opt/pateta-bot/.env
```

Adicione suas configurações:
```env
BOT_TOKEN=seu_token_aqui
ALLOWED_CHAT_IDS=seu_id_aqui
```

### 4. Reiniciar serviço
```bash
sudo systemctl restart pateta-bot
```

## 🔧 Instalação Manual

### 1. Atualizar sistema
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv curl wget git
```

### 2. Instalar Ollama
```bash
curl -fsSL https://ollama.ai/install.sh | sh
sudo systemctl enable ollama
sudo systemctl start ollama
```

### 3. Baixar modelo
```bash
ollama pull llama3.2
```

### 4. Configurar projeto
```bash
# Criar diretório
sudo mkdir -p /opt/pateta-bot
sudo chown ubuntu:ubuntu /opt/pateta-bot
cd /opt/pateta-bot

# Criar virtualenv
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install python-telegram-bot==21.6 ollama==0.5.3 tqdm==4.66.5 python-dotenv==1.1.1
```

### 5. Configurar serviço systemd
```bash
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

# Habilitar e iniciar
sudo systemctl daemon-reload
sudo systemctl enable pateta-bot
sudo systemctl start pateta-bot
```

## 📤 Deploy Automático

### Da sua máquina local:

1. **Tornar scripts executáveis**:
```bash
chmod +x deploy_oracle_cloud.sh
```

2. **Fazer deploy**:
```bash
./deploy_oracle_cloud.sh <IP_DA_VM>
```

## 🔍 Monitoramento

### Verificar status
```bash
sudo systemctl status pateta-bot
```

### Ver logs em tempo real
```bash
sudo journalctl -u pateta-bot -f
```

### Ver logs das últimas 100 linhas
```bash
sudo journalctl -u pateta-bot -n 100
```

## 🛠️ Comandos Úteis

```bash
# Reiniciar bot
sudo systemctl restart pateta-bot

# Parar bot
sudo systemctl stop pateta-bot

# Iniciar bot
sudo systemctl start pateta-bot

# Verificar se Ollama está rodando
sudo systemctl status ollama

# Ver modelos disponíveis
ollama list

# Testar modelo
ollama run llama3.2 "Olá, como você está?"
```

## 🔧 Troubleshooting

### Bot não inicia
```bash
# Verificar logs
sudo journalctl -u pateta-bot -f

# Verificar se Ollama está rodando
sudo systemctl status ollama

# Verificar se o modelo está baixado
ollama list
```

### Ollama não responde
```bash
# Reiniciar Ollama
sudo systemctl restart ollama

# Verificar se há espaço em disco
df -h

# Verificar uso de memória
free -h
```

### Problemas de rede
```bash
# Verificar conectividade
ping 8.8.8.8

# Verificar DNS
nslookup google.com

# Verificar portas abertas
sudo netstat -tlnp
```

## 📊 Recursos Recomendados

Para uma VM na Oracle Cloud, recomendo:

- **CPU**: 2 vCPUs mínimo (4 recomendado)
- **RAM**: 8GB mínimo (16GB recomendado)
- **Storage**: 50GB mínimo (100GB recomendado)
- **OS**: Ubuntu 20.04 LTS ou 22.04 LTS

## 🔒 Segurança

### Firewall
```bash
# Instalar UFW
sudo apt install ufw

# Configurar regras
sudo ufw allow ssh
sudo ufw allow 11434  # Porta do Ollama (se necessário)
sudo ufw enable
```

### Atualizações automáticas
```bash
# Instalar unattended-upgrades
sudo apt install unattended-upgrades

# Configurar
sudo dpkg-reconfigure -plow unattended-upgrades
```

## 💰 Custos Estimados

- **VM Standard.E2.1.Micro**: ~$0.01/hora
- **VM Standard.E2.2.Micro**: ~$0.02/hora
- **VM Standard.E3.Flex**: ~$0.03/hora

**Custo mensal estimado**: $7-30 dependendo da configuração.

## 🎯 Próximos Passos

1. ✅ Instalar na VM
2. ✅ Configurar token do bot
3. ✅ Testar funcionamento
4. 🔄 Configurar monitoramento
5. 🔄 Configurar backup
6. 🔄 Configurar SSL (se necessário)
