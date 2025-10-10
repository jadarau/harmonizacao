# 🎯 Harmonização AI - Sistema RAG Avançado

Um sistema de Retrieval-Augmented Generation (RAG) robusto e escalável construído com FastAPI, integrando LLMs com busca semântica para respostas baseadas em documentos, além de gerenciamento completo de clientes com MongoDB.

## 🚀 Início Rápido

### **Docker (Recomendado)**
```powershell
cd docker
.\start.ps1
```

### **Local (Desenvolvimento)**
```powershell
pip insta## 💡 Dicas

### **Sistema de Clientes**
- ✅ Use `.\start.ps1` para inicialização automática
- ✅ Acesse `/docs` para testar endpoints interativamente  
- ✅ Logs em tempo real: `docker-compose logs -f`
- ✅ Dados persistem em `C:\projects\db\harmonizacao\`
- ✅ Hot reload ativo durante desenvolvimento

### **Sistema RAG**
- 🧠 Use **sentence_transformer** para começar (gratuito)
- 📄 Prefira documentos **PDF** e **MD** para melhor extração
- 🔍 Configure **chunk_size=1000** e **overlap=200** como padrão
- 📊 Monitore métricas em `/v1/rag/stats`
- 🎯 Use **min_relevance_score=0.3** para filtragem de qualidade

## 🤝 Contribuição

1. Fork do projeto
2. Criar branch para feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit das mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para o branch (`git push origin feature/nova-funcionalidade`)
5. Criar Pull Request

## 🆘 Suporte

Para dúvidas e suporte:
- 📂 Abra uma issue no GitHub
- 📖 Consulte a documentação da API em `/docs` (Swagger UI)
- 📋 Verifique os logs em `./logs/` ou `docker-compose logs`
- 💬 Chat com sistema RAG para dúvidas sobre documentosequirements.txt
uvicorn app.main:app --reload
```

## 📋 Funcionalidades

### Sistema RAG (Retrieval-Augmented Generation)
- 🧠 **Chat Inteligente com RAG**: Respostas baseadas em documentos indexados
- 📄 **Gerenciamento de Documentos**: Upload multi-formato (PDF, TXT, MD, DOCX)
- 🔍 **Busca Semântica Avançada**: Embeddings e vector store para alta performance
- 📊 **Chunking Adaptativo**: Estratégias otimizadas de segmentação
- 🎯 **Citação de Fontes**: Referências automáticas aos documentos utilizados

### Sistema de Clientes
- ✅ **API REST** completa com FastAPI
- ✅ **CRUD de Clientes** com validação
- ✅ **MongoDB** com collections automáticas
- ✅ **Chat com IA** (Groq integration)
- ✅ **Docker** containerizado
- ✅ **Documentação** automática (Swagger)

## 🌐 Endpoints Principais

### Sistema de Clientes
| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/docs` | GET | Documentação interativa |
| `/v1/cliente/formulario` | POST | Criar cliente via formulário |
| `/v1/cliente/` | GET | Listar clientes |
| `/v1/cliente/{id}` | GET/PUT/DELETE | CRUD cliente específico |

### Chat e Conversação
| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/v1/chat` | POST | Chat tradicional (sem RAG) |
| `/v1/rag/chat` | POST | Chat com RAG |
| `/v1/rag/chat/stream` | POST | Chat RAG com streaming |

### Gerenciamento de Documentos RAG
| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/v1/rag/documents/upload` | POST | Upload de documento |
| `/v1/rag/documents/{id}/index` | POST | Indexar documento |
| `/v1/rag/documents/upload-and-index` | POST | Upload + indexação automática |
| `/v1/rag/documents` | GET | Listar documentos |
| `/v1/rag/documents/{id}` | GET/DELETE | Detalhes/deletar documento |
| `/v1/rag/documents/search` | POST | Busca semântica |
| `/v1/rag/stats` | GET | Estatísticas do sistema |

### Sistema Geral
| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/v1/healthz` | GET | Health check |

## 🏗️ Arquitetura

```
FastAPI App (Port 8000)
├── 🌐 API Routes
│   ├── Cliente (CRUD + MongoDB)
│   ├── Chat (Groq LLM) 
│   ├── RAG (Document processing & semantic search)
│   └── File (Upload/Download)
├── 🗄️ MongoDB (Port 27017)
│   ├── Database: harmonizacao
│   ├── Collection: clientes
│   └── Dados: C:\projects\db\harmonizacao\
├── 🧠 Sistema RAG
│   ├── rag/embeddings/     # Serviços de embeddings
│   ├── rag/vectorstore/    # Armazenamento vetorial (Chroma DB)
│   ├── rag/loaders/        # Carregadores multi-formato
│   ├── rag/chunking/       # Estratégias de segmentação
│   └── rag/retrieval/      # Serviços de busca semântica
└── 🤖 IA Integration
    └── Groq API (LLM + RAG-enhanced responses)
```

## 📂 Estrutura do Projeto

