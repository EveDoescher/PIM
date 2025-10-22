# PLANO DE HOMOLOGAÇÃO E TESTES
## Sistema Acadêmico Colaborativo

---

## 📋 INFORMAÇÕES GERAIS

**Sistema:** Sistema Acadêmico Colaborativo  
**Versão:** 1.0  
**Data de Elaboração:** 22/10/2025  
**Responsável:** Equipe de Qualidade  
**Tecnologia:** Python 3.13, Flet 0.24.1, SQLAlchemy 2.0.35, MySQL 8.0  

---

## 🎯 OBJETIVO

Este documento define os procedimentos, critérios e estratégias para homologação e testes do Sistema Acadêmico Colaborativo, garantindo que todas as funcionalidades atendam aos requisitos especificados e operem com qualidade, segurança e performance adequadas.

---

## 🏗️ ARQUITETURA DO SISTEMA

### Componentes Principais:
- **Frontend:** Flet (Python) - Interface desktop moderna
- **Backend:** SQLAlchemy + PyMySQL - Camada de dados
- **Banco de Dados:** MySQL 8.0 - Armazenamento persistente
- **Módulo de Estatísticas:** Python + C - Performance otimizada
- **Autenticação:** Sistema próprio com validação de RA

### Perfis de Usuário:
- **Professor:** Criação, edição e avaliação de tarefas
- **Aluno:** Visualização, resposta e acompanhamento de tarefas

---

## 📊 ESCOPO DOS TESTES

### Funcionalidades Cobertas:
✅ Sistema de autenticação (login/registro)  
✅ Gestão de tarefas (CRUD completo)  
✅ Upload e gerenciamento de arquivos  
✅ Sistema de avaliação e feedback  
✅ Dashboards com estatísticas em tempo real  
✅ Navegação entre páginas  
✅ Validações de entrada  
✅ Tratamento de erros  

---

## 🧪 TIPOS DE TESTE

## 1. TESTES UNITÁRIOS

### 1.1 Módulo de Autenticação (`backend/database.py`)

#### **TU001 - Função authenticate_user()**
- **Objetivo:** Validar autenticação de usuários
- **Cenários:**
  - ✅ Login com credenciais válidas (professor)
  - ✅ Login com credenciais válidas (aluno)
  - ❌ Login com RA inexistente
  - ❌ Login com senha incorreta
  - ❌ Login com RA em formato inválido
  - ❌ Login com campos vazios

**Dados de Teste:**
```
RA Válido: R123456 | Senha: senha123
RA Inválido: X123456 | Senha: qualquer
RA Inexistente: R999999 | Senha: qualquer
```

#### **TU002 - Função insert_user()**
- **Objetivo:** Validar cadastro de novos usuários
- **Cenários:**
  - ✅ Cadastro de professor com dados válidos
  - ✅ Cadastro de aluno com dados válidos
  - ❌ Cadastro com RA já existente
  - ❌ Cadastro com RA em formato inválido
  - ❌ Cadastro com campos obrigatórios vazios

#### **TU003 - Função get_user_id()**
- **Objetivo:** Validar recuperação de ID por RA
- **Cenários:**
  - ✅ Busca com RA existente
  - ❌ Busca com RA inexistente
  - ❌ Busca com RA nulo/vazio

### 1.2 Módulo de Tarefas (`backend/database.py`)

#### **TU004 - Função insert_task()**
- **Objetivo:** Validar criação de tarefas
- **Cenários:**
  - ✅ Criação com dados válidos e data futura
  - ❌ Criação com título vazio
  - ❌ Criação com descrição vazia
  - ❌ Criação com data no passado
  - ❌ Criação com creator_id inválido

#### **TU005 - Função update_task()**
- **Objetivo:** Validar atualização de tarefas
- **Cenários:**
  - ✅ Atualização com dados válidos
  - ❌ Atualização de tarefa inexistente
  - ❌ Atualização com data no passado

#### **TU006 - Função delete_task()**
- **Objetivo:** Validar exclusão de tarefas
- **Cenários:**
  - ✅ Exclusão de tarefa existente
  - ✅ Verificar exclusão em cascata das respostas
  - ❌ Exclusão de tarefa inexistente

