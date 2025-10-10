import flet as ft
import re
from db.database import insert_user

class Register(ft.Container):
    """Classe responsável pela tela de registro do aplicativo."""

    def __init__(self, page: ft.Page, controller):
        """Inicializa a tela de registro."""
        super().__init__()
        self.page = page
        self.controller = controller

        # Estado para toggle de senha
        self.password_visible = False
        self.confirm_password_visible = False

        # Campos do formulário
        self.name_field = ft.TextField(
            label="Nome completo",
            width=400,
            prefix_icon=ft.Icons.PERSON,
            border_radius=15,
            filled=True,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.TEAL_600,
            label_style=ft.TextStyle(color=ft.Colors.GREY_700),
            text_style=ft.TextStyle(size=16)
        )

        self.ra_field = ft.TextField(
            label="RA",
            width=400,
            prefix_icon=ft.Icons.BADGE,
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

        self.confirm_password_toggle = ft.IconButton(
            icon=ft.Icons.VISIBILITY_OFF,
            on_click=self.show_confirm_password_toggle,
            icon_color=ft.Colors.GREY_600,
            tooltip="Mostrar/Ocultar senha"
        )

        self.confirm_password_field = ft.TextField(
            label="Confirme a senha",
            password=True,
            width=400,
            prefix_icon=ft.Icons.LOCK,
            suffix=self.confirm_password_toggle,
            border_radius=15,
            filled=True,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_300,
            focused_border_color=ft.Colors.TEAL_600,
            label_style=ft.TextStyle(color=ft.Colors.GREY_700),
            text_style=ft.TextStyle(size=16)
        )

        # Radio buttons para role
        self.role_value = "aluno"
        self.radio_group = ft.RadioGroup(
            content=ft.Row([
                ft.Container(
                    content=ft.Row([
                        ft.Radio(value="aluno", active_color=ft.Colors.TEAL_600),
                        ft.Text("Aluno", size=16, color=ft.Colors.GREY_800)
                    ]),
                    padding=ft.padding.symmetric(horizontal=15, vertical=10),
                    border_radius=10,
                    border=ft.border.all(1, ft.Colors.GREY_300)
                ),
                ft.Container(width=20),
                ft.Container(
                    content=ft.Row([
                        ft.Radio(value="professor", active_color=ft.Colors.TEAL_600),
                        ft.Text("Professor", size=16, color=ft.Colors.GREY_800)
                    ]),
                    padding=ft.padding.symmetric(horizontal=15, vertical=10),
                    border_radius=10,
                    border=ft.border.all(1, ft.Colors.GREY_300)
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            value="aluno",
            on_change=self.on_tipo_change
        )

        # Botão de registro
        self.register_button = ft.ElevatedButton(
            "Criar Conta",
            width=400,
            height=55,
            bgcolor=ft.Colors.TEAL_600,
            color=ft.Colors.WHITE,
            on_click=self.register,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=27),
                elevation=5,
                text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
            )
        )

        # Link para login
        self.login_link = ft.TextButton(
            "Já tenho uma conta",
            on_click=self.go_to_login,
            style=ft.ButtonStyle(
                color=ft.Colors.TEAL_600,
                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_500)
            )
        )

        # Card principal de registro
        self.register_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.PERSON_ADD, size=64, color=ft.Colors.TEAL_600),
                            ft.Container(height=10),
                            ft.Text(
                                "Criar Conta", 
                                size=32, 
                                weight=ft.FontWeight.BOLD, 
                                color=ft.Colors.TEAL_600,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Text(
                                "Preencha os dados para se cadastrar", 
                                size=16, 
                                color=ft.Colors.GREY_600,
                                text_align=ft.TextAlign.CENTER
                            )
                        ], 
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=ft.padding.only(bottom=25)
                    ),
                    self.name_field,
                    ft.Container(height=15),
                    self.ra_field,
                    ft.Container(height=15),
                    self.password_field,
                    ft.Container(height=15),
                    self.confirm_password_field,
                    ft.Container(height=20),
                    ft.Text("Tipo de usuário:", size=16, color=ft.Colors.GREY_700, weight=ft.FontWeight.W_500),
                    ft.Container(height=10),
                    self.radio_group,
                    ft.Container(height=25),
                    self.register_button,
                    ft.Container(height=20),
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
                    ft.Container(height=10),
                    self.login_link
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO
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
            padding=ft.padding.all(20),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.Colors.TEAL_50, ft.Colors.WHITE]
            ),
            content=ft.Column([
                ft.Container(expand=True),
                self.register_card,
                ft.Container(expand=True)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
            )
        )

    def on_tipo_change(self, e):
        self.role_value = e.control.value

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

    def register(self, e):
        """Função executada quando o botão de registro é pressionado"""
        name = self.name_field.value
        ra = self.ra_field.value
        password = self.password_field.value
        confirm_password = self.confirm_password_field.value
        role = self.role_value

        # Validação dos campos
        if not all([name, ra, password, confirm_password]):
            self.show_snackbar("Preencha todos os campos!", ft.Colors.RED_400)
            return

        # Validação do formato do RA
        if not re.match(r'^R\d{6}$', ra):
            self.show_snackbar("RA deve ser R seguido de exatamente 6 dígitos!", ft.Colors.RED_400)
            return

        # Verificar se as senhas coincidem
        if password != confirm_password:
            self.show_snackbar("As senhas não coincidem!", ft.Colors.RED_400)
            return

        # Tentar inserir no banco
        if insert_user(name, ra, password, role):
            self.show_snackbar("Conta criada com sucesso!", ft.Colors.GREEN_600)
            # Aguardar um pouco antes de navegar
            self.page.run_task(self.delayed_navigation)
        else:
            self.show_snackbar("RA já cadastrado!", ft.Colors.RED_400)

    async def delayed_navigation(self):
        """Navega para login após um pequeno delay"""
        import asyncio
        await asyncio.sleep(1.5)
        self.go_to_login(None)

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

    def show_confirm_password_toggle(self, e):
        """Alterna a visibilidade da senha de confirmação."""
        self.confirm_password_visible = not self.confirm_password_visible
        self.confirm_password_field.password = not self.confirm_password_visible
        self.confirm_password_toggle.icon = ft.Icons.VISIBILITY if self.confirm_password_visible else ft.Icons.VISIBILITY_OFF
        self.page.update()

    def go_to_login(self, e):
        """Navega para a tela de login"""
        self.controller.show_page("Login")