import flet as ft
from db.database import get_tasks_by_user_id, get_user_id
from datetime import datetime

class VerTarefa(ft.Container):
    """Classe responsável pela tela de visualização de tarefas do professor."""

    def __init__(self, page: ft.Page, controller):
        """Inicializa a tela de ver tarefas."""
        super().__init__()
        self.page = page
        self.controller = controller

        # Título da tela
        self.title = ft.Text(
            "Minhas Tarefas",
            size=36,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.TEAL_600,
            text_align=ft.TextAlign.CENTER
        )

        # Botão voltar
        self.back_button = ft.ElevatedButton(
            "Voltar",
            width=120,
            height=40,
            bgcolor=ft.Colors.GREY_600,
            color=ft.Colors.WHITE,
            icon=ft.Icons.ARROW_BACK,
            on_click=self.go_back,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
                elevation=3
            )
        )

        # Container para a lista de tarefas
        self.tasks_container = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=15
        )

        # Layout principal responsivo
        self.content = ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            padding=ft.padding.all(30),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.Colors.TEAL_50, ft.Colors.WHITE]
            ),
            content=ft.Column([
                ft.Row([
                    ft.Container(expand=True),
                    self.back_button
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=30),
                self.title,
                ft.Container(height=40),
                ft.Container(
                    content=self.tasks_container,
                    width=900,
                    height=500,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=20,
                    padding=25,
                    border=ft.border.all(1, ft.Colors.GREY_200)
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
            )
        )

        # Carregar tarefas inicialmente
        self.refresh()

    def refresh(self):
        """Atualiza a lista de tarefas"""
        # Obter tarefas apenas do professor logado
        if not self.controller.current_user:
            self.tasks_container.controls.clear()
            self.tasks_container.controls.append(
                ft.Container(
                    content=ft.Text(
                        "Erro: usuário não está logado.",
                        size=18,
                        color=ft.Colors.RED_600,
                        text_align=ft.TextAlign.CENTER
                    ),
                    alignment=ft.alignment.center,
                    height=300
                )
            )
            self.page.update()
            return

        user_id = get_user_id(self.controller.current_user["ra"])
        if not user_id:
            self.tasks_container.controls.clear()
            self.tasks_container.controls.append(
                ft.Container(
                    content=ft.Text(
                        "Erro: não foi possível identificar o usuário.",
                        size=18,
                        color=ft.Colors.RED_600,
                        text_align=ft.TextAlign.CENTER
                    ),
                    alignment=ft.alignment.center,
                    height=300
                )
            )
            self.page.update()
            return

        tasks = get_tasks_by_user_id(user_id)
        self.tasks_container.controls.clear()

        if not tasks:
            self.tasks_container.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.ASSIGNMENT_OUTLINED, size=64, color=ft.Colors.GREY_400),
                        ft.Container(height=20),
                        ft.Text(
                            "Nenhuma tarefa encontrada.",
                            size=18,
                            color=ft.Colors.GREY_600,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=15),
                        ft.Text(
                            "Crie sua primeira tarefa!",
                            size=14,
                            color=ft.Colors.GREY_500,
                            text_align=ft.TextAlign.CENTER
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.alignment.center,
                    height=300
                )
            )
        else:
            for task in tasks:
                exp_date = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S')
                creation_date = datetime.strptime(task[3], '%Y-%m-%d %H:%M:%S.%f')
                is_expired = datetime.now() > exp_date

                # Determinar status e cor
                if is_expired:
                    status = "Expirada"
                    status_color = ft.Colors.RED_600
                    status_icon = ft.Icons.SCHEDULE_OUTLINED
                else:
                    status = "Ativa"
                    status_color = ft.Colors.GREEN_600
                    status_icon = ft.Icons.CHECK_CIRCLE_OUTLINE

                task_card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(status_icon, size=24, color=status_color),
                                ft.Container(width=15),
                                ft.Text(
                                    task[1],
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLACK,
                                    expand=True
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        status,
                                        size=12,
                                        color=ft.Colors.WHITE,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    bgcolor=status_color,
                                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                    border_radius=15
                                )
                            ]),
                            ft.Container(height=15),
                            
                            ft.Container(
                                content=ft.Text(
                                    task[2] if task[2] else "Sem descrição",
                                    size=14,
                                    color=ft.Colors.GREY_700,
                                    max_lines=2,
                                    overflow=ft.TextOverflow.ELLIPSIS
                                ),
                                bgcolor=ft.Colors.GREY_50,
                                padding=12,
                                border_radius=8,
                                border=ft.border.all(1, ft.Colors.GREY_200)
                            ),
                            
                            ft.Container(height=15),
                            ft.Row([
                                ft.Icon(ft.Icons.CALENDAR_TODAY, size=16, color=ft.Colors.GREY_500),
                                ft.Container(width=5),
                                ft.Text(
                                    f"Criado: {creation_date.strftime('%d/%m/%Y')}",
                                    size=12,
                                    color=ft.Colors.GREY_600
                                ),
                                ft.Container(width=20),
                                ft.Icon(ft.Icons.SCHEDULE, size=16, color=ft.Colors.GREY_500),
                                ft.Container(width=5),
                                ft.Text(
                                    f"Vence: {exp_date.strftime('%d/%m/%Y às %H:%M')}",
                                    size=12,
                                    color=ft.Colors.GREY_600
                                )
                            ]),
                            
                            ft.Container(height=20),
                            ft.Row([
                                ft.ElevatedButton(
                                    "Ver Detalhes",
                                    width=140,
                                    height=35,
                                    bgcolor=ft.Colors.TEAL_600,
                                    color=ft.Colors.WHITE,
                                    icon=ft.Icons.VISIBILITY,
                                    on_click=lambda e, t=task: self.show_task_detail(t),
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=17),
                                        elevation=2
                                    )
                                ),
                            ], alignment=ft.MainAxisAlignment.CENTER)
                        ]),
                        width=850,
                        padding=20,
                        border_radius=15
                    ),
                    elevation=4
                )
                self.tasks_container.controls.append(task_card)

        self.page.update()

    def show_task_detail(self, task):
        """Exibe os detalhes da tarefa selecionada."""
        self.controller.current_task = task
        self.controller.show_page("DetalheTarefa")

    def go_back(self, e):
        """Volta para o dashboard do professor."""
        self.controller.show_page("DashboardProfessor")