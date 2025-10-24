import flet as ft
from backend.database import get_all_tasks, get_user_id, get_student_response
from datetime import datetime

class VerNotasAluno(ft.Container):

    def __init__(self, page: ft.Page, controller):
        # Inicializa a tela de visualização de notas do aluno
        super().__init__(
            expand=True,
            width=None,
            height=None,
            padding=ft.padding.all(0),
            margin=ft.margin.all(0)
        )
        self.page = page
        self.controller = controller

        self.create_components()
        self.setup_layout()

    def create_components(self):
        # Cria os componentes principais da interface
        
        self.back_button = ft.Container(
            content=ft.Row([
                ft.Icon(ft.icons.ARROW_BACK_ROUNDED, color=ft.colors.PINK_500, size=24),
                ft.Text("Voltar", color=ft.colors.PINK_500, size=18, weight=ft.FontWeight.W_600)
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
            on_click=self.go_back
        )

        self.tasks_container = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def setup_layout(self):
        # Organiza o layout principal da página
        
        header = ft.Container(
            content=ft.Row([
                self.back_button,
                ft.Container(expand=True),
                ft.Column([
                    ft.Text(
                        "Minhas Notas",
                        size=42,
                        weight=ft.FontWeight.W_600,
                        color=ft.colors.GREY_800,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Visualize suas notas e avaliações",
                        size=20,
                        color=ft.colors.GREY_500,
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(expand=True)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=60, vertical=45)
        )

        notes_section = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=self.tasks_container,
                    width=1100,
                    height=600,
                    bgcolor=ft.colors.WHITE,
                    border_radius=25,
                    padding=ft.padding.all(35),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=20,
                        color=ft.colors.with_opacity(0.08, ft.colors.BLACK),
                        offset=ft.Offset(0, 8)
                    ),
                    border=ft.border.all(1, ft.colors.with_opacity(0.05, ft.colors.BLACK))
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=60, vertical=25)
        )

        self.content = ft.Container(
            expand=True,
            width=None,
            height=None,
            padding=ft.padding.all(0),
            margin=ft.margin.all(0),

            content=ft.Column([
                header,
                notes_section,
                ft.Container(expand=True)
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        self.refresh()

    def refresh(self):
        # Atualiza a lista de tarefas com notas e avaliações
        tasks = get_all_tasks()
        self.tasks_container.controls.clear()

        if not tasks:
            self.tasks_container.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.GRADE_OUTLINED, size=80, color=ft.colors.GREY_400),
                        ft.Container(height=25),
                        ft.Text(
                            "Nenhuma tarefa encontrada",
                            size=28,
                            weight=ft.FontWeight.W_600,
                            color=ft.colors.GREY_600,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=12),
                        ft.Text(
                            "Não há tarefas disponíveis no momento",
                            size=18,
                            color=ft.colors.GREY_500,
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
            user_ra = self.controller.current_user['ra']
            user_id = get_user_id(user_ra)
            tasks.sort(key=lambda x: datetime.strptime(x[3], '%Y-%m-%d %H:%M:%S'), reverse=True)
            for task in tasks:
                task_id = task[0]
                response = get_student_response(task_id, user_id) if user_id else None
                exp_date = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S')
                expired = datetime.now() > exp_date

                if response:
                    rating = response[3]
                    comment = response[4]
                    if rating is not None and comment and comment.strip():
                        status = "Corrigido"
                        status_color = ft.colors.BLUE_400
                        status_icon = ft.icons.DONE_ALL_ROUNDED
                        display_rating = True
                    else:
                        status = "Entregue"
                        status_color = ft.colors.GREEN_400
                        status_icon = ft.icons.DONE_ROUNDED
                        display_rating = False
                else:
                    if expired:
                        status = "Expirado"
                        status_color = ft.colors.RED_400
                        status_icon = ft.icons.CLOSE_ROUNDED
                    else:
                        status = "Ativo"
                        status_color = ft.colors.ORANGE_400
                        status_icon = ft.icons.SCHEDULE_ROUNDED
                    display_rating = False

                card_content = [
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(status_icon, size=32, color=status_color),
                            width=70,
                            height=70,
                            border_radius=35,
                            bgcolor=ft.colors.with_opacity(0.1, status_color),
                            alignment=ft.alignment.center
                        ),
                        ft.Container(width=20),
                        ft.Column([
                            ft.Text(
                                task[1],
                                size=24,
                                weight=ft.FontWeight.W_600,
                                color=ft.colors.GREY_800,
                                expand=True
                            ),
                            ft.Text(
                                f"Vencimento: {exp_date.strftime('%d/%m/%Y às %H:%M')}",
                                size=16,
                                color=ft.colors.GREY_600
                            )
                        ], expand=True, spacing=8),
                        ft.Container(
                            content=ft.Text(
                                status,
                                size=16,
                                color=ft.colors.WHITE,
                                weight=ft.FontWeight.W_600
                            ),
                            bgcolor=status_color,
                            padding=ft.padding.symmetric(horizontal=16, vertical=10),
                            border_radius=20
                        )
                    ])
                ]

                if display_rating:
                    card_content.extend([
                        ft.Container(height=25),
                        ft.Row([
                            ft.Container(
                                content=ft.Text(
                                    f"Nota: {rating}",
                                    size=24,
                                    weight=ft.FontWeight.W_700,
                                    color=ft.colors.WHITE
                                ),
                                bgcolor=ft.colors.PURPLE_400,
                                padding=ft.padding.symmetric(horizontal=20, vertical=12),
                                border_radius=25
                            )
                        ]),
                        ft.Container(height=15),
                        ft.Container(
                            content=ft.Text(
                                f"Comentário: {comment}",
                                size=18,
                                color=ft.colors.GREY_700
                            ),
                            bgcolor=ft.colors.with_opacity(0.05, ft.colors.PURPLE_400),
                            padding=ft.padding.all(20),
                            border_radius=15,
                            border=ft.border.all(1, ft.colors.with_opacity(0.1, ft.colors.PURPLE_400))
                        )
                    ])

                task_card = ft.Container(
                    content=ft.Column(card_content),
                    width=1000,
                    bgcolor=ft.colors.WHITE,
                    border_radius=20,
                    padding=ft.padding.all(25),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=12,
                        color=ft.colors.with_opacity(0.05, ft.colors.BLACK),
                        offset=ft.Offset(0, 4)
                    ),
                    border=ft.border.all(1, ft.colors.with_opacity(0.05, ft.colors.BLACK))
                )
                self.tasks_container.controls.append(task_card)

        self.page.update()

    def go_back(self, e):
        # Retorna para o dashboard do aluno
        self.controller.show_page("DashboardAluno")