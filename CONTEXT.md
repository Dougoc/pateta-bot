# Pateta Bot - Contexto e Plano de Implementação

## 🎯 Visão Geral

O Pateta Bot é um bot do Telegram que utiliza Ollama local para processamento de linguagem natural, com capacidade de buscar informações na internet através de MCP (Model Context Protocol).

## 🏗️ Arquitetura Proposta

```
pateta-bot/
├── main.py                 # Bot principal
├── config/
│   ├── __init__.py
│   ├── settings.py         # Configurações
│   └── logging_config.py   # Configuração de logs
├── core/
│   ├── __init__.py
│   ├── bot_handlers.py     # Handlers do Telegram
│   └── ollama_client.py     # Cliente Ollama
├── mcp/
│   ├── __init__.py
│   ├── base_tool.py        # Classe base para ferramentas
│   ├── news_tool.py        # Ferramenta de notícias
│   ├── sports_tool.py      # Ferramenta de esportes
│   ├── weather_tool.py     # Ferramenta de clima
│   └── tools_registry.py   # Registro de ferramentas
├── services/
│   ├── __init__.py
│   ├── news_service.py     # Serviço de notícias
│   ├── sports_service.py   # Serviço de esportes
│   └── weather_service.py  # Serviço de clima
├── utils/
│   ├── __init__.py
│   ├── cache_manager.py    # Gerenciamento de cache
│   ├── web_scraper.py      # Web scraping
│   └── text_processor.py   # Processamento de texto
├── scripts/
│   ├── install_oracle_cloud.sh
│   ├── deploy_oracle_cloud.sh
│   └── daily_news.py       # Script para resumo diário
└── docs/
    ├── README.md
    ├── README_ORACLE_CLOUD.md
    └── API.md
```

## 🔧 Implementação MCP (Model Context Protocol)

### Fase 1: Estrutura Base MCP
- [ ] Criar classe base `BaseTool`
- [ ] Implementar sistema de registro de ferramentas
- [ ] Integrar com Ollama via MCP
- [ ] Sistema de cache para ferramentas

### Fase 2: Ferramentas de Informação
- [ ] **NewsTool**: Busca notícias por cidade/assunto
- [ ] **SportsTool**: Notícias esportivas por time
- [ ] **WeatherTool**: Clima atual por cidade
- [ ] **SearchTool**: Busca geral na web

### Fase 3: Integração com Ollama
- [ ] Modificar prompt do sistema para incluir ferramentas
- [ ] Implementar detecção de intenção do usuário
- [ ] Sistema de fallback para ferramentas
- [ ] Logs detalhados de uso das ferramentas

## 📋 Plano de Implementação Detalhado

### Etapa 1: Reorganização da Estrutura (1-2 dias)
```
1. Criar estrutura de pastas
2. Mover arquivos existentes
3. Refatorar imports
4. Testar funcionamento básico
```

### Etapa 2: Implementação MCP Base (2-3 dias)
```
1. Classe BaseTool com métodos:
   - execute(params)
   - get_description()
   - get_parameters()
   - validate_input()

2. ToolsRegistry com:
   - register_tool()
   - get_tool()
   - list_tools()
   - execute_tool()

3. Integração com Ollama:
   - Modificar prompt do sistema
   - Adicionar instruções de uso das ferramentas
   - Sistema de detecção de necessidade de ferramenta
```

### Etapa 3: Ferramenta de Notícias (2-3 dias)
```
1. NewsTool implementação:
   - Google News RSS
   - Web scraping de sites locais
   - Cache de 1 hora
   - Rate limiting

2. Fontes de notícias:
   - Google News (RSS)
   - Sites locais (scraping)
   - Fallback para DuckDuckGo

3. Comandos:
   - /news [cidade]
   - /news [assunto]
   - Resumo automático matinal
```

### Etapa 4: Ferramenta de Esportes (1-2 dias)
```
1. SportsTool implementação:
   - Sites esportivos específicos
   - RSS feeds de times
   - Cache de 30 minutos

2. Times suportados:
   - Flamengo (prioridade)
   - Outros times brasileiros
   - Times internacionais

3. Comandos:
   - /sports [time]
   - /flamengo (atalho)
   - /scores (placares)
```

