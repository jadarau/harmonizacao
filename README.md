# 🎯 Harmonização - API FastAPI + MongoDB + IA

Sistema completo de harmonização com API REST, banco de dados e integração com IA.

## 🚀 Início Rápido

### **Docker (Recomendado)**
```powershell
cd docker
.\start.ps1
```

### **Local (Desenvolvimento)**
```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 📋 Funcionalidades

- ✅ **API REST** completa com FastAPI
- ✅ **CRUD de Clientes** com validação
- ✅ **MongoDB** com collections automáticas
- ✅ **Chat com IA** (Groq integration)
- ✅ **Docker** containerizado
- ✅ **Documentação** automática (Swagger)

## 🌐 Endpoints Principais

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/docs` | GET | Documentação interativa |
| `/v1/cliente/formulario` | POST | Criar cliente via formulário |
| `/v1/cliente/` | GET | Listar clientes |
| `/v1/cliente/{id}` | GET/PUT/DELETE | CRUD cliente específico |
| `/v1/chat` | POST | Chat com IA |
| `/v1/healthz` | GET | Health check |

## 🏗️ Arquitetura

```
FastAPI App (Port 8000)
├── 🌐 API Routes
│   ├── Cliente (CRUD + MongoDB)
│   ├── Chat (Groq LLM) 
│   └── File (Upload/Download)
├── 🗄️ MongoDB (Port 27017)
│   ├── Database: harmonizacao
│   ├── Collection: clientes
│   └── Dados: C:\projects\db\harmonizacao\
└── 🤖 IA Integration
    └── Groq API
```

## 📂 Estrutura do Projeto

```
harmonizacao/
├── app/                    # Código da aplicação
│   ├── main.py            # FastAPI app principal
│   ├── models/            # Modelos Pydantic
│   ├── api/routes/        # Endpoints REST
│   ├── database/          # MongoDB connection & repository
│   ├── llm/              # Integração com IA
│   └── schemas/          # Validação de dados
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
# Obrigatório
GROQ_API_KEY=sua_chave_groq_aqui

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

## 🚨 Troubleshooting

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

## 💡 Dicas

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