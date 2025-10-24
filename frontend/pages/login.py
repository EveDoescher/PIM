import flet as ft
import re
from backend.database import authenticate_user

class Login(ft.Container):

    def __init__(self, page: ft.Page, controller):
        # Inicializa a interface de login com configurações básicas
        super().__init__(
            expand=True,
            width=None,
            height=None,
            padding=ft.padding.all(0),
            margin=ft.margin.all(0)
        )
        self.page = page
        self.controller = controller

        self.password_visible = False
        self.is_loading = False

        self.create_components()
        self.setup_layout()

    def create_components(self):
        # Cria todos os componentes visuais da tela de login
        
        self.ra_field = ft.TextField(
            label="Registro Acadêmico (RA)",
            width=620,
            height=84,
            prefix_icon=ft.icons.PERSON_OUTLINE,
            max_length=7,
            on_change=self.validate_ra,
            border_radius=22,
            filled=True,
            bgcolor=ft.colors.with_opacity(0.05, ft.colors.PINK_600),
            border_color=ft.colors.with_opacity(0.2, ft.colors.PINK_600),
            focused_border_color=ft.colors.PINK_600,
            focused_bgcolor=ft.colors.WHITE,
            label_style=ft.TextStyle(
                color=ft.colors.GREY_700,
                size=19,
                weight=ft.FontWeight.W_500
            ),
            text_style=ft.TextStyle(
                size=21,
                weight=ft.FontWeight.W_500,
                color=ft.colors.GREY_900
            ),
            cursor_color=ft.colors.PINK_600,
            selection_color=ft.colors.PINK_100,
            content_padding=ft.padding.symmetric(horizontal=26, vertical=26)
        )

        self.password_toggle = ft.IconButton(
            icon=ft.icons.VISIBILITY_OFF_OUTLINED,
            on_click=self.show_password_toggle,
            icon_color=ft.colors.GREY_600,
            tooltip="Mostrar/Ocultar senha",
            icon_size=28,
            style=ft.ButtonStyle(
                overlay_color=ft.colors.PINK_50
            )
        )

        self.password_field = ft.TextField(
            label="Senha",
            password=True,
            width=620,
            height=84,
            prefix_icon=ft.icons.LOCK_OUTLINE,
            suffix=self.password_toggle,
            border_radius=22,
            filled=True,
            bgcolor=ft.colors.with_opacity(0.05, ft.colors.PINK_600),
            border_color=ft.colors.with_opacity(0.2, ft.colors.PINK_600),
            focused_border_color=ft.colors.PINK_600,
            focused_bgcolor=ft.colors.WHITE,
            label_style=ft.TextStyle(
                color=ft.colors.GREY_700,
                size=19,
                weight=ft.FontWeight.W_500
            ),
            text_style=ft.TextStyle(
                size=21,
                weight=ft.FontWeight.W_500,
                color=ft.colors.GREY_900
            ),
            cursor_color=ft.colors.PINK_600,
            selection_color=ft.colors.PINK_100,
            content_padding=ft.padding.symmetric(horizontal=26, vertical=26)
        )

        self.loading_indicator = ft.ProgressRing(
            width=30,
            height=30,
            stroke_width=4.5,
            color=ft.colors.WHITE,
            visible=False
        )

        self.login_button = ft.ElevatedButton(
            content=ft.Row([
                self.loading_indicator,
                ft.Text(
                    "Entrar",
                    size=24,
                    weight=ft.FontWeight.W_600,
                    color=ft.colors.WHITE
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=14
            ),
            width=620,
            height=76,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.PINK_600,
                shadow_color=ft.colors.PINK_200,
                elevation=11,
                animation_duration=250,
                shape=ft.RoundedRectangleBorder(radius=22)
            ),
            on_click=self.login
        )

        self.register_link = ft.TextButton(
            content=ft.Text(
                "Não tem uma conta? Criar nova conta",
                color=ft.colors.PINK_600,
                size=19,
                weight=ft.FontWeight.W_500
            ),
            on_click=self.go_to_register,
            style=ft.ButtonStyle(
                overlay_color=ft.colors.PINK_50,
                animation_duration=200
            )
        )

    def setup_layout(self):
        # Organiza o layout da página em duas colunas principais
        
        left_side = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Image(
                        src="frontend/assets/personagem_1.png",
                        width=520,
                        height=520,
                        fit=ft.ImageFit.CONTAIN
                    ),
                    width=600,
                    height=600,
                    border_radius=300,
                    bgcolor=ft.colors.with_opacity(0.08, ft.colors.PINK_600),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=55,
                        color=ft.colors.with_opacity(0.19, ft.colors.PINK_600),
                        offset=ft.Offset(0, 22)
                    ),
                    alignment=ft.alignment.center,
                    animate=ft.animation.Animation(1000, ft.AnimationCurve.EASE_OUT)
                ),
                
                ft.Container(height=45),
                
                ft.Text(
                    "Sistema Acadêmico",
                    size=64,
                    weight=ft.FontWeight.W_700,
                    color=ft.colors.GREY_900,
                    text_align=ft.TextAlign.CENTER
                ),
                
                ft.Text(
                    "Colaborativo",
                    size=64,
                    weight=ft.FontWeight.W_700,
                    color=ft.colors.PINK_600,
                    text_align=ft.TextAlign.CENTER
                ),
                
                ft.Container(height=36),
                
                ft.Text(
                    "Plataforma educacional moderna\npara gestão acadêmica colaborativa",
                    size=26,
                    color=ft.colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.W_400
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER
            ),
            expand=2,
            padding=ft.padding.symmetric(horizontal=70, vertical=45)
        )
        
        right_side = ft.Container(
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon(
                            ft.icons.LOGIN_ROUNDED,
                            size=90,
                            color=ft.colors.PINK_600
                        ),
                        width=145,
                        height=145,
                        border_radius=72,
                        bgcolor=ft.colors.PINK_50,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(height=40),
                    ft.Text(
                        "Bem-vindo de volta!",
                        size=46,
                        weight=ft.FontWeight.W_700,
                        color=ft.colors.GREY_900,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=18),
                    ft.Text(
                        "Faça login para acessar sua conta",
                        size=24,
                        color=ft.colors.GREY_600,
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.W_400
                    ),
                    ft.Container(height=65),

                    self.ra_field,
                    ft.Container(height=33),
                    self.password_field,
                    ft.Container(height=44),
                    self.login_button,
                    ft.Container(height=40),

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
                                    size=19,
                                    weight=ft.FontWeight.W_500
                                ),
                                padding=ft.padding.symmetric(horizontal=26)
                            ),
                            ft.Container(
                                content=ft.Divider(color=ft.colors.with_opacity(0.3, ft.colors.PINK_600), thickness=1),
                                expand=True
                            )
                        ]),
                        margin=ft.margin.symmetric(vertical=22)
                    ),

                    self.register_link
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO
                ),
                padding=ft.padding.all(65),
                bgcolor=ft.colors.WHITE,
                border_radius=30,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=65,
                    color=ft.colors.with_opacity(0.16, ft.colors.BLACK),
                    offset=ft.Offset(-5.5, 11)
                ),
                border=ft.border.all(1, ft.colors.with_opacity(0.1, ft.colors.PINK_600)),
                width=825
            ),
            expand=False,
            width=925,
            padding=ft.padding.symmetric(horizontal=65, vertical=42)
        )

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
            padding=ft.padding.all(0),
            margin=ft.margin.all(0),
            width=None,
            height=None
        )

        self.content = ft.Container(
            content=main_container,
            expand=True,
            width=None,
            height=None,
            padding=ft.padding.all(0),
            margin=ft.margin.all(0),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[
                    ft.colors.with_opacity(0.11, ft.colors.PINK_600),
                    ft.colors.WHITE,
                    ft.colors.with_opacity(0.09, ft.colors.PURPLE_600)
                ]
            )
        )

    def validate_ra(self, e):
        # Valida e formata o RA em tempo real
        value = e.control.value.upper()
        cleaned = ''.join(c for c in value if c.isdigit() or c == 'R')
        
        if not cleaned.startswith('R'):
            cleaned = 'R' + ''.join(c for c in cleaned if c.isdigit())
        
        if cleaned.count('R') > 1:
            cleaned = 'R' + ''.join(c for c in cleaned[1:] if c.isdigit())
        
        cleaned = cleaned[:7]
        self.ra_field.value = cleaned
        
        if len(cleaned) == 7 and re.match(r'^R\d{6}$', cleaned):
            self.ra_field.border_color = ft.colors.GREEN_500
            self.ra_field.focused_border_color = ft.colors.GREEN_500
        else:
            self.ra_field.border_color = ft.colors.with_opacity(0.2, ft.colors.PINK_600)
            self.ra_field.focused_border_color = ft.colors.PINK_600
            
        if self.page:
            self.page.update()

    def login(self, e):
        # Processa o login do usuário
        if self.is_loading:
            return
            
        ra = self.ra_field.value
        password = self.password_field.value

        if not ra or not password:
            self.show_snackbar("Preencha todos os campos!", "error")
            return

        if not re.match(r'^R\d{6}$', ra):
            self.show_snackbar("RA deve ser R seguido de exatamente 6 dígitos!", "error")
            return

        self.start_loading()

        try:
            user = authenticate_user(ra, password)
            if user:
                self.controller.current_user = user
                self.show_snackbar("Login realizado com sucesso!", "success")
                
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
        # Ativa o estado de carregamento
        self.is_loading = True
        self.loading_indicator.visible = True
        self.login_button.style.bgcolor = ft.colors.with_opacity(0.7, ft.colors.PINK_600)
        if self.page:
            self.page.update()

    def stop_loading(self):
        # Desativa o estado de carregamento
        self.is_loading = False
        self.loading_indicator.visible = False
        self.login_button.style.bgcolor = ft.colors.PINK_600
        if self.page:
            self.page.update()

    def show_snackbar(self, message, type):
        # Exibe mensagens de feedback para o usuário
        self.controller.show_snackbar(message, type)

    def show_password_toggle(self, e):
        # Alterna a visibilidade da senha
        self.password_visible = not self.password_visible
        self.password_field.password = not self.password_visible
        self.password_toggle.icon = (
            ft.icons.VISIBILITY_OUTLINED if self.password_visible 
            else ft.icons.VISIBILITY_OFF_OUTLINED
        )
        if self.page:
            self.page.update()

    def go_to_register(self, e):
        # Navega para a tela de registro
        self.controller.show_page("Register")