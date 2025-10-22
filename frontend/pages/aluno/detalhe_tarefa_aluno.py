import flet as ft
from datetime import datetime
from backend.database import insert_student_response, get_user_id, get_student_response
import os

class DetalheTarefaAluno(ft.Container):
    """Classe responsável pela tela de detalhes da tarefa do aluno com design clean."""

    def __init__(self, page: ft.Page, controller):
        """Inicializa a tela de detalhes da tarefa do aluno."""
        super().__init__(
            expand=True,
            width=None,
            height=None,
            padding=ft.padding.all(0),
            margin=ft.margin.all(0)
        )
        self.page = page
        self.controller = controller

        # File picker
        self.file_picker = ft.FilePicker(on_result=self.on_file_selected)
        self.page.overlay.append(self.file_picker)

        # File preview dialog
        self.file_preview_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Visualização do Arquivo", size=24, weight=ft.FontWeight.W_600, color=ft.colors.GREY_800),
            content=ft.Container(),
            actions=[
                ft.Container(
                    content=ft.Text("Fechar", color=ft.colors.WHITE, size=16, weight=ft.FontWeight.W_600),
                    bgcolor=ft.colors.PINK_400,
                    border_radius=15,
                    padding=ft.padding.symmetric(horizontal=25, vertical=12),
                    on_click=self.close_file_preview
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Variáveis para arquivo selecionado
        self.selected_file_path = None
        self.selected_file_name = None

        self.create_components()
        self.setup_layout()

    def create_components(self):
        """Cria todos os componentes da interface"""
        
        # Botão voltar clean - MAIOR
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

        # Container para detalhes da tarefa - MAIOR
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

        # Container para controles de upload - MAIOR
        self.upload_container = ft.Container(
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

    def setup_layout(self):
        """Configura o layout da página"""
        
        # Header clean - MAIOR
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
                        "Visualize informações e envie sua resposta",
                        size=20,
                        color=ft.colors.GREY_500,
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(expand=True)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=60, vertical=45)
        )

        # Seção de detalhes da tarefa - MAIOR
        task_section = ft.Container(
            content=ft.Column([
                self.task_details_container
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=60, vertical=25)
        )

        # Seção de upload - MAIOR
        upload_section = ft.Container(
            content=ft.Column([
                self.upload_container
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=60, vertical=25)
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
                task_section,
                upload_section,
                ft.Container(expand=True)
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        # Carregar detalhes inicialmente
        self.refresh()

    def refresh(self):
        """Atualiza os detalhes da tarefa e controles de upload."""
        if self.controller.current_task:
            task = self.controller.current_task
            
            # Detalhes da tarefa - MAIORES
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
                    ft.Icon(ft.icons.PERSON_ROUNDED, size=24, color=ft.colors.GREY_600),
                    ft.Container(width=12),
                    ft.Text(
                        f"Professor: {task[5]}",
                        size=18,
                        color=ft.colors.GREY_600,
                        weight=ft.FontWeight.W_500
                    )
                ]),
                ft.Container(height=15),
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

            # Verificar se o aluno já enviou resposta
            task_id = task[0]
            user_ra = self.controller.current_user['ra']
            user_id = get_user_id(user_ra)
            response = get_student_response(task_id, user_id) if user_id else None

            if response:
                # Tarefa já entregue
                filename, file_data, *_ = response
                self.file_data = file_data
                
                upload_content = ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(ft.icons.CHECK_CIRCLE_ROUNDED, size=45, color=ft.colors.GREEN_400),
                            width=90,
                            height=90,
                            border_radius=45,
                            bgcolor=ft.colors.with_opacity(0.1, ft.colors.GREEN_400),
                            alignment=ft.alignment.center
                        ),
                        ft.Container(width=25),
                        ft.Column([
                            ft.Text(
                                "Tarefa Entregue",
                                size=32,
                                weight=ft.FontWeight.W_600,
                                color=ft.colors.GREEN_400
                            ),
                            ft.Text(
                                f"Arquivo: {filename}",
                                size=18,
                                color=ft.colors.GREY_600,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                max_lines=1
                            )
                        ], spacing=8)
                    ]),
                    ft.Container(height=35),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.icons.VISIBILITY_ROUNDED, color=ft.colors.WHITE, size=24),
                            ft.Text("Visualizar Arquivo Enviado", color=ft.colors.WHITE, size=18, weight=ft.FontWeight.W_600)
                        ], spacing=15, alignment=ft.MainAxisAlignment.CENTER),
                        width=300,
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
                        on_click=self.show_file_preview
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                
            elif datetime.now() <= exp_date:
                # Tarefa ativa - mostrar controles de upload
                self.selected_file_label = ft.Text(
                    "Nenhum arquivo selecionado",
                    size=18,
                    color=ft.colors.GREY_600
                )
                
                upload_content = ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(ft.icons.UPLOAD_FILE_ROUNDED, size=45, color=ft.colors.PURPLE_400),
                            width=90,
                            height=90,
                            border_radius=45,
                            bgcolor=ft.colors.with_opacity(0.1, ft.colors.PURPLE_400),
                            alignment=ft.alignment.center
                        ),
                        ft.Container(width=25),
                        ft.Column([
                            ft.Text(
                                "Enviar Resposta",
                                size=32,
                                weight=ft.FontWeight.W_600,
                                color=ft.colors.PURPLE_400
                            ),
                            ft.Text(
                                "Formatos aceitos: PNG, JPG, JPEG, PDF (máx. 10MB)",
                                size=16,
                                color=ft.colors.GREY_500
                            )
                        ], spacing=8)
                    ]),
                    ft.Container(height=25),
                    self.selected_file_label,
                    ft.Container(height=35),
                    ft.Row([
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.icons.FOLDER_OPEN_ROUNDED, color=ft.colors.WHITE, size=24),
                                ft.Text("Selecionar Arquivo", color=ft.colors.WHITE, size=18, weight=ft.FontWeight.W_600)
                            ], spacing=15, alignment=ft.MainAxisAlignment.CENTER),
                            width=200,
                            height=60,
                            bgcolor=ft.colors.GREY_600,
                            border_radius=30,
                            alignment=ft.alignment.center,
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=15,
                                color=ft.colors.with_opacity(0.2, ft.colors.GREY_600),
                                offset=ft.Offset(0, 4)
                            ),
                            on_click=self.select_file
                        ),
                        ft.Container(width=25),
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.icons.SEND_ROUNDED, color=ft.colors.WHITE, size=24),
                                ft.Text("Enviar Resposta", color=ft.colors.WHITE, size=18, weight=ft.FontWeight.W_600)
                            ], spacing=15, alignment=ft.MainAxisAlignment.CENTER),
                            width=200,
                            height=60,
                            bgcolor=ft.colors.PURPLE_400,
                            border_radius=30,
                            alignment=ft.alignment.center,
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=15,
                                color=ft.colors.with_opacity(0.2, ft.colors.PURPLE_400),
                                offset=ft.Offset(0, 4)
                            ),
                            on_click=self.send_response
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                
            else:
                # Tarefa expirada
                upload_content = ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(ft.icons.SCHEDULE_SEND_ROUNDED, size=45, color=ft.colors.RED_400),
                            width=90,
                            height=90,
                            border_radius=45,
                            bgcolor=ft.colors.with_opacity(0.1, ft.colors.RED_400),
                            alignment=ft.alignment.center
                        ),
                        ft.Container(width=25),
                        ft.Column([
                            ft.Text(
                                "Tarefa Expirada",
                                size=32,
                                weight=ft.FontWeight.W_600,
                                color=ft.colors.RED_400
                            ),
                            ft.Text(
                                "O prazo para entrega desta tarefa já passou",
                                size=18,
                                color=ft.colors.GREY_600
                            )
                        ], spacing=8)
                    ])
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

            self.upload_container.content = upload_content
            self.upload_container.width = 1000

        else:
            # Caso não haja tarefa selecionada
            self.task_details_container.content = ft.Text(
                "Nenhuma tarefa selecionada",
                size=24,
                color=ft.colors.GREY_600
            )
            self.upload_container.content = ft.Container()

        # Resetar arquivo selecionado
        self.selected_file_path = None
        self.selected_file_name = None

        self.page.update()

    def select_file(self, e):
        """Abre o seletor de arquivos para escolher um arquivo para upload."""
        self.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["png", "jpg", "jpeg", "pdf"]
        )

    def on_file_selected(self, e: ft.FilePickerResultEvent):
        """Manipula o resultado da seleção de arquivo."""
        if e.files:
            file = e.files[0]
            self.selected_file_path = file.path
            self.selected_file_name = file.name
            self.selected_file_label.value = f"Arquivo selecionado: {self.selected_file_name}"
            self.selected_file_label.color = ft.colors.GREEN_600
        else:
            self.selected_file_path = None
            self.selected_file_name = None
            self.selected_file_label.value = "Nenhum arquivo selecionado"
            self.selected_file_label.color = ft.colors.GREY_600
        self.page.update()

    def send_response(self, e):
        """Envia a resposta do aluno para a tarefa."""
        if not self.controller.current_task:
            self.controller.show_snackbar("Nenhuma tarefa selecionada!", "error")
            return
            
        if not self.selected_file_path:
            self.controller.show_snackbar("Nenhum arquivo selecionado!", "error")
            return

        task_id = self.controller.current_task[0]
        user_ra = self.controller.current_user['ra']
        user_id = get_user_id(user_ra)
        if not user_id:
            self.controller.show_snackbar("Usuário não encontrado!", "error")
            return

        filename = self.selected_file_name

        # Verificar tamanho do arquivo (limite de 10MB)
        file_size = os.path.getsize(self.selected_file_path)
        max_size = 10 * 1024 * 1024  # 10MB
        if file_size > max_size:
            self.controller.show_snackbar("Arquivo muito grande. Limite de 10MB.", "error")
            return

        try:
            with open(self.selected_file_path, 'rb') as f:
                file_data = f.read()
        except FileNotFoundError:
            self.controller.show_snackbar("Arquivo não encontrado.", "error")
            return
        except PermissionError:
            self.controller.show_snackbar("Permissão negada para acessar o arquivo.", "error")
            return
        except OSError as ex:
            self.controller.show_snackbar(f"Erro ao ler o arquivo: {ex}", "error")
            return

        if insert_student_response(task_id, user_id, filename, file_data):
            self.controller.show_snackbar("Resposta enviada com sucesso!", "success")
            self.selected_file_path = None
            self.selected_file_name = None
            self.refresh()  # Recarregar para mostrar status entregue
        else:
            self.controller.show_snackbar("Falha ao enviar resposta.", "error")

    def show_file_preview(self, e):
        if not hasattr(self, 'file_data') or not self.file_data:
            self.controller.show_snackbar("Nenhum arquivo para visualizar.", "error")
            return

        import base64

        filename = self.controller.current_task[1] if self.controller.current_task else "arquivo"
        user_ra = self.controller.current_user['ra']
        user_id = get_user_id(user_ra)
        response = get_student_response(self.controller.current_task[0], user_id)
        
        if response:
            filename = response[0]
            file_ext = filename.split('.')[-1].lower()
            content = None

            if file_ext in ['png', 'jpg', 'jpeg']:
                # Mostrar imagem
                content = ft.Image(
                    src_base64=base64.b64encode(self.file_data).decode('utf-8'),
                    width=600,
                    height=800,
                    fit=ft.ImageFit.CONTAIN
                )
            elif file_ext == 'pdf':
                # Mostrar mensagem para PDF
                content = ft.Column([
                    ft.Icon(ft.icons.PICTURE_AS_PDF, size=64, color=ft.colors.RED_600),
                    ft.Container(height=20),
                    ft.Text(
                        "Pré-visualização não disponível para PDFs.",
                        size=16,
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            else:
                content = ft.Column([
                    ft.Icon(ft.icons.INSERT_DRIVE_FILE, size=64, color=ft.colors.GREY_600),
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
        """Fecha o diálogo de pré-visualização do arquivo."""
        self.file_preview_dialog.open = False
        self.page.update()

    def go_back(self, e):
        """Volta para Ver Tarefas Aluno"""
        self.controller.show_page("VerTarefasAluno")