# Harmonização AI - Sistema RAG Avançado

Um sistema de Retrieval-Augmented Generation (RAG) robusto e escalável construído com FastAPI, integrando LLMs com busca semântica para respostas baseadas em documentos.

## 🚀 Funcionalidades

### Chat Inteligente com RAG
- **Chat Tradicional**: Respostas diretas do LLM (Groq/Llama)
- **Chat RAG**: Respostas baseadas em documentos indexados
- **Streaming**: Suporte a respostas em tempo real
- **Citação de Fontes**: Referências automáticas aos documentos utilizados

### Gerenciamento de Documentos
- **Upload Multi-formato**: PDF, TXT, MD, DOCX
- **Processamento Inteligente**: Extração automática de texto
- **Chunking Adaptativo**: Estratégias otimizadas de segmentação
- **Indexação Vetorial**: Busca semântica de alta performance

### Busca Semântica Avançada
- **Embeddings**: Suporte a Sentence Transformers e OpenAI
- **Vector Store**: Chroma DB para armazenamento otimizado
- **Ranking Inteligente**: Algoritmos de relevância aprimorados
- **Filtros Flexíveis**: Busca por metadados e tags

## 🏗️ Arquitetura

```
app/
├── api/routes/          # Endpoints da API
│   ├── chat.py         # Chat tradicional
│   ├── rag.py          # RAG e gerenciamento de documentos
│   └── file.py         # Upload de arquivos
├── core/               # Configurações centrais
├── llm/                # Clientes LLM
│   ├── groq.py         # Cliente Groq
│   ├── rag_client.py   # Cliente RAG-enhanced
│   └── rag_deps.py     # Dependências RAG
├── models/             # Modelos de dados
│   └── document.py     # Modelos de documentos
├── rag/                # Sistema RAG
│   ├── embeddings/     # Serviços de embeddings
│   ├── vectorstore/    # Armazenamento vetorial
│   ├── loaders/        # Carregadores de documentos
│   ├── chunking/       # Estratégias de segmentação
│   └── retrieval/      # Serviços de busca
├── schemas/            # Schemas de API
│   ├── chat.py         # Schemas de chat
│   └── rag.py          # Schemas RAG
└── services/           # Serviços de negócio
    └── rag_service.py  # Orquestrador principal
```

## 🛠️ Instalação

### 1. Clonar o Repositório
```bash
git clone <repository-url>
cd harmonizacao
```

### 2. Criar Ambiente Virtual
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas chaves de API
```

### 5. Executar a Aplicação
```bash
# Desenvolvimento
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Produção
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📋 Configuração

### Variáveis de Ambiente Principais

```env
# LLM (Obrigatório)
GROQ_API_KEY=your_groq_api_key_here

# Embeddings (Escolha uma opção)
EMBEDDING_SERVICE_TYPE=sentence_transformer  # Recomendado para início
# OU
EMBEDDING_SERVICE_TYPE=openai
OPENAI_API_KEY=your_openai_api_key_here

# Modelos de Embedding
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2  # Rápido, 384 dim
# EMBEDDING_MODEL_NAME=all-mpnet-base-v2  # Melhor qualidade, 768 dim
# EMBEDDING_MODEL_NAME=multi-qa-MiniLM-L6-cos-v1  # Otimizado para Q&A

# Processamento de Documentos
DEFAULT_CHUNK_SIZE=1000
DEFAULT_CHUNK_OVERLAP=200
DEFAULT_CHUNKING_STRATEGY=recursive  # Recomendado
```

## 🚀 Uso da API

### 1. Upload e Indexação de Documento
```bash
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

### 2. Chat RAG
```bash
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

### 3. Busca de Documentos
```bash
# Busca semântica
curl -X POST "http://localhost:8000/v1/rag/documents/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "harmonização tributária",
    "max_results": 10,
    "min_score": 0.4
  }'
```

