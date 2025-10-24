# Sistema Acadêmico Colaborativo

## 📋 Visão Geral

O Sistema Acadêmico Colaborativo é uma plataforma educacional moderna desenvolvida para facilitar a gestão de tarefas acadêmicas entre professores e alunos. O sistema oferece uma interface intuitiva e funcionalidades robustas para criação, submissão e avaliação de atividades educacionais.

## 🎯 Objetivos

- **Facilitar a comunicação** entre professores e alunos
- **Centralizar o gerenciamento** de tarefas acadêmicas
- **Automatizar processos** de submissão e avaliação
- **Fornecer estatísticas** em tempo real sobre desempenho
- **Garantir segurança** e integridade dos dados

## 🏗️ Arquitetura do Sistema

### Tecnologias Utilizadas

- **Frontend**: Flet (Python GUI Framework)
- **Backend**: Python 3.x com SQLAlchemy ORM
- **Banco de Dados**: MySQL 8.0+
- **Estatísticas**: Módulo C integrado via wrapper Python
- **Containerização**: Docker e Docker Compose

### Estrutura do Projeto

```
PIM_copia/
├── README.md                          # Documentação principal
├── main.py                           # Ponto de entrada da aplicação
├── requirements.txt                  # Dependências Python
├── backend/                          # Lógica de negócio
│   ├── config.py                    # Configurações do sistema
│   ├── database.py                  # Modelos e operações do banco
│   ├── statistics.c                 # Módulo de estatísticas em C
│   ├── statistics.exe               # Executável compilado
│   └── statistics_wrapper.py        # Wrapper Python para C
├── frontend/                         # Interface do usuário
│   ├── assets/                      # Recursos visuais
│   │   ├── Book.png
│   │   ├── personagem_*.png         # Avatares dos usuários
│   │   └── personagem_bg*.png       # Backgrounds
│   └── pages/                       # Páginas da aplicação
│       ├── login.py                 # Tela de login
│       ├── register.py              # Tela de cadastro
│       ├── aluno/                   # Páginas do aluno
│       │   ├── dashboard_aluno.py
│       │   ├── detalhe_tarefa_aluno.py
│       │   ├── ver_notas_aluno.py
│       │   └── ver_tarefas_aluno.py
│       └── professor/               # Páginas do professor
│           ├── dashboard_professor.py
│           ├── criar_tarefa.py
│           ├── detalhe_tarefa.py
│           ├── editar_tarefa.py
│           ├── ver_tarefa.py
│           └── detalhe_resposta_aluno.py
└── database/                         # Configuração do banco
    ├── docker-compose.yml           # Orquestração MySQL
    └── init.sql                     # Script de inicialização
```

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- MySQL 8.0 ou superior
- Docker e Docker Compose (opcional)
- Compilador GCC (para módulo C de estatísticas)

