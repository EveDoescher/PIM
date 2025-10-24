import flet as ft
from backend.database import get_students_who_responded, delete_task
from datetime import datetime

class DetalheTarefa(ft.Container):

    def __init__(self, page: ft.Page, controller):
        # Inicializa a tela de detalhes da tarefa
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
        # Cria todos os componentes da interface
        
        self.back_button = ft.Container(
            content=ft.Row([
                ft.Icon(ft.icons.ARROW_BACK_ROUNDED, color=ft.colors.PINK_500, size=24),
                ft.Text("Voltar", color=ft.colors.PINK_500, size=18, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER)
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

        self.task_details_container = ft.Container(
            bgcolor=ft.colors.WHITE,
            border_radius=25,
            padding=ft.padding.all(40),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.colors.with_opacity(0.08, ft.colors.BLACK),
                offset=ft.Offset(0, 8)
            ),
            border=ft.border.all(1, ft.colors.with_opacity(0.05, ft.colors.BLACK))
        )

        self.responses_container = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=20
        )

        self.edit_button = ft.Container(
            content=ft.Row([
                ft.Icon(ft.icons.EDIT_ROUNDED, color=ft.colors.WHITE, size=24),
                ft.Text("Editar Tarefa", color=ft.colors.WHITE, size=18, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER)
            ], spacing=15, alignment=ft.MainAxisAlignment.CENTER),
            width=200,
            height=60,
            bgcolor=ft.colors.ORANGE_400,
            border_radius=30,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=15,
                color=ft.colors.with_opacity(0.2, ft.colors.ORANGE_400),
                offset=ft.Offset(0, 4)
            ),
            on_click=self.edit_task
        )

        self.delete_button = ft.Container(
            content=ft.Row([
                ft.Icon(ft.icons.DELETE_ROUNDED, color=ft.colors.WHITE, size=24),
                ft.Text("Excluir Tarefa", color=ft.colors.WHITE, size=18, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER)
            ], spacing=15, alignment=ft.MainAxisAlignment.CENTER),
            width=200,
            height=60,
            bgcolor=ft.colors.RED_400,
            border_radius=30,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=15,
                color=ft.colors.with_opacity(0.2, ft.colors.RED_400),
                offset=ft.Offset(0, 4)
            ),
            on_click=self.confirm_delete_task
        )

    def setup_layout(self):
        # Configura o layout da página
        
        header = ft.Container(
            content=ft.Row([
                self.back_button,
                ft.Container(expand=True),
                ft.Column([
                    ft.Text(
                        "Detalhes da Tarefa",
                        size=42,
                        weight=ft.FontWeight.W_600,
                        color=ft.colors.GREY_800,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Visualize informações e respostas dos alunos",
                        size=20,
                        color=ft.colors.GREY_500,
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(expand=True)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=60, vertical=45)
        )

        task_section = ft.Container(
            content=ft.Column([
                self.task_details_container,
                ft.Container(height=35),
                ft.Row([
                    self.edit_button,
                    ft.Container(width=25),
                    self.delete_button
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=60, vertical=25)
        )

        responses_section = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Respostas dos Alunos",
                    size=32,
                    weight=ft.FontWeight.W_600,
                    color=ft.colors.GREY_800,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=25),
                ft.Container(
                    content=self.responses_container,
                    width=1100,
                    height=500,
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
                task_section,
                responses_section,
                ft.Container(expand=True)
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO
            )
        )

        self.refresh()

    def refresh(self):
        # Atualiza os detalhes da tarefa e respostas dos alunos
        if self.controller.current_task:
            task = self.controller.current_task
            
            creation_date = datetime.strptime(task[3], '%Y-%m-%d %H:%M:%S')
            exp_date = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S')
            is_expired = datetime.now() > exp_date

            status = "Expirada" if is_expired else "Ativa"
            status_color = ft.colors.RED_400 if is_expired else ft.colors.GREEN_400
            status_icon = ft.icons.SCHEDULE_SEND_ROUNDED if is_expired else ft.icons.SCHEDULE_ROUNDED

            task_info = ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.icons.ASSIGNMENT_ROUNDED, size=45, color=ft.colors.PURPLE_400),
                        width=90,
                        height=90,
                        border_radius=45,
                        bgcolor=ft.colors.with_opacity(0.1, ft.colors.PURPLE_400),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(width=25),
                    ft.Column([
                        ft.Text(
                            task[1],
                            size=34,
                            weight=ft.FontWeight.W_600,
                            color=ft.colors.GREY_800,
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(status_icon, size=20, color=status_color),
                                ft.Text(
                                    status,
                                    size=18,
                                    color=status_color,
                                    weight=ft.FontWeight.W_600
                                )
                            ], spacing=8),
                            padding=ft.padding.symmetric(horizontal=16, vertical=10),
                            border_radius=20,
                            bgcolor=ft.colors.with_opacity(0.1, status_color)
                        )
                    ], expand=True, spacing=12)
                ]),
                
                ft.Container(height=25),
                
                ft.Container(
                    content=ft.Text(
                        task[2] if task[2] else "Sem descrição disponível",
                        size=20,
                        color=ft.colors.GREY_700
                    ),
                    bgcolor=ft.colors.with_opacity(0.05, ft.colors.PURPLE_400),
                    padding=ft.padding.all(25),
                    border_radius=20,
                    border=ft.border.all(1, ft.colors.with_opacity(0.1, ft.colors.PURPLE_400))
                ),
                
                ft.Container(height=25),
                ft.Row([
                    ft.Icon(ft.icons.CALENDAR_TODAY_ROUNDED, size=24, color=ft.colors.GREY_600),
                    ft.Container(width=12),
                    ft.Text(
                        f"Criada em: {creation_date.strftime('%d/%m/%Y às %H:%M')}",
                        size=18,
                        color=ft.colors.GREY_600,
                        weight=ft.FontWeight.W_500
                    )
                ]),
                ft.Container(height=15),
                ft.Row([
                    ft.Icon(status_icon, size=24, color=status_color),
                    ft.Container(width=12),
                    ft.Text(
                        f"Vence em: {exp_date.strftime('%d/%m/%Y às %H:%M')}",
                        size=18,
                        color=status_color,
                        weight=ft.FontWeight.W_500
                    )
                ])
            ])

            self.task_details_container.content = task_info
            self.task_details_container.width = 1000

            self.load_student_responses()
        else:
            self.task_details_container.content = ft.Text(
                "Nenhuma tarefa selecionada",
                size=24,
                color=ft.colors.GREY_600
            )

        self.page.update()

    def load_student_responses(self):
        # Carrega as respostas dos alunos para a tarefa atual
        self.responses_container.controls.clear()

        if self.controller.current_task:
            task_id = self.controller.current_task[0]
            responses = get_students_who_responded(task_id)

            if not responses:
                self.responses_container.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.icons.ASSIGNMENT_OUTLINED, size=80, color=ft.colors.GREY_400),
                            ft.Container(height=25),
                            ft.Text(
                                "Nenhuma resposta encontrada",
                                size=26,
                                color=ft.colors.GREY_600,
                                text_align=ft.TextAlign.CENTER,
                                weight=ft.FontWeight.W_600
                            ),
                            ft.Container(height=12),
                            ft.Text(
                                "Os alunos ainda não enviaram suas respostas",
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
                for response in responses:
                    student_name = response[0]
                    user_id = response[1]
                    has_rating = response[2]
                    rating = response[3]
                    comment = response[4]
                    upload_date_str = response[5]
                    filename = response[6]

                    try:
                        submission_date = datetime.strptime(upload_date_str, '%Y-%m-%d %H:%M:%S.%f')
                    except ValueError:
                        try:
                            submission_date = datetime.strptime(upload_date_str, '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            submission_date = datetime.now()

                    is_graded = rating is not None

                    response_card = ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    content=ft.Icon(ft.icons.PERSON_ROUNDED, size=32, color=ft.colors.PURPLE_400),
                                    width=70,
                                    height=70,
                                    border_radius=35,
                                    bgcolor=ft.colors.with_opacity(0.1, ft.colors.PURPLE_400),
                                    alignment=ft.alignment.center
                                ),
                                ft.Container(width=20),
                                ft.Column([
                                    ft.Text(
                                        student_name,
                                        size=20,
                                        weight=ft.FontWeight.W_600,
                                        color=ft.colors.GREY_800,
                                        expand=True
                                    ),
                                    ft.Text(
                                        f"Arquivo: {filename}",
                                        size=16,
                                        color=ft.colors.GREY_600
                                    )
                                ], expand=True, spacing=6),
                                ft.Container(
                                    content=ft.Text(
                                        "Corrigido" if is_graded else "Pendente",
                                        size=16,
                                        color=ft.colors.WHITE,
                                        weight=ft.FontWeight.W_600
                                    ),
                                    bgcolor=ft.colors.GREEN_400 if is_graded else ft.colors.ORANGE_400,
                                    padding=ft.padding.symmetric(horizontal=16, vertical=10),
                                    border_radius=20
                                )
                            ]),
                            ft.Container(height=15),

                            ft.Row([
                                ft.Icon(ft.icons.SCHEDULE_ROUNDED, size=20, color=ft.colors.GREY_600),
                                ft.Container(width=8),
                                ft.Text(
                                    f"Enviado em: {submission_date.strftime('%d/%m/%Y às %H:%M')}",
                                    size=18,
                                    color=ft.colors.GREY_600
                                )
                            ]),

                            ft.Container(height=20),
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.icons.VISIBILITY_ROUNDED, color=ft.colors.WHITE, size=24),
                                    ft.Text("Ver Detalhes", color=ft.colors.WHITE, size=18, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER)
                                ], spacing=15, alignment=ft.MainAxisAlignment.CENTER),
                                width=200,
                                height=60,
                                bgcolor=ft.colors.PINK_400,
                                border_radius=30,
                                alignment=ft.alignment.center,
                                shadow=ft.BoxShadow(
                                    spread_radius=0,
                                    blur_radius=15,
                                    color=ft.colors.with_opacity(0.2, ft.colors.PINK_400),
                                    offset=ft.Offset(0, 4)
                                ),
                                on_click=lambda e, r=response: self.show_response_detail(r)
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
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
                    self.responses_container.controls.append(response_card)

        self.page.update()

    def show_response_detail(self, response):
        # Exibe os detalhes da resposta do aluno
        self.controller.current_student_response = response
        self.controller.show_page("DetalheRespostaAluno")

    def edit_task(self, e):
        # Navega para a tela de editar tarefa
        self.controller.show_page("EditarTarefa")

    def confirm_delete_task(self, e):
        # Abre diálogo de confirmação para exclusão da tarefa
        def delete_confirmed(e):
            dialog.open = False
            self.page.update()
            if self.controller.current_task:
                task_id = self.controller.current_task[0]
                if delete_task(task_id):
                    self.controller.show_snackbar("Tarefa excluída com sucesso!", "success")
                    self.controller.current_task = None
                    self.controller.show_page("VerTarefa")
                else:
                    self.controller.show_snackbar("Erro ao excluir tarefa!", "error")

        def cancel_delete(e):
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Exclusão", size=24, weight=ft.FontWeight.W_600, color=ft.colors.GREY_800),
            content=ft.Text("Tem certeza que deseja excluir esta tarefa?\nEsta ação não pode ser desfeita.", size=18),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=cancel_delete,
                    style=ft.ButtonStyle(
                        color=ft.colors.GREY_600
                    )
                ),
                ft.Container(
                    content=ft.Text("Excluir", color=ft.colors.WHITE, size=16, weight=ft.FontWeight.W_600),
                    bgcolor=ft.colors.RED_400,
                    border_radius=15,
                    padding=ft.padding.symmetric(horizontal=25, vertical=12),
                    on_click=delete_confirmed
                )
            ]
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def go_back(self, e):
        # Retorna para a tela de visualizar tarefas
        self.controller.show_page("VerTarefa")