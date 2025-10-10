import flet as ft

class DashboardProfessor(ft.Container):
    """Classe responsável pelo dashboard do professor."""

    def __init__(self, page: ft.Page, controller):
        """Inicializa o dashboard do professor."""
        super().__init__()
        self.page = page
        self.controller = controller

        # Título de boas-vindas
        username = self.controller.current_user['username'] if self.controller.current_user else "Professor"
        self.welcome_text = ft.Text(
            f"Bem-vindo(a), {username}!",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.TEAL_600,
            text_align=ft.TextAlign.CENTER
        )

        self.subtitle_text = ft.Text(
            "Painel do Professor",
            size=18,
            color=ft.Colors.GREY_600,
            text_align=ft.TextAlign.CENTER
        )

        # Botão de logout
        self.logout_button = ft.ElevatedButton(
            "Sair",
            width=100,
            height=40,
            bgcolor=ft.Colors.RED_400,
            color=ft.Colors.WHITE,
            icon=ft.Icons.LOGOUT,
            on_click=self.logout,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
                elevation=3
            )
        )

        # Card para criar tarefa
        self.create_task_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon(ft.Icons.ADD_TASK, size=64, color=ft.Colors.TEAL_600),
                        padding=ft.padding.only(bottom=15)
                    ),
                    ft.Text(
                        "Criar Tarefa", 
                        size=22, 
                        weight=ft.FontWeight.BOLD, 
                        color=ft.Colors.BLACK,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "Crie uma nova tarefa\npara seus alunos", 
                        size=14, 
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        "Criar Nova",
                        width=150,
                        height=40,
                        bgcolor=ft.Colors.TEAL_600,
                        color=ft.Colors.WHITE,
                        on_click=self.go_to_criar_tarefa,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=20),
                            elevation=3
                        )
                    )
                ], 
                alignment=ft.MainAxisAlignment.CENTER, 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                width=280,
                height=340,
                padding=25,
                border_radius=15,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[ft.Colors.WHITE, ft.Colors.TEAL_50]
                )
            ),
            elevation=6
        )

        # Card para ver tarefas
        self.view_task_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon(ft.Icons.VIEW_LIST, size=64, color=ft.Colors.BLUE_600),
                        padding=ft.padding.only(bottom=15)
                    ),
                    ft.Text(
                        "Ver Tarefas", 
                        size=22, 
                        weight=ft.FontWeight.BOLD, 
                        color=ft.Colors.BLACK,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "Visualize e gerencie\nsuas tarefas criadas", 
                        size=14, 
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        "Visualizar",
                        width=150,
                        height=40,
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE,
                        on_click=self.go_to_ver_tarefa,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=20),
                            elevation=3
                        )
                    )
                ], 
                alignment=ft.MainAxisAlignment.CENTER, 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                width=280,
                height=340,
                padding=25,
                border_radius=15,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[ft.Colors.WHITE, ft.Colors.BLUE_50]
                )
            ),
            elevation=6
        )

        # Layout principal adaptado para tela cheia
        self.content = ft.Container(
            expand=True,
            padding=ft.padding.all(30),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.Colors.GREY_50, ft.Colors.WHITE]
            ),
            content=ft.Column([
                # Header com logout
                ft.Container(
                    content=ft.Row([
                        ft.Container(expand=True),
                        self.logout_button
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.padding.only(bottom=30)
                ),
                
                # Título centralizado
                ft.Container(
                    content=ft.Column([
                        self.welcome_text,
                        ft.Container(height=10),
                        self.subtitle_text
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.padding.only(bottom=50)
                ),
                
                # Cards de ação centralizados e responsivos
                ft.Container(
                    content=ft.ResponsiveRow([
                        ft.Container(
                            content=self.create_task_card,
                            col={"sm": 12, "md": 4, "lg": 2},
                            alignment=ft.alignment.center
                        ),
                        ft.Container(
                            content=self.view_task_card,
                            col={"sm": 12, "md": 4, "lg": 2},
                            alignment=ft.alignment.center
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    expand=True,
                    alignment=ft.alignment.center
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
            )
        )

    def logout(self, e):
        """Executa o logout do usuário."""
        self.controller.current_user = None
        self.controller.show_page("Login")

    def go_to_criar_tarefa(self, e):
        """Navega para a tela de criar tarefa."""
        self.controller.current_task = None
        self.controller.show_page("CriarTarefa")

    def go_to_ver_tarefa(self, e):
        """Navega para a tela de ver tarefas."""
        self.controller.show_page("VerTarefa")