### 1.3 Módulo de Respostas (`backend/database.py`)

#### **TU007 - Função insert_student_response()**
- **Objetivo:** Validar envio de respostas
- **Cenários:**
  - ✅ Primeira resposta do aluno
  - ✅ Atualização de resposta existente
  - ✅ Upload de arquivo PNG (≤10MB)
  - ✅ Upload de arquivo PDF (≤10MB)
  - ❌ Upload de arquivo > 10MB
  - ❌ Upload de tipo não suportado

#### **TU008 - Função update_student_response_rating()**
- **Objetivo:** Validar avaliação de respostas
- **Cenários:**
  - ✅ Avaliação com nota válida (0-100)
  - ✅ Avaliação com comentário
  - ❌ Avaliação com nota inválida (-1, 101)
  - ❌ Avaliação de resposta inexistente

### 1.4 Módulo de Estatísticas (`backend/statistics.py`)

#### **TU009 - Sistema RealStatisticsSystem**
- **Objetivo:** Validar cálculos estatísticos
- **Cenários:**
  - ✅ get_professor_active_tasks() - contagem correta
  - ✅ get_total_students() - contagem de alunos
  - ✅ get_student_pending_tasks() - tarefas pendentes
  - ✅ get_student_average_grade() - cálculo de média
  - ✅ test_database_connection() - conectividade

---

## 2. TESTES DE INTEGRAÇÃO

### 2.1 Integração Frontend-Backend

#### **TI001 - Fluxo de Login**
- **Objetivo:** Validar integração entre tela de login e autenticação
- **Cenários:**
  - ✅ Login bem-sucedido → Redirecionamento para dashboard correto
  - ❌ Login falhado → Exibição de mensagem de erro
  - ✅ Validação de formato RA em tempo real

#### **TI002 - Fluxo de Criação de Tarefa**
- **Objetivo:** Validar integração entre interface e banco de dados
- **Cenários:**
  - ✅ Preenchimento → Validação → Inserção → Confirmação
  - ✅ Preview em tempo real durante digitação
  - ❌ Validação de campos obrigatórios

#### **TI003 - Fluxo de Upload de Arquivo**
- **Objetivo:** Validar integração de upload com armazenamento
- **Cenários:**
  - ✅ Seleção → Validação → Upload → Armazenamento no banco
  - ✅ Preview de imagens após upload
  - ❌ Validação de tamanho e tipo de arquivo

### 2.2 Integração Banco de Dados

#### **TI004 - Relacionamentos entre Tabelas**
- **Objetivo:** Validar integridade referencial
- **Cenários:**
  - ✅ Criação de tarefa → Vínculo com usuário criador
  - ✅ Resposta de tarefa → Vínculos com tarefa e aluno
  - ✅ Exclusão em cascata (tarefa → respostas)
  - ❌ Tentativa de inserção com FK inválida

#### **TI005 - Transações de Banco**
- **Objetivo:** Validar consistência transacional
- **Cenários:**
  - ✅ Commit bem-sucedido em operações válidas
  - ✅ Rollback em caso de erro
  - ✅ Isolamento entre sessões concorrentes

---

## 3. TESTES DE SISTEMA

### 3.1 Teste de Recuperação

#### **TR001 - Falha de Conexão com Banco**
- **Cenário:** Simular perda de conexão com MySQL
- **Comportamento Esperado:**
  - Sistema deve exibir mensagem de erro amigável
  - Não deve ocorrer crash da aplicação
  - Deve tentar reconectar automaticamente
  - Dados em memória devem ser preservados quando possível

#### **TR002 - Falha durante Upload**
- **Cenário:** Interrupção durante upload de arquivo grande
- **Comportamento Esperado:**
  - Sistema deve detectar falha
  - Não deve deixar registros parciais no banco
  - Deve permitir nova tentativa
  - Interface deve retornar ao estado anterior

