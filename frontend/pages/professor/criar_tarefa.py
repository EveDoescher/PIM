import flet as ft
from datetime import datetime, timedelta
from backend.database import insert_task

class CriarTarefa(ft.Container):

    def __init__(self, page: ft.Page, controller):
        # Inicializa a interface de criação de tarefas
        super().__init__(
            expand=True,
            width=None,
            height=None,
            padding=ft.padding.all(0),
            margin=ft.margin.all(0)
        )
        self.page = page
        self.controller = controller
        
        self.is_loading = False
        self.selected_date = datetime.now() + timedelta(days=7)
        
        self.create_components()
        self.setup_layout()

    def create_components(self):
        # Cria todos os componentes da interface de usuário
        
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

        self.title_field = ft.TextField(
            label="Título da Tarefa",
            width=700,
            height=90,
            prefix_icon=ft.icons.TITLE_ROUNDED,
            border_radius=20,
            filled=True,
            bgcolor=ft.colors.WHITE,
            border_color=ft.colors.with_opacity(0.1, ft.colors.GREY_400),
            focused_border_color=ft.colors.PINK_400,
            focused_bgcolor=ft.colors.WHITE,
            label_style=ft.TextStyle(
                color=ft.colors.GREY_600,
                size=20,
                weight=ft.FontWeight.W_500
            ),
            text_style=ft.TextStyle(
                size=20,
                weight=ft.FontWeight.W_500,
                color=ft.colors.GREY_800
            ),
            cursor_color=ft.colors.PINK_400,
            selection_color=ft.colors.PINK_100,
            content_padding=ft.padding.symmetric(horizontal=25, vertical=25),
            on_change=self.update_preview
        )

        self.description_field = ft.TextField(
            label="Descrição da Tarefa",
            width=700,
            height=150,
            prefix_icon=ft.icons.DESCRIPTION_ROUNDED,
            multiline=True,
            min_lines=5,
            max_lines=7,
            border_radius=20,
            filled=True,
            bgcolor=ft.colors.WHITE,
            border_color=ft.colors.with_opacity(0.1, ft.colors.GREY_400),
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
            content_padding=ft.padding.symmetric(horizontal=25, vertical=25),
            on_change=self.update_preview
        )

        self.date_picker = ft.DatePicker(
            first_date=datetime.now(),
            last_date=datetime.now() + timedelta(days=365),
            on_change=self.on_date_change
        )
        self.page.overlay.append(self.date_picker)

        self.date_button = ft.Container(
            content=ft.Row([
                ft.Icon(ft.icons.CALENDAR_TODAY_ROUNDED, color=ft.colors.PINK_400, size=24),
                ft.Text(
                    self.selected_date.strftime("%d/%m/%Y"),
                    size=20,
                    weight=ft.FontWeight.W_500,
                    color=ft.colors.GREY_800
                ),
                ft.Icon(ft.icons.EXPAND_MORE_ROUNDED, color=ft.colors.GREY_500, size=24)
            ], spacing=15, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            width=330,
            height=90,
            bgcolor=ft.colors.WHITE,
            border_radius=20,
            border=ft.border.all(1, ft.colors.with_opacity(0.1, ft.colors.GREY_400)),
            padding=ft.padding.symmetric(horizontal=25, vertical=25),
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=ft.colors.with_opacity(0.04, ft.colors.BLACK),
                offset=ft.Offset(0, 3)
            ),
            on_click=self.open_date_picker
        )

        self.time_field = ft.TextField(
            label="Horário (HH:MM)",
            width=330,
            height=90,
            prefix_icon=ft.icons.ACCESS_TIME_ROUNDED,
            value="23:59",
            border_radius=20,
            filled=True,
            bgcolor=ft.colors.WHITE,
            border_color=ft.colors.with_opacity(0.1, ft.colors.GREY_400),
            focused_border_color=ft.colors.PINK_400,
            focused_bgcolor=ft.colors.WHITE,
            label_style=ft.TextStyle(
                color=ft.colors.GREY_600,
                size=20,
                weight=ft.FontWeight.W_500
            ),
            text_style=ft.TextStyle(
                size=20,
                weight=ft.FontWeight.W_500,
                color=ft.colors.GREY_800
            ),
            cursor_color=ft.colors.PINK_400,
            selection_color=ft.colors.PINK_100,
            content_padding=ft.padding.symmetric(horizontal=25, vertical=25),
            on_change=self.validate_time
        )

        self.loading_indicator = ft.ProgressRing(
            width=35,
            height=35,
            stroke_width=4,
            color=ft.colors.WHITE,
            visible=False
        )

        self.create_button = ft.Container(
            content=ft.Row([
                self.loading_indicator,
                ft.Text(
                    "Criar Tarefa",
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color=ft.colors.WHITE
                )
            ], 
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12
            ),
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
            on_click=self.create_task
        )

        self.preview_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.PREVIEW_ROUNDED, size=36, color=ft.colors.PURPLE_400),
                    ft.Text(
                        "Preview da Tarefa",
                        size=26,
                        weight=ft.FontWeight.W_600,
                        color=ft.colors.GREY_800
                    )
                ], spacing=15),

                ft.Container(height=25),

                ft.Column([
                    ft.Text(
                        "Título: Nova Tarefa",
                        size=20,
                        weight=ft.FontWeight.W_600,
                        color=ft.colors.GREY_700
                    ),
                    ft.Container(height=12),
                    ft.Text(
                        "Descrição: Descrição da tarefa aparecerá aqui...",
                        size=18,
                        color=ft.colors.GREY_600
                    ),
                    ft.Container(height=12),
                    ft.Text(
                        f"Prazo: {self.selected_date.strftime('%d/%m/%Y')} às 23:59",
                        size=18,
                        color=ft.colors.GREY_600
                    )
                ], spacing=0)
            ]),
            width=600,
            bgcolor=ft.colors.WHITE,
            border_radius=20,
            padding=ft.padding.all(40),
            alignment=ft.alignment.top_left,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=15,
                color=ft.colors.with_opacity(0.06, ft.colors.BLACK),
                offset=ft.Offset(0, 5)
            ),
            border=ft.border.all(1, ft.colors.with_opacity(0.05, ft.colors.BLACK))
        )

    def setup_layout(self):
        # Configura o layout principal da página
        
        header = ft.Container(
            content=ft.Row([
                self.back_button,
                ft.Container(expand=True),
                ft.Column([
                    ft.Text(
                        "Criar Nova Tarefa",
                        size=42,
                        weight=ft.FontWeight.W_600,
                        color=ft.colors.GREY_800,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Preencha os dados abaixo para criar uma nova tarefa",
                        size=20,
                        color=ft.colors.GREY_500,
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(expand=True)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=60, vertical=45)
        )

        form_section = ft.Container(
            content=ft.Column([
                self.title_field,
                ft.Container(height=35),
                self.description_field,
                ft.Container(height=40),
                
                ft.Row([
                    ft.Column([
                        ft.Text(
                            "Data de Entrega",
                            size=20,
                            weight=ft.FontWeight.W_600,
                            color=ft.colors.GREY_700
                        ),
                        ft.Container(height=15),
                        self.date_button
                    ]),
                    ft.Container(width=40),
                    ft.Column([
                        ft.Text(
                            "Horário Limite",
                            size=20,
                            weight=ft.FontWeight.W_600,
                            color=ft.colors.GREY_700
                        ),
                        ft.Container(height=15),
                        self.time_field
                    ])
                ], alignment=ft.MainAxisAlignment.CENTER),
                
                ft.Container(height=45),
                self.create_button
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=60)
        )

        main_content = ft.Row([
            ft.Container(
                content=form_section,
                expand=2
            ),
            
            ft.Container(
                content=ft.Column([
                    ft.Container(height=140),
                    self.preview_card
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                expand=1,
                padding=ft.padding.only(right=60)
            )
        ], alignment=ft.MainAxisAlignment.START)

        self.content = ft.Container(
            expand=True,
            width=None,
            height=None,
            padding=ft.padding.all(0),
            margin=ft.margin.all(0),
            
            content=ft.Column([
                header,
                main_content,
                ft.Container(expand=True)
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO
            )
        )

    def open_date_picker(self, e):
        # Abre o seletor de data
        self.date_picker.pick_date()

    def on_date_change(self, e):
        # Processa mudança de data selecionada
        if self.date_picker.value:
            self.selected_date = self.date_picker.value
            self.date_button.content.controls[1].value = self.selected_date.strftime("%d/%m/%Y")
            self.update_preview()
            self.page.update()

    def validate_time(self, e):
        # Valida e formata o horário inserido
        value = e.control.value
        cleaned = ''.join(c for c in value if c.isdigit() or c == ':')
        
        if len(cleaned) > 2 and ':' not in cleaned:
            cleaned = cleaned[:2] + ':' + cleaned[2:]
        
        cleaned = cleaned[:5]
        
        e.control.value = cleaned
        self.update_preview()
        self.page.update()

    def update_preview(self, e=None):
        # Atualiza o preview da tarefa em tempo real
        title = self.title_field.value or "Nova Tarefa"
        description = self.description_field.value or "Descrição da tarefa aparecerá aqui..."
        time = self.time_field.value or "23:59"

        preview_content = self.preview_card.content.controls[2].controls
        preview_content[0].value = f"Título: {title}"
        preview_content[2].value = f"Descrição: {description}"
        preview_content[4].value = f"Prazo: {self.selected_date.strftime('%d/%m/%Y')} às {time}"

        self.page.update()

    def create_task(self, e):
        # Processa a criação da tarefa
        if self.is_loading:
            return

        title = self.title_field.value.strip()
        description = self.description_field.value.strip()
        time = self.time_field.value.strip()

        if not title:
            self.controller.show_snackbar("Título é obrigatório!", "error")
            return

        if not description:
            self.controller.show_snackbar("Descrição é obrigatória!", "error")
            return

        import re
        if not re.match(r'^\d{2}:\d{2}$', time):
            self.controller.show_snackbar("Horário deve estar no formato HH:MM!", "error")
            return

        try:
            hour, minute = map(int, time.split(':'))
            if hour > 23 or minute > 59:
                self.controller.show_snackbar("Horário inválido!", "error")
                return

            expiration_datetime = self.selected_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            if expiration_datetime <= datetime.now():
                self.controller.show_snackbar("A data de entrega deve ser futura!", "error")
                return

            self.start_loading()

            user_id = self.controller.current_user['id']
            expiration_str = expiration_datetime.strftime('%d/%m/%Y %H:%M')
            
            success = insert_task(title, description, expiration_str, user_id)
            
            if success:
                self.controller.show_snackbar("Tarefa criada com sucesso!", "success")
                self.controller.show_page("VerTarefa")
            else:
                self.controller.show_snackbar("Erro ao criar tarefa. Tente novamente.", "error")

        except Exception as ex:
            self.controller.show_snackbar(f"Erro: {str(ex)}", "error")
        finally:
            self.stop_loading()

    def start_loading(self):
        # Inicia o estado de carregamento
        self.is_loading = True
        self.loading_indicator.visible = True
        self.create_button.bgcolor = ft.colors.with_opacity(0.7, ft.colors.PINK_500)
        self.page.update()

    def stop_loading(self):
        # Para o estado de carregamento
        self.is_loading = False
        self.loading_indicator.visible = False
        self.create_button.bgcolor = ft.colors.PINK_500
        self.page.update()

    def go_back(self, e):
        # Retorna para o dashboard do professor
        self.controller.show_page("DashboardProfessor")