### Instalação Rápida

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd PIM_copia
```

2. **Instale as dependências Python:**
```bash
pip install -r requirements.txt
```

3. **Configure o banco de dados:**

**Opção A - Docker (Recomendado):**
```bash
cd database
docker-compose up -d
```

**Opção B - MySQL Local:**
```bash
mysql -u root -p < database/init.sql
```

4. **Configure variáveis de ambiente (opcional):**
```bash
# Crie um arquivo .env na raiz do projeto
DB_HOST=localhost
DB_PORT=3306
DB_NAME=sistema_academico
DB_USER=app_user
DB_PASSWORD=app_password
DEBUG=False
```

5. **Compile o módulo de estatísticas (opcional):**
```bash
cd backend
gcc -shared -fPIC -o statistics.so statistics.c -lmysqlclient
```

6. **Execute a aplicação:**
```bash
python main.py
```

## 👥 Tipos de Usuário

### Professor
- **Dashboard personalizado** com estatísticas
- **Criação e edição** de tarefas
- **Gerenciamento** de atividades
- **Avaliação** de respostas dos alunos
- **Visualização** de relatórios

### Aluno
- **Dashboard individual** com progresso
- **Visualização** de tarefas disponíveis
- **Submissão** de respostas (texto/arquivo)
- **Acompanhamento** de notas
- **Histórico** de atividades

## 🔧 Funcionalidades Principais

### Autenticação e Segurança
- Sistema de login com RA (Registro Acadêmico)
- Validação de credenciais
- Sessões seguras
- Controle de acesso por perfil

### Gestão de Tarefas
- Criação de tarefas com descrição detalhada
- Definição de prazos de entrega
- Suporte a múltiplos tipos de resposta
- Edição e exclusão de atividades

### Submissão de Respostas
- Upload de arquivos (até 10MB)
- Respostas em texto
- Histórico de submissões
- Reenvio permitido até o prazo

### Sistema de Avaliação
- Atribuição de notas (0-100)
- Comentários personalizados
- Feedback detalhado
- Relatórios de desempenho

### Estatísticas Avançadas
- Módulo em C para performance
- Estatísticas em tempo real
- Dashboards interativos
- Métricas de engajamento

## 🗄️ Modelo de Dados

### Entidades Principais

**Users (Usuários)**
- id (PK)
- username (RA único)
- password
- full_name
- user_type (professor/aluno)
- created_at

**Tasks (Tarefas)**
- id (PK)
- title
- description
- creator_id (FK → Users)
- created_at
- due_date
- max_score

**TaskResponses (Respostas)**
- id (PK)
- task_id (FK → Tasks)
- student_id (FK → Users)
- response_text
- file_data (BLOB)
- file_name
- submitted_at
- score
- feedback

## 🔒 Segurança

### Medidas Implementadas
- **Validação de entrada** em todos os campos
- **Sanitização** de dados do usuário
- **Controle de acesso** baseado em perfis
- **Criptografia** de senhas (recomendado implementar)
- **Validação de tipos** de arquivo
- **Limitação de tamanho** de upload

### Recomendações Adicionais
- Implementar hash de senhas (bcrypt)
- Adicionar autenticação de dois fatores
- Configurar HTTPS em produção
- Implementar rate limiting
- Adicionar logs de auditoria

## 📊 Monitoramento

### Métricas Disponíveis
- **Professores**: Tarefas ativas, total de alunos, avaliações realizadas
- **Alunos**: Tarefas pendentes, tarefas concluídas, média de notas
- **Sistema**: Performance, uso de recursos, estatísticas de acesso

## 🐛 Solução de Problemas

### Problemas Comuns

**Erro de conexão com banco:**
```bash
# Verifique se o MySQL está rodando
sudo systemctl status mysql

# Teste a conexão
mysql -u app_user -p sistema_academico
```

**Dependências não encontradas:**
```bash
# Reinstale as dependências
pip install --upgrade -r requirements.txt
```

**Módulo C não carrega:**
```bash
# Recompile o módulo
cd backend
gcc -shared -fPIC -o statistics.so statistics.c -lmysqlclient
```

## 📈 Roadmap

### Versão Atual (1.0)
- ✅ Sistema de autenticação
- ✅ Gestão de tarefas
- ✅ Submissão de respostas
- ✅ Sistema de avaliação
- ✅ Estatísticas básicas

### Próximas Versões
- 🔄 Notificações em tempo real
- 🔄 Sistema de mensagens
- 🔄 Relatórios avançados
- 🔄 API REST
- 🔄 Aplicativo mobile

## 🤝 Contribuição

### Como Contribuir
1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Código
- Siga PEP 8 para Python
- Documente todas as funções
- Escreva testes para novas funcionalidades
- Mantenha compatibilidade com versões anteriores

## 📚 Documentação Adicional

Para informações mais detalhadas, consulte:

- **[Manual de Uso](MANUAL_DE_USO.md)** - Guia completo para usuários finais
- **[Diagramas e Requisitos](DIAGRAMAS_E_REQUISITOS.md)** - Especificações técnicas e arquitetura
- **[Plano de Homologação e Testes](PLANO_HOMOLOGACAO_TESTES.md)** - Estratégias de teste e validação

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Equipe de Desenvolvimento

- **Desenvolvedor Principal**: [Nome do Desenvolvedor]
- **Arquiteto de Software**: [Nome do Arquiteto]
- **Designer UI/UX**: [Nome do Designer]
- **Analista de Qualidade**: [Nome do QA]

## 📞 Suporte

Para suporte técnico ou dúvidas:
- **Email**: suporte@sistema-academico.com
- **Documentação**: [Link da documentação]
- **Issues**: [Link do GitHub Issues]

---

**Versão**: 1.0.0  
**Última Atualização**: Outubro 2024  
**Status**: Produção