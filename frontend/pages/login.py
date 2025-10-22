import flet as ft
import re
from backend.database import authenticate_user

class Login(ft.Container):
    """Classe responsável pela tela de login moderna e elegante em tela cheia."""

    def __init__(self, page: ft.Page, controller):
        """Inicializa a tela de login com design profissional mas bonito."""
        super().__init__(
            expand=True,
            width=None,
            height=None,
            padding=ft.padding.all(0),  # SEM PADDING
            margin=ft.margin.all(0)     # SEM MARGEM
        )
        self.page = page
        self.controller = controller

        # Estado para toggle de senha
        self.password_visible = False
        self.is_loading = False

        # Criar componentes
        self.create_components()
        self.setup_layout()

    def create_components(self):
        """Cria todos os componentes da interface"""
        
        # Campo RA com design elegante - MEIO TERMO IDEAL
        self.ra_field = ft.TextField(
            label="Registro Acadêmico (RA)",
            width=620,  # Meio termo: 580 → 620 (era 650)
            height=84,  # Meio termo: 80 → 84 (era 88)
            prefix_icon=ft.icons.PERSON_OUTLINE,
            max_length=7,
            on_change=self.validate_ra,
            border_radius=22,  # Meio termo: 20 → 22 (era 24)
            filled=True,
            bgcolor=ft.colors.with_opacity(0.05, ft.colors.PINK_600),
            border_color=ft.colors.with_opacity(0.2, ft.colors.PINK_600),
            focused_border_color=ft.colors.PINK_600,
            focused_bgcolor=ft.colors.WHITE,
            label_style=ft.TextStyle(
                color=ft.colors.GREY_700,
                size=19,  # Meio termo: 18 → 19 (era 20)
                weight=ft.FontWeight.W_500
            ),
            text_style=ft.TextStyle(
                size=21,  # Meio termo: 20 → 21 (era 22)
                weight=ft.FontWeight.W_500,
                color=ft.colors.GREY_900
            ),
            cursor_color=ft.colors.PINK_600,
            selection_color=ft.colors.PINK_100,
            content_padding=ft.padding.symmetric(horizontal=26, vertical=26)  # Meio termo: 24 → 26 (era 28)
        )

        # Toggle de senha
        self.password_toggle = ft.IconButton(
            icon=ft.icons.VISIBILITY_OFF_OUTLINED,
            on_click=self.show_password_toggle,
            icon_color=ft.colors.GREY_600,
            tooltip="Mostrar/Ocultar senha",
            icon_size=28,  # Meio termo: 26 → 28 (era 30)
            style=ft.ButtonStyle(
                overlay_color=ft.colors.PINK_50
            )
        )

        # Campo senha com design elegante - MEIO TERMO IDEAL
        self.password_field = ft.TextField(
            label="Senha",
            password=True,
            width=620,  # Meio termo: 580 → 620 (era 650)
            height=84,  # Meio termo: 80 → 84 (era 88)
            prefix_icon=ft.icons.LOCK_OUTLINE,
            suffix=self.password_toggle,
            border_radius=22,  # Meio termo: 20 → 22 (era 24)
            filled=True,
            bgcolor=ft.colors.with_opacity(0.05, ft.colors.PINK_600),
            border_color=ft.colors.with_opacity(0.2, ft.colors.PINK_600),
            focused_border_color=ft.colors.PINK_600,
            focused_bgcolor=ft.colors.WHITE,
            label_style=ft.TextStyle(
                color=ft.colors.GREY_700,
                size=19,  # Meio termo: 18 → 19 (era 20)
                weight=ft.FontWeight.W_500
            ),
            text_style=ft.TextStyle(
                size=21,  # Meio termo: 20 → 21 (era 22)
                weight=ft.FontWeight.W_500,
                color=ft.colors.GREY_900
            ),
            cursor_color=ft.colors.PINK_600,
            selection_color=ft.colors.PINK_100,
            content_padding=ft.padding.symmetric(horizontal=26, vertical=26)  # Meio termo: 24 → 26 (era 28)
        )

        # Indicador de loading
        self.loading_indicator = ft.ProgressRing(
            width=30,  # Meio termo: 28 → 30 (era 32)
            height=30,  # Meio termo: 28 → 30 (era 32)
            stroke_width=4.5,  # Meio termo: 4 → 4.5 (era 5)
            color=ft.colors.WHITE,
            visible=False
        )

        # Botão de login elegante - MEIO TERMO IDEAL
        self.login_button = ft.ElevatedButton(
            content=ft.Row([
                self.loading_indicator,
                ft.Text(
                    "Entrar",
                    size=24,  # Meio termo: 22 → 24 (era 26)
                    weight=ft.FontWeight.W_600,
                    color=ft.colors.WHITE
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=14  # Meio termo: 12 → 14 (era 16)
            ),
            width=620,  # Meio termo: 580 → 620 (era 650)
            height=76,  # Meio termo: 72 → 76 (era 80)
            style=ft.ButtonStyle(
                bgcolor=ft.colors.PINK_600,
                shadow_color=ft.colors.PINK_200,
                elevation=11,  # Meio termo: 10 → 11 (era 12)
                animation_duration=250,
                shape=ft.RoundedRectangleBorder(radius=22)  # Meio termo: 20 → 22 (era 24)
            ),
            on_click=self.login
        )

        # Link para registro elegante
        self.register_link = ft.TextButton(
            content=ft.Text(
                "Não tem uma conta? Criar nova conta",
                color=ft.colors.PINK_600,
                size=19,  # Meio termo: 18 → 19 (era 20)
                weight=ft.FontWeight.W_500
            ),
            on_click=self.go_to_register,
            style=ft.ButtonStyle(
                overlay_color=ft.colors.PINK_50,
                animation_duration=200
            )
        )

    def setup_layout(self):
        """Configura o layout da página para tela cheia"""
        
        # Lado esquerdo - Personagem e branding - MEIO TERMO IDEAL
        left_side = ft.Container(
            content=ft.Column([
                # Personagem com círculo elegante - MEIO TERMO IDEAL
                ft.Container(
                    content=ft.Image(
                        src="frontend/assets/personagem_1.png",
                        width=520,  # Meio termo: 480 → 520 (era 550)
                        height=520,  # Meio termo: 480 → 520 (era 550)
                        fit=ft.ImageFit.CONTAIN
                    ),
                    width=600,  # Meio termo: 560 → 600 (era 640)
                    height=600,  # Meio termo: 560 → 600 (era 640)
                    border_radius=300,  # Meio termo: 280 → 300 (era 320)
                    bgcolor=ft.colors.with_opacity(0.08, ft.colors.PINK_600),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=55,  # Meio termo: 50 → 55 (era 60)
                        color=ft.colors.with_opacity(0.19, ft.colors.PINK_600),  # Meio termo: 0.18 → 0.19 (era 0.20)
                        offset=ft.Offset(0, 22)  # Meio termo: 20 → 22 (era 25)
                    ),
                    alignment=ft.alignment.center,
                    animate=ft.animation.Animation(1000, ft.AnimationCurve.EASE_OUT)
                ),
                
                ft.Container(height=45),  # Meio termo: 40 → 45 (era 50)
                
                # Título principal elegante - MEIO TERMO IDEAL
                ft.Text(
                    "Sistema Acadêmico",
                    size=64,  # Meio termo: 60 → 64 (era 68)
                    weight=ft.FontWeight.W_700,
                    color=ft.colors.GREY_900,
                    text_align=ft.TextAlign.CENTER
                ),
                
                ft.Text(
                    "Colaborativo",
                    size=64,  # Meio termo: 60 → 64 (era 68)
                    weight=ft.FontWeight.W_700,
                    color=ft.colors.PINK_600,
                    text_align=ft.TextAlign.CENTER
                ),
                
                ft.Container(height=36),  # Meio termo: 32 → 36 (era 40)
                
                # Subtítulo profissional - MEIO TERMO IDEAL
                ft.Text(
                    "Plataforma educacional moderna\npara gestão acadêmica colaborativa",
                    size=26,  # Meio termo: 24 → 26 (era 28)
                    color=ft.colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.W_400
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER
            ),
            expand=2,  # 40% da largura
            padding=ft.padding.symmetric(horizontal=70, vertical=45)  # Meio termo: 60,40 → 70,45 (era 80,50)
        )
        
        # Lado direito - Formulário elegante - MEIO TERMO IDEAL
        right_side = ft.Container(
            content=ft.Container(
                content=ft.Column([
                    # Cabeçalho do formulário - MEIO TERMO IDEAL
                    ft.Container(
                        content=ft.Icon(
                            ft.icons.LOGIN_ROUNDED,
                            size=90,  # Meio termo: 80 → 90 (era 100)
                            color=ft.colors.PINK_600
                        ),
                        width=145,  # Meio termo: 130 → 145 (era 160)
                        height=145,  # Meio termo: 130 → 145 (era 160)
                        border_radius=72,  # Meio termo: 65 → 72 (era 80)
                        bgcolor=ft.colors.PINK_50,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(height=40),  # Meio termo: 36 → 40 (era 44)
                    ft.Text(
                        "Bem-vindo de volta!",
                        size=46,  # Meio termo: 42 → 46 (era 50)
                        weight=ft.FontWeight.W_700,
                        color=ft.colors.GREY_900,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=18),  # Meio termo: 16 → 18 (era 20)
                    ft.Text(
                        "Faça login para acessar sua conta",
                        size=24,  # Meio termo: 22 → 24 (era 26)
                        color=ft.colors.GREY_600,
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.W_400
                    ),
                    ft.Container(height=65),  # Meio termo: 60 → 65 (era 70)

                    # Campos do formulário
                    self.ra_field,
                    ft.Container(height=33),  # Meio termo: 30 → 33 (era 36)
                    self.password_field,
                    ft.Container(height=44),  # Meio termo: 40 → 44 (era 48)
                    self.login_button,
                    ft.Container(height=40),  # Meio termo: 36 → 40 (era 44)

                    # Divider elegante
                    ft.Container(
                        content=ft.Row([
                            ft.Container(
                                content=ft.Divider(color=ft.colors.with_opacity(0.3, ft.colors.PINK_600), thickness=1),
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Text(
                                    "ou",
                                    color=ft.colors.GREY_500,
                                    size=19,  # Meio termo: 18 → 19 (era 20)
                                    weight=ft.FontWeight.W_500
                                ),
                                padding=ft.padding.symmetric(horizontal=26)  # Meio termo: 24 → 26 (era 28)
                            ),
                            ft.Container(
                                content=ft.Divider(color=ft.colors.with_opacity(0.3, ft.colors.PINK_600), thickness=1),
                                expand=True
                            )
                        ]),
                        margin=ft.margin.symmetric(vertical=22)  # Meio termo: 20 → 22 (era 24)
                    ),

                    self.register_link
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO
                ),
                padding=ft.padding.all(65),  # Meio termo: 60 → 65 (era 70)
                bgcolor=ft.colors.WHITE,
                border_radius=30,  # Meio termo: 28 → 30 (era 32)
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=65,  # Meio termo: 60 → 65 (era 70)
                    color=ft.colors.with_opacity(0.16, ft.colors.BLACK),  # Meio termo: 0.15 → 0.16 (era 0.18)
                    offset=ft.Offset(-5.5, 11)  # Meio termo: -5,10 → -5.5,11 (era -6,12)
                ),
                border=ft.border.all(1, ft.colors.with_opacity(0.1, ft.colors.PINK_600)),
                width=825  # Meio termo: 750 → 825 (era 900)
            ),
            expand=False,  # Largura fixa
            width=925,  # Meio termo: 850 → 925 (era 1000)
            padding=ft.padding.symmetric(horizontal=65, vertical=42)  # Meio termo: 60,40 → 65,42 (era 70,50)
        )

        # Container principal - OCUPAR 100% DA TELA SEM MARGENS
        main_container = ft.Container(
            content=ft.Row([
                left_side,
                right_side
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True
            ),
            expand=True,
            padding=ft.padding.all(0),  # ZERO PADDING
            margin=ft.margin.all(0),   # ZERO MARGEM
            width=None,  # 100% da largura
            height=None  # 100% da altura
        )

        # Layout principal com gradiente elegante - OCUPAR 100% DA TELA
        self.content = ft.Container(
            content=main_container,
            expand=True,
            width=None,  # 100% da largura
            height=None,  # 100% da altura
            padding=ft.padding.all(0),  # ZERO PADDING
            margin=ft.margin.all(0),   # ZERO MARGEM
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[
                    ft.colors.with_opacity(0.11, ft.colors.PINK_600),   # Meio termo: 0.10 → 0.11 (era 0.12)
                    ft.colors.WHITE,
                    ft.colors.with_opacity(0.09, ft.colors.PURPLE_600)  # Meio termo: 0.08 → 0.09 (era 0.10)
                ]
            )
        )

    def validate_ra(self, e):
        """Valida e formata o input do RA em tempo real."""
        value = e.control.value.upper()
        cleaned = ''.join(c for c in value if c.isdigit() or c == 'R')
        
        if not cleaned.startswith('R'):
            cleaned = 'R' + ''.join(c for c in cleaned if c.isdigit())
        
        if cleaned.count('R') > 1:
            cleaned = 'R' + ''.join(c for c in cleaned[1:] if c.isdigit())
        
        cleaned = cleaned[:7]
        self.ra_field.value = cleaned
        
        # Feedback visual elegante
        if len(cleaned) == 7 and re.match(r'^R\d{6}$', cleaned):
            self.ra_field.border_color = ft.colors.GREEN_500
            self.ra_field.focused_border_color = ft.colors.GREEN_500
        else:
            self.ra_field.border_color = ft.colors.with_opacity(0.2, ft.colors.PINK_600)
            self.ra_field.focused_border_color = ft.colors.PINK_600
            
        if self.page:
            self.page.update()

    def login(self, e):
        """Executa o login com animações elegantes"""
        if self.is_loading:
            return
            
        ra = self.ra_field.value
        password = self.password_field.value

        # Validação básica
        if not ra or not password:
            self.show_snackbar("Preencha todos os campos!", "error")
            return

        # Validação do formato do RA
        if not re.match(r'^R\d{6}$', ra):
            self.show_snackbar("RA deve ser R seguido de exatamente 6 dígitos!", "error")
            return

        # Iniciar loading
        self.start_loading()

        try:
            user = authenticate_user(ra, password)
            if user:
                self.controller.current_user = user
                self.show_snackbar("Login realizado com sucesso!", "success")
                
                # Navegar após sucesso
                if user['role'] == 'professor':
                    self.controller.show_page("DashboardProfessor")
                else:
                    self.controller.show_page("DashboardAluno")
            else:
                self.show_snackbar("RA ou senha incorretos!", "error")
        except Exception as ex:
            self.show_snackbar(f"Erro ao fazer login: {str(ex)}", "error")

        self.stop_loading()

    def start_loading(self):
        """Inicia estado de loading"""
        self.is_loading = True
        self.loading_indicator.visible = True
        self.login_button.style.bgcolor = ft.colors.with_opacity(0.7, ft.colors.PINK_600)
        if self.page:
            self.page.update()

    def stop_loading(self):
        """Para estado de loading"""
        self.is_loading = False
        self.loading_indicator.visible = False
        self.login_button.style.bgcolor = ft.colors.PINK_600
        if self.page:
            self.page.update()

    def show_snackbar(self, message, type):
        """Exibe snackbar elegante"""
        self.controller.show_snackbar(message, type)

    def show_password_toggle(self, e):
        """Alterna visibilidade da senha"""
        self.password_visible = not self.password_visible
        self.password_field.password = not self.password_visible
        self.password_toggle.icon = (
            ft.icons.VISIBILITY_OUTLINED if self.password_visible 
            else ft.icons.VISIBILITY_OFF_OUTLINED
        )
        if self.page:
            self.page.update()

    def go_to_register(self, e):
        """Navega para tela de registro"""
        self.controller.show_page("Register")