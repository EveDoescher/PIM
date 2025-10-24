# Manual de Uso - Sistema Acadêmico Colaborativo

## 📖 Índice

1. [Introdução](#introdução)
2. [Primeiros Passos](#primeiros-passos)
3. [Interface do Sistema](#interface-do-sistema)
4. [Guia do Professor](#guia-do-professor)
5. [Guia do Aluno](#guia-do-aluno)
6. [Funcionalidades Avançadas](#funcionalidades-avançadas)
7. [Solução de Problemas](#solução-de-problemas)
8. [Dicas e Melhores Práticas](#dicas-e-melhores-práticas)

## 🚀 Introdução

O Sistema Acadêmico Colaborativo é uma plataforma intuitiva projetada para facilitar a interação entre professores e alunos no ambiente educacional. Este manual fornece instruções detalhadas para utilizar todas as funcionalidades do sistema.

### Público-Alvo
- **Professores**: Criação e gestão de tarefas acadêmicas
- **Alunos**: Submissão de atividades e acompanhamento de notas
- **Administradores**: Gestão geral do sistema

## 🎯 Primeiros Passos

### Acessando o Sistema

1. **Inicialização**
   - Execute o arquivo `main.py` ou clique no ícone da aplicação
   - Aguarde o carregamento da interface principal
   - A tela de login será exibida automaticamente

2. **Tela de Login**
   - **RA (Registro Acadêmico)**: Digite seu RA no formato R123456
   - **Senha**: Insira sua senha de acesso
   - Clique em "Entrar" para acessar o sistema

### Primeiro Acesso

**Para Novos Usuários:**
1. Clique em "Não tem uma conta? Criar nova conta"
2. Preencha o formulário de cadastro:
   - **Nome Completo**: Seu nome completo
   - **RA**: Registro Acadêmico (formato R123456)
   - **Senha**: Crie uma senha segura
   - **Tipo de Usuário**: Selecione Professor ou Aluno
3. Clique em "Cadastrar"
4. Retorne à tela de login com suas credenciais

## 🖥️ Interface do Sistema

### Elementos Comuns

**Barra Superior:**
- Avatar do usuário
- Nome e informações pessoais
- Botão de logout

**Navegação:**
- Menu principal com opções específicas do perfil
- Breadcrumbs para localização atual
- Botões de ação contextuais

**Notificações:**
- Mensagens de sucesso (verde)
- Alertas de erro (vermelho)
- Informações gerais (azul)

## 👨‍🏫 Guia do Professor

### Dashboard do Professor

Ao fazer login como professor, você verá:

**Estatísticas Principais:**
- **Tarefas Ativas**: Número de tarefas com prazo em aberto
- **Total de Alunos**: Alunos cadastrados no sistema
- **Avaliações**: Respostas já avaliadas por você

**Ações Principais:**
- **Criar Tarefa**: Botão para criar nova atividade
- **Gerenciar Tarefas**: Visualizar e editar tarefas existentes

### Criando uma Tarefa

1. **Acesse "Criar Tarefa"**
   - Clique no card "Criar Tarefa" no dashboard
   - Ou use o menu de navegação

2. **Preencha os Dados:**
   - **Título**: Nome da tarefa (obrigatório)
   - **Descrição**: Detalhes da atividade (obrigatório)
   - **Data de Entrega**: Prazo final (opcional)
   - **Pontuação Máxima**: Valor padrão 100 pontos

3. **Salvar a Tarefa:**
   - Clique em "Criar Tarefa"
   - Aguarde confirmação de sucesso
   - A tarefa estará disponível para os alunos

### Gerenciando Tarefas

**Visualizar Tarefas:**
1. Acesse "Gerenciar Tarefas"
2. Veja a lista de todas suas tarefas
3. Informações exibidas:
   - Título da tarefa
   - Data de criação
   - Data de entrega
   - Status (ativa/expirada)

**Ações Disponíveis:**
- **👁️ Visualizar**: Ver detalhes completos
- **✏️ Editar**: Modificar informações
- **🗑️ Excluir**: Remover tarefa (cuidado!)

### Avaliando Respostas

1. **Acesse a Tarefa:**
   - Clique em "Visualizar" na tarefa desejada
   - Veja a lista de alunos que responderam

2. **Avaliar Resposta:**
   - Clique no nome do aluno
   - Visualize a resposta enviada
   - Baixe arquivos se necessário
   - Atribua uma nota (0-100)
   - Adicione comentários de feedback
   - Clique em "Salvar Avaliação"

### Editando Tarefas

1. **Selecione a Tarefa:**
   - Na lista de tarefas, clique em "Editar"

2. **Modifique os Campos:**
   - Altere título, descrição ou prazo
   - Mantenha consistência com respostas já enviadas

3. **Salvar Alterações:**
   - Clique em "Atualizar Tarefa"
   - Confirme as modificações

## 👨‍🎓 Guia do Aluno

### Dashboard do Aluno

Seu painel principal mostra:

**Estatísticas Pessoais:**
- **Tarefas Pendentes**: Atividades ainda não respondidas
- **Tarefas Concluídas**: Atividades já enviadas
- **Média de Notas**: Sua média geral de desempenho

**Ações Disponíveis:**
- **Ver Tarefas**: Lista de todas as tarefas
- **Ver Notas**: Histórico de avaliações

### Visualizando Tarefas

1. **Acesse "Ver Tarefas"**
   - Clique no card correspondente no dashboard

2. **Lista de Tarefas:**
   - Tarefas ordenadas por data de criação
   - Status indicado por cores:
     - 🟢 Verde: Tarefa respondida
     - 🟡 Amarelo: Pendente dentro do prazo
     - 🔴 Vermelho: Prazo expirado

3. **Detalhes da Tarefa:**
   - Clique em qualquer tarefa para ver detalhes
   - Leia a descrição completa
   - Verifique o prazo de entrega

### Enviando Respostas

1. **Selecione a Tarefa:**
   - Clique na tarefa desejada
   - Acesse "Responder Tarefa"

2. **Tipos de Resposta:**

   **Resposta em Texto:**
   - Digite sua resposta no campo de texto
   - Use formatação básica se necessário

   **Upload de Arquivo:**
   - Clique em "Escolher Arquivo"
   - Selecione o arquivo (máx. 10MB)
   - Formatos aceitos: PDF, DOC, DOCX, TXT, etc.

3. **Enviar Resposta:**
   - Revise sua resposta antes de enviar
   - Clique em "Enviar Resposta"
   - Aguarde confirmação de sucesso

### Acompanhando Notas

1. **Acesse "Ver Notas"**
   - Visualize todas suas avaliações

2. **Informações Disponíveis:**
   - Nome da tarefa
   - Nota recebida
   - Comentários do professor
   - Data da avaliação

3. **Detalhes da Avaliação:**
   - Clique em qualquer nota para ver feedback completo
   - Leia os comentários do professor
   - Use o feedback para melhorar

## 🔧 Funcionalidades Avançadas

### Sistema de Notificações

**Tipos de Notificação:**
- ✅ Sucesso: Operações realizadas com êxito
- ❌ Erro: Problemas que precisam de atenção
- ℹ️ Informação: Mensagens gerais do sistema
- ⚠️ Aviso: Alertas importantes

### Filtros e Buscas

**Filtrar Tarefas:**
- Por status (pendente/concluída)
- Por data de criação
- Por prazo de entrega
- Por professor (para alunos)

### Estatísticas Detalhadas

**Para Professores:**
- Gráficos de desempenho da turma
- Taxa de entrega de tarefas
- Distribuição de notas
- Engajamento dos alunos

**Para Alunos:**
- Evolução das notas ao longo do tempo
- Comparação com média da turma
- Histórico de entregas
- Metas de desempenho

## 🔧 Solução de Problemas

### Problemas de Login

**Erro "RA ou senha incorretos":**
- Verifique se o RA está no formato R123456
- Confirme se a senha está correta
- Certifique-se de que o usuário está cadastrado

**Sistema não carrega:**
- Verifique conexão com internet
- Reinicie a aplicação
- Entre em contato com suporte se persistir

### Problemas de Upload

**Arquivo não é aceito:**
- Verifique o tamanho (máx. 10MB)
- Confirme o formato do arquivo
- Tente converter para PDF se necessário

**Upload falha:**
- Verifique conexão com internet
- Tente um arquivo menor
- Reinicie a aplicação se necessário

### Problemas de Performance

**Sistema lento:**
- Feche outras aplicações
- Verifique uso de memória
- Reinicie o computador se necessário

**Erro de banco de dados:**
- Entre em contato com administrador
- Não tente resolver sozinho
- Anote a mensagem de erro exata

## 💡 Dicas e Melhores Práticas

### Para Professores

**Criação de Tarefas:**
- Use títulos descritivos e claros
- Forneça instruções detalhadas
- Defina prazos realistas
- Considere a carga de trabalho dos alunos

**Avaliação:**
- Seja consistente nos critérios
- Forneça feedback construtivo
- Avalie em tempo hábil
- Use a escala de notas de forma justa

**Gestão:**
- Organize tarefas por módulos/temas
- Mantenha backup das avaliações
- Monitore estatísticas regularmente
- Comunique-se claramente com alunos

### Para Alunos

**Organização:**
- Verifique tarefas pendentes diariamente
- Organize seu tempo de estudo
- Leia instruções completamente
- Comece tarefas com antecedência

**Submissões:**
- Revise respostas antes de enviar
- Use nomes descritivos para arquivos
- Mantenha backup de seus trabalhos
- Respeite prazos de entrega

**Aprendizado:**
- Leia feedback dos professores
- Use notas para identificar pontos de melhoria
- Participe ativamente das atividades
- Tire dúvidas quando necessário

### Segurança

**Proteção de Dados:**
- Não compartilhe suas credenciais
- Faça logout ao sair
- Use senhas seguras
- Mantenha informações pessoais atualizadas

**Backup:**
- Mantenha cópias de trabalhos importantes
- Salve arquivos em múltiplos locais
- Use serviços de nuvem quando possível
- Documente seu progresso regularmente

## 📞 Suporte Técnico

### Canais de Suporte

**Suporte Imediato:**
- Email: suporte@sistema-academico.com
- Telefone: (11) 1234-5678
- Chat online: Disponível no sistema

**Documentação:**
- Manual completo: [Link]
- FAQ: [Link]
- Vídeos tutoriais: [Link]
- Fórum da comunidade: [Link]

### Informações para Suporte

Ao entrar em contato, forneça:
- Seu RA e tipo de usuário
- Descrição detalhada do problema
- Mensagens de erro (se houver)
- Passos para reproduzir o problema
- Screenshots quando relevante

---

**Este manual é atualizado regularmente. Verifique a versão mais recente em nossa documentação online.**

**Versão do Manual**: 1.0.0  
**Última Atualização**: Outubro 2024  
**Sistema Compatível**: Versão 1.0.0+