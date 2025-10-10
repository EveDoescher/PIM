import flet as ft
from datetime import datetime
from db.database import insert_student_response, get_user_id, get_student_response
import os

class DetalheTarefaAluno(ft.Container):
    """Classe responsável pela tela de detalhes da tarefa do aluno."""

    def __init__(self, page: ft.Page, controller):
        """Inicializa a tela de detalhes da tarefa do aluno."""
        super().__init__()
        self.page = page
        self.controller = controller

        # File picker
        self.file_picker = ft.FilePicker(on_result=self.on_file_selected)
        self.page.overlay.append(self.file_picker)

        # File preview dialog
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

        # Variáveis para arquivo selecionado
        self.selected_file_path = None
        self.selected_file_name = None

        # Título da tela
        self.title_screen = ft.Text(
            "Detalhes da Tarefa", 
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

        # Container para detalhes da tarefa
        self.task_details_container = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=25,
            border=ft.border.all(1, ft.Colors.GREY_300)
        )

        # Container para controles de upload
        self.upload_container = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            padding=25,
            border=ft.border.all(1, ft.Colors.GREY_300)
        )

        # Controles para arquivo enviado
        self.submitted_file_button = ft.ElevatedButton(
            "",
            icon=ft.Icons.DESCRIPTION,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            on_click=self.show_file_preview,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
                elevation=3
            )
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
                self.title_screen,
                ft.Container(height=40),
                self.task_details_container,
                ft.Container(height=20),
                self.upload_container
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO)
        )

        # Carregar detalhes inicialmente
        self.refresh()

    def refresh(self):
        if self.controller.current_task:
            task = self.controller.current_task
            
            # Detalhes da tarefa
            creation_dt = datetime.strptime(task[3], '%Y-%m-%d %H:%M:%S.%f')
            exp_dt = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S')
            
            task_info = ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.ASSIGNMENT, size=28, color=ft.Colors.TEAL_600),
                    ft.Container(width=15),
                    ft.Text(
                        task[1], 
                        size=24, 
                        weight=ft.FontWeight.BOLD, 
                        color=ft.Colors.BLACK
                    )
                ]),
                ft.Container(height=20),
                ft.Container(
                    content=ft.Text(
                        task[2] if task[2] else 'Sem descrição disponível', 
                        size=16, 
                        color=ft.Colors.GREY_800
                    ),
                    bgcolor=ft.Colors.GREY_50,
                    padding=15,
                    border_radius=10,
                    border=ft.border.all(1, ft.Colors.GREY_200)
                ),
                ft.Container(height=20),
                ft.Row([
                    ft.Icon(ft.Icons.CALENDAR_TODAY, size=20, color=ft.Colors.GREY_600),
                    ft.Container(width=10),
                    ft.Text(
                        f"Criado em: {creation_dt.strftime('%d/%m/%Y às %H:%M')}", 
                        size=14, 
                        color=ft.Colors.GREY_700
                    )
                ]),
                ft.Container(height=10),
                ft.Row([
                    ft.Icon(ft.Icons.SCHEDULE, size=20, color=ft.Colors.GREY_600),
                    ft.Container(width=10),
                    ft.Text(
                        f"Vence em: {exp_dt.strftime('%d/%m/%Y às %H:%M')}", 
                        size=14, 
                        color=ft.Colors.GREY_700
                    )
                ])
            ])

            self.task_details_container.content = task_info
            self.task_details_container.width = 700

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
                        ft.Icon(ft.Icons.CHECK_CIRCLE, size=28, color=ft.Colors.GREEN_600),
                        ft.Container(width=15),
                        ft.Text(
                            "Tarefa Entregue", 
                            size=20, 
                            weight=ft.FontWeight.BOLD, 
                            color=ft.Colors.GREEN_600
                        )
                    ]),
                    ft.Container(height=20),
                    ft.Row([
                        ft.Icon(ft.Icons.ATTACH_FILE, size=20, color=ft.Colors.GREY_600),
                        ft.Container(width=10),
                        ft.Text(f"Arquivo: {filename}", size=16, color=ft.Colors.GREY_800)
                    ]),
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        "Visualizar Arquivo Enviado",
                        width=250,
                        height=45,
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE,
                        icon=ft.Icons.VISIBILITY,
                        on_click=self.show_file_preview,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=22),
                            elevation=3
                        )
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                
            elif datetime.now() <= exp_dt:
                # Tarefa ativa - mostrar controles de upload
                self.selected_file_label = ft.Text(
                    "Nenhum arquivo selecionado", 
                    size=14, 
                    color=ft.Colors.GREY_600
                )
                
                upload_content = ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.UPLOAD_FILE, size=28, color=ft.Colors.TEAL_600),
                        ft.Container(width=15),
                        ft.Text(
                            "Enviar Resposta", 
                            size=20, 
                            weight=ft.FontWeight.BOLD, 
                            color=ft.Colors.TEAL_600
                        )
                    ]),
                    ft.Container(height=20),
                    ft.Text(
                        "Formatos aceitos: PNG, JPG, JPEG, PDF (máx. 10MB)", 
                        size=12, 
                        color=ft.Colors.GREY_600
                    ),
                    ft.Container(height=15),
                    self.selected_file_label,
                    ft.Container(height=20),
                    ft.Row([
                        ft.ElevatedButton(
                            "Selecionar Arquivo",
                            width=180,
                            height=40,
                            bgcolor=ft.Colors.GREY_600,
                            color=ft.Colors.WHITE,
                            icon=ft.Icons.FOLDER_OPEN,
                            on_click=self.select_file,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=20),
                                elevation=3
                            )
                        ),
                        ft.Container(width=20),
                        ft.ElevatedButton(
                            "Enviar Resposta",
                            width=180,
                            height=40,
                            bgcolor=ft.Colors.TEAL_600,
                            color=ft.Colors.WHITE,
                            icon=ft.Icons.SEND,
                            on_click=self.send_response,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=20),
                                elevation=3
                            )
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                
            else:
                # Tarefa expirada
                upload_content = ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.SCHEDULE_OUTLINED, size=28, color=ft.Colors.RED_600),
                        ft.Container(width=15),
                        ft.Text(
                            "Tarefa Expirada", 
                            size=20, 
                            weight=ft.FontWeight.BOLD, 
                            color=ft.Colors.RED_600
                        )
                    ]),
                    ft.Container(height=15),
                    ft.Text(
                        "O prazo para entrega desta tarefa já passou.", 
                        size=16, 
                        color=ft.Colors.GREY_700,
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

            self.upload_container.content = upload_content
            self.upload_container.width = 700

        else:
            # Caso não haja tarefa selecionada
            self.task_details_container.content = ft.Text(
                "Nenhuma tarefa selecionada", 
                size=18, 
                color=ft.Colors.GREY_600
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
            self.selected_file_label.color = ft.Colors.GREEN_600
        else:
            self.selected_file_path = None
            self.selected_file_name = None
            self.selected_file_label.value = "Nenhum arquivo selecionado"
            self.selected_file_label.color = ft.Colors.GREY_600
        self.page.update()

    def send_response(self, e):
        """Envia a resposta do aluno para a tarefa."""
        if not self.controller.current_task:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Nenhuma tarefa selecionada!"), 
                bgcolor=ft.Colors.RED
            )
            self.page.snack_bar.open = True
            self.page.update()
            return
            
        if not self.selected_file_path:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Nenhum arquivo selecionado!"), 
                bgcolor=ft.Colors.RED
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        task_id = self.controller.current_task[0]
        user_ra = self.controller.current_user['ra']
        user_id = get_user_id(user_ra)
        if not user_id:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Usuário não encontrado!"), 
                bgcolor=ft.Colors.RED
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        filename = self.selected_file_name

        # Verificar tamanho do arquivo (limite de 10MB)
        file_size = os.path.getsize(self.selected_file_path)
        max_size = 10 * 1024 * 1024  # 10MB
        if file_size > max_size:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Arquivo muito grande. Limite de 10MB."), 
                bgcolor=ft.Colors.RED
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        try:
            with open(self.selected_file_path, 'rb') as f:
                file_data = f.read()
        except FileNotFoundError:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Arquivo não encontrado."), 
                bgcolor=ft.Colors.RED
            )
            self.page.snack_bar.open = True
            self.page.update()
            return
        except PermissionError:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Permissão negada para acessar o arquivo."), 
                bgcolor=ft.Colors.RED
            )
            self.page.snack_bar.open = True
            self.page.update()
            return
        except OSError as ex:
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Erro ao ler o arquivo: {ex}"), 
                bgcolor=ft.Colors.RED
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        if insert_student_response(task_id, user_id, filename, file_data):
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Resposta enviada com sucesso!"), 
                bgcolor=ft.Colors.GREEN
            )
            self.page.snack_bar.open = True
            self.selected_file_path = None
            self.selected_file_name = None
            self.refresh()  # Recarregar para mostrar status entregue
        else:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Falha ao enviar resposta."), 
                bgcolor=ft.Colors.RED
            )
            self.page.snack_bar.open = True
        self.page.update()

    def go_back(self, e):
        """Volta para Ver Tarefas Aluno"""
        self.controller.show_page("VerTarefasAluno")

    def show_file_preview(self, e):
        if not hasattr(self, 'file_data') or not self.file_data:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Nenhum arquivo para visualizar."), 
                bgcolor=ft.Colors.RED
            )
            self.page.snack_bar.open = True
            self.page.update()
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
                    ft.Icon(ft.Icons.PICTURE_AS_PDF, size=64, color=ft.Colors.RED_600),
                    ft.Container(height=20),
                    ft.Text(
                        "Pré-visualização não disponível para PDFs.", 
                        size=16, 
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
        """Fecha o diálogo de pré-visualização do arquivo."""
        self.file_preview_dialog.open = False
        self.page.update()