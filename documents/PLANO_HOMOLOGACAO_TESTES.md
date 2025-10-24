# Plano de Homologação e Testes - Sistema Acadêmico Colaborativo

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Estratégia de Testes](#estratégia-de-testes)
3. [Tipos de Testes](#tipos-de-testes)
4. [Casos de Teste](#casos-de-teste)
5. [Cenários de Homologação](#cenários-de-homologação)
6. [Critérios de Aceitação](#critérios-de-aceitação)
7. [Ambiente de Testes](#ambiente-de-testes)
8. [Cronograma de Execução](#cronograma-de-execução)
9. [Relatórios e Métricas](#relatórios-e-métricas)

## 🎯 Visão Geral

### Objetivo
Este plano define a estratégia, procedimentos e critérios para validação completa do Sistema Acadêmico Colaborativo, garantindo que todas as funcionalidades atendam aos requisitos especificados e proporcionem uma experiência de usuário satisfatória.

### Escopo
- **Funcionalidades**: Todas as funcionalidades do sistema
- **Usuários**: Professores e Alunos
- **Plataformas**: Windows, Linux, macOS
- **Navegadores**: Aplicação desktop Flet

### Responsabilidades
- **Equipe de QA**: Execução dos testes
- **Desenvolvedores**: Correção de bugs
- **Product Owner**: Validação de requisitos
- **Usuários Finais**: Testes de aceitação

## 🧪 Estratégia de Testes

### Abordagem de Testes

**Pirâmide de Testes:**
```
                    ┌─────────────────┐
                    │   Testes E2E    │ ← 20%
                    │   (Interface)   │
                ┌───┴─────────────────┴───┐
                │   Testes Integração     │ ← 30%
                │   (APIs + Database)     │
            ┌───┴─────────────────────────┴───┐
            │      Testes Unitários           │ ← 50%
            │   (Funções individuais)         │
            └─────────────────────────────────┘
```

### Fases de Teste

1. **Testes de Desenvolvimento** (Dev)
2. **Testes de Integração** (QA)
3. **Testes de Sistema** (Staging)
4. **Testes de Aceitação** (UAT)
5. **Testes de Produção** (Smoke Tests)

### Critérios de Entrada/Saída

**Critérios de Entrada:**
- Código desenvolvido e revisado
- Ambiente de teste configurado
- Dados de teste preparados
- Casos de teste aprovados

**Critérios de Saída:**
- 100% dos casos de teste executados
- 95% de taxa de sucesso mínima
- Bugs críticos resolvidos
- Documentação atualizada

## 🔬 Tipos de Testes

### 1. Testes Funcionais

#### 1.1 Testes Unitários
**Objetivo**: Validar funções individuais
**Ferramentas**: pytest, unittest
**Cobertura**: Mínimo 80%

**Componentes Testados:**
- Funções de autenticação
- Validações de entrada
- Operações de banco de dados
- Cálculos de estatísticas

#### 1.2 Testes de Integração
**Objetivo**: Validar interação entre componentes
**Escopo**: 
- Frontend ↔ Backend
- Backend ↔ Database
- Módulos Python ↔ Módulo C

#### 1.3 Testes de Sistema
**Objetivo**: Validar sistema completo
**Cenários**: Fluxos completos de usuário

#### 1.4 Testes de Aceitação
**Objetivo**: Validar requisitos de negócio
**Executores**: Usuários finais

### 2. Testes Não-Funcionais

#### 2.1 Testes de Performance
**Objetivo**: Validar desempenho do sistema
**Métricas**:
- Tempo de resposta < 3s
- Throughput > 100 req/s
- Uso de CPU < 80%
- Uso de memória < 2GB

#### 2.2 Testes de Carga
**Objetivo**: Validar comportamento sob carga
**Cenários**:
- 100 usuários simultâneos
- 500 usuários simultâneos
- 1000 usuários simultâneos

#### 2.3 Testes de Segurança
**Objetivo**: Identificar vulnerabilidades
**Verificações**:
- SQL Injection
- Cross-site Scripting (XSS)
- Autenticação e autorização
- Criptografia de dados

#### 2.4 Testes de Usabilidade
**Objetivo**: Avaliar experiência do usuário
**Critérios**:
- Facilidade de uso
- Intuitividade da interface
- Acessibilidade
- Tempo de aprendizado

## 📝 Casos de Teste

### CT001 - Login de Usuário

**Pré-condições**: Sistema iniciado, usuário cadastrado

| Caso | Entrada | Ação | Resultado Esperado |
|------|---------|------|-------------------|
| CT001.1 | RA: R123456, Senha: 123456 | Clicar "Entrar" | Login realizado, redirecionamento para dashboard |
| CT001.2 | RA: R123456, Senha: errada | Clicar "Entrar" | Mensagem "RA ou senha incorretos" |
| CT001.3 | RA: 123456, Senha: 123456 | Clicar "Entrar" | Mensagem "RA deve ser R seguido de 6 dígitos" |
| CT001.4 | RA: vazio, Senha: 123456 | Clicar "Entrar" | Mensagem "Preencha todos os campos" |

### CT002 - Cadastro de Usuário

**Pré-condições**: Sistema iniciado, tela de cadastro aberta

| Caso | Entrada | Ação | Resultado Esperado |
|------|---------|------|-------------------|
| CT002.1 | Nome: João Silva, RA: R123457, Senha: 123456, Tipo: Aluno | Clicar "Cadastrar" | Cadastro realizado com sucesso |
| CT002.2 | Nome: João Silva, RA: R123456, Senha: 123456, Tipo: Aluno | Clicar "Cadastrar" | Mensagem "RA já cadastrado" |
| CT002.3 | Nome: vazio, RA: R123458, Senha: 123456, Tipo: Aluno | Clicar "Cadastrar" | Mensagem de erro para campo obrigatório |

### CT003 - Criação de Tarefa (Professor)

**Pré-condições**: Professor logado, tela de criar tarefa aberta

| Caso | Entrada | Ação | Resultado Esperado |
|------|---------|------|-------------------|
| CT003.1 | Título: "Exercício 1", Descrição: "Resolver problemas", Data: 30/12/2024 | Clicar "Criar" | Tarefa criada com sucesso |
| CT003.2 | Título: vazio, Descrição: "Resolver problemas" | Clicar "Criar" | Mensagem "Título é obrigatório" |
| CT003.3 | Título: "Exercício 2", Descrição: vazio | Clicar "Criar" | Mensagem "Descrição é obrigatória" |

### CT004 - Submissão de Resposta (Aluno)

**Pré-condições**: Aluno logado, tarefa disponível

| Caso | Entrada | Ação | Resultado Esperado |
|------|---------|------|-------------------|
| CT004.1 | Arquivo: documento.pdf (2MB) | Upload e enviar | Resposta enviada com sucesso |
| CT004.2 | Arquivo: arquivo.exe (1MB) | Upload e enviar | Mensagem "Tipo de arquivo não permitido" |
| CT004.3 | Arquivo: video.mp4 (15MB) | Upload e enviar | Mensagem "Arquivo muito grande (máx. 10MB)" |
| CT004.4 | Texto: "Minha resposta detalhada" | Enviar resposta | Resposta em texto enviada com sucesso |

### CT005 - Avaliação de Resposta (Professor)

**Pré-condições**: Professor logado, resposta de aluno disponível

| Caso | Entrada | Ação | Resultado Esperado |
|------|---------|------|-------------------|
| CT005.1 | Nota: 85, Comentário: "Bom trabalho" | Salvar avaliação | Avaliação salva com sucesso |
| CT005.2 | Nota: 105, Comentário: "Excelente" | Salvar avaliação | Mensagem "Nota deve ser entre 0 e 100" |
| CT005.3 | Nota: -5, Comentário: "Precisa melhorar" | Salvar avaliação | Mensagem "Nota deve ser entre 0 e 100" |

### CT006 - Visualização de Estatísticas

**Pré-condições**: Usuário logado, dados disponíveis no sistema

| Caso | Usuário | Ação | Resultado Esperado |
|------|---------|------|-------------------|
| CT006.1 | Professor | Acessar dashboard | Estatísticas: tarefas ativas, alunos, avaliações |
| CT006.2 | Aluno | Acessar dashboard | Estatísticas: tarefas pendentes, concluídas, média |
| CT006.3 | Qualquer | Atualizar página | Estatísticas atualizadas em tempo real |

## 🏆 Cenários de Homologação

### Cenário H001 - Fluxo Completo do Professor

**Objetivo**: Validar jornada completa do professor no sistema

**Passos**:
1. **Login**: Professor faz login com credenciais válidas
2. **Dashboard**: Visualiza estatísticas atualizadas
3. **Criar Tarefa**: Cria nova tarefa com prazo
4. **Visualizar Tarefas**: Confirma tarefa na lista
5. **Aguardar Respostas**: Simula tempo para alunos responderem
6. **Avaliar Respostas**: Avalia respostas dos alunos
7. **Editar Tarefa**: Modifica descrição da tarefa
8. **Estatísticas**: Verifica atualização das métricas
9. **Logout**: Sai do sistema com segurança

**Critérios de Sucesso**:
- Todas as operações executadas sem erro
- Dados persistidos corretamente
- Interface responsiva e intuitiva
- Estatísticas atualizadas em tempo real

### Cenário H002 - Fluxo Completo do Aluno

**Objetivo**: Validar jornada completa do aluno no sistema

**Passos**:
1. **Cadastro**: Novo aluno se cadastra no sistema
2. **Login**: Faz login com as credenciais criadas
3. **Dashboard**: Visualiza suas estatísticas pessoais
4. **Ver Tarefas**: Lista tarefas disponíveis
5. **Detalhar Tarefa**: Visualiza descrição completa
6. **Enviar Resposta**: Submete arquivo como resposta
7. **Reenviar**: Modifica resposta antes do prazo
8. **Ver Notas**: Acompanha avaliações recebidas
9. **Estatísticas**: Verifica atualização da média
10. **Logout**: Sai do sistema

**Critérios de Sucesso**:
- Cadastro e login funcionam corretamente
- Upload de arquivos funciona sem problemas
- Notas são exibidas após avaliação
- Interface clara e fácil de usar

### Cenário H003 - Teste de Carga

**Objetivo**: Validar comportamento com múltiplos usuários

**Configuração**:
- 50 professores simultâneos
- 500 alunos simultâneos
- Operações mistas durante 30 minutos

**Operações Testadas**:
- Login/logout
- Criação de tarefas
- Upload de arquivos
- Consulta de estatísticas
- Avaliação de respostas

**Critérios de Sucesso**:
- Tempo de resposta < 5s sob carga
- Sem perda de dados
- Sem travamentos do sistema
- CPU < 90%, Memória < 4GB

### Cenário H004 - Teste de Recuperação

**Objetivo**: Validar recuperação após falhas

**Simulações**:
1. **Queda de Banco**: Simular indisponibilidade do MySQL
2. **Falha de Rede**: Interromper conexão durante operação
3. **Crash da Aplicação**: Forçar encerramento abrupto
4. **Corrupção de Dados**: Simular dados inconsistentes

**Critérios de Sucesso**:
- Sistema detecta falhas automaticamente
- Mensagens de erro são claras
- Recuperação automática quando possível
- Dados não são corrompidos

## ✅ Critérios de Aceitação

### Funcionais

**F1 - Autenticação**
- ✅ Login com RA e senha funciona
- ✅ Validação de formato do RA
- ✅ Mensagens de erro apropriadas
- ✅ Redirecionamento correto por perfil

**F2 - Gestão de Tarefas**
- ✅ Professor pode criar tarefas
- ✅ Professor pode editar tarefas
- ✅ Professor pode excluir tarefas
- ✅ Validação de campos obrigatórios

**F3 - Submissão de Respostas**
- ✅ Aluno pode enviar arquivos
- ✅ Aluno pode enviar texto
- ✅ Validação de tamanho de arquivo
- ✅ Possibilidade de reenvio

**F4 - Sistema de Avaliação**
- ✅ Professor pode atribuir notas
- ✅ Professor pode adicionar comentários
- ✅ Aluno pode visualizar notas
- ✅ Validação de faixa de notas (0-100)

**F5 - Estatísticas**
- ✅ Cálculos corretos para professores
- ✅ Cálculos corretos para alunos
- ✅ Atualização em tempo real
- ✅ Performance adequada

### Não-Funcionais

**NF1 - Performance**
- ✅ Tempo de resposta < 3s (operações normais)
- ✅ Tempo de resposta < 5s (sob carga)
- ✅ Suporte a 1000 usuários simultâneos
- ✅ Uso eficiente de recursos

**NF2 - Usabilidade**
- ✅ Interface intuitiva
- ✅ Navegação clara
- ✅ Mensagens de feedback apropriadas
- ✅ Acessibilidade básica

**NF3 - Confiabilidade**
- ✅ Sistema estável durante operação
- ✅ Recuperação automática de falhas menores
- ✅ Integridade dos dados mantida
- ✅ Backup e recuperação funcionais

**NF4 - Segurança**
- ✅ Autenticação obrigatória
- ✅ Controle de acesso por perfil
- ✅ Validação de entrada de dados
- ✅ Proteção contra uploads maliciosos

## 🖥️ Ambiente de Testes

### Configurações de Hardware

**Mínima**:
- CPU: Intel i3 ou equivalente
- RAM: 4GB
- HD: 10GB livres
- Rede: 10Mbps

**Recomendada**:
- CPU: Intel i5 ou equivalente
- RAM: 8GB
- SSD: 20GB livres
- Rede: 50Mbps

### Configurações de Software

**Sistema Operacional**:
- Windows 10/11
- Ubuntu 20.04+
- macOS 10.15+

**Dependências**:
- Python 3.8+
- MySQL 8.0+
- Docker (opcional)

### Dados de Teste

**Usuários Padrão**:
```
Professor Teste:
- RA: R000001
- Senha: prof123
- Nome: Professor Teste

Aluno Teste:
- RA: R000002
- Senha: aluno123
- Nome: Aluno Teste
```

**Tarefas de Exemplo**:
- Tarefa Ativa: "Exercício de Matemática"
- Tarefa Expirada: "Trabalho de História"
- Tarefa Futura: "Projeto Final"

**Arquivos de Teste**:
- documento_valido.pdf (2MB)
- arquivo_grande.zip (15MB)
- texto_simples.txt (1KB)
- imagem_teste.jpg (500KB)

## 📅 Cronograma de Execução

### Fase 1: Preparação (Semana 1)
- **Dia 1-2**: Configuração de ambientes
- **Dia 3-4**: Preparação de dados de teste
- **Dia 5**: Revisão de casos de teste

### Fase 2: Testes Funcionais (Semana 2)
- **Dia 1**: Testes de autenticação
- **Dia 2**: Testes de gestão de tarefas
- **Dia 3**: Testes de submissão
- **Dia 4**: Testes de avaliação
- **Dia 5**: Testes de estatísticas

### Fase 3: Testes Não-Funcionais (Semana 3)
- **Dia 1-2**: Testes de performance
- **Dia 3**: Testes de carga
- **Dia 4**: Testes de segurança
- **Dia 5**: Testes de usabilidade

### Fase 4: Homologação (Semana 4)
- **Dia 1-3**: Execução de cenários completos
- **Dia 4**: Correção de bugs críticos
- **Dia 5**: Aprovação final

### Fase 5: Preparação para Produção (Semana 5)
- **Dia 1-2**: Smoke tests em produção
- **Dia 3**: Treinamento de usuários
- **Dia 4-5**: Monitoramento inicial

## 📊 Relatórios e Métricas

### Métricas de Qualidade

**Cobertura de Testes**:
- Meta: 90% de cobertura de código
- Mínimo aceitável: 80%

**Taxa de Defeitos**:
- Meta: < 2 defeitos por 100 linhas de código
- Críticos: 0 defeitos em produção

**Eficiência de Testes**:
- Meta: 95% de casos de teste passando
- Tempo de execução: < 4 horas (suite completa)

### Relatório de Execução

**Template de Relatório Diário**:
```
Data: [DD/MM/AAAA]
Responsável: [Nome do Testador]

Casos Executados: X/Y
Taxa de Sucesso: X%
Bugs Encontrados: X (Críticos: X, Altos: X, Médios: X, Baixos: X)

Principais Problemas:
1. [Descrição do problema]
2. [Descrição do problema]

Próximos Passos:
1. [Ação planejada]
2. [Ação planejada]
```

### Relatório Final

**Estrutura do Relatório Final**:
1. **Resumo Executivo**
2. **Estatísticas Gerais**
3. **Resultados por Funcionalidade**
4. **Bugs Encontrados e Resolvidos**
5. **Recomendações**
6. **Aprovação para Produção**

### Dashboard de Acompanhamento

**Métricas em Tempo Real**:
- Progresso da execução de testes
- Taxa de sucesso por categoria
- Distribuição de bugs por severidade
- Tempo médio de correção
- Cobertura de código atual

## 🚨 Gestão de Defeitos

### Classificação de Severidade

**Crítica**: Sistema não funciona ou perda de dados
**Alta**: Funcionalidade principal não funciona
**Média**: Funcionalidade secundária com problema
**Baixa**: Problema cosmético ou de usabilidade

### Processo de Correção

1. **Identificação**: Testador identifica e reporta bug
2. **Triagem**: Equipe classifica severidade e prioridade
3. **Atribuição**: Bug é atribuído a desenvolvedor
4. **Correção**: Desenvolvedor implementa correção
5. **Reteste**: Testador valida correção
6. **Fechamento**: Bug é fechado se correção aprovada

### Critérios de Bloqueio

**Bloqueio de Release**:
- Qualquer bug crítico não resolvido
- Mais de 5 bugs de alta severidade
- Taxa de sucesso < 90%
- Cobertura de testes < 80%

---

**Este plano garante a qualidade e confiabilidade do Sistema Acadêmico Colaborativo através de testes abrangentes e critérios rigorosos de aceitação.**

**Versão**: 1.0.0  
**Data**: Outubro 2024  
**Aprovado por**: Gerente de Qualidade