#### **TR003 - Falha de Memória**
- **Cenário:** Upload de múltiplos arquivos grandes simultaneamente
- **Comportamento Esperado:**
  - Sistema deve controlar uso de memória
  - Deve rejeitar uploads que excedam limites
  - Não deve afetar outros usuários/operações

### 3.2 Teste de Segurança

#### **TS001 - Validação de Entrada**
- **Objetivo:** Prevenir ataques de injeção
- **Cenários:**
  - ❌ Tentativa de SQL Injection nos campos de login
  - ❌ Inserção de scripts maliciosos em campos de texto
  - ❌ Upload de arquivos executáveis
  - ❌ Manipulação de parâmetros de URL/formulário

**Dados de Teste Maliciosos:**
```sql
RA: R123456'; DROP TABLE users; --
Senha: ' OR '1'='1
Título: <script>alert('XSS')</script>
```

#### **TS002 - Controle de Acesso**
- **Objetivo:** Validar autorização por perfil
- **Cenários:**
  - ❌ Aluno tentando acessar funções de professor
  - ❌ Usuário não autenticado acessando sistema
  - ❌ Professor editando tarefa de outro professor
  - ✅ Isolamento de dados entre usuários

#### **TS003 - Proteção de Dados**
- **Objetivo:** Validar proteção de informações sensíveis
- **Cenários:**
  - ✅ Senhas não aparecem em logs
  - ✅ Dados pessoais protegidos
  - ✅ Arquivos acessíveis apenas ao proprietário
  - ❌ Tentativa de acesso direto a arquivos

### 3.3 Teste de Estresse

#### **TE001 - Carga de Usuários**
- **Objetivo:** Validar comportamento sob alta carga
- **Cenários:**
  - 50 usuários simultâneos fazendo login
  - 100 uploads simultâneos de arquivos 5MB
  - 200 consultas de estatísticas simultâneas
  - 500 operações de CRUD em tarefas

**Métricas Monitoradas:**
- Tempo de resposta (< 2 segundos para operações básicas)
- Uso de CPU (< 80%)
- Uso de memória (< 2GB)
- Conexões de banco (< 100 simultâneas)

#### **TE002 - Volume de Dados**
- **Objetivo:** Validar performance com grande volume
- **Cenários:**
  - 10.000 usuários cadastrados
  - 50.000 tarefas criadas
  - 100.000 respostas enviadas
  - Arquivos totalizando 10GB

#### **TE003 - Stress de Recursos**
- **Objetivo:** Testar limites do sistema
- **Cenários:**
  - Upload de arquivo no limite (10MB)
  - Descrições de tarefa com 10.000 caracteres
  - 1.000 tarefas por professor
  - Consultas complexas com JOINs múltiplos

### 3.4 Teste de Desempenho

#### **TD001 - Tempo de Resposta**
- **Objetivos de Performance:**
  - Login: < 1 segundo
  - Carregamento de dashboard: < 2 segundos
  - Upload de arquivo 5MB: < 10 segundos
  - Consulta de estatísticas: < 0.5 segundo
  - Navegação entre páginas: < 0.5 segundo

#### **TD002 - Otimização de Consultas**
- **Objetivo:** Validar eficiência das queries
- **Métricas:**
  - Uso de índices nas consultas frequentes
  - Tempo de execução das queries complexas
  - Plano de execução otimizado
  - Cache de resultados quando aplicável

---

## 4. TESTES DE VALIDAÇÃO

### 4.1 Conformidade com Requisitos Funcionais

#### **TV001 - RF01: Autenticação de Usuários**
- ✅ Login com RA e senha
- ✅ Cadastro de novos usuários
- ✅ Validação de formato RA (R + 6 dígitos)
- ✅ Criptografia de senhas

#### **TV002 - RF02: Gestão de Tarefas (Professor)**
- ✅ Criar novas tarefas
- ✅ Editar tarefas existentes
- ✅ Excluir tarefas
- ✅ Visualizar todas as tarefas criadas
- ✅ Definir prazo de entrega

#### **TV003 - RF03: Visualização de Tarefas (Aluno)**
- ✅ Visualizar todas as tarefas disponíveis
- ✅ Ver detalhes de tarefa específica
- ✅ Filtrar por status (ativas/expiradas)

