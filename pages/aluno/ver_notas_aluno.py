import flet as ft
from db.database import get_all_tasks, get_user_id, get_student_response
from datetime import datetime

class VerNotasAluno(ft.Container):
    """Classe responsável pela tela de visualização de notas do aluno."""

    def __init__(self, page: ft.Page, controller):
        """Inicializa a tela de ver notas do aluno."""
        super().__init__()
        self.page = page
        self.controller = controller

        # Título
        self.title = ft.Text(
            "Minhas Notas", 
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

        # Container para a lista de tarefas
        self.tasks_container = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=15
        )

        # Layout principal centralizado
        self.content = ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            padding=ft.padding.all(40),
            content=ft.Column([
                ft.Row([
                    ft.Container(),  # Spacer
                    self.back_button
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=40),
                self.title,
                ft.Container(height=40),
                ft.Container(
                    content=self.tasks_container,
                    width=800,
                    height=500,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=15,
                    padding=20,
                    border=ft.border.all(1, ft.Colors.GREY_300)
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO)
        )

        # Carregar tarefas inicialmente
        self.refresh()

    def refresh(self):
        """Atualiza a lista de tarefas com status de entrega"""
        tasks = get_all_tasks()
        self.tasks_container.controls.clear()

        if not tasks:
            self.tasks_container.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.GRADE_OUTLINED, size=64, color=ft.Colors.GREY_400),
                        ft.Container(height=20),
                        ft.Text(
                            "Nenhuma tarefa encontrada.", 
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
            user_ra = self.controller.current_user['ra']
            user_id = get_user_id(user_ra)
            for task in tasks:
                task_id = task[0]
                response = get_student_response(task_id, user_id) if user_id else None
                exp_date = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S')
                expired = datetime.now() > exp_date

                # Determinar status e cor
                if response:
                    rating = response[3]
                    comment = response[4]
                    if rating is not None and comment and comment.strip():
                        status = "Corrigido"
                        status_color = ft.Colors.BLUE_600
                        status_icon = ft.Icons.DONE_ALL
                        display_rating = True
                    else:
                        status = "Entregue"
                        status_color = ft.Colors.GREEN_600
                        status_icon = ft.Icons.DONE
                        display_rating = False
                else:
                    if expired:
                        status = "Expirado"
                        status_color = ft.Colors.RED_600
                        status_icon = ft.Icons.CLOSE
                    else:
                        status = "Ativo"
                        status_color = ft.Colors.ORANGE_600
                        status_icon = ft.Icons.SCHEDULE
                    display_rating = False

                # Conteúdo do card
                card_content = [
                    ft.Row([
                        ft.Icon(status_icon, size=24, color=status_color),
                        ft.Container(width=10),
                        ft.Text(
                            task[1], 
                            size=18, 
                            weight=ft.FontWeight.BOLD, 
                            color=ft.Colors.BLACK,
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Text(
                                status, 
                                size=14, 
                                color=ft.Colors.WHITE,
                                weight=ft.FontWeight.BOLD
                            ),
                            bgcolor=status_color,
                            padding=ft.padding.symmetric(horizontal=12, vertical=6),
                            border_radius=15
                        )
                    ]),
                    ft.Container(height=10),
                    ft.Text(
                        f"Vencimento: {exp_date.strftime('%d/%m/%Y às %H:%M')}", 
                        size=14, 
                        color=ft.Colors.GREY_700
                    ),
                ]

                if display_rating:
                    card_content.extend([
                        ft.Container(height=15),
                        ft.Row([
                            ft.Container(
                                content=ft.Text(
                                    f"Nota: {rating}", 
                                    size=20, 
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE
                                ),
                                bgcolor=ft.Colors.TEAL_600,
                                padding=ft.padding.symmetric(horizontal=15, vertical=8),
                                border_radius=20
                            )
                        ]),
                        ft.Container(height=10),
                        ft.Container(
                            content=ft.Text(
                                f"Comentário: {comment}", 
                                size=14, 
                                color=ft.Colors.GREY_800
                            ),
                            bgcolor=ft.Colors.GREY_100,
                            padding=15,
                            border_radius=10,
                            border=ft.border.all(1, ft.Colors.GREY_300)
                        )
                    ])

                task_card = ft.Card(
                    content=ft.Container(
                        content=ft.Column(card_content),
                        width=750,
                        padding=20,
                        border_radius=10
                    ),
                    elevation=4
                )
                self.tasks_container.controls.append(task_card)

        self.page.update()

    def go_back(self, e):
        """Volta para o dashboard do aluno."""
        self.controller.show_page("DashboardAluno")