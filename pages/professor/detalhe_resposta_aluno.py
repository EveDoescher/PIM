import flet as ft
from datetime import datetime
from db.database import get_student_response, update_student_response_rating

class DetalheRespostaAluno(ft.Container):
    """Classe responsável pela tela de detalhes da resposta do aluno."""

    def __init__(self, page: ft.Page, controller):
        """Inicializa a tela de detalhes da resposta do aluno."""
        super().__init__()
        self.page = page
        self.controller = controller

        # Título da tela
        self.title = ft.Text(
            "Avaliar Resposta do Aluno",
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

        # File picker e preview
        self.file_picker = ft.FilePicker()
        self.page.overlay.append(self.file_picker)

        self.file_preview_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Visualização do Arquivo", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Container(),
            actions=[
                ft.ElevatedButton(
                    "Fechar",
                    on_click=self.close_file_preview,
                    bgcolor=ft.Colors.TEAL_600,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=20)
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Dialog de confirmação de sucesso para lançamento de nota
        self.success_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Sucesso", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Text("Nota lançada com sucesso!"),
            actions=[
                ft.ElevatedButton(
                    "Ok",
                    bgcolor=ft.Colors.TEAL_600,
                    color=ft.Colors.WHITE,
                    on_click=self.close_success_dialog,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=15)
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Variáveis de estado
        self.selected_rating = None
        self.file_data = None

        # Container para informações do aluno e tarefa
        self.student_info_container = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=20,
            padding=20,
            border=ft.border.all(1, ft.Colors.GREY_200)
        )

        # Container para avaliação
        self.evaluation_container = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=20,
            padding=20,
            border=ft.border.all(1, ft.Colors.GREY_200)
        )

        # Botões de nota (0-10)
        self.rating_buttons = []
        for i in range(11):
            if i <= 6:
                color = ft.Colors.RED_600
            elif i <= 8:
                color = ft.Colors.ORANGE_600
            else:
                color = ft.Colors.GREEN_600

            btn = ft.ElevatedButton(
                text=str(i),
                width=50,
                height=50,
                bgcolor=ft.Colors.WHITE,
                color=color,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=25),
                    elevation=3,
                    side=ft.BorderSide(2, color)
                ),
                on_click=self.on_rating_click
            )
            self.rating_buttons.append(btn)

        # Campo de comentário
        self.comment_field = ft.TextField(
            label="Comentário sobre a resposta",
            multiline=True,
            min_lines=4,
            max_lines=6,
            width=600,
            border_radius=15,
            filled=True,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.TEAL_600,
            label_style=ft.TextStyle(color=ft.Colors.GREY_700),
            text_style=ft.TextStyle(size=16)
        )

        # Botão submeter avaliação
        self.submit_button = ft.ElevatedButton(
            "Lançar Nota",
            width=200,
            height=55,
            bgcolor=ft.Colors.TEAL_600,
            color=ft.Colors.WHITE,
            icon=ft.Icons.GRADE,
            on_click=self.submit_rating,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=27),
                elevation=5,
                text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
            )
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
                self.student_info_container,
                ft.Container(height=25),
                self.evaluation_container
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
            )
        )

        # Carregar dados inicialmente
        self.refresh()

    def refresh(self):
        """Atualiza os dados da tela."""
        if self.controller.current_task and hasattr(self.controller, 'current_student_response'):
            task = self.controller.current_task
            task_id = task[0]
            student_info = self.controller.current_student_response

            if student_info:
                # Estrutura correta: (username, user_id, has_rating, rating, comment, upload_date, filename)
                username = student_info[0]
                user_id = student_info[1]

                # Informações do aluno e tarefa
                student_info_content = ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.PERSON, size=28, color=ft.Colors.TEAL_600),
                        ft.Container(width=15),
                        ft.Text(
                            f"Aluno: {username}",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK
                        )
                    ]),
                    ft.Container(height=15),
                    ft.Row([
                        ft.Icon(ft.Icons.ASSIGNMENT, size=20, color=ft.Colors.GREY_600),
                        ft.Container(width=10),
                        ft.Text(
                            f"Tarefa: {task[1]}",
                            size=16,
                            color=ft.Colors.GREY_700
                        )
                    ])
                ])

                if user_id:
                    response = get_student_response(task_id, user_id)
                    if response:
                        # Estrutura correta: filename, file_data, upload_date, rating, comment
                        filename = response[0]
                        file_data = response[1]
                        upload_date = response[2]
                        rating = response[3]
                        comment = response[4]
                        
                        try:
                            upload_dt = datetime.strptime(upload_date, '%Y-%m-%d %H:%M:%S.%f')
                        except ValueError:
                            try:
                                upload_dt = datetime.strptime(upload_date, '%Y-%m-%d %H:%M:%S')
                            except ValueError:
                                upload_dt = datetime.now()
                        
                        self.file_data = file_data
                        self.selected_rating = rating
                        self.comment_field.value = comment or ""

                        # Adicionar informações do arquivo
                        student_info_content.controls.extend([
                            ft.Container(height=15),
                            ft.Row([
                                ft.Icon(ft.Icons.ATTACH_FILE, size=20, color=ft.Colors.GREY_600),
                                ft.Container(width=10),
                                ft.Text(
                                    f"Arquivo: {filename}",
                                    size=16,
                                    color=ft.Colors.GREY_700
                                )
                            ]),
                            ft.Container(height=10),
                            ft.Row([
                                ft.Icon(ft.Icons.SCHEDULE, size=20, color=ft.Colors.GREY_600),
                                ft.Container(width=10),
                                ft.Text(
                                    f"Enviado em: {upload_dt.strftime('%d/%m/%Y às %H:%M')}",
                                    size=16,
                                    color=ft.Colors.GREY_700
                                )
                            ]),
                            ft.Container(height=20),
                            ft.Row([
                                ft.ElevatedButton(
                                    "Visualizar Arquivo",
                                    width=160,
                                    height=40,
                                    bgcolor=ft.Colors.BLUE_600,
                                    color=ft.Colors.WHITE,
                                    icon=ft.Icons.VISIBILITY,
                                    on_click=self.show_file_preview,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=20),
                                        elevation=3
                                    )
                                ),
                                ft.Container(width=15),
                                ft.ElevatedButton(
                                    "Baixar Arquivo",
                                    width=160,
                                    height=40,
                                    bgcolor=ft.Colors.GREEN_600,
                                    color=ft.Colors.WHITE,
                                    icon=ft.Icons.DOWNLOAD,
                                    on_click=self.download_file,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=20),
                                        elevation=3
                                    )
                                )
                            ])
                        ])
                    else:
                        student_info_content.controls.append(
                            ft.Text(
                                "Nenhuma resposta encontrada.",
                                size=16,
                                color=ft.Colors.RED_600
                            )
                        )

                self.student_info_container.content = student_info_content
                self.student_info_container.width = 700

                # Container de avaliação
                evaluation_content = ft.Column([
                    ft.Text(
                        "Avaliação da Resposta",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.TEAL_600,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=15),
                    ft.Text(
                        "Selecione uma nota de 0 a 10:",
                        size=16,
                        color=ft.Colors.GREY_700,
                        weight=ft.FontWeight.W_500
                    ),
                    ft.Container(height=10),
                    ft.Row(
                        controls=self.rating_buttons,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8
                    ),
                    ft.Container(height=25),
                    self.comment_field,
                    ft.Container(height=25),
                    self.submit_button
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

                self.evaluation_container.content = evaluation_content
                self.evaluation_container.width = 700

                # Atualizar botões de nota
                self.update_rating_buttons()

        self.page.update()

    def update_rating_buttons(self):
        """Atualiza a aparência dos botões de nota."""
        for btn in self.rating_buttons:
            rating_value = int(btn.text)
            if self.selected_rating is not None and rating_value == self.selected_rating:
                # Botão selecionado
                if rating_value <= 6:
                    btn.bgcolor = ft.Colors.RED_600
                elif rating_value <= 8:
                    btn.bgcolor = ft.Colors.ORANGE_600
                else:
                    btn.bgcolor = ft.Colors.GREEN_600
                btn.color = ft.Colors.WHITE
            else:
                # Botão não selecionado
                btn.bgcolor = ft.Colors.WHITE
                if rating_value <= 6:
                    btn.color = ft.Colors.RED_600
                elif rating_value <= 8:
                    btn.color = ft.Colors.ORANGE_600
                else:
                    btn.color = ft.Colors.GREEN_600

    def on_rating_click(self, e):
        """Manipula o clique em um botão de nota."""
        clicked_button = e.control
        self.selected_rating = int(clicked_button.text)
        self.update_rating_buttons()
        self.page.update()

    def show_file_preview(self, e):
        """Exibe a pré-visualização do arquivo."""
        if not self.file_data:
            self.show_snackbar("Nenhum arquivo para visualizar.", ft.Colors.RED_400)
            return

        import base64

        # Obter informações do arquivo
        task = self.controller.current_task
        student_info = self.controller.current_student_response
        user_id = student_info[1]
        response = get_student_response(task[0], user_id)
        
        if response:
            filename = response[0]
            file_ext = filename.split('.')[-1].lower()
            content = None

            if file_ext in ['png', 'jpg', 'jpeg']:
                content = ft.Image(
                    src_base64=base64.b64encode(self.file_data).decode('utf-8'),
                    width=600,
                    height=800,
                    fit=ft.ImageFit.CONTAIN
                )
            elif file_ext == 'pdf':
                content = ft.Column([
                    ft.Icon(ft.Icons.PICTURE_AS_PDF, size=64, color=ft.Colors.RED_600),
                    ft.Container(height=20),
                    ft.Text(
                        "Pré-visualização não disponível para PDFs.",
                        size=16,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=15),
                    ft.Text(
                        "Por favor, baixe o arquivo para visualizar.",
                        size=14,
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            else:
                content = ft.Column([
                    ft.Icon(ft.Icons.INSERT_DRIVE_FILE, size=64, color=ft.Colors.GREY_600),
                    ft.Container(height=20),
                    ft.Text(
                        "Visualização não suportada para este tipo de arquivo.",
                        size=16,
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

            self.file_preview_dialog.content = ft.Container(
                content=content,
                width=620,
                height=820,
                alignment=ft.alignment.center
            )
            self.page.open(self.file_preview_dialog)

    def close_file_preview(self, e):
        """Fecha o diálogo de pré-visualização."""
        self.file_preview_dialog.open = False
        self.page.update()

    def download_file(self, e):
        """Baixa o arquivo da resposta."""
        if self.file_data:
            # Obter nome do arquivo
            task = self.controller.current_task
            student_info = self.controller.current_student_response
            user_id = student_info[1]
            response = get_student_response(task[0], user_id)
            
            if response:
                filename = response[0]
                
                def on_save_result(e):
                    if e.path:
                        try:
                            with open(e.path, "wb") as f:
                                f.write(self.file_data)
                            self.show_snackbar(f"Arquivo salvo em: {e.path}", ft.Colors.GREEN_600)
                        except Exception as ex:
                            self.show_snackbar(f"Erro ao salvar arquivo: {ex}", ft.Colors.RED_400)
                    else:
                        self.show_snackbar("Download cancelado.", ft.Colors.ORANGE_600)

                self.file_picker.save_file(file_name=filename)
                self.file_picker.on_result = on_save_result
        else:
            self.show_snackbar("Nenhum arquivo para baixar.", ft.Colors.RED_400)

    def submit_rating(self, e):
        """Submete a avaliação da resposta."""
        if self.selected_rating is None:
            self.show_snackbar("Selecione uma nota antes de lançar.", ft.Colors.RED_400)
            return

        task = self.controller.current_task
        task_id = task[0]
        student_info = self.controller.current_student_response
        user_id = student_info[1]
        comment = self.comment_field.value or ""

        success = update_student_response_rating(task_id, user_id, self.selected_rating, comment)
        if success:
            # Mostrar dialog de sucesso
            self.page.open(self.success_dialog)
        else:
            self.show_snackbar("Erro ao lançar nota.", ft.Colors.RED_400)

    def close_success_dialog(self, e):
        """Fecha o dialog de sucesso e volta para detalhes da tarefa."""
        self.success_dialog.open = False
        self.page.update()
        self.controller.show_page("DetalheTarefa")

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
        """Volta para a tela de detalhes da tarefa."""
        self.controller.show_page("DetalheTarefa")