#### **TV004 - RF04: Sistema de Respostas**
- ✅ Envio de arquivos (PNG, JPG, JPEG, PDF)
- ✅ Limite de 10MB por arquivo
- ✅ Visualização de arquivos enviados

#### **TV005 - RF05: Sistema de Avaliação**
- ✅ Avaliação de respostas (notas 0-100)
- ✅ Adição de comentários/feedback
- ✅ Visualização de notas pelo aluno

#### **TV006 - RF06: Dashboard e Estatísticas**
- ✅ Estatísticas em tempo real
- ✅ Dados específicos por perfil (professor/aluno)
- ✅ Integração com módulo C para performance

### 4.2 Conformidade com Requisitos Não Funcionais

#### **TV007 - RNF01: Usabilidade**
- ✅ Interface moderna e intuitiva
- ✅ Tempo de resposta < 2s para operações básicas
- ✅ Feedback visual para ações do usuário
- ✅ Design responsivo

#### **TV008 - RNF02: Performance**
- ✅ Suporte a 100+ usuários simultâneos
- ✅ Módulo de estatísticas otimizado em C
- ✅ Queries otimizadas com índices

#### **TV009 - RNF03: Segurança**
- ✅ Autenticação obrigatória
- ✅ Validação de entrada
- ✅ Proteção contra SQL Injection
- ✅ Controle de acesso por perfil

---

## 5. TESTES ESPECIAIS

### 5.1 Teste de Fumaça (Smoke Test)

#### **TF001 - Validação Rápida Pós-Deploy**
**Tempo Estimado:** 15 minutos

**Cenários Críticos:**
1. ✅ Sistema inicia sem erros
2. ✅ Conexão com banco estabelecida
3. ✅ Login de professor funciona
4. ✅ Login de aluno funciona
5. ✅ Criação de tarefa básica
6. ✅ Upload de arquivo pequeno
7. ✅ Navegação entre páginas principais
8. ✅ Logout funciona

**Critério de Aprovação:** Todos os cenários devem passar

### 5.2 Teste de Caminho Básico (Complexidade Ciclomática)

#### **TC001 - Análise de Complexidade**

**Função authenticate_user():**
- Complexidade: 4
- Caminhos: Login válido, RA inválido, senha inválida, erro de conexão

**Função insert_task():**
- Complexidade: 5  
- Caminhos: Sucesso, título vazio, data inválida, erro de conversão, erro de banco

**Função insert_student_response():**
- Complexidade: 6
- Caminhos: Nova resposta, atualização, erro de arquivo, erro de banco, resposta existente, validação falhou

**Critério:** Complexidade ciclomática deve ser ≤ 10 para manutenibilidade

---

## 📋 CASOS DE TESTE DETALHADOS

### CT001 - Login de Professor
**Pré-condições:** Sistema iniciado, banco conectado  
**Dados:** RA: R123456, Senha: prof123  
**Passos:**
1. Abrir tela de login
2. Inserir RA no formato correto
3. Inserir senha
4. Clicar em "Entrar"

**Resultado Esperado:** Redirecionamento para DashboardProfessor  
**Pós-condições:** Usuário autenticado, sessão ativa

### CT002 - Criação de Tarefa
**Pré-condições:** Professor logado  
**Dados:** Título: "Exercício 1", Descrição: "Resolver problemas 1-10", Data: Amanhã  
**Passos:**
1. Navegar para "Criar Tarefa"
2. Preencher título
3. Preencher descrição
4. Selecionar data futura
5. Definir horário
6. Clicar "Criar Tarefa"

**Resultado Esperado:** Tarefa criada, redirecionamento para lista de tarefas  
**Pós-condições:** Nova tarefa no banco, visível para alunos

### CT003 - Upload de Arquivo por Aluno
**Pré-condições:** Aluno logado, tarefa ativa disponível  
**Dados:** Arquivo: exercicio1.pdf (2MB)  
**Passos:**
1. Navegar para "Minhas Tarefas"
2. Selecionar tarefa ativa
3. Clicar "Selecionar Arquivo"
4. Escolher arquivo PDF válido
5. Clicar "Enviar Resposta"

