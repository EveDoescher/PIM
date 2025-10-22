import flet as ft
from datetime import datetime, timedelta
from backend.database import update_task

class EditarTarefa(ft.Container):
    """Classe responsável pela tela de editar tarefa do professor com design clean."""

    def __init__(self, page: ft.Page, controller):
        """Inicializa a tela de editar tarefa."""
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

        # Campos do formulário clean - MAIORES
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
            content_padding=ft.padding.symmetric(horizontal=25, vertical=25)
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
            content_padding=ft.padding.symmetric(horizontal=25, vertical=25)
        )

        # Data e hora de expiração
        self.selected_date = datetime.now().date()
        
        self.date_picker = ft.DatePicker(
            first_date=datetime.now().date(),
            last_date=datetime.now().date() + timedelta(days=365),
            value=self.selected_date,
            on_change=self.on_date_change
        )
        self.page.overlay.append(self.date_picker)

        self.date_button = ft.Container(
            content=ft.Row([
                ft.Icon(ft.icons.CALENDAR_TODAY_ROUNDED, color=ft.colors.PINK_400, size=24),
                ft.Text(
                    f"{self.selected_date.strftime('%d/%m/%Y')}",
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
            value="23:59",
            prefix_icon=ft.icons.ACCESS_TIME_ROUNDED,
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

        # Botão salvar alterações clean - MAIOR
        self.save_button = ft.Container(
            content=ft.Text(
                "Salvar Alterações",
                size=20,
                weight=ft.FontWeight.W_600,
                color=ft.colors.WHITE
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
            on_click=self.save_task
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
                        "Editar Tarefa",
                        size=42,
                        weight=ft.FontWeight.W_600,
                        color=ft.colors.GREY_800,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Modifique os dados da tarefa selecionada",
                        size=20,
                        color=ft.colors.GREY_500,
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(expand=True)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=60, vertical=45)
        )

        # Card principal do formulário clean - MAIOR
        form_card = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Icon(ft.icons.EDIT_ROUNDED, size=65, color=ft.colors.PURPLE_400),
                            width=130,
                            height=130,
                            border_radius=65,
                            bgcolor=ft.colors.with_opacity(0.1, ft.colors.PURPLE_400),
                            alignment=ft.alignment.center
                        ),
                        ft.Container(height=20),
                        ft.Text(
                            "Edite os dados da tarefa",
                            size=22,
                            color=ft.colors.GREY_600,
                            text_align=ft.TextAlign.CENTER,
                            weight=ft.FontWeight.W_500
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.padding.only(bottom=40)
                ),
                
                self.title_field,
                ft.Container(height=35),
                
                self.description_field,
                ft.Container(height=40),
                
                ft.Text(
                    "Data e Hora de Expiração:",
                    size=20,
                    color=ft.colors.GREY_700,
                    weight=ft.FontWeight.W_600
                ),
                ft.Container(height=20),
                
                ft.Row([
                    self.date_button,
                    ft.Container(width=40),
                    self.time_field
                ], alignment=ft.MainAxisAlignment.CENTER),
                
                ft.Container(height=45),
                self.save_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
            ),
            width=800,
            bgcolor=ft.colors.WHITE,
            border_radius=25,
            padding=ft.padding.all(50),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.colors.with_opacity(0.08, ft.colors.BLACK),
                offset=ft.Offset(0, 8)
            ),
            border=ft.border.all(1, ft.colors.with_opacity(0.05, ft.colors.BLACK))
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
                ft.Container(
                    content=form_card,
                    expand=True,
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(horizontal=60, vertical=25)
                )
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO
            )
        )

        # Carregar dados da tarefa atual
        self.load_task_data()

    def load_task_data(self):
        """Carrega os dados da tarefa atual nos campos."""
        if self.controller.current_task:
            task = self.controller.current_task
            
            # Preencher campos
            self.title_field.value = task[1]  # título
            self.description_field.value = task[2] or ""  # descrição
            
            # Processar data de expiração
            try:
                exp_date = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S')
                self.selected_date = exp_date.date()
                self.date_picker.value = self.selected_date
                self.date_button.content.controls[1].value = self.selected_date.strftime('%d/%m/%Y')
                self.time_field.value = exp_date.strftime('%H:%M')
            except ValueError:
                # Usar valores padrão se houver erro na conversão
                tomorrow = datetime.now() + timedelta(days=1)
                self.selected_date = tomorrow.date()
                self.date_picker.value = self.selected_date
                self.date_button.content.controls[1].value = tomorrow.strftime('%d/%m/%Y')
                self.time_field.value = "23:59"

    def on_date_change(self, e):
        """Atualiza o texto do botão quando a data é alterada."""
        if self.date_picker.value:
            self.selected_date = self.date_picker.value
            self.date_button.content.controls[1].value = self.selected_date.strftime('%d/%m/%Y')
            self.page.update()

    def validate_time(self, e):
        """Valida o formato do horário em tempo real."""
        value = e.control.value
        # Remove caracteres não numéricos exceto ':'
        cleaned = ''.join(c for c in value if c.isdigit() or c == ':')
        
        # Formata automaticamente HH:MM
        if len(cleaned) > 2 and ':' not in cleaned:
            cleaned = cleaned[:2] + ':' + cleaned[2:]
        
        # Limitar a 5 caracteres
        cleaned = cleaned[:5]
        
        self.time_field.value = cleaned
        self.page.update()

    def save_task(self, e):
        """Salva as alterações da tarefa."""
        if not self.controller.current_task:
            self.controller.show_snackbar("Erro: nenhuma tarefa selecionada!", "error")
            return

        task_id = self.controller.current_task[0]
        title = self.title_field.value.strip()
        description = self.description_field.value.strip()
        time_str = self.time_field.value.strip()

        # Validações
        if not title:
            self.controller.show_snackbar("O título da tarefa é obrigatório!", "error")
            return

        if not description:
            self.controller.show_snackbar("A descrição da tarefa é obrigatória!", "error")
            return

        # Validar formato do horário
        try:
            time_parts = time_str.split(':')
            if len(time_parts) != 2:
                raise ValueError()
            hours = int(time_parts[0])
            minutes = int(time_parts[1])
            if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
                raise ValueError()
        except (ValueError, IndexError):
            self.controller.show_snackbar("Formato de horário inválido! Use HH:MM (ex: 14:30)", "error")
            return

        # Criar datetime de expiração
        exp_datetime = datetime.combine(self.selected_date, datetime.strptime(time_str, '%H:%M').time())

        # Verificar se a data não é no passado
        if exp_datetime <= datetime.now():
            self.controller.show_snackbar("A data de expiração deve ser no futuro!", "error")
            return

        # Atualizar no banco de dados
        if update_task(task_id, title, description, exp_datetime):
            # Atualizar a tarefa atual no controller
            updated_task = list(self.controller.current_task)
            updated_task[1] = title
            updated_task[2] = description
            updated_task[4] = exp_datetime.strftime('%Y-%m-%d %H:%M:%S')
            self.controller.current_task = tuple(updated_task)
            
            # Mostrar sucesso e voltar
            self.controller.show_snackbar("Tarefa editada com sucesso!", "success")
            self.controller.show_page("DetalheTarefa")
        else:
            self.controller.show_snackbar("Erro ao editar tarefa. Tente novamente.", "error")

    def open_date_picker(self, e):
        """Abre o seletor de data para escolher a data de expiração."""
        self.date_picker.pick_date()

    def go_back(self, e):
        """Volta para os detalhes da tarefa."""
        self.controller.show_page("DetalheTarefa")