### Etapa 5: Ferramenta de Clima (1-2 dias)
```
1. WeatherTool implementação:
   - OpenWeatherMap API (gratuita)
   - Cache de 15 minutos
   - Múltiplas cidades

2. Funcionalidades:
   - Clima atual
   - Previsão para 5 dias
   - Alertas meteorológicos

3. Comandos:
   - /weather [cidade]
   - /clima [cidade]
```

### Etapa 6: Integração e Testes (2-3 dias)
```
1. Integração completa:
   - Testar todas as ferramentas
   - Ajustar prompts do Ollama
   - Otimizar performance

2. Testes:
   - Testes unitários
   - Testes de integração
   - Testes de carga

3. Documentação:
   - README atualizado
   - Exemplos de uso
   - Troubleshooting
```

## 🔄 Fluxo de Processamento

### Fluxo Principal:
```
1. Usuário envia mensagem
2. Bot analisa intenção
3. Se precisa de informação externa:
   - Identifica ferramenta necessária
   - Executa ferramenta via MCP
   - Obtém dados
   - Formata para Ollama
4. Ollama processa com contexto
5. Retorna resposta formatada
```

### Exemplo de Fluxo:
```
Usuário: "me de a ultima noticia sobre o flamengo"

1. Bot detecta: precisa de notícias esportivas
2. Executa: SportsTool.execute({"team": "flamengo"})
3. Obtém: 3-5 notícias recentes
4. Formata: "Contexto: [notícias formatadas]"
5. Ollama: Processa e responde como Pateta
6. Retorna: Resposta personalizada do Pateta
```

## 🛠️ Tecnologias e APIs

### APIs Gratuitas:
- **Google News RSS**: Notícias gerais
- **OpenWeatherMap**: Clima (1000 calls/dia grátis)
- **DuckDuckGo Instant Answer**: Busca geral
- **Wikipedia API**: Informações estruturadas

### Web Scraping:
- **BeautifulSoup4**: Parsing HTML
- **Requests**: HTTP requests
- **Rate limiting**: 1 request/minuto por fonte
- **User-Agent rotation**: Evitar bloqueios

### Cache:
- **Redis** (opcional) ou **arquivo JSON**
- **TTL**: 15min-1hora dependendo da fonte
- **Compressão**: Para economizar espaço

## 📊 Monitoramento e Logs

### Logs Estruturados:
```
- Uso de ferramentas
- Performance de cada API
- Erros e fallbacks
- Cache hit/miss rates
- Tempo de resposta
```

### Métricas:
- Requests por ferramenta
- Tempo médio de resposta
- Taxa de sucesso
- Uso de cache
- Erros por fonte

## 🔒 Segurança e Limites

### Rate Limiting:
- Máximo 1 request/minuto por fonte
- Cache obrigatório para evitar spam
- Fallback para fontes alternativas

### Validação:
- Sanitização de inputs
- Validação de URLs
- Timeout de requests
- Tratamento de erros

### Privacidade:
- Não armazenar dados pessoais
- Logs anonimizados
- Cache temporário apenas

## 🚀 Próximos Passos

### Imediato (Esta Semana):
1. ✅ Criar estrutura de pastas
2. ✅ Implementar BaseTool
3. ✅ Criar NewsTool básico
4. ✅ Testar integração com Ollama

### Curto Prazo (Próximas 2 Semanas):
1. 🔄 Implementar todas as ferramentas
2. 🔄 Sistema de cache robusto
3. 🔄 Testes completos
4. 🔄 Documentação

### Médio Prazo (Próximo Mês):
1. 🔄 Resumo matinal automático
2. 🔄 Mais fontes de dados
3. 🔄 Interface web de admin
4. 🔄 Deploy na Oracle Cloud

## 💡 Considerações Especiais

### Integração Ollama:
- Usar MCP para comunicação estruturada
- Manter contexto entre ferramentas
- Preservar personalidade do Pateta
- Logs detalhados para debug

### Performance:
- Cache agressivo para APIs externas
- Processamento assíncrono quando possível
- Timeout adequado para cada fonte
- Fallback automático

### Manutenibilidade:
- Código modular e testável
- Configuração centralizada
- Logs estruturados
- Documentação completa
