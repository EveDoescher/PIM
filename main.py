# Importações das bibliotecas necessárias
import flet as ft

# Importações das páginas do frontend
from frontend.pages.login import Login
from frontend.pages.register import Register
from frontend.pages.professor.dashboard_professor import DashboardProfessor
from frontend.pages.aluno.dashboard_aluno import DashboardAluno
from frontend.pages.professor.criar_tarefa import CriarTarefa
from frontend.pages.professor.ver_tarefa import VerTarefa
from frontend.pages.professor.detalhe_tarefa import DetalheTarefa
from frontend.pages.professor.editar_tarefa import EditarTarefa
from frontend.pages.professor.detalhe_resposta_aluno import DetalheRespostaAluno
from frontend.pages.aluno.ver_tarefas_aluno import VerTarefasAluno
from frontend.pages.aluno.ver_notas_aluno import VerNotasAluno
from frontend.pages.aluno.detalhe_tarefa_aluno import DetalheTarefaAluno

# Importação da função de inicialização do banco de dados
from backend.database import init_database

class App:
    """Classe principal da aplicação que gerencia toda a interface e navegação"""

    def __init__(self, page: ft.Page):
        """Inicializa a aplicação principal e configura todas as propriedades da janela"""
        # Armazena a referência da página principal do Flet
        self.page = page
        
        # Configurações básicas da aplicação
        self.page.title = "Sistema Acadêmico Colaborativo"  # Define o título da janela
        self.page.theme_mode = ft.ThemeMode.LIGHT  # Define tema claro como padrão
        self.page.scroll = ft.ScrollMode.AUTO  # Habilita scroll automático quando necessário
        
        # Configurações de janela para maximizar a área de trabalho
        self.page.window.maximized = True  # Inicia a janela maximizada
        self.page.window.full_screen = False  # Não inicia em tela cheia
        
        # Remove espaçamentos desnecessários para aproveitar toda a tela
        self.page.padding = 0  # Remove padding interno da página
        self.page.spacing = 0  # Remove espaçamento entre elementos
        
        # Força a página a ocupar toda a altura disponível
        self.page.expand = True
        
        # Define tamanhos mínimos da janela para garantir usabilidade
        self.page.window.min_width = 1024  # Largura mínima de 1024px
        self.page.window.min_height = 768  # Altura mínima de 768px
        
        # Define tamanho inicial da janela caso não maximize
        self.page.window.width = 1366  # Largura inicial padrão
        self.page.window.height = 768  # Altura inicial padrão

        # Inicializa o banco de dados criando as tabelas necessárias
        init_database()

        # Variáveis de estado da aplicação para controle de dados globais
        self.current_user = None  # Armazena dados do usuário logado
        self.current_task = None  # Armazena dados da tarefa sendo visualizada
        self.current_student_response = None  # Armazena dados da resposta sendo avaliada

        # Dicionário que mapeia nomes de páginas para suas respectivas classes
        self.pages = {
            "Login": Login,  # Página de login
            "Register": Register,  # Página de cadastro
            "DashboardProfessor": DashboardProfessor,  # Dashboard do professor
            "DashboardAluno": DashboardAluno,  # Dashboard do aluno
            "CriarTarefa": CriarTarefa,  # Página para criar tarefas
            "VerTarefa": VerTarefa,  # Página para listar tarefas
            "DetalheTarefa": DetalheTarefa,  # Página de detalhes da tarefa
            "EditarTarefa": EditarTarefa,  # Página para editar tarefas
            "DetalheRespostaAluno": DetalheRespostaAluno,  # Página para avaliar respostas
            "VerTarefasAluno": VerTarefasAluno,  # Página do aluno ver tarefas
            "VerNotasAluno": VerNotasAluno,  # Página do aluno ver notas
            "DetalheTarefaAluno": DetalheTarefaAluno,  # Página do aluno ver detalhes da tarefa
        }

        # Armazena referência da página atualmente sendo exibida
        self.current_page = None

        # Inicia a aplicação mostrando a tela de login
        self.show_page("Login")

    def show_snackbar(self, message: str, type: str = "info"):
        """Exibe mensagens de notificação temporárias na tela com cores diferentes por tipo"""
        # Define a cor de fundo baseada no tipo da mensagem
        if type == "success":
            bgcolor = ft.colors.PINK_600  # Rosa para mensagens de sucesso
        elif type == "error":
            bgcolor = ft.colors.PURPLE_600  # Roxo escuro para erros
        elif type == "warning":
            bgcolor = ft.colors.DEEP_PURPLE_600  # Roxo profundo para avisos
        else:
            bgcolor = ft.colors.PURPLE_400  # Roxo claro para informações gerais

        # Cria o componente snackbar com a mensagem e configurações
        snackbar = ft.SnackBar(
            content=ft.Text(message, color=ft.colors.WHITE),  # Texto branco para contraste
            bgcolor=bgcolor,  # Cor de fundo definida acima
            duration=3000  # Duração de 3 segundos na tela
        )
        
        # Adiciona o snackbar à sobreposição da página e o exibe
        self.page.overlay.append(snackbar)
        snackbar.open = True  # Torna o snackbar visível
        self.page.update()  # Atualiza a interface para mostrar a mudança

    def show_page(self, page_name: str):
        """Navega para uma página específica da aplicação limpando a tela atual"""
        # Busca a classe da página no dicionário de páginas
        page_class = self.pages[page_name]
        
        # Cria uma nova instância da página passando a referência da página e da app
        self.current_page = page_class(self.page, self)
        
        # Limpa todo o conteúdo atual da tela
        self.page.clean()
        
        # Adiciona a nova página à tela
        self.page.add(self.current_page)
        
        # Atualiza a interface para mostrar a nova página
        self.page.update()

def main(page: ft.Page):
    """Função principal que inicializa a aplicação criando uma instância da classe App"""
    # Cria uma instância da aplicação passando a página do Flet
    app = App(page)

# Ponto de entrada da aplicação - executa apenas quando o arquivo é executado diretamente
if __name__ == "__main__":
    # Inicia a aplicação Flet como aplicação desktop
    ft.app(target=main, view=ft.AppView.FLET_APP)