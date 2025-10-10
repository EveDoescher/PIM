import flet as ft
import re
from db.database import authenticate_user

class Login(ft.Container):
    """Classe responsável pela tela de login do aplicativo."""

    def __init__(self, page: ft.Page, controller):
        """Inicializa a tela de login."""
        super().__init__()
        self.page = page
        self.controller = controller

        # Estado para toggle de senha
        self.password_visible = False

        # Campos do formulário
        self.ra_field = ft.TextField(
            label="RA",
            width=400,
            prefix_icon=ft.Icons.PERSON,
            max_length=7,
            on_change=self.validate_ra,
            border_radius=15,
            filled=True,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.TEAL_600,
            label_style=ft.TextStyle(color=ft.Colors.GREY_700),
            text_style=ft.TextStyle(size=16)
        )

        self.password_toggle = ft.IconButton(
            icon=ft.Icons.VISIBILITY_OFF,
            on_click=self.show_password_toggle,
            icon_color=ft.Colors.GREY_600,
            tooltip="Mostrar/Ocultar senha"
        )

        self.password_field = ft.TextField(
            label="Senha",
            password=True,
            width=400,
            prefix_icon=ft.Icons.LOCK,
            suffix=self.password_toggle,
            border_radius=15,
            filled=True,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.TEAL_600,
            label_style=ft.TextStyle(color=ft.Colors.GREY_700),
            text_style=ft.TextStyle(size=16)
        )

        # Botão de login
        self.login_button = ft.ElevatedButton(
            "Entrar",
            width=400,
            height=55,
            bgcolor=ft.Colors.TEAL_600,
            color=ft.Colors.WHITE,
            on_click=self.login,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=27),
                elevation=5,
                text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
            )
        )

        # Link para registro
        self.register_link = ft.TextButton(
            "Criar nova conta",
            on_click=self.go_to_register,
            style=ft.ButtonStyle(
                color=ft.Colors.TEAL_600,
                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_500)
            )
        )

        # Card principal de login
        self.login_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.SCHOOL, size=64, color=ft.Colors.TEAL_600),
                            ft.Container(height=10),
                            ft.Text(
                                "Sistema acadêmico colaborativo", 
                                size=32, 
                                weight=ft.FontWeight.BOLD, 
                                color=ft.Colors.TEAL_600,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Text(
                                "Faça login para continuar", 
                                size=16, 
                                color=ft.Colors.GREY_600,
                                text_align=ft.TextAlign.CENTER
                            )
                        ], 
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=ft.padding.only(bottom=30)
                    ),
                    self.ra_field,
                    ft.Container(height=20),
                    self.password_field,
                    ft.Container(height=30),
                    self.login_button,
                    ft.Container(height=25),
                    ft.Row([
                        ft.Container(
                            content=ft.Divider(color=ft.Colors.GREY_300),
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Text("ou", color=ft.Colors.GREY_500),
                            padding=ft.padding.symmetric(horizontal=15)
                        ),
                        ft.Container(
                            content=ft.Divider(color=ft.Colors.GREY_300),
                            expand=True
                        )
                    ]),
                    ft.Container(height=15),
                    self.register_link
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                width=500,
                padding=40,
                border_radius=20
            ),
            elevation=8
        )

        # Layout da página adaptado para tela cheia com scroll
        self.content = ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            padding=ft.padding.all(0),
            
            content=ft.Column([
                ft.Container(expand=True),
                self.login_card,
                ft.Container(expand=True)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
            )
        )

    def validate_ra(self, e):
        """Valida e corrige o input do RA em tempo real."""
        value = e.control.value.upper()  # Converte para maiúsculo
        # Permite apenas R e dígitos
        cleaned = ''.join(c for c in value if c.isdigit() or c == 'R')
        # Garante que comece com R
        if not cleaned.startswith('R'):
            cleaned = 'R' + ''.join(c for c in cleaned if c.isdigit())
        # Remove R extras
        if cleaned.count('R') > 1:
            cleaned = 'R' + ''.join(c for c in cleaned[1:] if c.isdigit())
        # Limita a 7 caracteres
        cleaned = cleaned[:7]
        self.ra_field.value = cleaned
        self.page.update()

    def login(self, e):
        """Função executada quando o botão de login é pressionado"""
        ra = self.ra_field.value
        password = self.password_field.value

        # Validação básica dos campos
        if not ra or not password:
            self.show_snackbar("Preencha todos os campos!", ft.Colors.RED_400)
            return

        # Validação do formato do RA
        if not re.match(r'^R\d{6}$', ra):
            self.show_snackbar("RA deve ser R seguido de exatamente 6 dígitos!", ft.Colors.RED_400)
            return

        user = authenticate_user(ra, password)
        if user:
            self.controller.current_user = user
            self.show_snackbar("Login realizado com sucesso!", ft.Colors.GREEN_600)
            if user['role'] == 'professor':
                self.controller.show_page("DashboardProfessor")
            else:
                self.controller.show_page("DashboardAluno")
        else:
            self.show_snackbar("RA ou senha incorretos!", ft.Colors.RED_400)

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

    def show_password_toggle(self, e):
        """Alterna a visibilidade da senha."""
        self.password_visible = not self.password_visible
        self.password_field.password = not self.password_visible
        self.password_toggle.icon = ft.Icons.VISIBILITY if self.password_visible else ft.Icons.VISIBILITY_OFF
        self.page.update()

    def go_to_register(self, e):
        """Navega para a tela de registro"""
        self.controller.show_page("Register")