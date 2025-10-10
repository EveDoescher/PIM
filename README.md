# Documentação Técnica - Sistema Acadêmico Colaborativo

## Índice
1. [Visão Geral](#visão-geral)
2. [Tecnologias Utilizadas](#tecnologias-utilizadas)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Estrutura do Banco de Dados](#estrutura-do-banco-de-dados)
5. [Fluxo de Uso do Sistema](#fluxo-de-uso-do-sistema)
6. [Documentação das Funções](#documentação-das-funções)
7. [Interfaces do Sistema](#interfaces-do-sistema)
8. [Considerações Técnicas](#considerações-técnicas)

---

## Visão Geral

O Sistema Acadêmico Colaborativo é uma aplicação desktop desenvolvida em Python com Flet para gerenciamento de tarefas acadêmicas entre professores e alunos. O sistema permite que professores criem tarefas, recebam respostas dos alunos em formato de arquivo, e avaliem essas respostas com notas e comentários.

### Características Principais:
- Interface gráfica moderna e responsiva desenvolvida com Flet
- Sistema de autenticação por RA (Registro Acadêmico) e senha
- Gerenciamento completo de tarefas com prazos de entrega
- Upload e visualização de arquivos pelos alunos
- Sistema de avaliação com notas e comentários do professor
- Dashboards diferenciados para professores e alunos
- Validação de RA no formato específico (ex: 2024001)

---

## Tecnologias Utilizadas

### Framework Principal
- **Flet (Python)**: Framework moderno para desenvolvimento de aplicações multiplataforma
  - Baseado no Flutter do Google
  - Permite criar interfaces nativas para desktop, web e mobile
  - Suporte a componentes responsivos e modernos

### Banco de Dados
- **SQLite3**: Banco de dados relacional leve e embutido
  - Armazenamento local em `db/database.db`
  - Suporte a transações ACID
  - Ideal para aplicações desktop

### Bibliotecas Python Utilizadas
- **datetime**: Manipulação de datas e horários
- **hashlib**: Criptografia de senhas (SHA-256)
- **sqlite3**: Interface para banco de dados SQLite
- **logging**: Sistema de logs para debug e monitoramento

### Recursos de Interface Flet
- **Componentes utilizados**:
  - `ft.Container`: Contêineres para layout
  - `ft.Card`: Cards para organização visual
  - `ft.TextField`: Campos de entrada de texto
  - `ft.ElevatedButton`: Botões com elevação
  - `ft.FilePicker`: Seletor de arquivos
  - `ft.ResponsiveRow`: Layout responsivo
  - `ft.AlertDialog`: Diálogos modais
  - `ft.SnackBar`: Notificações temporárias
  - `ft.Image`: Exibição de imagens
  - `ft.DataTable`: Tabelas de dados

---

## Estrutura do Projeto

```
/PIM
├── main.py                                    # Arquivo principal com classe App
├── db/
│   ├── database.py                            # Funções de banco de dados
│   └── database.db                            # Arquivo do banco SQLite (criado automaticamente)
├── pages/
│   ├── login.py                               # Tela de login
│   ├── register.py                            # Tela de cadastro
│   ├── professor/
│   │   ├── dashboard_professor.py             # Dashboard do professor
│   │   ├── criar_tarefa.py                    # Criação de tarefas
│   │   ├── ver_tarefa.py                      # Visualização de tarefas do professor
│   │   ├── detalhe_tarefa.py                  # Detalhes da tarefa
│   │   ├── editar_tarefa.py                   # Edição de tarefas
│   │   └── detalhe_resposta_aluno.py          # Avaliação de respostas dos alunos
│   └── aluno/
│       ├── dashboard_aluno.py                 # Dashboard do aluno
│       ├── ver_tarefas_aluno.py              # Visualização de tarefas disponíveis
│       ├── detalhe_tarefa_aluno.py           # Detalhes da tarefa e envio de resposta
│       └── ver_notas_aluno.py                # Visualização de notas e comentários
└── README.md                                  # Documentação do projeto
```

---

## Estrutura do Banco de Dados

### Tabela: `users`
Armazena informações dos usuários do sistema.

| Campo | Tipo | Descrição | Constraints |
|-------|------|-----------|-------------|
| id | INTEGER | Identificador único | PRIMARY KEY, AUTOINCREMENT |
| username | TEXT | Nome do usuário | NOT NULL |
| ra | TEXT | Registro Acadêmico | UNIQUE, NOT NULL |
| encrypted_password | TEXT | Senha criptografada (SHA-256) | NOT NULL |
| role | TEXT | Tipo de usuário ('aluno' ou 'professor') | NOT NULL, CHECK |

### Tabela: `tasks`
Armazena as tarefas criadas pelos professores.

| Campo | Tipo | Descrição | Constraints |
|-------|------|-----------|-------------|
| id | INTEGER | Identificador único | PRIMARY KEY, AUTOINCREMENT |
| title | TEXT | Título da tarefa | NOT NULL |
| description | TEXT | Descrição detalhada | |
| creation_date | DATETIME | Data de criação | NOT NULL |
| expiration_date | DATETIME | Data de expiração | NOT NULL |
| user_id | INTEGER | ID do professor criador | FOREIGN KEY → users(id) |

### Tabela: `student_responses`
Armazena as respostas enviadas pelos alunos.

| Campo | Tipo | Descrição | Constraints |
|-------|------|-----------|-------------|
| id | INTEGER | Identificador único | PRIMARY KEY, AUTOINCREMENT |
| task_id | INTEGER | ID da tarefa | FOREIGN KEY → tasks(id) |
| user_id | INTEGER | ID do aluno | FOREIGN KEY → users(id) |
| filename | TEXT | Nome do arquivo enviado | NOT NULL |
| file_data | BLOB | Dados binários do arquivo | NOT NULL |
| upload_date | DATETIME | Data do envio | NOT NULL |
| rating | INTEGER | Nota atribuída (0-10) | |
| comment | TEXT | Comentário do professor | |

### Relacionamentos
- `tasks.user_id` → `users.id` (Professor que criou a tarefa)
- `student_responses.task_id` → `tasks.id` (Tarefa respondida)
- `student_responses.user_id` → `users.id` (Aluno que respondeu)

---

## Fluxo de Uso do Sistema

### Arquitetura da Aplicação

#### Classe Principal: `App`
A classe `App` em `main.py` gerencia:
- Navegação entre páginas através do método `show_page()`
- Estado global da aplicação (`current_user`, `current_task`, `current_student_response`)
- Dicionário de páginas disponíveis
- Configurações da página Flet (título, tema, scroll)

### Fluxo do Professor

#### 1. Autenticação
1. Acesso à tela de login (`Login`)
2. Validação de RA e senha através de `authenticate_user()`
3. Redirecionamento para `DashboardProfessor`

#### 2. Dashboard do Professor
- Interface com boas-vindas personalizadas
- Opções principais:
  - **Criar Tarefa**: Navegação para `CriarTarefa`
  - **Ver Tarefas**: Navegação para `VerTarefa`
  - **Logout**: Retorno ao login

#### 3. Criação de Tarefas (`CriarTarefa`)
- Formulário com validações:
  - Título (obrigatório)
  - Descrição (obrigatório)
  - Data de expiração (DatePicker)
  - Horário (formato HH:MM)
- Salvamento via `insert_task()`

#### 4. Gerenciamento de Tarefas
- **Ver Tarefas** (`VerTarefa`): Lista todas as tarefas do professor
- **Detalhes** (`DetalheTarefa`): Informações completas e lista de respostas
- **Editar** (`EditarTarefa`): Modificação de tarefas existentes
- **Avaliar** (`DetalheRespostaAluno`): Sistema de notas e comentários

### Fluxo do Aluno

#### 1. Autenticação
- Mesmo processo de login dos professores
- Redirecionamento para `DashboardAluno`

#### 2. Dashboard do Aluno
- Opções disponíveis:
  - **Ver Tarefas**: Visualizar tarefas ativas
  - **Ver Notas**: Consultar avaliações
  - **Logout**: Sair do sistema

#### 3. Visualização e Resposta de Tarefas
- **Lista de Tarefas** (`VerTarefasAluno`): Apenas tarefas não expiradas
- **Detalhes** (`DetalheTarefaAluno`): Upload de arquivos e visualização de status
- **Estados**: Ativa, Entregue, Expirada

#### 4. Consulta de Notas (`VerNotasAluno`)
- Visualização de todas as tarefas
- Status: Ativo, Entregue, Corrigido, Expirado
- Notas e comentários dos professores

---

## Documentação das Funções

### Arquivo: `db/database.py`

#### Funções de Conexão e Inicialização

##### `get_connection()`
**Finalidade**: Retorna conexão com o banco SQLite
**Retorno**: Objeto de conexão sqlite3
**Localização**: `db/database.db`

##### Inicialização Automática
- Criação automática das tabelas na importação do módulo
- Adição de colunas `rating` e `comment` com ALTER TABLE se necessário
- Logging de sucesso na criação

#### Funções de Usuário

##### `insert_user(username, ra, password, role)`
**Finalidade**: Cadastra novo usuário no sistema
**Parâmetros**:
- `username`: Nome do usuário
- `ra`: Registro Acadêmico (único)
- `password`: Senha em texto plano
- `role`: 'aluno' ou 'professor'
**Retorno**: True/False
**Segurança**: Hash SHA-256 da senha

##### `authenticate_user(ra, password)`
**Finalidade**: Autentica usuário no sistema
**Parâmetros**: RA e senha
**Retorno**: Dict com dados do usuário ou None
**Implementação**: Comparação de hash SHA-256

##### `get_user_id(ra)`
**Finalidade**: Obtém ID do usuário pelo RA
**Uso**: Conversão RA → ID interno

#### Funções de Tarefas

##### `insert_task(title, description, expiration_date_str, user_id)`
**Finalidade**: Cria nova tarefa
**Validações**:
- Formato de data: '%d/%m/%Y %H:%M'
- user_id obrigatório
- Data de criação automática

##### `get_tasks_by_user_id(user_id)`
**Finalidade**: Lista tarefas de um professor específico
**Ordenação**: Por data de criação (DESC)

##### `get_all_tasks()`
**Finalidade**: Lista todas as tarefas do sistema
**Uso**: Visualização pelos alunos

##### `delete_task(task_id)`
**Finalidade**: Remove tarefa e respostas associadas
**Implementação**: CASCADE delete manual

##### `update_task(task_id, title, description, expiration_date_str)`
**Finalidade**: Atualiza dados de tarefa existente

#### Funções de Respostas dos Alunos

##### `insert_student_response(task_id, user_id, filename, file_data)`
**Finalidade**: Salva resposta do aluno
**Armazenamento**: BLOB para dados binários
**Data**: Upload automático (datetime.now())

##### `get_student_response(task_id, user_id)`
**Finalidade**: Recupera resposta específica
**Retorno**: Tupla com dados completos ou None

##### `get_students_who_responded(task_id)`
**Finalidade**: Lista alunos que responderam uma tarefa
**Dados**: Nome, ID, status de correção, nota, comentário
**Ordenação**: Por data de upload (DESC)

##### `update_student_response_rating(task_id, user_id, rating, comment)`
**Finalidade**: Avalia resposta do aluno
**Parâmetros**: Nota (0-10) e comentário do professor

### Arquivo: `main.py`

#### Classe `App`

##### `__init__(self, page: ft.Page)`
**Configurações**:
- Título: "Sistema acadêmico colaborativo"
- Tema: LIGHT
- Scroll: AUTO
- Estado inicial: Login

##### `show_page(self, page_name)`
**Finalidade**: Navegação entre páginas
**Implementação**:
- Limpeza de controles atuais
- Instanciação da nova página
- Atualização da interface
- Manutenção do estado global

#### Função `main(page: ft.Page)`
**Finalidade**: Ponto de entrada da aplicação
**Execução**: `ft.app(target=main)`

---

## Interfaces do Sistema

### Padrão de Design das Páginas

#### Estrutura Base
Todas as páginas herdam de `ft.Container` e seguem o padrão:
```python
class NomeDaPagina(ft.Container):
    def __init__(self, page: ft.Page, app):
        super().__init__()
        self.page = page
        self.app = app
        # Configurações específicas
```

#### Componentes Comuns

##### Sistema de Navegação
- Botões de retorno padronizados
- Navegação via `app.show_page()`
- Manutenção de estado entre páginas

##### Validações de Formulário
- Validação em tempo real
- Feedback visual com cores
- Prevenção de envio com dados inválidos

##### Sistema de Notificações
- SnackBar para feedback ao usuário
- Cores padronizadas (sucesso, erro, aviso)
- Ícones integrados

##### Gerenciamento de Arquivos
- FilePicker para seleção
- Validação de tipo e tamanho
- Armazenamento em BLOB
- Download e visualização

### Páginas Específicas

#### Login (`pages/login.py`)
- Campos: RA e senha
- Validação de RA (formato numérico)
- Autenticação via `authenticate_user()`
- Redirecionamento baseado no role

#### Register (`pages/register.py`)
- Formulário completo de cadastro
- Validação de RA único
- Seleção de tipo de usuário
- Hash automático da senha

#### Dashboard Professor (`pages/professor/dashboard_professor.py`)
- Boas-vindas personalizadas
- Menu principal com opções
- Acesso às funcionalidades do professor

#### Dashboard Aluno (`pages/aluno/dashboard_aluno.py`)
- Interface simplificada
- Foco em tarefas e notas
- Navegação intuitiva

#### Criar Tarefa (`pages/professor/criar_tarefa.py`)
- Formulário com validações
- DatePicker para data de expiração
- Campo de horário com máscara
- Salvamento com feedback

#### Detalhe Tarefa Aluno (`pages/aluno/detalhe_tarefa_aluno.py`)
- Visualização completa da tarefa
- Upload de arquivos
- Estados visuais (Ativa/Entregue/Expirada)
- Preview de arquivos enviados

#### Avaliação de Respostas (`pages/professor/detalhe_resposta_aluno.py`)
- Visualização do arquivo do aluno
- Sistema de notas (0-10)
- Campo para comentários
- Download do arquivo

---

## Considerações Técnicas

### Segurança

#### Autenticação
- Senhas criptografadas com SHA-256 via hashlib
- Validação de sessão por página
- Logout seguro com limpeza de estado
- RA como identificador único

#### Validação de Dados
- Sanitização de entradas de formulário
- Validação de tipos de arquivo no upload
- Prepared statements para prevenção de SQL injection
- Tratamento de exceções em todas as operações de banco

### Performance

#### Banco de Dados
- Conexões otimizadas com context managers
- Transações para operações múltiplas
- Índices implícitos em chaves primárias e únicas
- Logging para monitoramento de operações

#### Interface
- Lazy loading de componentes pesados
- Refresh seletivo de dados
- Gerenciamento eficiente de memória com limpeza de controles
- Scroll automático para conteúdo longo

### Arquitetura

#### Padrões Utilizados
- **MVC Adaptado**: Separação entre modelo (database.py), visão (pages/) e controle (App)
- **Page Controller**: Cada página gerencia seu próprio estado
- **Dependency Injection**: App injetado em todas as páginas
- **State Management**: Estado global na classe App

#### Modularidade
- Páginas organizadas por tipo de usuário
- Funções de banco isoladas em módulo específico
- Reutilização de componentes entre páginas
- Fácil extensão para novos tipos de usuário

### Limitações Atuais

1. **Banco de Dados**: SQLite adequado para uso local, limitado para múltiplos usuários simultâneos
2. **Arquivos**: Armazenamento em BLOB pode impactar performance com arquivos grandes
3. **Autenticação**: Sistema básico sem recursos como 2FA ou recuperação de senha
4. **Backup**: Dependente de backup manual do arquivo database.db
5. **Concorrência**: Sem controle de acesso simultâneo a recursos

### Melhorias Futuras Sugeridas

#### Curto Prazo
1. **Sistema de backup automático** do banco de dados
2. **Logs de auditoria** para rastreamento de ações
3. **Validação mais robusta** de tipos de arquivo
4. **Compressão de arquivos** antes do armazenamento

#### Médio Prazo
1. **Migração para PostgreSQL** para melhor performance multiusuário
2. **Sistema de arquivos externo** (local storage ou cloud)
3. **API REST** para integração com outros sistemas
4. **Notificações** para prazos de entrega

#### Longo Prazo
1. **Autenticação avançada** com tokens JWT
2. **Dashboard com estatísticas** e relatórios
3. **Sistema de grupos/turmas** para organização
4. **Mobile app** utilizando a mesma base Flet

---

## Instalação e Execução

### Pré-requisitos
- Python 3.8 ou superior
- Flet framework

### Instalação
```bash
pip install flet
```

### Execução
```bash
python main.py
```

### Estrutura de Arquivos Criada
- `db/database.db`: Banco SQLite criado automaticamente
- Logs de operações no console

---

## Conclusão

O Sistema Acadêmico Colaborativo representa uma solução completa e bem estruturada para gerenciamento de tarefas acadêmicas. Utilizando Flet como framework principal e SQLite para persistência, oferece uma experiência de usuário moderna e funcionalidades robustas.

A arquitetura modular facilita manutenção e extensão, enquanto o design responsivo garante usabilidade. O sistema de segurança, embora básico, atende aos requisitos fundamentais de proteção de dados acadêmicos.

Esta documentação serve como guia completo para desenvolvedores que precisem manter, estender ou integrar o sistema, fornecendo visão detalhada de todos os aspectos técnicos e funcionais da aplicação.