**Resultado Esperado:** Upload bem-sucedido, confirmação exibida  
**Pós-condições:** Arquivo armazenado no banco, resposta registrada

### CT004 - Avaliação de Resposta
**Pré-condições:** Professor logado, resposta de aluno disponível  
**Dados:** Nota: 85, Comentário: "Bom trabalho"  
**Passos:**
1. Navegar para tarefa com respostas
2. Selecionar resposta de aluno
3. Inserir nota (0-100)
4. Adicionar comentário
5. Salvar avaliação

**Resultado Esperado:** Avaliação salva, aluno pode visualizar  
**Pós-condições:** Nota e feedback registrados no banco

---

## 🔧 AMBIENTE DE TESTE

### Configuração Mínima:
- **SO:** Windows 10/11, Linux Ubuntu 20.04+, macOS 11+
- **Python:** 3.11 ou superior
- **MySQL:** 8.0 ou superior
- **RAM:** 4GB mínimo, 8GB recomendado
- **Disco:** 2GB livres mínimo
- **Rede:** Conexão estável para banco de dados

### Dados de Teste:
```sql
-- Usuários de Teste
INSERT INTO users VALUES 
(1, 'R123456', 'prof123', 'Professor Teste', 'professor'),
(2, 'R654321', 'aluno123', 'Aluno Teste', 'aluno');

-- Tarefas de Teste
INSERT INTO tasks VALUES 
(1, 'Tarefa Teste 1', 'Descrição da tarefa teste', 1, NOW(), DATE_ADD(NOW(), INTERVAL 7 DAY), 100);
```

### Arquivos de Teste:
- **teste_pequeno.png** (500KB)
- **teste_medio.jpg** (2MB)
- **teste_grande.pdf** (8MB)
- **teste_limite.pdf** (10MB)
- **teste_invalido.exe** (arquivo não permitido)

---

## 📊 CRITÉRIOS DE ACEITAÇÃO

### Critérios de Aprovação:
- ✅ **Testes Unitários:** 95% de aprovação mínima
- ✅ **Testes de Integração:** 100% de aprovação
- ✅ **Testes de Sistema:** 90% de aprovação mínima
- ✅ **Testes de Validação:** 100% de aprovação
- ✅ **Performance:** Atender todos os requisitos de tempo
- ✅ **Segurança:** Zero vulnerabilidades críticas

### Critérios de Reprovação:
- ❌ Falha em funcionalidade crítica (login, criação de tarefa)
- ❌ Vulnerabilidade de segurança identificada
- ❌ Performance abaixo dos requisitos especificados
- ❌ Perda de dados durante operações
- ❌ Crash da aplicação em cenários normais

---

## 📈 MÉTRICAS DE QUALIDADE

### Cobertura de Código:
- **Meta:** 85% de cobertura mínima
- **Ferramentas:** pytest-cov, coverage.py
- **Exclusões:** Arquivos de configuração, assets

### Defeitos por Severidade:
- **Crítico:** 0 permitidos
- **Alto:** Máximo 2
- **Médio:** Máximo 5
- **Baixo:** Máximo 10

### Performance:
- **Tempo de Resposta Médio:** < 1.5 segundos
- **Taxa de Erro:** < 0.1%
- **Disponibilidade:** > 99%
- **Throughput:** > 50 transações/segundo

---

## 🗓️ CRONOGRAMA DE EXECUÇÃO

### Fase 1: Testes Unitários (3 dias)
- Dia 1: Módulos de autenticação e usuários
- Dia 2: Módulos de tarefas e respostas  
- Dia 3: Módulo de estatísticas e correções

### Fase 2: Testes de Integração (2 dias)
- Dia 1: Integração frontend-backend
- Dia 2: Integração com banco de dados

### Fase 3: Testes de Sistema (3 dias)
- Dia 1: Testes de recuperação e segurança
- Dia 2: Testes de estresse e performance
- Dia 3: Análise de resultados e correções

