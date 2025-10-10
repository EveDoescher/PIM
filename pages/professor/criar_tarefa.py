import flet as ft
from datetime import datetime, timedelta
from db.database import insert_task, get_user_id

class CriarTarefa(ft.Container):
    """Classe responsável pela tela de criar tarefa do professor."""

    def __init__(self, page: ft.Page, controller):
        """Inicializa a tela de criar tarefa."""
        super().__init__()
        self.page = page
        self.controller = controller

        # Título da tela
        self.title = ft.Text(
            "Criar Nova Tarefa",
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

        # Campos do formulário - aumentando largura para tela cheia
        self.title_field = ft.TextField(
            label="Título da Tarefa",
            width=700,
            border_radius=15,
            filled=True,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.TEAL_600,
            label_style=ft.TextStyle(color=ft.Colors.GREY_700),
            text_style=ft.TextStyle(size=16),
            prefix_icon=ft.Icons.TITLE
        )

        self.description_field = ft.TextField(
            label="Descrição da Tarefa",
            width=700,
            multiline=True,
            min_lines=4,
            max_lines=8,
            border_radius=15,
            filled=True,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.TEAL_600,
            label_style=ft.TextStyle(color=ft.Colors.GREY_700),
            text_style=ft.TextStyle(size=16),
            prefix_icon=ft.Icons.DESCRIPTION
        )

        # Data e hora de expiração
        tomorrow = datetime.now() + timedelta(days=1)
        self.selected_date = tomorrow.date()
        
        self.date_picker = ft.DatePicker(
            first_date=datetime.now().date(),
            last_date=datetime.now().date() + timedelta(days=365),
            value=self.selected_date,
            on_change=self.on_date_change
        )
        self.page.overlay.append(self.date_picker)

        self.date_button = ft.ElevatedButton(
            f"Data: {tomorrow.strftime('%d/%m/%Y')}",
            width=320,
            height=50,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.GREY_800,
            icon=ft.Icons.CALENDAR_TODAY,
            on_click=self.open_date_picker,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=15),
                side=ft.BorderSide(1, ft.Colors.GREY_300)
            )
        )

        self.time_field = ft.TextField(
            label="Horário (HH:MM)",
            width=320,
            value="23:59",
            border_radius=15,
            filled=True,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.TEAL_600,
            label_style=ft.TextStyle(color=ft.Colors.GREY_700),
            text_style=ft.TextStyle(size=16),
            prefix_icon=ft.Icons.ACCESS_TIME,
            on_change=self.validate_time
        )

        # Botão criar tarefa
        self.create_button = ft.ElevatedButton(
            "Criar Tarefa",
            width=300,
            height=55,
            bgcolor=ft.Colors.TEAL_600,
            color=ft.Colors.WHITE,
            icon=ft.Icons.ADD_TASK,
            on_click=self.create_task,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=27),
                elevation=5,
                text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
            )
        )

        # Dialog de confirmação de sucesso
        self.success_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Sucesso", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Text("Tarefa criada com sucesso!"),
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

        # Card principal do formulário - adaptado para tela cheia
        self.form_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.ADD_TASK, size=48, color=ft.Colors.TEAL_600),
                            ft.Container(height=15),
                            ft.Text(
                                "Preencha os dados da nova tarefa",
                                size=16,
                                color=ft.Colors.GREY_600,
                                text_align=ft.TextAlign.CENTER
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=ft.padding.only(bottom=30)
                    ),
                    
                    self.title_field,
                    ft.Container(height=20),
                    
                    self.description_field,
                    ft.Container(height=25),
                    
                    ft.Text(
                        "Data e Hora de Expiração:",
                        size=16,
                        color=ft.Colors.GREY_700,
                        weight=ft.FontWeight.W_500
                    ),
                    ft.Container(height=15),
                    
                    ft.ResponsiveRow([
                        ft.Container(
                            content=self.date_button,
                            col={"sm": 12, "md": 6, "lg": 6},
                            alignment=ft.alignment.center
                        ),
                        ft.Container(
                            content=self.time_field,
                            col={"sm": 12, "md": 6, "lg": 6},
                            alignment=ft.alignment.center
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    
                    ft.Container(height=35),
                    self.create_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO
                ),
                width=800,
                padding=40,
                border_radius=20
            ),
            elevation=8
        )

        # Layout principal adaptado para tela cheia
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
                ft.Container(height=40),
                ft.Container(
                    content=self.form_card,
                    expand=True,
                    alignment=ft.alignment.center
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
            )
        )

    def on_date_change(self, e):
        """Atualiza o texto do botão quando a data é alterada."""
        if self.date_picker.value:
            self.selected_date = self.date_picker.value
            self.date_button.text = f"Data: {self.selected_date.strftime('%d/%m/%Y')}"
            self.page.update()

    def validate_time(self, e):
        """Valida o formato do horário em tempo real."""
        value = e.control.value
        # Remove caracteres não numéricos exceto ':'
        cleaned = ''.join(c for c in value if c.isdigit() or c == ':')
        
        # Formata automaticamente HH:MM
        if len(cleaned) == 1 and cleaned.isdigit():
            cleaned = cleaned
        elif len(cleaned) == 2 and cleaned.isdigit():
            cleaned = cleaned
        elif len(cleaned) == 3 and ':' not in cleaned:
            cleaned = cleaned[:2] + ':' + cleaned[2:]
        elif len(cleaned) == 4 and ':' not in cleaned:
            cleaned = cleaned[:2] + ':' + cleaned[2:]
        elif len(cleaned) > 5:
            cleaned = cleaned[:5]
        
        self.time_field.value = cleaned
        self.page.update()

    def create_task(self, e):
        """Cria uma nova tarefa."""
        title = self.title_field.value.strip()
        description = self.description_field.value.strip()
        time_str = self.time_field.value.strip()

        # Validações
        if not title:
            self.show_snackbar("O título da tarefa é obrigatório!", ft.Colors.RED_400)
            return

        if not description:
            self.show_snackbar("A descrição da tarefa é obrigatória!", ft.Colors.RED_400)
            return

        # Verificar se o usuário está logado
        if not self.controller.current_user:
            self.show_snackbar("Erro: usuário não está logado!", ft.Colors.RED_400)
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
            self.show_snackbar("Formato de horário inválido! Use HH:MM (ex: 14:30)", ft.Colors.RED_400)
            return

        # Criar datetime de expiração
        exp_datetime = datetime.combine(self.selected_date, datetime.strptime(time_str, '%H:%M').time())

        # Verificar se a data não é no passado
        if exp_datetime <= datetime.now():
            self.show_snackbar("A data de expiração deve ser no futuro!", ft.Colors.RED_400)
            return

        # Obter user_id do professor logado
        user_id = get_user_id(self.controller.current_user["ra"])
        if not user_id:
            self.show_snackbar("Erro: não foi possível identificar o usuário!", ft.Colors.RED_400)
            return

        # Inserir no banco de dados
        if insert_task(title, description, exp_datetime, user_id):
            # Limpar campos
            self.title_field.value = ""
            self.description_field.value = ""
            self.time_field.value = "23:59"
            tomorrow = datetime.now() + timedelta(days=1)
            self.selected_date = tomorrow.date()
            self.date_picker.value = self.selected_date
            self.date_button.text = f"Data: {tomorrow.strftime('%d/%m/%Y')}"
            self.page.update()
            
            # Mostrar dialog de sucesso
            self.page.open(self.success_dialog)
        else:
            self.show_snackbar("Erro ao criar tarefa. Tente novamente.", ft.Colors.RED_400)

    def close_success_dialog(self, e):
        """Fecha o dialog de sucesso e redireciona para o dashboard do professor."""
        self.success_dialog.open = False
        self.page.update()
        self.controller.show_page("DashboardProfessor")

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

    def open_date_picker(self, e):
        """Abre o seletor de data para escolher a data de expiração."""
        self.date_picker.open = True
        self.page.update()

    def go_back(self, e):
        """Volta para o dashboard do professor."""
        self.controller.show_page("DashboardProfessor")