```
harmonizacao/
├── app/                    # Código da aplicação
│   ├── main.py            # FastAPI app principal
│   ├── models/            # Modelos Pydantic (Cliente, Endereco, Documents)
│   ├── api/routes/        # Endpoints REST
│   │   ├── cliente.py     # CRUD clientes
│   │   ├── chat.py        # Chat tradicional
│   │   ├── rag.py         # Sistema RAG
│   │   └── file.py        # Upload de arquivos
│   ├── database/          # MongoDB connection & repository
│   ├── llm/              # Integração com IA
│   │   ├── groq.py        # Cliente Groq
│   │   ├── rag_client.py  # Cliente RAG-enhanced
│   │   └── rag_deps.py    # Dependências RAG
│   ├── rag/              # Sistema RAG completo
│   │   ├── embeddings/    # Serviços de embeddings
│   │   ├── vectorstore/   # Chroma DB & vector store
│   │   ├── loaders/       # PDF, TXT, MD, DOCX loaders
│   │   ├── chunking/      # Estratégias de segmentação
│   │   └── retrieval/     # Busca semântica
│   ├── schemas/          # Validação de dados (Chat, RAG, Cliente)
│   └── services/         # Serviços de negócio (RAG service)
├── docker/                # Configuração Docker
│   ├── docker-compose.yml # Orquestração
│   ├── start.ps1         # Script Windows
│   └── README.md         # Documentação Docker
├── requirements.txt       # Dependências Python
└── README.md             # Esta documentação
```

## ⚡ Comandos Essenciais

### **Iniciar Ambiente**
```powershell
# Automático (Docker)
cd docker && .\start.ps1

# Manual
cd docker && docker-compose up --build -d

# Local
uvicorn app.main:app --reload
```

### **Verificar Status**
```powershell
docker-compose ps                    # Status containers
curl http://localhost:8000/v1/healthz  # Testar API
```

### **Parar Ambiente**
```powershell
docker-compose down           # Parar (mantém dados)
docker-compose down --volumes # Parar + limpar dados
```

### **Logs e Debug**
```powershell
docker-compose logs -f              # Todos os logs
docker-compose logs -f mongodb      # Logs MongoDB
docker-compose logs -f harmonizacao_app  # Logs API
```

## 🔧 Configuração

### **Variáveis de Ambiente (.env)**
```env
# Obrigatório - LLM
GROQ_API_KEY=sua_chave_groq_aqui

# Embeddings (Escolha uma opção)
EMBEDDING_SERVICE_TYPE=sentence_transformer  # Recomendado para início
# OU
EMBEDDING_SERVICE_TYPE=openai
OPENAI_API_KEY=your_openai_api_key_here

# Modelos de Embedding
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2  # Rápido, 384 dim
# EMBEDDING_MODEL_NAME=all-mpnet-base-v2  # Melhor qualidade, 768 dim
# EMBEDDING_MODEL_NAME=multi-qa-MiniLM-L6-cos-v1  # Otimizado para Q&A

# Processamento de Documentos RAG
DEFAULT_CHUNK_SIZE=1000
DEFAULT_CHUNK_OVERLAP=200
DEFAULT_CHUNKING_STRATEGY=recursive  # Recomendado

# MongoDB (Docker - padrão)
MONGODB_URL=mongodb://admin:admin123@mongodb:27017/harmonizacao?authSource=admin
MONGODB_DATABASE=harmonizacao
MONGODB_COLLECTION_CLIENTES=clientes

# API
ENABLE_CORS=true
CORS_ALLOW_ORIGINS=["*"]
```

### **Credenciais MongoDB**
- **Usuário**: admin
- **Senha**: admin123  
- **URL**: mongodb://localhost:27017
- **Database**: harmonizacao

## 🗄️ Banco de Dados

### **Collections Criadas Automaticamente**
- ✅ **clientes** - Dados dos clientes
- ✅ **Índices** - email, telefone, nome, created_at
- ✅ **Validação** - Schema JSON automático
- ✅ **Exemplo** - Cliente de teste inserido

### **Localização dos Dados**
- **Docker**: `C:\projects\db\harmonizacao\`
- **Backup**: Simples cópia de pasta
- **Acesso**: `mongosh -u admin -p admin123`

## 🌐 Acessos

Após inicializar:

- **API**: http://localhost:8000
- **Documentação**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc
- **MongoDB**: localhost:27017

## 📚 Documentação Detalhada

- **Docker Setup**: [docker/README.md](docker/README.md)
- **API Docs**: http://localhost:8000/docs (após iniciar)
- **Schemas**: Modelos em `app/models/`

## 🛠️ Desenvolvimento

### **Instalar Dependências**
```powershell
pip install -r requirements.txt
```

### **Rodar Local**
```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Testes**
```powershell
# Testar endpoint
curl http://localhost:8000/v1/healthz

# Criar cliente
curl -X POST "http://localhost:8000/v1/cliente/formulario" \
  -H "Content-Type: application/json" \
  -d '{"nome":"João","telefone":["11999999999"],"email":["joao@email.com"],"nascimento":"1990-01-01","enderecos":[]}'
```

## � Uso da API RAG