### Fase 4: Testes de Validação (2 dias)
- Dia 1: Validação de requisitos funcionais
- Dia 2: Validação de requisitos não funcionais

### Fase 5: Testes Especiais (1 dia)
- Teste de fumaça e caminho básico

**Total Estimado:** 11 dias úteis

---

## 🚨 GESTÃO DE DEFEITOS

### Classificação de Severidade:

#### **Crítico:**
- Sistema não inicia
- Perda de dados
- Falha de segurança grave
- Impossibilidade de login

#### **Alto:**
- Funcionalidade principal não funciona
- Performance muito abaixo do esperado
- Erro que afeta múltiplos usuários

#### **Médio:**
- Funcionalidade secundária com problema
- Interface com problemas visuais
- Performance ligeiramente abaixo do esperado

#### **Baixo:**
- Problemas cosméticos
- Melhorias de usabilidade
- Documentação incorreta

### Processo de Correção:
1. **Identificação:** Registro detalhado do defeito
2. **Classificação:** Atribuição de severidade e prioridade
3. **Atribuição:** Designação para desenvolvedor responsável
4. **Correção:** Implementação da solução
5. **Reteste:** Validação da correção
6. **Fechamento:** Confirmação da resolução

---

## 📋 RELATÓRIOS DE TESTE

### Relatório Diário:
- Casos executados vs. planejados
- Taxa de aprovação/reprovação
- Defeitos encontrados por severidade
- Bloqueadores identificados
- Próximos passos

### Relatório Final:
- Resumo executivo
- Cobertura de testes alcançada
- Métricas de qualidade
- Defeitos encontrados e corrigidos
- Recomendações para produção
- Riscos identificados

---

## ✅ CHECKLIST DE HOMOLOGAÇÃO

### Pré-Homologação:
- [ ] Ambiente de teste configurado
- [ ] Dados de teste carregados
- [ ] Equipe de teste treinada
- [ ] Ferramentas de teste instaladas
- [ ] Critérios de aceitação definidos

### Durante Execução:
- [ ] Todos os casos de teste executados
- [ ] Defeitos registrados e classificados
- [ ] Performance monitorada
- [ ] Segurança validada
- [ ] Usabilidade avaliada

### Pós-Execução:
- [ ] Relatórios gerados
- [ ] Defeitos críticos corrigidos
- [ ] Retestes executados
- [ ] Aprovação formal obtida
- [ ] Documentação atualizada

---

## 🔒 CONSIDERAÇÕES DE SEGURANÇA

### Testes de Penetração:
- Validação de autenticação e autorização
- Teste de injeção SQL e XSS
- Verificação de controle de acesso
- Análise de vulnerabilidades conhecidas

### Proteção de Dados:
- Dados de teste anonimizados
- Senhas não expostas em logs
- Arquivos de teste seguros
- Conformidade com LGPD

---

## 📞 CONTATOS E RESPONSABILIDADES

### Equipe de Teste:
- **Coordenador de Testes:** [Nome] - [email]
- **Analista de Testes Sênior:** [Nome] - [email]
- **Especialista em Performance:** [Nome] - [email]
- **Especialista em Segurança:** [Nome] - [email]

### Equipe de Desenvolvimento:
- **Líder Técnico:** [Nome] - [email]
- **Desenvolvedor Backend:** [Nome] - [email]
- **Desenvolvedor Frontend:** [Nome] - [email]

### Stakeholders:
- **Product Owner:** [Nome] - [email]
- **Gerente de Projeto:** [Nome] - [email]

---

## 📚 ANEXOS

### Anexo A: Scripts de Teste Automatizado
### Anexo B: Dados de Teste Detalhados
### Anexo C: Configuração de Ambiente
### Anexo D: Checklist de Segurança
### Anexo E: Métricas de Performance

---

**Documento elaborado em:** 22/10/2025  
**Versão:** 1.0  
**Próxima revisão:** 22/01/2026  

---

*Este plano de homologação e testes garante a qualidade, segurança e performance do Sistema Acadêmico Colaborativo, seguindo as melhores práticas da indústria e atendendo aos requisitos específicos do projeto.*