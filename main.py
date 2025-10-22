"""
Sistema Acadêmico Colaborativo
Aplicação principal usando Flet para interface desktop
"""
import flet as ft
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
from backend.database import init_database

class App:
    """Classe principal da aplicação"""

    def __init__(self, page: ft.Page):
        """Inicializa a aplicação"""
        self.page = page
        self.page.title = "Sistema Acadêmico Colaborativo"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.scroll = ft.ScrollMode.AUTO
        
        # Configurações para tela cheia - FORÇAR ALTURA TOTAL
        self.page.window.maximized = True
        self.page.window.full_screen = False
        
        # REMOVER padding e spacing que podem limitar a altura
        self.page.padding = 0
        self.page.spacing = 0
        
        # FORÇAR que a página ocupe 100% da altura disponível
        self.page.expand = True
        
        # Configurar tamanho mínimo da janela
        self.page.window.min_width = 1024
        self.page.window.min_height = 768
        
        # Configurar tamanho inicial da janela (caso não maximize)
        self.page.window.width = 1366
        self.page.window.height = 768

        # Inicializar banco de dados
        init_database()

        # Estado da aplicação
        self.current_user = None
        self.current_task = None
        self.current_student_response = None

        # Dicionário de páginas
        self.pages = {
            "Login": Login,
            "Register": Register,
            "DashboardProfessor": DashboardProfessor,
            "DashboardAluno": DashboardAluno,
            "CriarTarefa": CriarTarefa,
            "VerTarefa": VerTarefa,
            "DetalheTarefa": DetalheTarefa,
            "EditarTarefa": EditarTarefa,
            "DetalheRespostaAluno": DetalheRespostaAluno,
            "VerTarefasAluno": VerTarefasAluno,
            "VerNotasAluno": VerNotasAluno,
            "DetalheTarefaAluno": DetalheTarefaAluno,
        }

        # Página atual
        self.current_page = None

        # Mostrar login inicial
        self.show_page("Login")

    def show_snackbar(self, message: str, type: str = "info"):
        """Exibe um snackbar com mensagem"""
        if type == "success":
            bgcolor = ft.colors.PINK_600
        elif type == "error":
            bgcolor = ft.colors.PURPLE_600
        elif type == "warning":
            bgcolor = ft.colors.DEEP_PURPLE_600
        else:
            bgcolor = ft.colors.PURPLE_400

        snackbar = ft.SnackBar(
            content=ft.Text(message, color=ft.colors.WHITE),
            bgcolor=bgcolor,
            duration=3000
        )
        self.page.overlay.append(snackbar)
        snackbar.open = True
        self.page.update()



    def show_page(self, page_name: str):
        """Navega para uma página específica"""
        page_class = self.pages[page_name]
        self.current_page = page_class(self.page, self)
        self.page.clean()
        self.page.add(self.current_page)
        self.page.update()

def main(page: ft.Page):
    """Função principal da aplicação"""
    app = App(page)

if __name__ == "__main__":
    # Executar como aplicação desktop
    ft.app(target=main, view=ft.AppView.FLET_APP)