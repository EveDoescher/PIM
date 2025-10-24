import flet as ft
from datetime import datetime
from backend.database import get_student_response, update_student_response_rating

class DetalheRespostaAluno(ft.Container):

    def __init__(self, page: ft.Page, controller):
        # Inicializa a tela de detalhes da resposta do aluno
        super().__init__(
            expand=True,
            width=None,
            height=None,
            padding=ft.padding.all(0),
            margin=ft.margin.all(0)
        )
        self.page = page
        self.controller = controller

        self.file_picker = ft.FilePicker()
        self.page.overlay.append(self.file_picker)

        self.file_preview_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Visualização do Arquivo", size=24, weight=ft.FontWeight.W_600, color=ft.colors.GREY_800),
            content=ft.Container(),
            actions=[
                ft.Container(
                    content=ft.Text("Fechar", color=ft.colors.WHITE, size=16, weight=ft.FontWeight.W_600),
                    bgcolor=ft.colors.PURPLE_400,
                    border_radius=15,
                    padding=ft.padding.symmetric(horizontal=25, vertical=12),
                    on_click=self.close_file_preview
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.selected_rating = None
        self.file_data = None

        self.create_components()
        self.setup_layout()

    def create_components(self):
        # Cria todos os componentes da interface
        
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

        self.student_info_container = ft.Container(
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

        self.evaluation_container = ft.Container(
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

        self.rating_buttons = []
        for i in range(11):
            if i <= 6:
                color = ft.colors.RED_400
            elif i <= 8:
                color = ft.colors.ORANGE_400
            else:
                color = ft.colors.GREEN_400

            btn = ft.Container(
                content=ft.Text(str(i), size=20, weight=ft.FontWeight.W_600, color=color),
                width=65,
                height=65,
                bgcolor=ft.colors.WHITE,
                border_radius=32,
                alignment=ft.alignment.center,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=10,
                    color=ft.colors.with_opacity(0.1, color),
                    offset=ft.Offset(0, 3)
                ),
                border=ft.border.all(3, color),
                on_click=self.on_rating_click
            )
            self.rating_buttons.append(btn)

        self.comment_field = ft.TextField(
            label="Comentário sobre a resposta",
            multiline=True,
            min_lines=5,
            max_lines=7,
            width=700,
            height=150,
            border_radius=20,
            filled=True,
            bgcolor=ft.colors.WHITE,
            border_color=ft.colors.PINK_400,
            focused_border_color=ft.colors.PINK_400,
            focused_bgcolor=ft.colors.WHITE,
            label_style=ft.TextStyle(
                color=ft.colors.GREY_600,
                size=20,
                weight=ft.FontWeight.W_500
            ),
            text_style=ft.TextStyle(
                size=20,
                weight=ft.FontWeight.W_400,
                color=ft.colors.GREY_800
            ),
            cursor_color=ft.colors.PINK_400,
            selection_color=ft.colors.PINK_100,
            content_padding=ft.padding.symmetric(horizontal=25, vertical=25)
        )

        self.submit_button = ft.Container(
            content=ft.Row([
                ft.Icon(ft.icons.GRADE_ROUNDED, color=ft.colors.WHITE, size=24),
                ft.Text(
                    "Lançar Nota",
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color=ft.colors.WHITE
                )
            ], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
            width=700,
            height=70,
            bgcolor=ft.colors.PINK_500,
            border_radius=20,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=18,
                color=ft.colors.with_opacity(0.25, ft.colors.PINK_500),
                offset=ft.Offset(0, 6)
            ),
            on_click=self.submit_rating
        )

    def setup_layout(self):
        # Configura o layout da página
        
        header = ft.Container(
            content=ft.Row([
                self.back_button,
                ft.Container(expand=True),
                ft.Column([
                    ft.Text(
                        "Avaliar Resposta do Aluno",
                        size=42,
                        weight=ft.FontWeight.W_600,
                        color=ft.colors.GREY_800,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Visualize a resposta e atribua uma nota",
                        size=20,
                        color=ft.colors.GREY_500,
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(expand=True)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=60, vertical=45)
        )

        self.content = ft.Container(
            expand=True,
            width=None,
            height=None,
            padding=ft.padding.all(0),
            margin=ft.margin.all(0),
           
            content=ft.Column([
                header,
                ft.Container(
                    content=self.student_info_container,
                    padding=ft.padding.symmetric(horizontal=60, vertical=25),
                    alignment=ft.alignment.center
                ),
                ft.Container(
                    content=self.evaluation_container,
                    padding=ft.padding.symmetric(horizontal=60, vertical=25),
                    alignment=ft.alignment.center
                ),
                ft.Container(expand=True)
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO
            )
        )

        self.refresh()

    def refresh(self):
        # Atualiza os dados da tela
        if self.controller.current_task and hasattr(self.controller, 'current_student_response'):
            task = self.controller.current_task
            task_id = task[0]
            student_info = self.controller.current_student_response

            if student_info:
                username = student_info[0]
                user_id = student_info[1]

                student_info_content = ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(ft.icons.PERSON_ROUNDED, size=45, color=ft.colors.PURPLE_400),
                            width=90,
                            height=90,
                            border_radius=45,
                            bgcolor=ft.colors.with_opacity(0.1, ft.colors.PURPLE_400),
                            alignment=ft.alignment.center
                        ),
                        ft.Container(width=25),
                        ft.Column([
                            ft.Text(
                                f"Aluno: {username}",
                                size=32,
                                weight=ft.FontWeight.W_600,
                                color=ft.colors.GREY_800
                            ),
                            ft.Text(
                                f"Tarefa: {task[1]}",
                                size=20,
                                color=ft.colors.GREY_600,
                                weight=ft.FontWeight.W_500
                            )
                        ], expand=True, spacing=8)
                    ])
                ])

                if user_id:
                    response = get_student_response(task_id, user_id)
                    if response:
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

                        student_info_content.controls.extend([
                            ft.Container(height=25),
                            ft.Row([
                                ft.Icon(ft.icons.ATTACH_FILE_ROUNDED, size=24, color=ft.colors.GREY_600),
                                ft.Container(width=12),
                                ft.Text(
                                    f"Arquivo: {filename}",
                                    size=20,
                                    color=ft.colors.GREY_700,
                                    weight=ft.FontWeight.W_500
                                )
                            ]),
                            ft.Container(height=15),
                            ft.Row([
                                ft.Icon(ft.icons.SCHEDULE_ROUNDED, size=24, color=ft.colors.GREY_600),
                                ft.Container(width=12),
                                ft.Text(
                                    f"Enviado em: {upload_dt.strftime('%d/%m/%Y às %H:%M')}",
                                    size=20,
                                    color=ft.colors.GREY_700,
                                    weight=ft.FontWeight.W_500
                                )
                            ]),
                            ft.Container(height=25),
                            ft.Row([
                                ft.Container(
                                    content=ft.Row([
                                        ft.Icon(ft.icons.VISIBILITY_ROUNDED, color=ft.colors.WHITE, size=22),
                                        ft.Text("Visualizar Arquivo", color=ft.colors.WHITE, size=20, weight=ft.FontWeight.W_600)
                                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                                    width=220,
                                    height=55,
                                    bgcolor=ft.colors.BLUE_400,
                                    border_radius=27,
                                    alignment=ft.alignment.center,
                                    shadow=ft.BoxShadow(
                                        spread_radius=0,
                                        blur_radius=10,
                                        color=ft.colors.with_opacity(0.2, ft.colors.BLUE_400),
                                        offset=ft.Offset(0, 3)
                                    ),
                                    on_click=self.show_file_preview
                                ),
                                ft.Container(width=20),
                                ft.Container(
                                    content=ft.Row([
                                        ft.Icon(ft.icons.DOWNLOAD_ROUNDED, color=ft.colors.WHITE, size=22),
                                        ft.Text("Baixar Arquivo", color=ft.colors.WHITE, size=20, weight=ft.FontWeight.W_600)
                                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                                    width=200,
                                    height=55,
                                    bgcolor=ft.colors.GREEN_400,
                                    border_radius=27,
                                    alignment=ft.alignment.center,
                                    shadow=ft.BoxShadow(
                                        spread_radius=0,
                                        blur_radius=10,
                                        color=ft.colors.with_opacity(0.2, ft.colors.GREEN_400),
                                        offset=ft.Offset(0, 3)
                                    ),
                                    on_click=self.download_file
                                )
                            ], alignment=ft.MainAxisAlignment.CENTER)
                        ])
                    else:
                        student_info_content.controls.append(
                            ft.Text(
                                "Nenhuma resposta encontrada.",
                                size=20,
                                color=ft.colors.RED_400
                            )
                        )

                self.student_info_container.content = student_info_content
                self.student_info_container.width = 1200

                evaluation_content = ft.Column([
                    ft.Text(
                        "Avaliação da Resposta",
                        size=32,
                        weight=ft.FontWeight.W_600,
                        color=ft.colors.PURPLE_400,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=20),
                    ft.Text(
                        "Selecione uma nota de 0 a 10:",
                        size=20,
                        color=ft.colors.GREY_700,
                        weight=ft.FontWeight.W_500
                    ),
                    ft.Container(height=20),
                    ft.Row(
                        controls=self.rating_buttons,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=15,
                        wrap=True
                    ),
                    ft.Container(height=35),
                    self.comment_field,
                    ft.Container(height=35),
                    self.submit_button
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

                self.evaluation_container.content = evaluation_content
                self.evaluation_container.width = 1200

                self.update_rating_buttons()

        self.page.update()

    def update_rating_buttons(self):
        # Atualiza a aparência dos botões de nota
        for i, btn in enumerate(self.rating_buttons):
            rating_value = i
            if self.selected_rating is not None and rating_value == self.selected_rating:
                if rating_value <= 6:
                    btn.bgcolor = ft.colors.RED_400
                elif rating_value <= 8:
                    btn.bgcolor = ft.colors.ORANGE_400
                else:
                    btn.bgcolor = ft.colors.GREEN_400
                btn.content.color = ft.colors.WHITE
            else:
                btn.bgcolor = ft.colors.WHITE
                if rating_value <= 6:
                    btn.content.color = ft.colors.RED_400
                elif rating_value <= 8:
                    btn.content.color = ft.colors.ORANGE_400
                else:
                    btn.content.color = ft.colors.GREEN_400

    def on_rating_click(self, e):
        # Processa clique em botão de nota
        clicked_button = e.control
        self.selected_rating = int(clicked_button.content.value)
        self.update_rating_buttons()
        self.page.update()

    def show_file_preview(self, e):
        # Exibe pré-visualização do arquivo
        if not self.file_data:
            self.controller.show_snackbar("Nenhum arquivo para visualizar.", "error")
            return

        import base64

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
                    height=700,
                    fit=ft.ImageFit.CONTAIN
                )
            elif file_ext == 'pdf':
                content = ft.Column([
                    ft.Icon(ft.icons.PICTURE_AS_PDF, size=80, color=ft.colors.RED_400),
                    ft.Container(height=25),
                    ft.Text(
                        "Pré-visualização não disponível para PDFs.",
                        size=22,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=15),
                    ft.Text(
                        "Por favor, baixe o arquivo para visualizar.",
                        size=18,
                        color=ft.colors.GREY_600,
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            else:
                content = ft.Column([
                    ft.Icon(ft.icons.INSERT_DRIVE_FILE, size=80, color=ft.colors.GREY_600),
                    ft.Container(height=25),
                    ft.Text(
                        "Visualização não suportada para este tipo de arquivo.",
                        size=22,
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

            self.file_preview_dialog.content = ft.Container(
                content=content,
                width=650,
                height=750,
                alignment=ft.alignment.center
            )
            self.page.dialog = self.file_preview_dialog
            self.file_preview_dialog.open = True
            self.page.update()

    def close_file_preview(self, e):
        # Fecha o diálogo de pré-visualização
        self.file_preview_dialog.open = False
        self.page.update()

    def download_file(self, e):
        # Processa download do arquivo
        if self.file_data:
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
                            self.controller.show_snackbar(f"Arquivo salvo em: {e.path}", "success")
                        except Exception as ex:
                            self.controller.show_snackbar(f"Erro ao salvar arquivo: {ex}", "error")
                    else:
                        self.controller.show_snackbar("Download cancelado.", "error")

                self.file_picker.save_file(file_name=filename)
                self.file_picker.on_result = on_save_result
        else:
            self.controller.show_snackbar("Nenhum arquivo para baixar.", "error")

    def submit_rating(self, e):
        # Submete a avaliação da resposta
        if self.selected_rating is None:
            self.controller.show_snackbar("Selecione uma nota antes de lançar.", "error")
            return

        task = self.controller.current_task
        task_id = task[0]
        student_info = self.controller.current_student_response
        user_id = student_info[1]
        comment = self.comment_field.value or ""

        success = update_student_response_rating(task_id, user_id, self.selected_rating, comment)
        if success:
            self.controller.show_snackbar("Nota lançada com sucesso!", "success")
            self.controller.show_page("DetalheTarefa")
        else:
            self.controller.show_snackbar("Erro ao lançar nota.", "error")

    def go_back(self, e):
        # Retorna para a tela de detalhes da tarefa
        self.controller.show_page("DetalheTarefa")