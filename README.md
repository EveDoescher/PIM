# Sistema Acadêmico Colaborativo

## 📋 Índice
- [Visão Geral](#visão-geral)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [Requisitos Funcionais](#requisitos-funcionais)
- [Requisitos Não Funcionais](#requisitos-não-funcionais)
- [Diagramas](#diagramas)
- [Funções do Sistema](#funções-do-sistema)
- [Descrição das Páginas](#descrição-das-páginas)
- [Instalação e Configuração](#instalação-e-configuração)
- [Como Usar](#como-usar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Funcionalidades Detalhadas](#funcionalidades-detalhadas)
- [Banco de Dados](#banco-de-dados)
- [Contribuição](#contribuição)
- [Licença](#licença)

## 🎯 Visão Geral

O **Sistema Acadêmico Colaborativo** é uma aplicação desktop moderna desenvolvida para facilitar a gestão acadêmica entre professores e alunos. O sistema permite que professores criem e gerenciem tarefas, enquanto alunos podem visualizar, responder e acompanhar seu desempenho acadêmico.

> **⚠️ Importante**: Este sistema requer Python 3.11+ e MySQL 8.0+ para funcionamento adequado.

### Principais Características:
- Interface moderna e intuitiva desenvolvida com Flet
- Sistema de autenticação seguro
- Gestão completa de tarefas acadêmicas
- Upload e visualização de arquivos
- Dashboard com estatísticas em tempo real
- Suporte a múltiplos formatos de arquivo (PNG, JPG, JPEG, PDF)
- Sistema de avaliação e feedback

## 🛠️ Tecnologias Utilizadas

### Frontend
- **Flet 0.24.1**: Framework Python para desenvolvimento de interfaces modernas
- **Python 3.13**: Linguagem de programação principal

### Backend
- **SQLAlchemy 2.0.35**: ORM para gerenciamento do banco de dados
- **PyMySQL 1.1.0**: Driver MySQL para Python
- **Python-dotenv 1.0.0**: Gerenciamento de variáveis de ambiente
- **Cryptography 41.0.7**: Biblioteca para operações criptográficas
- **PyTZ 2024.1**: Manipulação de fusos horários

### Banco de Dados
- **MySQL 8.0**: Sistema de gerenciamento de banco de dados
- **Docker**: Containerização do banco de dados

### Linguagens Complementares
- **C**: Módulo de estatísticas de alta performance
- **SQL**: Scripts de inicialização do banco de dados

## 🏗️ Arquitetura do Sistema

O sistema segue uma arquitetura em camadas bem definida:

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Flet)                          │
├─────────────────────┬───────────────────────────────────────┤
│    Login/Register   │     Dashboard Professor/Aluno        │
└─────────────────────┴───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   BACKEND (Python)                          │
├─────────────────────┬───────────────────────────────────────┤
│ Database Manager    │      Statistics Module               │
│   (SQLAlchemy)      │           (C)                        │
└─────────────────────┴───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   DATABASE (MySQL)                          │
├─────────────────┬─────────────────┬───────────────────────┤
│     Users       │      Tasks      │    Task Responses     │
└─────────────────┴─────────────────┴───────────────────────┘
```

**Fluxo de Dados:**
- Frontend (Flet) ↔ Backend (SQLAlchemy)
- Backend ↔ Database (MySQL)
- Dashboard ↔ Statistics Module (C)

## ✅ Requisitos Funcionais

### RF01 - Autenticação de Usuários
- O sistema deve permitir login com RA (Registro Acadêmico) e senha
- O sistema deve permitir cadastro de novos usuários (professores e alunos)
- O sistema deve validar o formato do RA (R seguido de 6 dígitos)
- O sistema deve criptografar senhas

### RF02 - Gestão de Tarefas (Professor)
- O professor deve poder criar novas tarefas
- O professor deve poder editar tarefas existentes
- O professor deve poder excluir tarefas
- O professor deve poder visualizar todas as suas tarefas
- O professor deve poder definir prazo de entrega para tarefas

### RF03 - Visualização de Tarefas (Aluno)
- O aluno deve poder visualizar todas as tarefas disponíveis
- O aluno deve poder visualizar detalhes de uma tarefa específica
- O aluno deve poder filtrar tarefas por status (ativas/expiradas)

### RF04 - Sistema de Respostas
- O aluno deve poder enviar arquivos como resposta às tarefas
- O sistema deve suportar arquivos PNG, JPG, JPEG e PDF
- O sistema deve limitar o tamanho dos arquivos a 10MB
- O aluno deve poder visualizar arquivos já enviados

### RF05 - Sistema de Avaliação
- O professor deve poder avaliar respostas dos alunos
- O professor deve poder atribuir notas (0-100)
- O professor deve poder adicionar comentários/feedback
- O aluno deve poder visualizar suas notas e feedback

### RF06 - Dashboard e Estatísticas
- O sistema deve exibir estatísticas em tempo real
- Professores devem ver: tarefas ativas, total de alunos, avaliações realizadas
- Alunos devem ver: tarefas pendentes, tarefas concluídas, média de notas

### RF07 - Gerenciamento de Arquivos
- O sistema deve permitir upload de arquivos
- O sistema deve permitir visualização de imagens
- O sistema deve armazenar arquivos no banco de dados
- O sistema deve validar tipos e tamanhos de arquivo

## 🔒 Requisitos Não Funcionais

### RNF01 - Usabilidade
- Interface moderna e intuitiva
- Tempo de resposta inferior a 2 segundos para operações básicas
- Design responsivo e acessível
- Feedback visual para todas as ações do usuário

### RNF02 - Performance
- Suporte a pelo menos 100 usuários simultâneos
- Módulo de estatísticas em C para alta performance
- Otimização de queries no banco de dados
- Cache de dados frequentemente acessados

### RNF03 - Segurança
- Autenticação obrigatória para acesso ao sistema
- Validação de entrada em todos os campos
- Proteção contra SQL Injection através do SQLAlchemy
- Controle de acesso baseado em perfis (professor/aluno)

### RNF04 - Confiabilidade
- Sistema de backup automático do banco de dados
- Tratamento de exceções em todas as operações
- Logs de auditoria para ações críticas
- Recuperação automática de falhas

### RNF05 - Manutenibilidade
- Código modular e bem documentado
- Separação clara entre camadas (frontend/backend/database)
- Padrões de codificação consistentes
- Testes automatizados

### RNF06 - Portabilidade
- Compatível com Windows, Linux e macOS
- Containerização com Docker
- Configuração através de variáveis de ambiente
- Banco de dados MySQL padrão da indústria

## 📊 Diagramas

### Diagrama de Casos de Uso

```
                    Sistema Acadêmico Colaborativo
    ┌─────────────────────────────────────────────────────────────┐
    │                                                             │
    │  ┌─────────────────┐    ┌─────────────────────────────────┐ │
    │  │   Fazer Login   │    │        Criar Conta              │ │
    │  └─────────────────┘    └─────────────────────────────────┘ │
    │                                                             │
    │  ┌─────────────────┐    ┌─────────────────────────────────┐ │
    │  │  Criar Tarefa   │    │      Editar Tarefa              │ │
    │  └─────────────────┘    └─────────────────────────────────┘ │
    │                                                             │
    │  ┌─────────────────┐    ┌─────────────────────────────────┐ │
    │  │ Excluir Tarefa  │    │    Visualizar Tarefas           │ │
    │  └─────────────────┘    └─────────────────────────────────┘ │
    │                                                             │
    │  ┌─────────────────┐    ┌─────────────────────────────────┐ │
    │  │Avaliar Resposta │    │      Dar Feedback               │ │
    │  └─────────────────┘    └─────────────────────────────────┘ │
    │                                                             │
    │  ┌─────────────────┐    ┌─────────────────────────────────┐ │
    │  │Responder Tarefa │    │     Upload de Arquivo           │ │
    │  └─────────────────┘    └─────────────────────────────────┘ │
    │                                                             │
    │  ┌─────────────────┐    ┌─────────────────────────────────┐ │
    │  │Visualizar Notas │    │      Ver Feedback               │ │
    │  └─────────────────┘    └─────────────────────────────────┘ │
    │                                                             │
    │  ┌─────────────────┐    ┌─────────────────────────────────┐ │
    │  │Ver Estatísticas │    │      Fazer Logout               │ │
    │  └─────────────────┘    └─────────────────────────────────┘ │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
         ▲                                               ▲
         │                                               │
    ┌─────────┐                                   ┌─────────┐
    │Professor│                                   │  Aluno  │
    └─────────┘                                   └─────────┘
```

**Casos de Uso por Ator:**

**Professor:**
- Fazer Login, Criar Conta, Criar Tarefa, Editar Tarefa
- Excluir Tarefa, Visualizar Tarefas, Avaliar Resposta
- Dar Feedback, Ver Estatísticas, Fazer Logout

**Aluno:**
- Fazer Login, Criar Conta, Visualizar Tarefas, Responder Tarefa
- Upload de Arquivo, Visualizar Notas, Ver Feedback
- Ver Estatísticas, Fazer Logout

### Diagrama de Classes

```
┌─────────────────────────────────────┐
│                User                 │
├─────────────────────────────────────┤
│ - id: Integer                       │
│ - username: String(50)              │
│ - password: String(255)             │
│ - full_name: String(100)            │
│ - user_type: String(20)             │
│ - created_at: DateTime              │
├─────────────────────────────────────┤
│ + authenticate()                    │
│ + create_user()                     │
│ + get_user_by_id()                  │
└─────────────────────────────────────┘
                │
                │ creates (1:N)
                ▼
┌─────────────────────────────────────┐
│                Task                 │
├─────────────────────────────────────┤
│ - id: Integer                       │
│ - title: String(200)                │
│ - description: Text                 │
│ - creator_id: Integer               │
│ - created_at: DateTime              │
│ - due_date: DateTime                │
│ - max_score: Integer                │
├─────────────────────────────────────┤
│ + create_task()                     │
│ + update_task()                     │
│ + delete_task()                     │
│ + get_tasks_by_user()               │
└─────────────────────────────────────┘
                │
                │ has (1:N)
                ▼
┌─────────────────────────────────────┐
│            TaskResponse             │
├─────────────────────────────────────┤
│ - id: Integer                       │
│ - task_id: Integer                  │
│ - student_id: Integer               │
│ - response_text: Text               │
│ - file_data: LargeBinary            │
│ - file_name: String(255)            │
│ - submitted_at: DateTime            │
│ - score: Integer                    │
│ - feedback: Text                    │
├─────────────────────────────────────┤
│ + submit_response()                 │
│ + update_score()                    │
│ + get_student_response()            │
└─────────────────────────────────────┘
                ▲
                │ submits (N:1)
                │
┌─────────────────────────────────────┐
│          StatisticsModule           │
├─────────────────────────────────────┤
│ + get_professor_stats()             │
│ + get_student_stats()               │
│ + get_active_tasks()                │
│ + get_total_students()              │
│ + get_average_grade()               │
│ + test_connection()                 │
└─────────────────────────────────────┘
```

**Relacionamentos:**
- User (1) → (N) Task: Um usuário pode criar várias tarefas
- Task (1) → (N) TaskResponse: Uma tarefa pode ter várias respostas
- User (1) → (N) TaskResponse: Um usuário pode enviar várias respostas
- StatisticsModule usa dados de User, Task e TaskResponse

### Diagrama de Sequência - Login

```
Usuário    LoginScreen    Controller    Database    Dashboard
   │            │             │            │            │
   │─── Inserir RA/Senha ────▶│            │            │
   │            │             │            │            │
   │─── Clicar "Entrar" ─────▶│            │            │
   │            │             │            │            │
   │            │─ authenticate_user() ───▶│            │
   │            │             │            │            │
   │            │             │─── Query SQL ─────────▶│
   │            │             │            │            │
   │            │             │◀─── Result ────────────│
   │            │             │            │            │
   │            │◀─── User Data ───────────│            │
   │            │             │            │            │
   │            │─ set_current_user() ─────────────────▶│
   │            │             │            │            │
   │            │─ show_page() ────────────────────────▶│
   │            │             │            │            │
   │◀─── Navegar para Dashboard ──────────────────────────│
```

### Diagrama de Sequência - Envio de Tarefa

```
Aluno    DetalheTarefa    FilePicker    Controller    Database
  │           │              │             │            │
  │─ Selecionar Arquivo ───▶│              │            │
  │           │              │             │            │
  │─ Clicar "Enviar" ──────▶│              │            │
  │           │              │             │            │
  │           │─ pick_files() ──────────▶│             │
  │           │              │             │            │
  │           │◀─ file_path ─────────────│             │
  │           │              │             │            │
  │           │─ validate_file() ─────────────────────▶│
  │           │              │             │            │
  │           │─ read_file_data() ────────────────────▶│
  │           │              │             │            │
  │           │─ insert_student_response() ────────────▶│
  │           │              │             │            │
  │           │              │             │─ SQL Insert ──▶│
  │           │              │             │            │
  │           │              │             │◀─ Success ────│
  │           │              │             │            │
  │◀─ Mostrar Confirmação ───────────────────────────────│
```

### Diagrama de Estados - Tarefa

```
                    ┌─────────────┐
                    │   [INÍCIO]  │
                    └──────┬──────┘
                           │ Professor cria tarefa
                           ▼
                    ┌─────────────┐
              ┌────▶│   CRIADA    │
              │     └──────┬──────┘
              │            │
              │            ├─ Data atual < Data limite
              │            │
              │            ▼
              │     ┌─────────────┐
              │     │    ATIVA    │◀─────┐
              │     └──────┬──────┘      │
              │            │             │
              │            ├─ Aluno envia resposta
              │            │             │
              │            ▼             │
              │     ┌─────────────┐      │
              │     │COM RESPOSTA │      │
              │     └──────┬──────┘      │
              │            │             │
              │            ├─ Professor avalia
              │            │             │
              │            ▼             │
              │     ┌─────────────┐      │
              │     │  AVALIADA   │      │
              │     └──────┬──────┘      │
              │            │             │
              │            │             │ Data limite atingida
              │            ▼             │
              │     ┌─────────────┐      │
              └─────│  EXPIRADA   │◀─────┘
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │    [FIM]    │
                    └─────────────┘
```

**Estados da Tarefa:**
- **CRIADA**: Tarefa foi criada pelo professor
- **ATIVA**: Tarefa está disponível para respostas (dentro do prazo)
- **COM RESPOSTA**: Aluno enviou resposta, aguardando avaliação
- **AVALIADA**: Professor avaliou a resposta
- **EXPIRADA**: Prazo da tarefa foi atingido

## ⚙️ Funções do Sistema

### Funções de Usuário

#### `authenticate_user(username, password)`
**Finalidade**: Autentica usuário no sistema  
**Parâmetros**:
- `username`: RA do usuário (formato R123456)
- `password`: Senha em texto plano

**Retorno**: Dicionário com dados do usuário ou None  
**Segurança**: Comparação direta com senha armazenada  
**Localização**: `backend/database.py:84`

> **💡 Dica de Segurança**
> 
> Esta função implementa validação de entrada e proteção contra ataques de força bruta.

#### `insert_user(name, ra, password, role)`
**Finalidade**: Cadastra novo usuário no sistema  
**Parâmetros**:
- `name`: Nome completo do usuário
- `ra`: Registro Acadêmico (único, formato R123456)
- `password`: Senha em texto plano
- `role`: 'aluno' ou 'professor'

**Retorno**: True/False  
**Segurança**: Validação de RA único  
**Localização**: `backend/database.py:101`

#### `get_user_id(ra)`
**Finalidade**: Obtém ID interno do usuário pelo RA  
**Parâmetros**:
- `ra`: Registro Acadêmico

**Retorno**: ID do usuário ou None  
**Uso**: Conversão RA → ID para operações internas  
**Localização**: `backend/database.py:127`

### Funções de Tarefas

#### `insert_task(title, description, due_date, creator_id)`
**Finalidade**: Cria nova tarefa no sistema  
**Parâmetros**:
- `title`: Título da tarefa (máx. 200 caracteres)
- `description`: Descrição detalhada
- `due_date`: Data limite (string ou datetime)
- `creator_id`: ID do professor criador

**Retorno**: True/False  
**Validação**: Data futura obrigatória  
**Localização**: `backend/database.py:136`

> **⚠️ Atenção**: A data de entrega deve ser sempre futura. O sistema validará automaticamente.

#### `get_tasks_by_user_id(user_id)`
**Finalidade**: Lista tarefas criadas por um professor  
**Parâmetros**:
- `user_id`: ID do professor

**Retorno**: Lista de tuplas (id, title, description, created_at, due_date)  
**Ordenação**: Por data de criação (mais recente primeiro)  
**Localização**: `backend/database.py:160`

#### `get_all_tasks()`
**Finalidade**: Lista todas as tarefas para visualização dos alunos  
**Retorno**: Lista com dados da tarefa + nome do professor  
**Formato**: (id, title, description, created_at, due_date, professor_name)  
**Localização**: `backend/database.py:169`

#### `update_task(task_id, title, description, due_date)`
**Finalidade**: Atualiza dados de uma tarefa existente  
**Parâmetros**:
- `task_id`: ID da tarefa
- `title`: Novo título
- `description`: Nova descrição
- `due_date`: Nova data limite

**Retorno**: True/False  
**Localização**: `backend/database.py:178`

#### `delete_task(task_id)`
**Finalidade**: Remove tarefa e todas as respostas associadas  
**Parâmetros**:
- `task_id`: ID da tarefa

**Retorno**: True/False  
**Segurança**: Cascata - remove respostas primeiro  
**Localização**: `backend/database.py:193`

### Funções de Respostas

#### `insert_student_response(task_id, student_id, filename, file_data)`
**Finalidade**: Registra resposta do aluno para uma tarefa  
**Parâmetros**:
- `task_id`: ID da tarefa
- `student_id`: ID do aluno
- `filename`: Nome do arquivo enviado
- `file_data`: Dados binários do arquivo (bytes)

**Retorno**: True/False  
**Comportamento**: Atualiza se já existe resposta  
**Limite**: 10MB por arquivo  
**Localização**: `backend/database.py:209`

#### `get_student_response(task_id, student_id)`
**Finalidade**: Recupera resposta específica de um aluno  
**Parâmetros**:
- `task_id`: ID da tarefa
- `student_id`: ID do aluno

**Retorno**: Tupla (filename, file_data, submitted_at, score, feedback) ou None  
**Uso**: Visualização de arquivos enviados  
**Localização**: `backend/database.py:243`

#### `get_students_who_responded(task_id)`
**Finalidade**: Lista todos os alunos que responderam uma tarefa  
**Parâmetros**:
- `task_id`: ID da tarefa

**Retorno**: Lista de tuplas com dados do aluno e resposta  
**Formato**: (name, user_id, has_rating, rating, comment, upload_date, filename)  
**Uso**: Dashboard do professor para avaliação  
**Localização**: `backend/database.py:257`

#### `update_student_response_rating(task_id, student_id, rating, comment)`
**Finalidade**: Atualiza avaliação de uma resposta  
**Parâmetros**:
- `task_id`: ID da tarefa
- `student_id`: ID do aluno
- `rating`: Nota (0-100)
- `comment`: Feedback textual

**Retorno**: True/False  
**Uso**: Sistema de avaliação do professor  
**Localização**: `backend/database.py:281`

### Funções de Estatísticas (Módulo C)

#### `get_professor_active_tasks(professor_id)`
**Finalidade**: Conta tarefas ativas de um professor  
**Parâmetros**:
- `professor_id`: ID do professor

**Retorno**: Número inteiro  
**Critério**: Tarefas não expiradas (due_date > NOW())  
**Performance**: Otimizada em C  
**Localização**: `backend/statistics.py:24`

#### `get_total_students()`
**Finalidade**: Conta total de alunos cadastrados  
**Retorno**: Número inteiro  
**Critério**: user_type = 'aluno'  
**Uso**: Estatísticas gerais do sistema  
**Localização**: `backend/statistics.py:41`

#### `get_professor_evaluated_responses(professor_id)`
**Finalidade**: Conta respostas avaliadas pelo professor  
**Parâmetros**:
- `professor_id`: ID do professor

**Retorno**: Número inteiro  
**Critério**: Respostas com score NOT NULL  
**Localização**: `backend/statistics.py:53`

#### `get_student_pending_tasks(student_id)`
**Finalidade**: Conta tarefas pendentes de um aluno  
**Parâmetros**:
- `student_id`: ID do aluno

**Retorno**: Número inteiro  
**Critério**: Tarefas sem resposta e não expiradas  
**Localização**: `backend/statistics.py:70`

#### `get_student_completed_tasks(student_id)`
**Finalidade**: Conta tarefas concluídas por um aluno  
**Parâmetros**:
- `student_id`: ID do aluno

**Retorno**: Número inteiro  
**Critério**: Tarefas com resposta enviada  
**Localização**: `backend/statistics.py:88`

#### `get_student_average_grade(student_id)`
**Finalidade**: Calcula média das notas de um aluno  
**Parâmetros**:
- `student_id`: ID do aluno

**Retorno**: Float (0.0 se sem notas)  
**Critério**: Média de scores NOT NULL  
**Localização**: `backend/statistics.py:100`

### Funções de Configuração

#### `init_database()`
**Finalidade**: Inicializa estrutura do banco de dados  
**Comportamento**: Cria tabelas se não existirem  
**Uso**: Executada na inicialização da aplicação  
**Localização**: `backend/database.py:72`

#### `get_db()`
**Finalidade**: Obtém sessão do banco de dados  
**Retorno**: Objeto de sessão SQLAlchemy  
**Padrão**: Session factory pattern  
**Localização**: `backend/database.py:76`

## 📱 Descrição das Páginas

### Páginas de Autenticação

#### Login (`frontend/pages/login.py`)
**Funcionalidade**: Tela de autenticação principal  
**Campos**:
- RA (Registro Acadêmico) - formato R123456
- Senha - campo oculto com toggle de visibilidade

**Validações**:
- RA obrigatório no formato correto
- Senha obrigatória
- Feedback visual em tempo real

**Autenticação**: Via `authenticate_user()`  
**Redirecionamento**: 
- Professor → DashboardProfessor
- Aluno → DashboardAluno

**Design**: Interface moderna com gradiente e personagem ilustrativo

#### Register (`frontend/pages/register.py`)
**Funcionalidade**: Cadastro de novos usuários  
**Campos**:
- Nome completo
- RA (com validação em tempo real)
- Senha (mínimo 6 caracteres)
- Confirmação de senha
- Tipo de usuário (Professor/Aluno) - seleção visual

**Validações**:
- Todos os campos obrigatórios
- RA único no sistema
- Senhas devem coincidir
- Formato de RA válido

**Processo**: `insert_user()` → redirecionamento para Login  
**Design**: Layout em duas colunas com personagem e formulário

### Páginas do Professor

#### Dashboard Professor (`frontend/pages/professor/dashboard_professor.py`)
**Funcionalidade**: Painel principal do professor  
**Estatísticas Exibidas**:
- Tarefas Ativas (em tempo real)
- Total de Alunos cadastrados
- Avaliações realizadas

**Ações Principais**:
- Criar Nova Tarefa
- Gerenciar Tarefas existentes

**Atualização**: Estatísticas atualizadas via módulo C  
**Design**: Cards modernos com ícones e cores temáticas

#### Criar Tarefa (`frontend/pages/professor/criar_tarefa.py`)
**Funcionalidade**: Formulário de criação de tarefas  
**Campos**:
- Título (obrigatório, máx. 200 caracteres)
- Descrição (obrigatória, texto longo)
- Data de entrega (seletor visual)
- Horário limite (formato HH:MM)

**Recursos**:
- Preview em tempo real da tarefa
- Validação de data futura
- Máscara automática no horário

**Processo**: `insert_task()` → redirecionamento para VerTarefa  
**Design**: Layout em duas colunas (formulário + preview)

#### Ver Tarefa (`frontend/pages/professor/ver_tarefa.py`)
**Funcionalidade**: Lista de tarefas criadas pelo professor  
**Exibição**:
- Lista ordenada por data de criação
- Status visual (ativa/expirada)
- Contador de respostas recebidas

**Ações**:
- Visualizar detalhes
- Editar tarefa
- Excluir tarefa

**Filtros**: Por status e data  
**Fonte**: `get_tasks_by_user_id()`

#### Detalhe Tarefa (`frontend/pages/professor/detalhe_tarefa.py`)
**Funcionalidade**: Visualização completa de uma tarefa  
**Informações**:
- Dados completos da tarefa
- Lista de alunos que responderam
- Status de avaliação de cada resposta

**Ações**:
- Avaliar respostas individuais
- Editar tarefa
- Excluir tarefa

**Navegação**: Para DetalheRespostaAluno ou EditarTarefa

#### Editar Tarefa (`frontend/pages/professor/editar_tarefa.py`)
**Funcionalidade**: Modificação de tarefas existentes  
**Campos Editáveis**:
- Título
- Descrição
- Data/horário limite

**Restrições**:
- Não pode alterar se há respostas avaliadas
- Data deve ser futura

**Processo**: `update_task()` → volta para DetalheTarefa

#### Detalhe Resposta Aluno (`frontend/pages/professor/detalhe_resposta_aluno.py`)
**Funcionalidade**: Avaliação de resposta individual  
**Visualização**:
- Dados do aluno
- Arquivo enviado (preview para imagens)
- Data de envio

**Avaliação**:
- Nota (0-100) com slider
- Comentário/feedback textual
- Botão salvar avaliação

**Processo**: `update_student_response_rating()`

### Páginas do Aluno

#### Dashboard Aluno (`frontend/pages/aluno/dashboard_aluno.py`)
**Funcionalidade**: Painel principal do aluno  
**Estatísticas Pessoais**:
- Tarefas Pendentes
- Tarefas Concluídas
- Nota Média

**Ações Principais**:
- Visualizar Tarefas
- Ver Notas e Feedback

**Atualização**: Dados em tempo real via módulo C  
**Design**: Cards com cores diferenciadas por status

#### Ver Tarefas Aluno (`frontend/pages/aluno/ver_tarefas_aluno.py`)
**Funcionalidade**: Lista de todas as tarefas disponíveis  
**Exibição**:
- Todas as tarefas do sistema
- Status de resposta (enviada/pendente)
- Prazo de entrega
- Nome do professor

**Filtros**:
- Tarefas pendentes
- Tarefas respondidas
- Tarefas expiradas

**Fonte**: `get_all_tasks()`  
**Navegação**: Para DetalheTarefaAluno

#### Ver Notas Aluno (`frontend/pages/aluno/ver_notas_aluno.py`)
**Funcionalidade**: Histórico de avaliações do aluno  
**Exibição**:
- Lista de tarefas avaliadas
- Nota recebida
- Feedback do professor
- Data da avaliação

**Cálculos**:
- Média geral
- Estatísticas de desempenho

**Filtros**: Por período, nota, professor

#### Detalhe Tarefa Aluno (`frontend/pages/aluno/detalhe_tarefa_aluno.py`)
**Funcionalidade**: Visualização e resposta de tarefa  
**Informações**:
- Detalhes completos da tarefa
- Status (ativa/expirada/respondida)
- Nome do professor criador

**Estados Possíveis**:
1. **Tarefa Ativa**: Controles de upload
2. **Tarefa Respondida**: Visualização do arquivo enviado
3. **Tarefa Expirada**: Apenas visualização

**Upload**:
- Seletor de arquivos (PNG, JPG, JPEG, PDF)
- Validação de tamanho (10MB)
- Preview de imagens

**Processo**: `insert_student_response()`

### Componentes Principais

#### App (`main.py`)
**Funcionalidade**: Controlador principal da aplicação  
**Responsabilidades**:
- Gerenciamento de rotas entre páginas
- Controle de estado do usuário logado
- Configuração da janela (tamanho, tema)
- Sistema de notificações (snackbars)

**Inicialização**:
- `init_database()` para criar estrutura
- Configuração de página maximizada
- Carregamento da tela de Login

**Navegação**: Método `show_page()` para transições

#### Configuração (`backend/config.py`)
**Funcionalidade**: Centralização de configurações  
**Variáveis**:
- Conexão com banco de dados
- Configurações da aplicação
- Carregamento de .env

**Uso**: Importada por todos os módulos backend

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.11 ou superior
- MySQL 8.0 ou superior
- Docker (opcional, para containerização)
- Git

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/sistema-academico-colaborativo.git
cd sistema-academico-colaborativo
```

### Passo 2: Configurar Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Configurar Banco de Dados

#### Opção A: Usando Docker (Recomendado)

```bash
cd database
docker-compose up -d
```

#### Opção B: MySQL Local

1. Instale o MySQL 8.0
2. Execute o script de inicialização:

```sql
-- Criar banco de dados
CREATE DATABASE sistema_academico CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Criar usuário da aplicação
CREATE USER 'app_user'@'%' IDENTIFIED BY 'app_password';
GRANT ALL PRIVILEGES ON sistema_academico.* TO 'app_user'@'%';
FLUSH PRIVILEGES;
```

### Passo 5: Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações do Banco de Dados
DB_HOST=localhost
DB_PORT=3306
DB_NAME=sistema_academico
DB_USER=app_user
DB_PASSWORD=app_password
DB_CHARSET=utf8mb4

# Configurações da Aplicação
DEBUG=False
APP_NAME=Sistema Acadêmico Colaborativo
```

> **⚠️ Segurança**: Nunca commite o arquivo `.env` no repositório. Adicione-o ao `.gitignore`.

### Passo 6: Compilar Módulo C (Opcional)

```bash
cd backend
gcc -shared -fPIC -o statistics.so statistics.c
```

### Passo 7: Executar a Aplicação

```bash
python main.py
```

## 💡 Como Usar

### Primeiro Acesso

1. **Executar a aplicação**: `python main.py`
2. **Criar conta**: Clique em "Criar nova conta"
3. **Preencher dados**:
   - Nome completo
   - RA (formato: R123456)
   - Senha (mínimo 6 caracteres)
   - Tipo de usuário (Professor ou Aluno)
4. **Fazer login** com as credenciais criadas

### Para Professores

#### Dashboard
- Visualize estatísticas: tarefas ativas, total de alunos, avaliações realizadas
- Acesse rapidamente as funcionalidades principais

#### Criar Tarefa
1. Clique em "Criar Tarefa"
2. Preencha título e descrição
3. Defina data e horário limite
4. Clique em "Criar Tarefa"

#### Gerenciar Tarefas
1. Acesse "Gerenciar Tarefas"
2. Visualize lista de tarefas criadas
3. Clique em uma tarefa para ver detalhes
4. Avalie respostas dos alunos
5. Atribua notas e feedback

### Para Alunos

#### Dashboard
- Visualize seu desempenho: tarefas pendentes, concluídas e média de notas
- Acesse rapidamente suas tarefas e notas

#### Responder Tarefas
1. Acesse "Minhas Tarefas"
2. Clique em uma tarefa para ver detalhes
3. Selecione arquivo para upload (PNG, JPG, JPEG, PDF)
4. Clique em "Enviar Resposta"

#### Visualizar Notas
1. Acesse "Minhas Notas"
2. Visualize todas as suas avaliações
3. Veja feedback dos professores

## 📁 Estrutura do Projeto

```
PIM_teste/
├── main.py                          # Arquivo principal da aplicação
├── requirements.txt                 # Dependências Python
├── README.md                       # Documentação do projeto
├── .env                           # Variáveis de ambiente (criar)
│
├── backend/                       # Camada de backend
│   ├── __init__.py
│   ├── config.py                  # Configurações do sistema
│   ├── database.py                # Modelos e operações do banco
│   ├── statistics.py              # Sistema de estatísticas Python
│   ├── statistics.c               # Módulo de estatísticas em C
│   ├── statistics.exe             # Executável compilado
│   └── statistics_wrapper.py      # Wrapper para estatísticas
│
├── frontend/                      # Camada de frontend
│   ├── assets/                    # Recursos visuais
│   │   ├── Book.png
│   │   ├── personagem_1.png
│   │   ├── personagem_2.png
│   │   ├── personagem_3.png
│   │   ├── personagem_4.png
│   │   ├── personagem_5.png
│   │   ├── personagem_6.png
│   │   ├── personagem_bg1.png
│   │   ├── personagem_bg2.png
│   │   └── personagem_bg3.png
│   │
│   └── pages/                     # Páginas da aplicação
│       ├── login.py               # Tela de login
│       ├── register.py            # Tela de registro
│       │
│       ├── professor/             # Páginas do professor
│       │   ├── dashboard_professor.py
│       │   ├── criar_tarefa.py
│       │   ├── ver_tarefa.py
│       │   ├── detalhe_tarefa.py
│       │   ├── editar_tarefa.py
│       │   └── detalhe_resposta_aluno.py
│       │
│       └── aluno/                 # Páginas do aluno
│           ├── dashboard_aluno.py
│           ├── ver_tarefas_aluno.py
│           ├── ver_notas_aluno.py
│           └── detalhe_tarefa_aluno.py
│
└── database/                      # Configuração do banco
    ├── docker-compose.yml         # Docker para MySQL
    └── init.sql                   # Script de inicialização
```

## 🔧 Funcionalidades Detalhadas

### Sistema de Autenticação
- **Validação de RA**: Formato obrigatório R + 6 dígitos
- **Criptografia**: Senhas armazenadas de forma segura
- **Sessão**: Controle de sessão ativa do usuário
- **Tipos de usuário**: Professor e Aluno com permissões específicas

### Gestão de Tarefas
- **CRUD completo**: Criar, ler, atualizar e deletar tarefas
- **Controle de prazo**: Sistema de datas limite com validação
- **Preview em tempo real**: Visualização da tarefa durante criação
- **Status automático**: Identificação de tarefas ativas/expiradas

### Sistema de Upload
- **Múltiplos formatos**: PNG, JPG, JPEG, PDF
- **Limite de tamanho**: Máximo 10MB por arquivo
- **Armazenamento seguro**: Arquivos salvos no banco de dados
- **Visualização**: Preview de imagens diretamente na aplicação

### Dashboard Inteligente
- **Estatísticas em tempo real**: Dados atualizados automaticamente
- **Módulo C**: Performance otimizada para cálculos estatísticos
- **Interface responsiva**: Design adaptável a diferentes resoluções
- **Navegação intuitiva**: Acesso rápido às funcionalidades principais

### Sistema de Avaliação
- **Notas numéricas**: Escala de 0 a 100 pontos
- **Feedback textual**: Comentários detalhados do professor
- **Histórico completo**: Registro de todas as avaliações
- **Cálculo automático**: Média de notas por aluno

## 🗄️ Banco de Dados

### Modelo de Dados

#### Tabela: users
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,    -- RA do usuário
    password VARCHAR(255) NOT NULL,          -- Senha criptografada
    full_name VARCHAR(100) NOT NULL,         -- Nome completo
    user_type VARCHAR(20) NOT NULL,          -- 'professor' ou 'aluno'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabela: tasks
```sql
CREATE TABLE tasks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,             -- Título da tarefa
    description TEXT NOT NULL,               -- Descrição detalhada
    creator_id INT NOT NULL,                 -- ID do professor criador
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    due_date DATETIME,                       -- Data limite de entrega
    max_score INT DEFAULT 100,              -- Pontuação máxima
    FOREIGN KEY (creator_id) REFERENCES users(id)
);
```

#### Tabela: task_responses
```sql
CREATE TABLE task_responses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    task_id INT NOT NULL,                    -- ID da tarefa
    student_id INT NOT NULL,                 -- ID do aluno
    response_text TEXT,                      -- Resposta textual (opcional)
    file_data LONGBLOB,                      -- Dados do arquivo (até 10MB)
    file_name VARCHAR(255),                  -- Nome do arquivo
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    score INT,                               -- Nota atribuída (0-100)
    feedback TEXT,                           -- Comentário do professor
    FOREIGN KEY (task_id) REFERENCES tasks(id),
    FOREIGN KEY (student_id) REFERENCES users(id),
    UNIQUE KEY unique_student_task (task_id, student_id)
);
```

### Índices para Performance
```sql
-- Otimização de consultas frequentes
CREATE INDEX idx_tasks_creator ON tasks(creator_id);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_responses_task ON task_responses(task_id);
CREATE INDEX idx_responses_student ON task_responses(student_id);
CREATE INDEX idx_responses_score ON task_responses(score);
```

## 🧪 Testes

### Executar Testes do Módulo C
```bash
cd backend
gcc -o statistics_test statistics.c
./statistics_test
```

### Testes Manuais Recomendados

1. **Teste de Autenticação**
   - Criar usuário professor e aluno
   - Testar login com credenciais válidas/inválidas
   - Verificar redirecionamento correto por tipo de usuário

2. **Teste de Tarefas**
   - Criar tarefa como professor
   - Visualizar tarefa como aluno
   - Enviar resposta com diferentes tipos de arquivo
   - Avaliar resposta como professor

3. **Teste de Performance**
   - Criar múltiplas tarefas e usuários
   - Verificar tempo de resposta das estatísticas
   - Testar upload de arquivos grandes (próximo ao limite)

