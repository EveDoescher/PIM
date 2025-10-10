import flet as ft
from db.database import get_students_who_responded, delete_task
from datetime import datetime

class DetalheTarefa(ft.Container):
    """Classe responsável pela tela de detalhes da tarefa do professor."""

    def __init__(self, page: ft.Page, controller):
        """Inicializa a tela de detalhes da tarefa."""
        super().__init__()
        self.page = page
        self.controller = controller

        # Título da tela
        self.title = ft.Text(
            "Detalhes da Tarefa",
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

        # Container para detalhes da tarefa
        self.task_details_container = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=20,
            padding=30,
            border=ft.border.all(1, ft.Colors.GREY_200)
        )

        # Container para respostas dos alunos
        self.responses_container = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=15
        )

        # Botões de ação
        self.edit_button = ft.ElevatedButton(
            "Editar Tarefa",
            width=150,
            height=45,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            icon=ft.Icons.EDIT,
            on_click=self.edit_task,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=22),
                elevation=3
            )
        )

        self.delete_button = ft.ElevatedButton(
            "Excluir Tarefa",
            width=150,
            height=45,
            bgcolor=ft.Colors.RED_600,
            color=ft.Colors.WHITE,
            icon=ft.Icons.DELETE,
            on_click=self.confirm_delete_task,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=22),
                elevation=3
            )
        )

        # Dialog de confirmação de exclusão
        self.delete_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Exclusão", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Text("Tem certeza que deseja excluir esta tarefa? Esta ação não pode ser desfeita."),
            actions=[
                ft.TextButton("Cancelar", on_click=self.close_delete_dialog),
                ft.ElevatedButton(
                    "Excluir",
                    bgcolor=ft.Colors.RED_600,
                    color=ft.Colors.WHITE,
                    on_click=self.delete_task,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=15)
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
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
                ft.Container(height=30),
                self.task_details_container,
                ft.Container(height=20),
                ft.Row([
                    self.edit_button,
                    ft.Container(width=20),
                    self.delete_button
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=30),
                ft.Text(
                    "Respostas dos Alunos",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.TEAL_600,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=20),
                ft.Container(
                    content=self.responses_container,
                    width=900,
                    height=400,
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

        # Carregar detalhes inicialmente
        self.refresh()

    def refresh(self):
        """Atualiza os detalhes da tarefa e respostas dos alunos."""
        if self.controller.current_task:
            task = self.controller.current_task
            
            # Detalhes da tarefa
            creation_date = datetime.strptime(task[3], '%Y-%m-%d %H:%M:%S.%f')
            exp_date = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S')
            is_expired = datetime.now() > exp_date

            status = "Expirada" if is_expired else "Ativa"
            status_color = ft.Colors.RED_600 if is_expired else ft.Colors.GREEN_600
            status_icon = ft.Icons.SCHEDULE_OUTLINED if is_expired else ft.Icons.CHECK_CIRCLE_OUTLINE

            task_info = ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.ASSIGNMENT, size=32, color=ft.Colors.TEAL_600),
                    ft.Container(width=15),
                    ft.Text(
                        task[1],
                        size=28,
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
                        padding=ft.padding.symmetric(horizontal=15, vertical=8),
                        border_radius=20
                    )
                ]),
                ft.Container(height=20),
                
                ft.Container(
                    content=ft.Text(
                        task[2] if task[2] else "Sem descrição disponível",
                        size=16,
                        color=ft.Colors.GREY_800
                    ),
                    bgcolor=ft.Colors.GREY_50,
                    padding=20,
                    border_radius=15,
                    border=ft.border.all(1, ft.Colors.GREY_200)
                ),
                
                ft.Container(height=20),
                ft.Row([
                    ft.Icon(ft.Icons.CALENDAR_TODAY, size=20, color=ft.Colors.GREY_600),
                    ft.Container(width=10),
                    ft.Text(
                        f"Criada em: {creation_date.strftime('%d/%m/%Y às %H:%M')}",
                        size=14,
                        color=ft.Colors.GREY_700
                    )
                ]),
                ft.Container(height=10),
                ft.Row([
                    ft.Icon(status_icon, size=20, color=status_color),
                    ft.Container(width=10),
                    ft.Text(
                        f"Vence em: {exp_date.strftime('%d/%m/%Y às %H:%M')}",
                        size=14,
                        color=status_color,
                        weight=ft.FontWeight.W_500
                    )
                ])
            ])

            self.task_details_container.content = task_info
            self.task_details_container.width = 850

            # Carregar respostas dos alunos
            self.load_student_responses()
        else:
            self.task_details_container.content = ft.Text(
                "Nenhuma tarefa selecionada",
                size=18,
                color=ft.Colors.GREY_600
            )

        self.page.update()

    def load_student_responses(self):
        """Carrega as respostas dos alunos para a tarefa atual."""
        self.responses_container.controls.clear()

        if self.controller.current_task:
            task_id = self.controller.current_task[0]
            responses = get_students_who_responded(task_id)

            if not responses:
                self.responses_container.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.ASSIGNMENT_OUTLINED, size=64, color=ft.Colors.GREY_400),
                            ft.Container(height=20),
                            ft.Text(
                                "Nenhuma resposta encontrada.",
                                size=18,
                                color=ft.Colors.GREY_600,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Container(height=10),
                            ft.Text(
                                "Os alunos ainda não enviaram suas respostas.",
                                size=14,
                                color=ft.Colors.GREY_500,
                                text_align=ft.TextAlign.CENTER
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        alignment=ft.alignment.center,
                        height=250
                    )
                )
            else:
                for response in responses:
                    # Estrutura correta: (username, user_id, has_rating, rating, comment, upload_date, filename)
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

                    # Determinar se foi corrigido
                    is_graded = rating is not None

                    response_card = ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.PERSON, size=24, color=ft.Colors.TEAL_600),
                                    ft.Container(width=10),
                                    ft.Text(
                                        student_name,
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.BLACK,
                                        expand=True
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            "Corrigido" if is_graded else "Pendente",
                                            size=12,
                                            color=ft.Colors.WHITE,
                                            weight=ft.FontWeight.BOLD
                                        ),
                                        bgcolor=ft.Colors.BLUE_600 if is_graded else ft.Colors.ORANGE_600,
                                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                        border_radius=15
                                    )
                                ]),
                                ft.Container(height=15),
                                
                                ft.Row([
                                    ft.Icon(ft.Icons.ATTACH_FILE, size=16, color=ft.Colors.GREY_600),
                                    ft.Container(width=5),
                                    ft.Text(f"Arquivo: {filename}", size=14, color=ft.Colors.GREY_700),
                                    ft.Container(width=20),
                                    ft.Icon(ft.Icons.SCHEDULE, size=16, color=ft.Colors.GREY_600),
                                    ft.Container(width=5),
                                    ft.Text(
                                        f"Enviado: {submission_date.strftime('%d/%m/%Y às %H:%M')}",
                                        size=14,
                                        color=ft.Colors.GREY_700
                                    )
                                ]),
                                
                                ft.Container(height=15),
                                ft.ElevatedButton(
                                    "Ver Detalhes",
                                    width=150,
                                    height=35,
                                    bgcolor=ft.Colors.TEAL_600,
                                    color=ft.Colors.WHITE,
                                    icon=ft.Icons.VISIBILITY,
                                    on_click=lambda e, r=response: self.show_response_detail(r),
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=17),
                                        elevation=2
                                    )
                                )
                            ]),
                            width=850,
                            padding=20,
                            border_radius=15
                        ),
                        elevation=4
                    )
                    self.responses_container.controls.append(response_card)

        self.page.update()

    def show_response_detail(self, response):
        """Exibe os detalhes da resposta do aluno."""
        self.controller.current_student_response = response
        self.controller.show_page("DetalheRespostaAluno")

    def edit_task(self, e):
        """Edita a tarefa atual."""
        self.controller.show_page("EditarTarefa")

    def confirm_delete_task(self, e):
        """Abre o diálogo de confirmação de exclusão."""
        self.page.open(self.delete_dialog)

    def close_delete_dialog(self, e):
        """Fecha o diálogo de confirmação de exclusão."""
        self.delete_dialog.open = False
        self.page.update()

    def delete_task(self, e):
        """Exclui a tarefa atual."""
        if self.controller.current_task:
            task_id = self.controller.current_task[0]
            if delete_task(task_id):
                self.show_snackbar("Tarefa excluída com sucesso!", ft.Colors.GREEN_600)
                self.delete_dialog.open = False
                self.controller.current_task = None
                self.controller.show_page("VerTarefa")
            else:
                self.show_snackbar("Erro ao excluir tarefa!", ft.Colors.RED_400)
                self.delete_dialog.open = False
        self.page.update()

    def show_snackbar(self, message, color):
        """Exibe uma mensagem de feedback ao usuário."""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.CHECK_CIRCLE if color == ft.Colors.GREEN_600 else ft.Icons.ERROR,
                    color=ft.Colors.WHITE
                ),
                ft.Text(message, color=ft.Colors.WHITE, size=16)
            ]),
            bgcolor=color,
            behavior=ft.SnackBarBehavior.FLOATING,
            margin=ft.margin.all(10),
            padding=ft.padding.all(15),
            shape=ft.RoundedRectangleBorder(radius=10)
        )
        self.page.snack_bar.open = True
        self.page.update()

    def go_back(self, e):
        """Volta para a tela de ver tarefas."""
        self.controller.show_page("VerTarefa")