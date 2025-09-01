# Pateta Bot 🤪

Bot do Telegram com personalidade do Pateta, integrado com Ollama local e capacidades de busca de informações via MCP (Model Context Protocol).

## 🚀 Funcionalidades

- **Chat inteligente** com personalidade do Pateta
- **Busca de notícias** em tempo real
- **Integração MCP** para ferramentas externas
- **Cache inteligente** para otimizar performance
- **Web scraping** de sites de notícias
- **Rate limiting** para evitar spam

## 🏗️ Arquitetura

```
pateta-bot/
├── main.py                 # Bot principal
├── config/                 # Configurações
├── core/                   # Núcleo do sistema
├── mcp/                    # Ferramentas MCP
├── services/               # Serviços externos
├── utils/                  # Utilitários
├── scripts/                # Scripts de deploy
└── docs/                   # Documentação
```

## 🛠️ Instalação

### Pré-requisitos
- Python 3.9+
- Ollama instalado e rodando
- Token do bot do Telegram

### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd pateta-bot
```

### 2. Configure o ambiente virtual
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

### 5. Baixe o modelo Ollama
```bash
ollama pull llama3.2
```

### 6. Execute o bot
```bash
python3 main.py
```

## 🔧 Configuração

### Variáveis de Ambiente (.env)
```env
# Bot do Telegram
BOT_TOKEN=seu_token_aqui
ALLOWED_CHAT_IDS=seu_id_aqui

# Ollama
OLLAMA_MODEL=llama3.2
OLLAMA_HOST=http://localhost:11434

# APIs (opcionais)
OPENWEATHER_API_KEY=sua_chave_aqui
NEWSAPI_API_KEY=sua_chave_aqui

# Configurações
DEFAULT_CITY=Rio de Janeiro
FAVORITE_TEAMS=flamengo,vasco,fluminense,botafogo
```

## 📱 Comandos Disponíveis

### Comandos Básicos
- `/start` - Mensagem de boas-vindas
- `/ask [pergunta]` - Faça uma pergunta para o Pateta

### Comandos de Informação
- `/news [assunto]` - Buscar notícias recentes
- `/sports [time]` - Notícias esportivas (em breve)
- `/weather [cidade]` - Clima atual (em breve)

### Exemplos de Uso
```
/ask como você está?
/ask me conte uma piada
/news flamengo
/news tecnologia
/sports flamengo
/weather Rio de Janeiro
```

## 🔍 Ferramentas MCP

### NewsTool
- **Descrição**: Busca notícias recentes sobre um assunto
- **Fontes**: Google News RSS, DuckDuckGo, Web Scraping
- **Cache**: 1 hora
- **Rate Limit**: 1 request/minuto

### SportsTool (em desenvolvimento)
- **Descrição**: Notícias esportivas por time
- **Fontes**: Sites esportivos específicos
- **Cache**: 30 minutos

### WeatherTool (em desenvolvimento)
- **Descrição**: Clima atual e previsão
- **Fonte**: OpenWeatherMap API
- **Cache**: 15 minutos

## 🚀 Deploy na Oracle Cloud

### Instalação Automática
```bash
# Na VM Oracle Cloud
ssh ubuntu@<IP_DA_VM>
wget https://raw.githubusercontent.com/seu-usuario/pateta-bot/main/scripts/install_oracle_cloud.sh
sudo bash install_oracle_cloud.sh
```

### Deploy da Máquina Local
```bash
# Na sua máquina local
./scripts/deploy_oracle_cloud.sh <IP_DA_VM>
```

## 🧪 Testes

### Teste das Ferramentas MCP
```bash
python3 test_mcp.py
```

### Teste Manual
1. Execute o bot: `python3 main.py`
2. No Telegram, envie: `/start`
3. Teste: `/news flamengo`
4. Teste: `/ask me de a ultima noticia sobre o flamengo`

## 📊 Monitoramento

### Logs
```bash
# Ver logs em tempo real
tail -f logs/pateta-bot.log

# Ver logs de ferramentas
grep "mcp" logs/pateta-bot.log
```

### Métricas
- Requests por ferramenta
- Tempo de resposta
- Taxa de cache hit/miss
- Erros por fonte

## 🔒 Segurança

### Rate Limiting
- Máximo 1 request/minuto por fonte
- Cache obrigatório para evitar spam
- Timeout de 10 segundos por request

### Validação
- Sanitização de inputs
- Validação de URLs
- Tratamento de erros

## 🛠️ Desenvolvimento

### Estrutura do Projeto
```
mcp/
├── base_tool.py        # Classe base para ferramentas
├── tools_registry.py   # Registro de ferramentas
├── news_tool.py        # Ferramenta de notícias
├── sports_tool.py      # Ferramenta de esportes
└── weather_tool.py     # Ferramenta de clima
```

### Adicionando Nova Ferramenta
1. Crie uma classe que herda de `BaseTool`
2. Implemente os métodos `execute()` e `get_parameters()`
3. Registre a ferramenta no `tools_registry`
4. Atualize a detecção de intenção

### Exemplo de Nova Ferramenta
```python
from mcp.base_tool import BaseTool

class MinhaTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="minha_tool",
            description="Descrição da minha ferramenta"
        )
    
    async def execute(self, params):
        # Implementação da ferramenta
        pass
    
    def get_parameters(self):
        return [
            {
                'name': 'param1',
                'type': 'string',
                'required': True,
                'description': 'Descrição do parâmetro'
            }
        ]
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🆘 Suporte

- **Issues**: Abra uma issue no GitHub
- **Documentação**: Veja a pasta `docs/`
- **Logs**: Verifique os logs para debug

## 🎯 Roadmap

### Próximas Funcionalidades
- [ ] Resumo matinal automático
- [ ] Mais fontes de notícias
- [ ] Interface web de admin
- [ ] Integração com mais APIs
- [ ] Sistema de backup
- [ ] Métricas avançadas

### Melhorias Técnicas
- [ ] Cache Redis
- [ ] Processamento assíncrono
- [ ] Testes automatizados
- [ ] CI/CD pipeline
- [ ] Docker container
