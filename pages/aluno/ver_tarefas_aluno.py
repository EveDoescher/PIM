import flet as ft
from db.database import get_all_tasks
from datetime import datetime

class VerTarefasAluno(ft.Container):
    """Classe responsável pela tela de visualização de tarefas do aluno."""

    def __init__(self, page: ft.Page, controller):
        """Inicializa a tela de ver tarefas do aluno."""
        super().__init__()
        self.page = page
        self.controller = controller

        # Título
        self.title = ft.Text(
            "Ver Tarefas", 
            size=36, 
            weight=ft.FontWeight.BOLD, 
            color=ft.Colors.BLACK,
            text_align=ft.TextAlign.CENTER
        )

        # Botão voltar
        self.back_button = ft.ElevatedButton(
            "Voltar",
            width=120,
            height=40,
            bgcolor=ft.Colors.TEAL_600,
            color=ft.Colors.WHITE,
            on_click=self.go_back,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
                elevation=3
            )
        )

        # Container para a lista de tarefas - adaptado para tela cheia
        self.tasks_container = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=15,
            expand=True
        )

        # Layout principal adaptado para tela cheia
        self.content = ft.Container(
            expand=True,
            padding=ft.padding.all(40),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.Colors.GREY_50, ft.Colors.WHITE]
            ),
            content=ft.Column([
                ft.Row([
                    ft.Container(),  # Spacer
                    self.back_button
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=30),
                self.title,
                ft.Container(height=30),
                ft.Container(
                    content=self.tasks_container,
                    expand=True,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=15,
                    padding=20,
                    border=ft.border.all(1, ft.Colors.GREY_300)
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
            )
        )

        # Carregar tarefas inicialmente
        self.refresh()

    def refresh(self):
        """Atualiza a lista de tarefas ativas"""
        tasks = get_all_tasks()
        self.tasks_container.controls.clear()

        active_tasks = [task for task in tasks if datetime.now() < datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S')]

        if not active_tasks:
            self.tasks_container.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.ASSIGNMENT_OUTLINED, size=64, color=ft.Colors.GREY_400),
                        ft.Container(height=20),
                        ft.Text(
                            "Nenhuma tarefa ativa encontrada.", 
                            size=18, 
                            color=ft.Colors.GREY_600,
                            text_align=ft.TextAlign.CENTER
                        )
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.alignment.center,
                    height=200
                )
            )
        else:
            for task in active_tasks:
                exp_date = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S')
                
                task_card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.ASSIGNMENT, size=24, color=ft.Colors.TEAL_600),
                                ft.Container(width=10),
                                ft.Text(
                                    task[1], 
                                    size=18, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=ft.Colors.BLACK,
                                    expand=True
                                )
                            ]),
                            ft.Container(height=10),
                            ft.Text(
                                f"Vence em: {exp_date.strftime('%d/%m/%Y às %H:%M')}", 
                                size=14, 
                                color=ft.Colors.GREY_700
                            ),
                            ft.Container(height=15),
                            ft.ElevatedButton(
                                "Ver Detalhes",
                                width=150,
                                height=35,
                                bgcolor=ft.Colors.TEAL_600,
                                color=ft.Colors.WHITE,
                                on_click=lambda e, t=task: self.show_task_detail(t),
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=17),
                                    elevation=2
                                )
                            )
                        ]),
                        padding=20,
                        border_radius=10
                    ),
                    elevation=4
                )
                self.tasks_container.controls.append(task_card)

        self.page.update()

    def show_task_detail(self, task):
        """Exibe os detalhes da tarefa selecionada."""
        self.controller.current_task = task
        self.controller.show_page("DetalheTarefaAluno")

    def go_back(self, e):
        """Volta para o dashboard"""
        self.controller.show_page("DashboardAluno")