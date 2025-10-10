import flet as ft
from datetime import datetime, timedelta
from db.database import update_task

class EditarTarefa(ft.Container):
    """Classe responsável pela tela de editar tarefa do professor."""

    def __init__(self, page: ft.Page, controller):
        """Inicializa a tela de editar tarefa."""
        super().__init__()
        self.page = page
        self.controller = controller

        # Título da tela
        self.title = ft.Text(
            "Editar Tarefa",
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

        # Campos do formulário
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
        self.selected_date = datetime.now().date()
        
        self.date_picker = ft.DatePicker(
            first_date=datetime.now().date(),
            last_date=datetime.now().date() + timedelta(days=365),
            value=self.selected_date,
            on_change=self.on_date_change
        )
        self.page.overlay.append(self.date_picker)

        self.date_button = ft.ElevatedButton(
            f"Data: {self.selected_date.strftime('%d/%m/%Y')}",
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

        # Botão salvar alterações
        self.save_button = ft.ElevatedButton(
            "Salvar Alterações",
            width=300,
            height=55,
            bgcolor=ft.Colors.TEAL_600,
            color=ft.Colors.WHITE,
            icon=ft.Icons.SAVE,
            on_click=self.save_task,
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
            content=ft.Text("Tarefa editada com sucesso!"),
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

        # Card principal do formulário
        self.form_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.EDIT, size=48, color=ft.Colors.TEAL_600),
                            ft.Container(height=15),
                            ft.Text(
                                "Edite os dados da tarefa",
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
                    self.save_button
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

        # Layout principal
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
                self.date_button.text = f"Data: {self.selected_date.strftime('%d/%m/%Y')}"
                self.time_field.value = exp_date.strftime('%H:%M')
            except ValueError:
                # Usar valores padrão se houver erro na conversão
                tomorrow = datetime.now() + timedelta(days=1)
                self.selected_date = tomorrow.date()
                self.date_picker.value = self.selected_date
                self.date_button.text = f"Data: {tomorrow.strftime('%d/%m/%Y')}"
                self.time_field.value = "23:59"

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

    def save_task(self, e):
        """Salva as alterações da tarefa."""
        if not self.controller.current_task:
            self.show_snackbar("Erro: nenhuma tarefa selecionada!", ft.Colors.RED_400)
            return

        task_id = self.controller.current_task[0]
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

        # Atualizar no banco de dados
        if update_task(task_id, title, description, exp_datetime):
            # Atualizar a tarefa atual no controller
            updated_task = list(self.controller.current_task)
            updated_task[1] = title
            updated_task[2] = description
            updated_task[4] = exp_datetime.strftime('%Y-%m-%d %H:%M:%S')
            self.controller.current_task = tuple(updated_task)
            
            # Mostrar dialog de sucesso
            self.page.open(self.success_dialog)
        else:
            self.show_snackbar("Erro ao editar tarefa. Tente novamente.", ft.Colors.RED_400)

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

    def open_date_picker(self, e):
        """Abre o seletor de data para escolher a data de expiração."""
        self.date_picker.open = True
        self.page.update()

    def go_back(self, e):
        """Volta para os detalhes da tarefa."""
        self.controller.show_page("DetalheTarefa")