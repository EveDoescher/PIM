# Diagramas e Requisitos - Sistema Acadêmico Colaborativo

## 📋 Índice

1. [Requisitos Funcionais](#requisitos-funcionais)
2. [Requisitos Não Funcionais](#requisitos-não-funcionais)
3. [Diagrama de Casos de Uso](#diagrama-de-casos-de-uso)
4. [Diagrama de Classes](#diagrama-de-classes)
5. [Diagramas de Sequência](#diagramas-de-sequência)
6. [Modelo Entidade-Relacionamento](#modelo-entidade-relacionamento)
7. [Arquitetura do Sistema](#arquitetura-do-sistema)

## 🎯 Requisitos Funcionais

### RF01 - Autenticação e Autorização
- **Descrição**: O sistema deve permitir login de usuários com RA e senha
- **Prioridade**: Alta
- **Atores**: Professor, Aluno
- **Pré-condições**: Usuário deve estar cadastrado no sistema
- **Fluxo Principal**:
  1. Usuário acessa tela de login
  2. Insere RA no formato R123456
  3. Insere senha
  4. Sistema valida credenciais
  5. Redireciona para dashboard apropriado
- **Fluxos Alternativos**:
  - FA01: Credenciais inválidas - exibir mensagem de erro
  - FA02: Usuário não cadastrado - redirecionar para cadastro

### RF02 - Cadastro de Usuários
- **Descrição**: O sistema deve permitir cadastro de novos usuários
- **Prioridade**: Alta
- **Atores**: Professor, Aluno
- **Pré-condições**: Nenhuma
- **Fluxo Principal**:
  1. Usuário acessa tela de cadastro
  2. Preenche nome completo, RA, senha e tipo de usuário
  3. Sistema valida dados
  4. Cria novo usuário no banco de dados
  5. Confirma cadastro realizado
- **Regras de Negócio**:
  - RN01: RA deve ser único no sistema
  - RN02: RA deve seguir formato R + 6 dígitos
  - RN03: Senha deve ter no mínimo 6 caracteres

### RF03 - Gestão de Tarefas (Professor)
- **Descrição**: Professor deve poder criar, editar e excluir tarefas
- **Prioridade**: Alta
- **Atores**: Professor
- **Pré-condições**: Usuário logado como professor
- **Fluxo Principal**:
  1. Professor acessa área de gestão de tarefas
  2. Seleciona ação desejada (criar/editar/excluir)
  3. Preenche/modifica dados da tarefa
  4. Sistema salva alterações
  5. Confirma operação realizada

### RF04 - Submissão de Respostas (Aluno)
- **Descrição**: Aluno deve poder enviar respostas para tarefas
- **Prioridade**: Alta
- **Atores**: Aluno
- **Pré-condições**: Usuário logado como aluno, tarefa disponível
- **Fluxo Principal**:
  1. Aluno visualiza tarefa disponível
  2. Acessa formulário de resposta
  3. Insere resposta (texto ou arquivo)
  4. Submete resposta
  5. Sistema confirma recebimento
- **Regras de Negócio**:
  - RN04: Arquivo deve ter no máximo 10MB
  - RN05: Aluno pode reenviar resposta até o prazo
  - RN06: Após prazo, submissão é bloqueada

### RF05 - Avaliação de Respostas (Professor)
- **Descrição**: Professor deve poder avaliar respostas dos alunos
- **Prioridade**: Alta
- **Atores**: Professor
- **Pré-condições**: Resposta submetida pelo aluno
- **Fluxo Principal**:
  1. Professor acessa lista de respostas
  2. Seleciona resposta para avaliar
  3. Visualiza conteúdo da resposta
  4. Atribui nota (0-100)
  5. Adiciona comentários de feedback
  6. Salva avaliação

### RF06 - Visualização de Notas (Aluno)
- **Descrição**: Aluno deve poder visualizar suas notas e feedback
- **Prioridade**: Média
- **Atores**: Aluno
- **Pré-condições**: Usuário logado como aluno, avaliação realizada
- **Fluxo Principal**:
  1. Aluno acessa área de notas
  2. Visualiza lista de tarefas avaliadas
  3. Seleciona tarefa para ver detalhes
  4. Visualiza nota e comentários do professor

### RF07 - Dashboard com Estatísticas
- **Descrição**: Sistema deve exibir estatísticas relevantes para cada tipo de usuário
- **Prioridade**: Média
- **Atores**: Professor, Aluno
- **Pré-condições**: Usuário logado
- **Fluxo Principal**:
  1. Usuário acessa dashboard
  2. Sistema calcula estatísticas em tempo real
  3. Exibe métricas relevantes ao perfil do usuário

### RF08 - Gerenciamento de Arquivos
- **Descrição**: Sistema deve permitir upload e download de arquivos
- **Prioridade**: Média
- **Atores**: Aluno, Professor
- **Pré-condições**: Usuário autenticado
- **Fluxo Principal**:
  1. Usuário seleciona arquivo para upload
  2. Sistema valida tipo e tamanho
  3. Armazena arquivo no banco de dados
  4. Permite download posterior

## 🔧 Requisitos Não Funcionais

### RNF01 - Performance
- **Descrição**: O sistema deve responder em até 3 segundos para operações normais
- **Categoria**: Performance
- **Critério**: Tempo de resposta < 3s para 95% das operações
- **Método de Teste**: Testes de carga com JMeter

### RNF02 - Usabilidade
- **Descrição**: Interface deve ser intuitiva e acessível
- **Categoria**: Usabilidade
- **Critério**: Usuário deve conseguir realizar tarefas básicas sem treinamento
- **Método de Teste**: Testes de usabilidade com usuários reais

### RNF03 - Confiabilidade
- **Descrição**: Sistema deve ter disponibilidade de 99% durante horário comercial
- **Categoria**: Confiabilidade
- **Critério**: Uptime > 99% entre 8h-18h
- **Método de Teste**: Monitoramento contínuo

### RNF04 - Segurança
- **Descrição**: Dados devem ser protegidos contra acesso não autorizado
- **Categoria**: Segurança
- **Critério**: Implementar autenticação, autorização e criptografia
- **Método de Teste**: Testes de penetração

### RNF05 - Escalabilidade
- **Descrição**: Sistema deve suportar até 1000 usuários simultâneos
- **Categoria**: Escalabilidade
- **Critério**: Manter performance com 1000 usuários ativos
- **Método de Teste**: Testes de carga progressiva

### RNF06 - Compatibilidade
- **Descrição**: Sistema deve funcionar em Windows, Linux e macOS
- **Categoria**: Compatibilidade
- **Critério**: Execução sem erros nos 3 sistemas operacionais
- **Método de Teste**: Testes em ambientes diversos

### RNF07 - Manutenibilidade
- **Descrição**: Código deve ser bem documentado e modular
- **Categoria**: Manutenibilidade
- **Critério**: Cobertura de documentação > 80%
- **Método de Teste**: Revisão de código

### RNF08 - Portabilidade
- **Descrição**: Sistema deve ser facilmente implantado em diferentes ambientes
- **Categoria**: Portabilidade
- **Critério**: Instalação automatizada via Docker
- **Método de Teste**: Deploy em ambientes de teste

## 📊 Diagrama de Casos de Uso

```
                    Sistema Acadêmico Colaborativo
    
    ┌─────────────────────────────────────────────────────────────────┐
    │                                                                 │
    │  Professor                              Aluno                   │
    │     │                                     │                     │
    │     │──── Fazer Login ────────────────────│                     │
    │     │                                     │                     │
    │     │──── Criar Tarefa                   │                     │
    │     │                                     │                     │
    │     │──── Editar Tarefa                  │                     │
    │     │                                     │                     │
    │     │──── Excluir Tarefa                 │                     │
    │     │                                     │                     │
    │     │──── Visualizar Tarefas ────────────│                     │
    │     │                                     │                     │
    │     │──── Avaliar Respostas              │                     │
    │     │                                     │                     │
    │     │──── Ver Estatísticas ──────────────│                     │
    │     │                                     │                     │
    │     │                              ───────│──── Submeter Resposta │
    │     │                                     │                     │
    │     │                              ───────│──── Ver Notas      │
    │     │                                     │                     │
    │     │                              ───────│──── Ver Tarefas    │
    │     │                                     │                     │
    │     │──── Fazer Logout ───────────────────│                     │
    │                                                                 │
    └─────────────────────────────────────────────────────────────────┘
    
    Casos de Uso Incluídos:
    - Autenticar Usuário (include em todos os casos)
    - Validar Permissões (include em operações específicas)
    - Calcular Estatísticas (include em dashboards)
    
    Casos de Uso Estendidos:
    - Notificar Usuário (extend em operações de sucesso/erro)
    - Gerar Relatório (extend em visualizações)
```

### Descrição dos Atores

**Professor:**
- Usuário responsável por criar e gerenciar tarefas acadêmicas
- Avalia respostas dos alunos
- Acessa estatísticas de desempenho da turma

**Aluno:**
- Usuário que visualiza tarefas disponíveis
- Submete respostas para atividades
- Acompanha suas notas e feedback

**Sistema (Ator Secundário):**
- Processa autenticação
- Calcula estatísticas
- Gerencia notificações

## 🏗️ Diagrama de Classes

```
┌─────────────────────────────────────────────────────────────────────┐
│                           App                                        │
├─────────────────────────────────────────────────────────────────────┤
│ - page: ft.Page                                                     │
│ - current_user: dict                                                │
│ - current_task: dict                                                │
│ - pages: dict                                                       │
├─────────────────────────────────────────────────────────────────────┤
│ + __init__(page: ft.Page)                                          │
│ + show_page(page_name: str)                                        │
│ + show_snackbar(message: str, type: str)                           │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                │ uses
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        User (Model)                                 │
├─────────────────────────────────────────────────────────────────────┤
│ - id: Integer (PK)                                                  │
│ - username: String(50) (Unique)                                     │
│ - password: String(255)                                             │
│ - full_name: String(100)                                            │
│ - user_type: String(20)                                             │
│ - created_at: DateTime                                              │
├─────────────────────────────────────────────────────────────────────┤
│ + tasks_created: relationship                                       │
│ + responses: relationship                                           │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                │ 1:N
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Task (Model)                                 │
├─────────────────────────────────────────────────────────────────────┤
│ - id: Integer (PK)                                                  │
│ - title: String(200)                                                │
│ - description: Text                                                 │
│ - creator_id: Integer (FK)                                          │
│ - created_at: DateTime                                              │
│ - due_date: DateTime                                                │
│ - max_score: Integer                                                │
├─────────────────────────────────────────────────────────────────────┤
│ + creator: relationship                                             │
│ + responses: relationship                                           │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                │ 1:N
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    TaskResponse (Model)                             │
├─────────────────────────────────────────────────────────────────────┤
│ - id: Integer (PK)                                                  │
│ - task_id: Integer (FK)                                             │
│ - student_id: Integer (FK)                                          │
│ - response_text: Text                                               │
│ - file_data: LargeBinary                                            │
│ - file_name: String(255)                                            │
│ - submitted_at: DateTime                                            │
│ - score: Integer                                                    │
│ - feedback: Text                                                    │
├─────────────────────────────────────────────────────────────────────┤
│ + task: relationship                                                │
│ + student: relationship                                             │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    StatisticsWrapper                                │
├─────────────────────────────────────────────────────────────────────┤
│ - lib: bool                                                         │
├─────────────────────────────────────────────────────────────────────┤
│ + get_professor_active_tasks(professor_id: int): int               │
│ + get_total_students(): int                                         │
│ + get_professor_evaluated_responses(professor_id: int): int         │
│ + get_student_pending_tasks(student_id: int): int                   │
│ + get_student_completed_tasks(student_id: int): int                 │
│ + get_student_average_grade(student_id: int): float                 │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                      Login (View)                                   │
├─────────────────────────────────────────────────────────────────────┤
│ - page: ft.Page                                                     │
│ - controller: App                                                   │
│ - ra_field: ft.TextField                                            │
│ - password_field: ft.TextField                                      │
├─────────────────────────────────────────────────────────────────────┤
│ + validate_ra(e): void                                              │
│ + login(e): void                                                    │
│ + show_password_toggle(e): void                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                 DashboardProfessor (View)                           │
├─────────────────────────────────────────────────────────────────────┤
│ - page: ft.Page                                                     │
│ - controller: App                                                   │
│ - stats_wrapper: StatisticsWrapper                                  │
├─────────────────────────────────────────────────────────────────────┤
│ + create_action_card(): ft.Container                                │
│ + create_stat_card(): ft.Container                                  │
│ + update_statistics(): void                                         │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                   DashboardAluno (View)                             │
├─────────────────────────────────────────────────────────────────────┤
│ - page: ft.Page                                                     │
│ - controller: App                                                   │
│ - stats_wrapper: StatisticsWrapper                                  │
├─────────────────────────────────────────────────────────────────────┤
│ + create_action_card(): ft.Container                                │
│ + create_stat_card(): ft.Container                                  │
│ + update_statistics(): void                                         │
└─────────────────────────────────────────────────────────────────────┘
```

### Padrões de Design Utilizados

**MVC (Model-View-Controller):**
- **Model**: Classes User, Task, TaskResponse
- **View**: Classes de interface (Login, Dashboard, etc.)
- **Controller**: Classe App principal

**Singleton:**
- StatisticsWrapper usa padrão singleton

**Factory:**
- Criação de páginas através do dicionário de classes

## 🔄 Diagramas de Sequência

### Sequência 1: Login de Usuário

```
Usuario          Login           Database        App
  │               │                │             │
  │──enter_credentials──→│         │             │
  │               │                │             │
  │               │──authenticate_user──→│       │
  │               │                │             │
  │               │←──user_data────────│         │
  │               │                │             │
  │               │──set_current_user──────────→│
  │               │                │             │
  │               │──show_dashboard─────────────→│
  │               │                │             │
  │←──redirect_to_dashboard────────│             │
```

### Sequência 2: Criação de Tarefa

```
Professor    CriarTarefa    Database    App
    │            │            │         │
    │──fill_form──→│          │         │
    │            │            │         │
    │            │──validate_data──→│   │
    │            │            │         │
    │            │──insert_task────→│   │
    │            │            │         │
    │            │←──success────────│   │
    │            │            │         │
    │            │──show_snackbar─────→│
    │            │            │         │
    │←──confirmation─────────│         │
```

### Sequência 3: Submissão de Resposta

```
Aluno    DetalheTarefaAluno    Database    App
  │              │               │         │
  │──select_file──→│             │         │
  │              │               │         │
  │              │──validate_file──→│     │
  │              │               │         │
  │              │──insert_response──→│   │
  │              │               │         │
  │              │←──success──────────│   │
  │              │               │         │
  │              │──show_confirmation────→│
  │              │               │         │
  │←──feedback────────────────────│       │
```

### Sequência 4: Avaliação de Resposta

```
Professor  DetalheResposta  Database  App
    │            │            │       │
    │──view_response──→│      │       │
    │            │            │       │
    │            │──get_response──→│  │
    │            │            │       │
    │            │←──response_data──│ │
    │            │            │       │
    │──enter_grade──→│         │       │
    │            │            │       │
    │            │──update_rating──→│ │
    │            │            │       │
    │            │←──success────────│ │
    │            │            │       │
    │←──confirmation────────────│     │
```

## 🗄️ Modelo Entidade-Relacionamento

```
┌─────────────────────────────────────────────────────────────────┐
│                            USERS                                │
├─────────────────────────────────────────────────────────────────┤
│ PK  id           INTEGER      AUTO_INCREMENT                    │
│ UK  username     VARCHAR(50)  NOT NULL                          │
│     password     VARCHAR(255) NOT NULL                          │
│     full_name    VARCHAR(100) NOT NULL                          │
│     user_type    VARCHAR(20)  NOT NULL                          │
│     created_at   DATETIME     DEFAULT CURRENT_TIMESTAMP         │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ 1:N (creator)
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                            TASKS                                │
├─────────────────────────────────────────────────────────────────┤
│ PK  id           INTEGER      AUTO_INCREMENT                    │
│     title        VARCHAR(200) NOT NULL                          │
│     description  TEXT         NOT NULL                          │
│ FK  creator_id   INTEGER      NOT NULL                          │
│     created_at   DATETIME     DEFAULT CURRENT_TIMESTAMP         │
│     due_date     DATETIME     NULL                              │
│     max_score    INTEGER      DEFAULT 100                       │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ 1:N
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                       TASK_RESPONSES                            │
├─────────────────────────────────────────────────────────────────┤
│ PK  id             INTEGER      AUTO_INCREMENT                  │
│ FK  task_id        INTEGER      NOT NULL                        │
│ FK  student_id     INTEGER      NOT NULL                        │
│     response_text  TEXT         NULL                            │
│     file_data      LONGBLOB     NULL                            │
│     file_name      VARCHAR(255) NULL                            │
│     submitted_at   DATETIME     DEFAULT CURRENT_TIMESTAMP       │
│     score          INTEGER      NULL                            │
│     feedback       TEXT         NULL                            │
└─────────────────────────────────────────────────────────────────┘
                                ▲
                                │ N:1 (student)
                                │
                    ┌───────────────────────┐
                    │       USERS           │
                    │   (student role)      │
                    └───────────────────────┘

Relacionamentos:
- USERS (1) ──── (N) TASKS (creator_id)
- TASKS (1) ──── (N) TASK_RESPONSES (task_id)
- USERS (1) ──── (N) TASK_RESPONSES (student_id)

Índices:
- users.username (UNIQUE)
- tasks.creator_id
- task_responses.task_id
- task_responses.student_id
- task_responses.task_id + student_id (COMPOSITE UNIQUE)

Constraints:
- users.user_type IN ('professor', 'aluno')
- tasks.max_score >= 0 AND <= 100
- task_responses.score >= 0 AND <= 100
- task_responses.file_data <= 10MB
```

## 🏛️ Arquitetura do Sistema

### Arquitetura em Camadas

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                           │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Flet GUI Framework                                     │    │
│  │  ├── Login.py                                           │    │
│  │  ├── Dashboard*.py                                      │    │
│  │  ├── CriarTarefa.py                                     │    │
│  │  └── Other Views...                                     │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     BUSINESS LAYER                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Application Controller                                 │    │
│  │  ├── App.py (Main Controller)                          │    │
│  │  ├── Navigation Logic                                  │    │
│  │  └── State Management                                  │    │
│  └─────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Statistics Module                                      │    │
│  │  ├── StatisticsWrapper.py                              │    │
│  │  └── statistics.c (C Module)                           │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  ORM Layer (SQLAlchemy)                                 │    │
│  │  ├── database.py                                       │    │
│  │  ├── Models (User, Task, TaskResponse)                 │    │
│  │  └── Database Operations                               │    │
│  └─────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Configuration                                          │    │
│  │  ├── config.py                                         │    │
│  │  └── Environment Variables                             │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DATABASE LAYER                                │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  MySQL Database                                         │    │
│  │  ├── users                                             │    │
│  │  ├── tasks                                             │    │
│  │  └── task_responses                                    │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Componentes Principais

**Frontend (Presentation Layer):**
- Interface gráfica baseada em Flet
- Componentes reutilizáveis
- Responsividade e acessibilidade
- Validação de entrada do usuário

**Backend (Business Layer):**
- Controlador principal da aplicação
- Lógica de negócio
- Gerenciamento de estado
- Processamento de estatísticas

**Data Access (Data Layer):**
- Abstração do banco de dados via ORM
- Operações CRUD
- Configurações centralizadas
- Gerenciamento de conexões

**Database (Database Layer):**
- Armazenamento persistente
- Integridade referencial
- Otimização de consultas
- Backup e recuperação

### Fluxo de Dados

```
User Input → Flet GUI → App Controller → Database Operations → MySQL
    ↑                                                              │
    └──────── Response ← View Update ← Business Logic ←───────────┘
```

### Padrões Arquiteturais

**MVC (Model-View-Controller):**
- Separação clara de responsabilidades
- Facilita manutenção e testes
- Reutilização de componentes

**Repository Pattern:**
- Abstração do acesso a dados
- Facilita mudanças de banco
- Melhora testabilidade

**Singleton Pattern:**
- Instância única de StatisticsWrapper
- Controle de recursos
- Estado global consistente

---

**Este documento técnico serve como referência para desenvolvimento, manutenção e evolução do sistema.**

**Versão**: 1.0.0  
**Data**: Outubro 2024  
**Responsável**: Equipe de Arquitetura