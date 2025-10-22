import flet as ft
from backend.statistics_wrapper import get_statistics_wrapper

class DashboardProfessor(ft.Container):
    """Dashboard do professor com design clean, moderno e fluido."""

    def __init__(self, page: ft.Page, controller):
        """Inicializa o dashboard com interface moderna."""
        super().__init__(
            expand=True,
            width=None,
            height=None,
            padding=ft.padding.all(0),
            margin=ft.margin.all(0)
        )
        self.page = page
        self.controller = controller
        
        # Obter wrapper de estatísticas
        self.stats_wrapper = get_statistics_wrapper()

        self.create_components()
        self.setup_layout()

    def get_real_statistics(self):
        """Obtém estatísticas reais do banco de dados via funções C"""
        if not self.controller.current_user:
            return {"tarefas": "0", "alunos": "0", "avaliacoes": "0"}
        
        professor_id = self.controller.current_user['id']
        
        # Obter estatísticas em tempo real
        stats = {"tarefas": "0", "alunos": "0", "avaliacoes": "0"}
        
        try:
            if self.stats_wrapper and self.stats_wrapper.lib:
                # Total de tarefas ativas do professor
                tarefas = self.stats_wrapper.get_professor_active_tasks(professor_id)
                stats["tarefas"] = str(tarefas)
                
                # Total de alunos cadastrados
                alunos = self.stats_wrapper.get_total_students()
                stats["alunos"] = str(alunos)
                
                # Total de respostas avaliadas pelo professor
                avaliacoes = self.stats_wrapper.get_professor_evaluated_responses(professor_id)
                stats["avaliacoes"] = str(avaliacoes)
        except:
            pass
        
        return stats

    def update_statistics(self):
        """Atualiza as estatísticas em tempo real"""
        real_stats = self.get_real_statistics()
        
        # Atualizar os valores nos cards de estatísticas
        if hasattr(self, 'stats_row') and self.stats_row.controls:
            # Card de tarefas ativas
            if len(self.stats_row.controls) > 0:
                card = self.stats_row.controls[0]
                if hasattr(card, 'content') and hasattr(card.content, 'controls'):
                    row_content = card.content.controls[0]
                    if hasattr(row_content, 'controls') and len(row_content.controls) > 2:
                        column = row_content.controls[2]
                        if hasattr(column, 'controls') and len(column.controls) > 0:
                            column.controls[0].value = real_stats["tarefas"]
            
            # Card de alunos
            if len(self.stats_row.controls) > 1:
                card = self.stats_row.controls[1]
                if hasattr(card, 'content') and hasattr(card.content, 'controls'):
                    row_content = card.content.controls[0]
                    if hasattr(row_content, 'controls') and len(row_content.controls) > 2:
                        column = row_content.controls[2]
                        if hasattr(column, 'controls') and len(column.controls) > 0:
                            column.controls[0].value = real_stats["alunos"]
            
            # Card de avaliações
            if len(self.stats_row.controls) > 2:
                card = self.stats_row.controls[2]
                if hasattr(card, 'content') and hasattr(card.content, 'controls'):
                    row_content = card.content.controls[0]
                    if hasattr(row_content, 'controls') and len(row_content.controls) > 2:
                        column = row_content.controls[2]
                        if hasattr(column, 'controls') and len(column.controls) > 0:
                            column.controls[0].value = real_stats["avaliacoes"]
        
        # Atualizar a página
        self.page.update()

    def create_components(self):
        """Cria todos os componentes da interface"""
        
        # Nome do usuário
        fullname = self.controller.current_user['full_name'] if self.controller.current_user else "Professor"
        
        # Avatar moderno e clean - MAIOR
        self.user_avatar = ft.Container(
            content=ft.Image(
                src="frontend/assets/personagem_3.png",
                width=90,
                height=90,
                fit=ft.ImageFit.CONTAIN,
                error_content=ft.Container(
                    content=ft.Icon(
                        ft.icons.PERSON_ROUNDED,
                        size=45,
                        color=ft.colors.PINK_400
                    ),
                    alignment=ft.alignment.center
                )
            ),
            width=120,
            height=120,
            border_radius=60,
            bgcolor=ft.colors.WHITE,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.colors.with_opacity(0.08, ft.colors.BLACK),
                offset=ft.Offset(0, 6)
            ),
            border=ft.border.all(4, ft.colors.PINK_100)
        )

        # Botão de logout clean - MAIOR
        self.logout_button = ft.Container(
            content=ft.Row([
                ft.Icon(ft.icons.LOGOUT_ROUNDED, color=ft.colors.PINK_500, size=24),
                ft.Text("Sair", color=ft.colors.PINK_500, size=18, weight=ft.FontWeight.W_600)
            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER, tight=True),
            width=130,
            height=60,
            bgcolor=ft.colors.WHITE,
            border_radius=30,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=15,
                color=ft.colors.with_opacity(0.06, ft.colors.BLACK),
                offset=ft.Offset(0, 4)
            ),
            border=ft.border.all(1, ft.colors.PINK_100),
            on_click=self.logout
        )

        # Cards de ação modernos e clean - MAIORES
        self.create_task_card = self.create_action_card(
            title="Criar Tarefa",
            subtitle="Crie uma nova tarefa\npara seus alunos",
            icon=ft.icons.ADD_TASK_ROUNDED,
            primary_color=ft.colors.PINK_400,
            action=self.go_to_criar_tarefa
        )

        self.view_tasks_card = self.create_action_card(
            title="Gerenciar Tarefas",
            subtitle="Visualize e gerencie\nsuas tarefas criadas",
            icon=ft.icons.ASSIGNMENT_ROUNDED,
            primary_color=ft.colors.PURPLE_400,
            action=self.go_to_ver_tarefa
        )

        # Obter estatísticas reais
        real_stats = self.get_real_statistics()

        # Estatísticas clean - MAIORES com dados reais
        self.stats_row = ft.Row([
            self.create_stat_card("Tarefas Ativas", real_stats["tarefas"], ft.icons.TASK_ALT_ROUNDED, ft.colors.PINK_400),
            self.create_stat_card("Alunos", real_stats["alunos"], ft.icons.PEOPLE_ROUNDED, ft.colors.PURPLE_400),
            self.create_stat_card("Avaliações", real_stats["avaliacoes"], ft.icons.GRADE_ROUNDED, ft.colors.PINK_300),
        ], spacing=60, alignment=ft.MainAxisAlignment.CENTER)

    def create_action_card(self, title, subtitle, icon, primary_color, action):
        """Cria um card de ação moderno e clean - MAIOR"""
        return ft.Container(
            content=ft.Column([
                # Ícone com design clean - MAIOR
                ft.Container(
                    content=ft.Icon(icon, size=55, color=primary_color),
                    width=110,
                    height=110,
                    border_radius=55,
                    bgcolor=ft.colors.WHITE,
                    alignment=ft.alignment.center,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=18,
                        color=ft.colors.with_opacity(0.08, ft.colors.BLACK),
                        offset=ft.Offset(0, 6)
                    ),
                    border=ft.border.all(3, ft.colors.with_opacity(0.1, primary_color))
                ),
                
                ft.Container(height=35),
                
                # Título - MAIOR
                ft.Text(
                    title,
                    size=26,
                    weight=ft.FontWeight.W_600,
                    color=ft.colors.GREY_800,
                    text_align=ft.TextAlign.CENTER
                ),
                
                ft.Container(height=12),
                
                # Subtítulo - MAIOR
                ft.Text(
                    subtitle,
                    size=18,
                    color=ft.colors.GREY_500,
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.W_400
                ),
                
                ft.Container(height=35),
                
                # Botão de ação clean - MAIOR
                ft.Container(
                    content=ft.Text(
                        "Acessar",
                        size=18,
                        weight=ft.FontWeight.W_600,
                        color=ft.colors.WHITE
                    ),
                    width=160,
                    height=55,
                    bgcolor=primary_color,
                    border_radius=27,
                    alignment=ft.alignment.center,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=12,
                        color=ft.colors.with_opacity(0.2, primary_color),
                        offset=ft.Offset(0, 4)
                    ),
                    on_click=action
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
            ),
            width=380,
            height=420,
            bgcolor=ft.colors.WHITE,
            border_radius=25,
            padding=ft.padding.all(40),
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.colors.with_opacity(0.06, ft.colors.BLACK),
                offset=ft.Offset(0, 8)
            ),
            border=ft.border.all(1, ft.colors.with_opacity(0.05, ft.colors.BLACK))
        )

    def create_stat_card(self, label, value, icon, color):
        """Cria um card de estatística clean - MAIOR"""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, size=32, color=color),
                    width=80,
                    height=80,
                    border_radius=40,
                    bgcolor=ft.colors.with_opacity(0.1, color),
                    alignment=ft.alignment.center
                ),
                ft.Container(width=20),
                ft.Column([
                    ft.Text(
                        value,
                        size=34,
                        weight=ft.FontWeight.W_700,
                        color=ft.colors.GREY_800
                    ),
                    ft.Text(
                        label,
                        size=16,
                        color=ft.colors.GREY_500,
                        weight=ft.FontWeight.W_500
                    )
                ], spacing=4)
            ], alignment=ft.MainAxisAlignment.START),
            width=280,
            height=120,
            bgcolor=ft.colors.WHITE,
            border_radius=20,
            padding=ft.padding.all(30),
            alignment=ft.alignment.center_left,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=15,
                color=ft.colors.with_opacity(0.05, ft.colors.BLACK),
                offset=ft.Offset(0, 5)
            ),
            border=ft.border.all(1, ft.colors.with_opacity(0.05, ft.colors.BLACK))
        )

    def setup_layout(self):
        """Configura o layout da página"""
        
        # Header clean - MAIOR
        header = ft.Container(
            content=ft.Row([
                # Lado esquerdo - Avatar e saudação
                ft.Row([
                    self.user_avatar,
                    ft.Container(width=30),
                    ft.Column([
                        ft.Text(
                            f"Olá, {self.controller.current_user['full_name'] if self.controller.current_user else 'Professor'}!",
                            size=34,
                            weight=ft.FontWeight.W_600,
                            color=ft.colors.GREY_800
                        ),
                        ft.Text(
                            "Bem-vindo ao seu painel de controle",
                            size=20,
                            color=ft.colors.GREY_500,
                            weight=ft.FontWeight.W_400
                        )
                    ], spacing=6)
                ], alignment=ft.MainAxisAlignment.START),
                
                # Lado direito - Controles
                self.logout_button
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=50, vertical=45)
        )

        # Seção de estatísticas - MAIOR
        stats_section = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Resumo Geral",
                    size=28,
                    weight=ft.FontWeight.W_600,
                    color=ft.colors.GREY_800
                ),
                ft.Container(height=25),
                self.stats_row
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=50, vertical=35)
        )

        # Seção de ações principais - MAIOR
        actions_section = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Ações Principais",
                    size=28,
                    weight=ft.FontWeight.W_600,
                    color=ft.colors.GREY_800,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=35),
                ft.Row([
                    self.create_task_card,
                    self.view_tasks_card,
                ], spacing=50, alignment=ft.MainAxisAlignment.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=50, vertical=35)
        )

        # Layout principal com fundo branco clean
        self.content = ft.Container(
            expand=True,
            width=None,
            height=None,
            padding=ft.padding.all(0),
            margin=ft.margin.all(0),
            
            content=ft.Column([
                header,
                stats_section,
                actions_section,
                ft.Container(expand=True)
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO
            )
        )

    def did_mount(self):
        """Chamado quando o componente é montado - atualiza estatísticas"""
        self.update_statistics()

    def logout(self, e):
        """Executa logout com animação"""
        self.controller.current_user = None
        self.controller.show_snackbar("Logout realizado com sucesso!", "success")
        self.controller.show_page("Login")

    def go_to_criar_tarefa(self, e):
        """Navega para criar tarefa"""
        self.controller.current_task = None
        self.controller.show_page("CriarTarefa")

    def go_to_ver_tarefa(self, e):
        """Navega para ver tarefas"""
        self.controller.show_page("VerTarefa")