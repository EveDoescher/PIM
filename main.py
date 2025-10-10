import flet as ft
from pages.login import Login
from pages.register import Register
from pages.professor.dashboard_professor import DashboardProfessor
from pages.aluno.dashboard_aluno import DashboardAluno
from pages.professor.criar_tarefa import CriarTarefa
from pages.professor.ver_tarefa import VerTarefa
from pages.professor.detalhe_tarefa import DetalheTarefa
from pages.professor.editar_tarefa import EditarTarefa
from pages.professor.detalhe_resposta_aluno import DetalheRespostaAluno
from pages.aluno.ver_tarefas_aluno import VerTarefasAluno
from pages.aluno.ver_notas_aluno import VerNotasAluno
from pages.aluno.detalhe_tarefa_aluno import DetalheTarefaAluno

class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Sistema acadêmico colaborativo"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.scroll = ft.ScrollMode.AUTO
        
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

    def show_page(self, page_name):
        """Navega para uma página específica"""
        if self.current_page:
            self.page.controls.clear()
        
        page_class = self.pages[page_name]
        self.current_page = page_class(self.page, self)
        self.page.add(self.current_page)
        self.page.update()

def main(page: ft.Page):
    app = App(page)

if __name__ == "__main__":
    ft.app(target=main)