### **Upload e Indexação de Documento**
```powershell
# Upload simples
curl -X POST "http://localhost:8000/v1/rag/documents/upload" \
  -F "file=@documento.pdf" \
  -F "tags=manual,tecnico" \
  -F "custom_metadata={\"author\": \"João Silva\"}"

# Upload + Indexação automática
curl -X POST "http://localhost:8000/v1/rag/documents/upload-and-index" \
  -F "file=@documento.pdf" \
  -F "chunk_size=1500" \
  -F "chunking_strategy=sentence"
```

### **Chat RAG**
```powershell
# Chat com contexto
curl -X POST "http://localhost:8000/v1/rag/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Como funciona o processo de harmonização?",
    "use_rag": true,
    "max_context_chunks": 5,
    "min_relevance_score": 0.3
  }'
```

### **Busca de Documentos**
```powershell
# Busca semântica
curl -X POST "http://localhost:8000/v1/rag/documents/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "harmonização tributária",
    "max_results": 10,
    "min_score": 0.4
  }'

# Listar documentos
curl -X GET "http://localhost:8000/v1/rag/documents?page=1&page_size=20"

# Estatísticas do sistema
curl -X GET "http://localhost:8000/v1/rag/stats"
```

## 🧠 Estratégias de Chunking RAG

### **1. Recursive Chunking (Recomendado)**
- Mantém coerência semântica
- Quebra em parágrafos, frases, então caracteres
- Ideal para documentos técnicos

### **2. Fixed Size Chunking**
- Tamanho fixo com sobreposição
- Simples e previsível
- Bom para textos uniformes

### **3. Sentence Chunking**
- Baseado em frases completas
- Preserva contexto linguístico
- Ideal para textos narrativos

## ⚙️ Modelos de Embedding

### **Sentence Transformers (Recomendado)**
```python
# Modelos disponíveis:
"all-MiniLM-L6-v2"          # 384 dim, rápido, uso geral
"all-mpnet-base-v2"         # 768 dim, alta qualidade
"multi-qa-MiniLM-L6-cos-v1" # 384 dim, otimizado para Q&A
```

### **OpenAI Embeddings**
```python
# Modelos disponíveis:
"text-embedding-3-small"    # 1536 dim, custo-efetivo
"text-embedding-3-large"    # 3072 dim, máxima qualidade
"text-embedding-ada-002"    # 1536 dim, legado
```

## �🚨 Troubleshooting

### **Problemas com PowerShell (Windows)**

#### **Script bloqueado - "execução de scripts foi desabilitada"**

**Soluções rápidas:**
```powershell
# Opção 1: Bypass temporário (recomendado)
PowerShell -ExecutionPolicy Bypass -File .\start.ps1

# Opção 2: Alterar política permanente
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Opção 3: Comandos manuais (sem script)
cd docker
if (!(Test-Path ".env")) { Copy-Item ".env.example" ".env"; notepad .env }
docker-compose up --build -d
```

### **Problemas Comuns**

1. **Porta ocupada**:
   ```powershell
   netstat -ano | findstr :8000
   netstat -ano | findstr :27017
   ```

2. **MongoDB não conecta**:
   ```powershell
   docker-compose logs mongodb
   ```

3. **API não responde**:
   ```powershell
   docker-compose logs harmonizacao_app
   ```

4. **Reset completo**:
   ```powershell
   docker-compose down --volumes
   docker system prune -f
   docker-compose up --build -d
   ```

## � Deploy e Produção

### **Docker Customizado**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### **Docker Compose Avançado**
```yaml
version: '3.8'
services:
  harmonizacao-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - EMBEDDING_SERVICE_TYPE=${EMBEDDING_SERVICE_TYPE}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
```

## 📊 Monitoramento

### **Métricas Disponíveis**
- Total de documentos indexados
- Performance de busca semântica
- Estatísticas de embeddings
- Status do vector store
- Health checks de conexões

### **Logs Estruturados**
```python
import logging
logging.basicConfig(level=logging.INFO)
# Logs disponíveis em ./logs/
```

## 🔒 Segurança

- ✅ Validação de tipos de arquivo (PDF, TXT, MD, DOCX)
- ✅ Limite de tamanho de upload
- ✅ Sanitização de metadados
- ✅ Autenticação MongoDB
- ⚠️ Rate limiting (recomendado para produção)
- ⚠️ HTTPS/SSL (configurar para produção)

## �💡 Dicas

- ✅ Use `.\start.ps1` para inicialização automática
- ✅ Acesse `/docs` para testar endpoints interativamente  
- ✅ Logs em tempo real: `docker-compose logs -f`
- ✅ Dados persistem em `C:\projects\db\harmonizacao\`
- ✅ Hot reload ativo durante desenvolvimento

---

**🔗 Links Úteis:**
- [Documentação Docker](docker/README.md)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [MongoDB Docs](https://www.mongodb.com/docs/)
- [Groq API](https://groq.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [Chroma DB](https://www.trychroma.com/)

---

**Harmonização AI** - Transformando conhecimento em inteligência acessível 🚀