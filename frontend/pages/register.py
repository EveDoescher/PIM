import flet as ft
import re
from backend.database import insert_user, get_user_id

class Register(ft.Container):
    """Classe responsável pela tela de registro moderna e elegante."""

    def __init__(self, page: ft.Page, controller):
        """Inicializa a tela de registro com design profissional mas bonito."""
        super().__init__(
            expand=True,
            width=None,
            height=None,
            padding=ft.padding.all(0),  # SEM PADDING
            margin=ft.margin.all(0)     # SEM MARGEM
        )
        self.page = page
        self.controller = controller
        
        self.is_loading = False
        self.password_visible = False
        self.confirm_password_visible = False
        
        self.create_components()
        self.setup_layout()

    def create_components(self):
        """Cria todos os componentes da interface"""
        
        # Campo nome completo - TAMANHO AJUSTADO
        self.name_field = ft.TextField(
            label="Nome Completo",
            width=380,  # Aumentado de 350 para 380
            height=58,  # Aumentado de 55 para 58
            prefix_icon=ft.icons.PERSON_OUTLINE,
            border_radius=14,  # Aumentado de 12 para 14
            filled=True,
            bgcolor=ft.colors.with_opacity(0.7, ft.colors.PURPLE_50),
            border_color=ft.colors.with_opacity(0.3, ft.colors.PURPLE_300),
            focused_border_color=ft.colors.PURPLE_500,
            focused_bgcolor=ft.colors.WHITE,
            label_style=ft.TextStyle(
                color=ft.colors.PURPLE_700,
                size=14,  # Aumentado de 13 para 14
                weight=ft.FontWeight.W_500
            ),
            text_style=ft.TextStyle(
                size=15,  # Aumentado de 14 para 15
                weight=ft.FontWeight.W_500,
                color=ft.colors.GREY_800
            ),
            cursor_color=ft.colors.PURPLE_600,
            content_padding=ft.padding.symmetric(horizontal=18, vertical=18)  # Aumentado de 16 para 18
        )

        # Campo RA - TAMANHO AJUSTADO
        self.ra_field = ft.TextField(
            label="Registro Acadêmico (RA)",
            width=380,  # Aumentado de 350 para 380
            height=58,  # Aumentado de 55 para 58
            prefix_icon=ft.icons.BADGE_OUTLINED,
            max_length=7,
            on_change=self.validate_ra,
            border_radius=14,  # Aumentado de 12 para 14
            filled=True,
            bgcolor=ft.colors.with_opacity(0.7, ft.colors.PURPLE_50),
            border_color=ft.colors.with_opacity(0.3, ft.colors.PURPLE_300),
            focused_border_color=ft.colors.PURPLE_500,
            focused_bgcolor=ft.colors.WHITE,
            label_style=ft.TextStyle(
                color=ft.colors.PURPLE_700,
                size=14,  # Aumentado de 13 para 14
                weight=ft.FontWeight.W_500
            ),
            text_style=ft.TextStyle(
                size=15,  # Aumentado de 14 para 15
                weight=ft.FontWeight.W_500,
                color=ft.colors.GREY_800
            ),
            cursor_color=ft.colors.PURPLE_600,
            content_padding=ft.padding.symmetric(horizontal=18, vertical=18)  # Aumentado de 16 para 18
        )

        # Toggles de senha - TAMANHO AJUSTADO
        self.password_toggle = ft.IconButton(
            icon=ft.icons.VISIBILITY_OFF_OUTLINED,
            on_click=self.toggle_password,
            icon_color=ft.colors.PURPLE_600,
            icon_size=20  # Aumentado de 18 para 20
        )

        self.confirm_password_toggle = ft.IconButton(
            icon=ft.icons.VISIBILITY_OFF_OUTLINED,
            on_click=self.toggle_confirm_password,
            icon_color=ft.colors.PURPLE_600,
            icon_size=20  # Aumentado de 18 para 20
        )

        # Campo senha - TAMANHO AJUSTADO
        self.password_field = ft.TextField(
            label="Senha",
            password=True,
            width=380,  # Aumentado de 350 para 380
            height=58,  # Aumentado de 55 para 58
            prefix_icon=ft.icons.LOCK_OUTLINE,
            suffix=self.password_toggle,
            border_radius=14,  # Aumentado de 12 para 14
            filled=True,
            bgcolor=ft.colors.with_opacity(0.7, ft.colors.PURPLE_50),
            border_color=ft.colors.with_opacity(0.3, ft.colors.PURPLE_300),
            focused_border_color=ft.colors.PURPLE_500,
            focused_bgcolor=ft.colors.WHITE,
            label_style=ft.TextStyle(
                color=ft.colors.PURPLE_700,
                size=14,  # Aumentado de 13 para 14
                weight=ft.FontWeight.W_500
            ),
            text_style=ft.TextStyle(
                size=15,  # Aumentado de 14 para 15
                weight=ft.FontWeight.W_500,
                color=ft.colors.GREY_800
            ),
            cursor_color=ft.colors.PURPLE_600,
            content_padding=ft.padding.symmetric(horizontal=18, vertical=18)  # Aumentado de 16 para 18
        )

        # Campo confirmar senha - TAMANHO AJUSTADO
        self.confirm_password_field = ft.TextField(
            label="Confirmar Senha",
            password=True,
            width=380,  # Aumentado de 350 para 380
            height=58,  # Aumentado de 55 para 58
            prefix_icon=ft.icons.LOCK_OUTLINE,
            suffix=self.confirm_password_toggle,
            border_radius=14,  # Aumentado de 12 para 14
            filled=True,
            bgcolor=ft.colors.with_opacity(0.7, ft.colors.PURPLE_50),
            border_color=ft.colors.with_opacity(0.3, ft.colors.PURPLE_300),
            focused_border_color=ft.colors.PURPLE_500,
            focused_bgcolor=ft.colors.WHITE,
            label_style=ft.TextStyle(
                color=ft.colors.PURPLE_700,
                size=14,  # Aumentado de 13 para 14
                weight=ft.FontWeight.W_500
            ),
            text_style=ft.TextStyle(
                size=15,  # Aumentado de 14 para 15
                weight=ft.FontWeight.W_500,
                color=ft.colors.GREY_800
            ),
            cursor_color=ft.colors.PURPLE_600,
            content_padding=ft.padding.symmetric(horizontal=18, vertical=18)  # Aumentado de 16 para 18
        )

        self.selected_role = "aluno"  # Padrão

        # Botões de seleção de tipo de usuário - TAMANHO AJUSTADO
        self.professor_button = self.create_role_button("professor", "Professor", ft.icons.SCHOOL_OUTLINED)
        self.aluno_button = self.create_role_button("aluno", "Aluno", ft.icons.PERSON_OUTLINE)

        # Seletor de tipo de usuário - TAMANHO AJUSTADO
        self.role_selector = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Tipo de Usuário",
                    size=15,  # Aumentado de 14 para 15
                    weight=ft.FontWeight.W_600,
                    color=ft.colors.PURPLE_700
                ),
                ft.Container(height=14),  # Aumentado de 12 para 14
                ft.Row([
                    self.professor_button,
                    ft.Container(width=20),  # Aumentado de 16 para 20
                    self.aluno_button
                ], alignment=ft.MainAxisAlignment.CENTER)
            ]),
            width=380  # Aumentado de 350 para 380
        )

        # Loading indicator - TAMANHO AJUSTADO
        self.loading_indicator = ft.ProgressRing(
            width=20,  # Aumentado de 18 para 20
            height=20,  # Aumentado de 18 para 20
            stroke_width=2.5,  # Aumentado de 2 para 2.5
            color=ft.colors.WHITE,
            visible=False
        )

        # Botão de registro - TAMANHO AJUSTADO
        self.register_button = ft.ElevatedButton(
            content=ft.Row([
                self.loading_indicator,
                ft.Text(
                    "Criar Conta",
                    size=15,  # Aumentado de 14 para 15
                    weight=ft.FontWeight.W_600,
                    color=ft.colors.WHITE
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8  # Aumentado de 6 para 8
            ),
            width=380,  # Aumentado de 350 para 380
            height=50,  # Aumentado de 46 para 50
            style=ft.ButtonStyle(
                bgcolor=ft.colors.PURPLE_600,
                shadow_color=ft.colors.PURPLE_300,
                elevation=6,  # Aumentado de 5 para 6
                animation_duration=250,
                shape=ft.RoundedRectangleBorder(radius=14)  # Aumentado de 12 para 14
            ),
            on_click=self.register
        )

        # Link para login - TAMANHO AJUSTADO
        self.login_link = ft.TextButton(
            content=ft.Text(
                "Já tem uma conta? Fazer login",
                color=ft.colors.PINK_600,
                size=14,  # Aumentado de 13 para 14
                weight=ft.FontWeight.W_500
            ),
            on_click=self.go_to_login,
            style=ft.ButtonStyle(
                overlay_color=ft.colors.PINK_50,
                animation_duration=200
            )
        )

    def create_role_button(self, value, label, icon):
        """Cria botão de opção de tipo de usuário elegante - TAMANHO AJUSTADO"""
        is_selected = self.selected_role == value

        return ft.ElevatedButton(
            content=ft.Column([
                ft.Icon(
                    icon,
                    size=32,  # Aumentado de 28 para 32
                    color=ft.colors.WHITE if is_selected else ft.colors.PURPLE_600
                ),
                ft.Container(height=8),  # Aumentado de 6 para 8
                ft.Text(
                    label,
                    size=13,  # Aumentado de 12 para 13
                    weight=ft.FontWeight.W_600,
                    color=ft.colors.WHITE if is_selected else ft.colors.PURPLE_700
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, spacing=0),
            width=120,  # Aumentado de 110 para 120
            height=95,  # Aumentado de 85 para 95
            style=ft.ButtonStyle(
                bgcolor=ft.colors.PINK_600 if is_selected else ft.colors.WHITE,
                shadow_color=ft.colors.PINK_300 if is_selected else ft.colors.with_opacity(0.1, ft.colors.BLACK),
                elevation=6 if is_selected else 2,  # Aumentado de 5,2 para 6,2
                animation_duration=200,
                shape=ft.RoundedRectangleBorder(radius=14),  # Aumentado de 12 para 14
                side=ft.BorderSide(
                    2,
                    ft.colors.PINK_600 if is_selected else ft.colors.PURPLE_300
                )
            ),
            on_click=lambda e, role=value: self.select_role(role)
        )

    def setup_layout(self):
        """Configura o layout da página"""
        
        # Lado esquerdo - Personagem e branding - AUMENTAR ELEMENTOS
        left_side = ft.Container(
            content=ft.Column([
                # Personagem com design mais refinado - AUMENTADO
                ft.Container(
                    content=ft.Image(
                        src="frontend/assets/personagem_2.png",
                        width=480,  # Aumentado de 350 para 480
                        height=480,  # Aumentado de 350 para 480
                        fit=ft.ImageFit.CONTAIN
                    ),
                    width=540,  # Aumentado de 380 para 540
                    height=540,  # Aumentado de 380 para 540
                    border_radius=270,  # Aumentado de 190 para 270
                    bgcolor=ft.colors.with_opacity(0.1, ft.colors.PURPLE_100),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=55,  # Aumentado de 40 para 55
                        color=ft.colors.with_opacity(0.22, ft.colors.PURPLE_400),  # Aumentado opacidade
                        offset=ft.Offset(0, 20)  # Aumentado de 15 para 20
                    ),
                    alignment=ft.alignment.center,
                    animate=ft.animation.Animation(1000, ft.AnimationCurve.EASE_OUT)
                ),
                
                ft.Container(height=45),  # Aumentado de 32 para 45
                
                # Título principal elegante - AUMENTADO
                ft.Text(
                    "Junte-se a Nós!",
                    size=58,  # Aumentado de 42 para 58
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.GREY_800,
                    text_align=ft.TextAlign.CENTER
                ),
                
                ft.Container(height=24),  # Aumentado de 16 para 24
                
                # Subtítulo refinado - AUMENTADO
                ft.Text(
                    "Crie sua conta e comece sua jornada\nno sistema acadêmico mais avançado",
                    size=26,  # Aumentado de 18 para 26
                    color=ft.colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.W_400
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER
            ),
            expand=True,
            padding=ft.padding.symmetric(horizontal=60, vertical=40)  # Aumentado de 20,0 para 60,40
        )
        
        # Lado direito - Formulário elegante com scroll - TAMANHO AJUSTADO COM MARGENS MANTIDAS
        right_side = ft.Container(
            content=ft.Column([
                # Cabeçalho do formulário - TAMANHO AJUSTADO
                ft.Container(
                    content=ft.Column([
                        # Ícone mais elegante - TAMANHO AJUSTADO
                        ft.Container(
                            content=ft.Icon(
                                ft.icons.PERSON_ADD_OUTLINED,
                                size=65,  # Aumentado de 60 para 65
                                color=ft.colors.PURPLE_600
                            ),
                            width=110,  # Aumentado de 100 para 110
                            height=110,  # Aumentado de 100 para 110
                            border_radius=55,  # Aumentado de 50 para 55
                            bgcolor=ft.colors.with_opacity(0.1, ft.colors.PURPLE_100),
                            alignment=ft.alignment.center
                        ),
                        ft.Container(height=24),  # Aumentado de 20 para 24
                        ft.Text(
                            "Criar Nova Conta",
                            size=32,  # Aumentado de 28 para 32
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.GREY_800,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=10),  # Aumentado de 8 para 10
                        ft.Text(
                            "Preencha os dados para se cadastrar",
                            size=17,  # Aumentado de 16 para 17
                            color=ft.colors.GREY_600,
                            text_align=ft.TextAlign.CENTER,
                            weight=ft.FontWeight.W_400
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.only(bottom=24)  # Aumentado de 20 para 24
                ),

                # Container com scroll para os campos do formulário - TAMANHO AJUSTADO
                ft.Container(
                    content=ft.Column([
                        self.name_field,
                        ft.Container(height=14),  # Aumentado de 12 para 14
                        self.ra_field,
                        ft.Container(height=14),  # Aumentado de 12 para 14
                        self.password_field,
                        ft.Container(height=14),  # Aumentado de 12 para 14
                        self.confirm_password_field,
                        ft.Container(height=18),  # Aumentado de 16 para 18
                        self.role_selector,
                        ft.Container(height=24),  # Aumentado de 20 para 24
                        self.register_button,
                        ft.Container(height=18),  # Aumentado de 16 para 18

                        # Divider elegante - TAMANHO AJUSTADO
                        ft.Container(
                            content=ft.Row([
                                ft.Container(
                                    content=ft.Divider(color=ft.colors.with_opacity(0.3, ft.colors.PURPLE_300), thickness=1),
                                    expand=True
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        "ou",
                                        color=ft.colors.PURPLE_500,
                                        size=14,  # Aumentado de 13 para 14
                                        weight=ft.FontWeight.W_500
                                    ),
                                    padding=ft.padding.symmetric(horizontal=18)  # Aumentado de 16 para 18
                                ),
                                ft.Container(
                                    content=ft.Divider(color=ft.colors.with_opacity(0.3, ft.colors.PURPLE_300), thickness=1),
                                    expand=True
                                )
                            ]),
                            margin=ft.margin.symmetric(vertical=14)  # Aumentado de 12 para 14
                        ),

                        self.login_link,
                        ft.Container(height=24)  # Aumentado de 20 para 24
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                    scroll=ft.ScrollMode.AUTO
                    ),
                    expand=True
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
            ),
            width=450,  # Aumentado de 420 para 450
            padding=ft.padding.symmetric(horizontal=25, vertical=18),  # Aumentado de 20,15 para 25,18
            bgcolor=ft.colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=45,  # Aumentado de 40 para 45
                color=ft.colors.with_opacity(0.10, ft.colors.BLACK),  # Aumentado opacidade
                offset=ft.Offset(-6, 0)  # Aumentado de -5 para -6
            ),
            border_radius=20  # Aumentado de 18 para 20
        )

        # Container principal - COM MARGENS PARA FLUTUAÇÃO (MANTIDAS)
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
            # MARGENS MANTIDAS CONFORME APROVADO
            padding=ft.padding.only(
                top=30,     # Margem superior
                bottom=30,  # Margem inferior
                left=20,    # Margem esquerda menor
                right=80    # Margem direita MAIOR que as outras
            ),
            margin=ft.margin.all(0),
            width=None,  # 100% da largura
            height=None  # 100% da altura
        )

        # Layout principal com gradiente refinado - OCUPAR 100% DA TELA
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
                    ft.colors.with_opacity(0.8, ft.colors.PURPLE_50),
                    ft.colors.with_opacity(0.6, ft.colors.PINK_50),
                    ft.colors.WHITE
                ]
            )
        )

    def validate_ra(self, e):
        """Valida formato do RA"""
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
        else:
            self.ra_field.border_color = ft.colors.with_opacity(0.3, ft.colors.PURPLE_300)
            
        if self.page:
            self.page.update()

    def select_role(self, role):
        """Seleciona tipo de usuário"""
        self.selected_role = role
        
        # Atualizar estilos dos botões de forma elegante
        self.professor_button.style.bgcolor = ft.colors.PINK_600 if role == "professor" else ft.colors.WHITE
        self.professor_button.style.shadow_color = ft.colors.PINK_300 if role == "professor" else ft.colors.with_opacity(0.1, ft.colors.BLACK)
        self.professor_button.style.elevation = 6 if role == "professor" else 2  # Ajustado para novo tamanho
        self.professor_button.style.side = ft.BorderSide(2, ft.colors.PINK_600 if role == "professor" else ft.colors.PURPLE_300)
        self.professor_button.content.controls[0].color = ft.colors.WHITE if role == "professor" else ft.colors.PURPLE_600
        self.professor_button.content.controls[2].color = ft.colors.WHITE if role == "professor" else ft.colors.PURPLE_700

        self.aluno_button.style.bgcolor = ft.colors.PINK_600 if role == "aluno" else ft.colors.WHITE
        self.aluno_button.style.shadow_color = ft.colors.PINK_300 if role == "aluno" else ft.colors.with_opacity(0.1, ft.colors.BLACK)
        self.aluno_button.style.elevation = 6 if role == "aluno" else 2  # Ajustado para novo tamanho
        self.aluno_button.style.side = ft.BorderSide(2, ft.colors.PINK_600 if role == "aluno" else ft.colors.PURPLE_300)
        self.aluno_button.content.controls[0].color = ft.colors.WHITE if role == "aluno" else ft.colors.PURPLE_600
        self.aluno_button.content.controls[2].color = ft.colors.WHITE if role == "aluno" else ft.colors.PURPLE_700

        if self.page:
            self.page.update()

    def toggle_password(self, e):
        """Toggle visibilidade senha"""
        self.password_visible = not self.password_visible
        self.password_field.password = not self.password_visible
        self.password_toggle.icon = (
            ft.icons.VISIBILITY_OUTLINED if self.password_visible 
            else ft.icons.VISIBILITY_OFF_OUTLINED
        )
        if self.page:
            self.page.update()

    def toggle_confirm_password(self, e):
        """Toggle visibilidade confirmar senha"""
        self.confirm_password_visible = not self.confirm_password_visible
        self.confirm_password_field.password = not self.confirm_password_visible
        self.confirm_password_toggle.icon = (
            ft.icons.VISIBILITY_OUTLINED if self.confirm_password_visible 
            else ft.icons.VISIBILITY_OFF_OUTLINED
        )
        if self.page:
            self.page.update()

    def register(self, e):
        """Executa registro do usuário"""
        if self.is_loading:
            return

        # Validações
        name = self.name_field.value.strip() if self.name_field.value else ""
        ra = self.ra_field.value.strip() if self.ra_field.value else ""
        password = self.password_field.value if self.password_field.value else ""
        confirm_password = self.confirm_password_field.value if self.confirm_password_field.value else ""

        if not all([name, ra, password, confirm_password]):
            self.controller.show_snackbar("Preencha todos os campos!", "error")
            return

        if not re.match(r'^R\d{6}$', ra):
            self.controller.show_snackbar("RA deve ter formato R seguido de 6 dígitos!", "error")
            return

        if password != confirm_password:
            self.controller.show_snackbar("As senhas não coincidem!", "error")
            return

        if len(password) < 6:
            self.controller.show_snackbar("A senha deve ter pelo menos 6 caracteres!", "error")
            return

        # Verificar se RA já existe
        if get_user_id(ra):
            self.controller.show_snackbar("Este RA já está cadastrado!", "error")
            return

        # Iniciar loading
        self.start_loading()

        # Tentar cadastrar
        try:
            success = insert_user(name, ra, password, self.selected_role)
            if success:
                self.controller.show_snackbar("Conta criada com sucesso!", "success")
                self.controller.show_page("Login")
            else:
                self.controller.show_snackbar("Erro ao criar conta. Tente novamente.", "error")
        except Exception as ex:
            self.controller.show_snackbar(f"Erro: {str(ex)}", "error")
        finally:
            self.stop_loading()

    def start_loading(self):
        """Inicia loading"""
        self.is_loading = True
        self.loading_indicator.visible = True
        self.register_button.style.bgcolor = ft.colors.PURPLE_400
        if self.page:
            self.page.update()

    def stop_loading(self):
        """Para loading"""
        self.is_loading = False
        self.loading_indicator.visible = False
        self.register_button.style.bgcolor = ft.colors.PURPLE_600
        if self.page:
            self.page.update()

    def go_to_login(self, e):
        """Navega para login"""
        self.controller.show_page("Login")