### 4. Gestão de Documentos
```bash
# Listar documentos
curl -X GET "http://localhost:8000/v1/rag/documents?page=1&page_size=20"

# Detalhes de um documento
curl -X GET "http://localhost:8000/v1/rag/documents/{document_id}"

# Deletar documento
curl -X DELETE "http://localhost:8000/v1/rag/documents/{document_id}"

# Estatísticas do sistema
curl -X GET "http://localhost:8000/v1/rag/stats"
```

## 🎯 Endpoints Principais

### Chat e Conversação
- `POST /v1/chat` - Chat tradicional (sem RAG)
- `POST /v1/rag/chat` - Chat com RAG
- `POST /v1/rag/chat/stream` - Chat RAG com streaming

### Gerenciamento de Documentos
- `POST /v1/rag/documents/upload` - Upload de documento
- `POST /v1/rag/documents/{id}/index` - Indexar documento
- `POST /v1/rag/documents/upload-and-index` - Upload + indexação
- `GET /v1/rag/documents` - Listar documentos
- `GET /v1/rag/documents/{id}` - Detalhes do documento
- `DELETE /v1/rag/documents/{id}` - Deletar documento

### Busca e Análise
- `POST /v1/rag/documents/search` - Busca semântica
- `GET /v1/rag/stats` - Estatísticas do sistema

## 🧠 Estratégias de Chunking

### 1. Recursive Chunking (Recomendado)
- Mantém coerência semântica
- Quebra em parágrafos, frases, então caracteres
- Ideal para documentos técnicos

### 2. Fixed Size Chunking
- Tamanho fixo com sobreposição
- Simples e previsível
- Bom para textos uniformes

### 3. Sentence Chunking
- Baseado em frases completas
- Preserva contexto linguístico
- Ideal para textos narrativos

## ⚙️ Modelos de Embedding

### Sentence Transformers (Recomendado)
```python
# Modelos disponíveis:
"all-MiniLM-L6-v2"          # 384 dim, rápido, uso geral
"all-mpnet-base-v2"         # 768 dim, alta qualidade
"multi-qa-MiniLM-L6-cos-v1" # 384 dim, otimizado para Q&A
```

### OpenAI Embeddings
```python
# Modelos disponíveis:
"text-embedding-3-small"    # 1536 dim, custo-efetivo
"text-embedding-3-large"    # 3072 dim, máxima qualidade
"text-embedding-ada-002"    # 1536 dim, legado
```

## 🔧 Personalização

### Adicionando Novos Loaders
```python
# app/rag/loaders/custom_loader.py
from app.rag.loaders.base import DocumentLoader

class CustomLoader(DocumentLoader):
    def supports_file_type(self, filename: str) -> bool:
        return filename.endswith('.custom')
    
    async def load_document(self, file_content, filename, metadata):
        # Implementar lógica customizada
        pass
```

### Configurando Vector Store Customizado
```python
# app/rag/vectorstore/custom_store.py
from app.rag.vectorstore.base import VectorStore

class CustomVectorStore(VectorStore):
    # Implementar interface customizada
    pass
```

## 🚀 Deploy

### Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  harmonizacao-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
    volumes:
      - ./data:/app/data
```

## 📊 Monitoramento

### Métricas Disponíveis
- Total de documentos indexados
- Performance de busca
- Estatísticas de embeddings
- Status do vector store

### Logs Estruturados
```python
# Configurar logging personalizado
import logging
logging.basicConfig(level=logging.INFO)
```

## 🔒 Segurança

- Validação de tipos de arquivo
- Limite de tamanho de upload
- Sanitização de metadados
- Rate limiting (recomendado)

## 🤝 Contribuição

1. Fork do projeto
2. Criar branch para feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit das mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para o branch (`git push origin feature/nova-funcionalidade`)
5. Criar Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

Para dúvidas e suporte:
- Abra uma issue no GitHub
- Consulte a documentação da API em `/docs` (Swagger UI)
- Verifique os logs em `./logs/`

---

**Harmonização AI** - Transformando conhecimento em inteligência acessível 🚀
