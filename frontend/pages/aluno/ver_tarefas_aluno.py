import flet as ft
from datetime import datetime
from backend.database import get_all_tasks, get_student_response

class VerTarefasAluno(ft.Container):
    """Classe responsável pela visualização de tarefas do aluno com design clean e moderno."""

    def __init__(self, page: ft.Page, controller):
        """Inicializa a tela de visualização de tarefas."""
        super().__init__(
            expand=True,
            width=None,
            height=None,
            padding=ft.padding.all(0),
            margin=ft.margin.all(0)
        )
        self.page = page
        self.controller = controller
        
        self.tasks = []
        self.filtered_tasks = []
        self.search_query = ""
        self.filter_status = "todas"  # todas, pendentes, entregues, expiradas
        
        self.load_tasks()
        self.create_components()
        self.setup_layout()

    def load_tasks(self):
        """Carrega todas as tarefas disponíveis"""
        all_tasks = get_all_tasks() or []
        user_id = self.controller.current_user.get('id') if self.controller.current_user else None

        # Adicionar status de entrega para cada tarefa
        self.tasks = []
        for task in all_tasks:
            task_data = list(task)
            # Verificar se o aluno já entregou
            response = get_student_response(task[0], user_id) if user_id else None
            task_data.append(response)  # Adicionar resposta como último elemento
            self.tasks.append(tuple(task_data))

        self.filtered_tasks = self.tasks.copy()

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

        # Campo de busca clean - MAIOR
        self.search_field = ft.TextField(
            label="Buscar tarefas...",
            width=500,
            height=65,
            prefix_icon=ft.icons.SEARCH_ROUNDED,
            border_radius=32,
            filled=True,
            bgcolor=ft.colors.WHITE,
            border_color=ft.colors.with_opacity(0.1, ft.colors.GREY_400),
            focused_border_color=ft.colors.PINK_400,
            focused_bgcolor=ft.colors.WHITE,
            label_style=ft.TextStyle(
                color=ft.colors.GREY_600,
                size=18,
                weight=ft.FontWeight.W_500
            ),
            text_style=ft.TextStyle(
                size=19,
                weight=ft.FontWeight.W_500,
                color=ft.colors.GREY_800
            ),
            cursor_color=ft.colors.PINK_400,
            content_padding=ft.padding.symmetric(horizontal=25, vertical=20),
            on_change=self.on_search_change
        )

        # Filtros clean - MAIORES
        self.filter_chips = ft.Row([
            self.create_filter_chip("todas", "Todas", ft.icons.LIST_ROUNDED),
            self.create_filter_chip("pendentes", "Pendentes", ft.icons.PENDING_ACTIONS_ROUNDED),
            self.create_filter_chip("entregues", "Entregues", ft.icons.TASK_ALT_ROUNDED),
            self.create_filter_chip("expiradas", "Expiradas", ft.icons.SCHEDULE_SEND_ROUNDED)
        ], spacing=15)

        # Container para lista de tarefas - CENTRALIZADAS
        self.tasks_container = ft.Column(
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.update_tasks_display()

        # Estatísticas clean - MAIORES
        self.stats_row = self.create_stats()

    def create_filter_chip(self, value, label, icon):
        """Cria um chip de filtro clean - MAIOR"""
        is_selected = self.filter_status == value
        
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=22, color=ft.colors.WHITE if is_selected else ft.colors.GREY_600),
                ft.Text(
                    label,
                    size=18,
                    weight=ft.FontWeight.W_600,
                    color=ft.colors.WHITE if is_selected else ft.colors.GREY_700
                )
            ], spacing=10, tight=True),
            width=140,
            height=50,
            bgcolor=ft.colors.PINK_400 if is_selected else ft.colors.WHITE,
            border_radius=25,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=ft.colors.with_opacity(0.15, ft.colors.PINK_400) if is_selected else ft.colors.with_opacity(0.05, ft.colors.BLACK),
                offset=ft.Offset(0, 3)
            ),
            border=ft.border.all(1, ft.colors.PINK_200 if is_selected else ft.colors.with_opacity(0.1, ft.colors.GREY_400)),
            on_click=lambda e, f=value: self.change_filter(f)
        )

    def get_task_status(self, task):
        """Determina o status da tarefa para o aluno"""
        expiration_date = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S')
        has_response = task[6] is not None  # Resposta do aluno
        
        if expiration_date < datetime.now():
            return "expirada" if not has_response else "entregue_expirada"
        elif has_response:
            return "entregue"
        else:
            return "pendente"

    def create_task_card(self, task):
        """Cria um card moderno e clean para cada tarefa - MAIOR e CENTRALIZADO"""
        status = self.get_task_status(task)
        expiration_date = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S')
        
        # Definir cores e textos baseados no status
        status_config = {
            "pendente": {
                "color": ft.colors.ORANGE_400,
                "text": "Pendente",
                "icon": ft.icons.PENDING_ACTIONS_ROUNDED
            },
            "entregue": {
                "color": ft.colors.GREEN_400,
                "text": "Entregue",
                "icon": ft.icons.TASK_ALT_ROUNDED
            },
            "expirada": {
                "color": ft.colors.RED_400,
                "text": "Expirada",
                "icon": ft.icons.SCHEDULE_SEND_ROUNDED
            },
            "entregue_expirada": {
                "color": ft.colors.BLUE_400,
                "text": "Entregue (Fora do Prazo)",
                "icon": ft.icons.TASK_ALT_ROUNDED
            }
        }
        
        config = status_config[status]

        # Card da tarefa clean - MAIOR e CENTRALIZADO
        return ft.Container(
            content=ft.Row([
                # Conteúdo principal
                ft.Container(
                    content=ft.Column([
                        # Cabeçalho com título e status
                        ft.Row([
                            ft.Text(
                                task[1],  # título
                                size=24,
                                weight=ft.FontWeight.W_600,
                                color=ft.colors.GREY_800,
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(config["icon"], size=20, color=config["color"]),
                                    ft.Text(
                                        config["text"],
                                        size=16,
                                        weight=ft.FontWeight.W_600,
                                        color=config["color"]
                                    )
                                ], spacing=8),
                                padding=ft.padding.symmetric(horizontal=16, vertical=8),
                                border_radius=16,
                                bgcolor=ft.colors.with_opacity(0.1, config["color"])
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        
                        ft.Container(height=15),
                        
                        # Descrição
                        ft.Text(
                            task[2][:120] + "..." if len(task[2]) > 120 else task[2],
                            size=18,
                            color=ft.colors.GREY_600,
                            max_lines=3
                        ),
                        
                        ft.Container(height=18),
                        
                        # Informações da tarefa
                        ft.Row([
                            ft.Row([
                                ft.Icon(ft.icons.PERSON_ROUNDED, size=20, color=ft.colors.GREY_500),
                                ft.Text(
                                    f"Professor: {task[5]}",  # nome do professor
                                    size=16,
                                    color=ft.colors.GREY_500
                                )
                            ], spacing=8),
                            ft.Row([
                                ft.Icon(ft.icons.ACCESS_TIME_ROUNDED, size=20, color=ft.colors.GREY_500),
                                ft.Text(
                                    f"Prazo: {expiration_date.strftime('%d/%m/%Y às %H:%M')}",
                                    size=16,
                                    color=ft.colors.GREY_500
                                )
                            ], spacing=8)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ]),
                    expand=True,
                    padding=ft.padding.all(30)
                ),
                
                # Ações clean - MAIORES
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Icon(ft.icons.VISIBILITY_ROUNDED, color=ft.colors.WHITE, size=22),
                            width=55,
                            height=55,
                            bgcolor=ft.colors.PURPLE_400,
                            border_radius=27,
                            alignment=ft.alignment.center,
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=10,
                                color=ft.colors.with_opacity(0.2, ft.colors.PURPLE_400),
                                offset=ft.Offset(0, 3)
                            ),
                            on_click=lambda e, t=task: self.view_task_details(t)
                        )
                    ], spacing=6),
                    padding=ft.padding.all(20)
                )
            ]),
            width=1000,  # MAIOR
            bgcolor=ft.colors.WHITE,
            border_radius=20,
            alignment=ft.alignment.center_left,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=15,
                color=ft.colors.with_opacity(0.06, ft.colors.BLACK),
                offset=ft.Offset(0, 5)
            ),
            border=ft.border.all(1, ft.colors.with_opacity(0.05, ft.colors.BLACK))
        )

    def create_stats(self):
        """Cria estatísticas das tarefas - MAIORES"""
        total_tasks = len(self.tasks)
        pending_tasks = len([t for t in self.tasks if self.get_task_status(t) == "pendente"])
        completed_tasks = len([t for t in self.tasks if self.get_task_status(t) in ["entregue", "entregue_expirada"]])
        expired_tasks = len([t for t in self.tasks if self.get_task_status(t) == "expirada"])
        
        return ft.Row([
            self.create_stat_card("Total", str(total_tasks), ft.icons.LIST_ROUNDED, ft.colors.PURPLE_400),
            self.create_stat_card("Pendentes", str(pending_tasks), ft.icons.PENDING_ACTIONS_ROUNDED, ft.colors.ORANGE_400),
            self.create_stat_card("Entregues", str(completed_tasks), ft.icons.TASK_ALT_ROUNDED, ft.colors.GREEN_400),
            self.create_stat_card("Expiradas", str(expired_tasks), ft.icons.SCHEDULE_SEND_ROUNDED, ft.colors.RED_400),
        ], spacing=60, alignment=ft.MainAxisAlignment.CENTER)

    def create_stat_card(self, label, value, icon, color):
        """Cria um card de estatística clean - MAIOR"""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, size=32, color=color),
                    width=80,
                    height=80,
                    border_radius=40,
                    bgcolor=ft.colors.with_opacity(0.1, color),
                    alignment=ft.alignment.center
                ),
                ft.Container(width=20),
                ft.Column([
                    ft.Text(
                        value,
                        size=30,
                        weight=ft.FontWeight.W_700,
                        color=ft.colors.GREY_800
                    ),
                    ft.Text(
                        label,
                        size=14,
                        color=ft.colors.GREY_500,
                        weight=ft.FontWeight.W_500
                    )
                ], spacing=4)
            ], alignment=ft.MainAxisAlignment.START),
            width=280,
            height=120,
            bgcolor=ft.colors.WHITE,
            border_radius=20,
            padding=ft.padding.all(30),
            alignment=ft.alignment.center_left,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=ft.colors.with_opacity(0.05, ft.colors.BLACK),
                offset=ft.Offset(0, 4)
            ),
            border=ft.border.all(1, ft.colors.with_opacity(0.05, ft.colors.BLACK))
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
                        "Tarefas Disponíveis",
                        size=42,
                        weight=ft.FontWeight.W_600,
                        color=ft.colors.GREY_800,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Visualize e responda às tarefas dos seus professores",
                        size=20,
                        color=ft.colors.GREY_500,
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(expand=True)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=60, vertical=45)
        )

        # Seção de estatísticas - MAIOR
        stats_section = ft.Container(
            content=self.stats_row,
            padding=ft.padding.symmetric(horizontal=60, vertical=25)
        )

        # Seção de filtros e busca - MAIOR
        filters_section = ft.Container(
            content=ft.Row([
                self.search_field,
                ft.Container(width=40),
                self.filter_chips
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=60, vertical=25)
        )

        # Lista de tarefas - CENTRALIZADA
        tasks_section = ft.Container(
            content=ft.Column([
                self.tasks_container
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=60, vertical=25),
            alignment=ft.alignment.center
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
                stats_section,
                filters_section,
                tasks_section,
                ft.Container(expand=True)
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO
            )
        )

    def update_tasks_display(self):
        """Atualiza a exibição das tarefas - CENTRALIZADA"""
        self.tasks_container.controls.clear()
        
        if not self.filtered_tasks:
            # Mensagem quando não há tarefas - MAIOR
            empty_state = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.ASSIGNMENT_ROUNDED, size=80, color=ft.colors.GREY_400),
                    ft.Container(height=25),
                    ft.Text(
                        "Nenhuma tarefa encontrada",
                        size=28,
                        weight=ft.FontWeight.W_600,
                        color=ft.colors.GREY_600
                    ),
                    ft.Container(height=12),
                    ft.Text(
                        "Não há tarefas disponíveis no momento",
                        size=18,
                        color=ft.colors.GREY_500
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(60),
                alignment=ft.alignment.center
            )
            self.tasks_container.controls.append(empty_state)
        else:
            # Adicionar cards das tarefas - CENTRALIZADAS
            for task in self.filtered_tasks:
                self.tasks_container.controls.append(self.create_task_card(task))

    def on_search_change(self, e):
        """Callback para mudança na busca"""
        self.search_query = e.control.value.lower()
        self.apply_filters()

    def change_filter(self, filter_value):
        """Muda o filtro ativo"""
        self.filter_status = filter_value
        # Recriar chips com nova seleção
        self.filter_chips.controls = [
            self.create_filter_chip("todas", "Todas", ft.icons.LIST_ROUNDED),
            self.create_filter_chip("pendentes", "Pendentes", ft.icons.PENDING_ACTIONS_ROUNDED),
            self.create_filter_chip("entregues", "Entregues", ft.icons.TASK_ALT_ROUNDED),
            self.create_filter_chip("expiradas", "Expiradas", ft.icons.SCHEDULE_SEND_ROUNDED)
        ]
        self.apply_filters()
        self.page.update()

    def apply_filters(self):
        """Aplica filtros e busca"""
        filtered = self.tasks.copy()
        
        # Filtro por status
        if self.filter_status == "pendentes":
            filtered = [t for t in filtered if self.get_task_status(t) == "pendente"]
        elif self.filter_status == "entregues":
            filtered = [t for t in filtered if self.get_task_status(t) in ["entregue", "entregue_expirada"]]
        elif self.filter_status == "expiradas":
            filtered = [t for t in filtered if self.get_task_status(t) == "expirada"]
        
        # Filtro por busca
        if self.search_query:
            filtered = [t for t in filtered if 
                       self.search_query in t[1].lower() or  # título
                       self.search_query in t[2].lower() or  # descrição
                       self.search_query in t[5].lower()]    # nome do professor
        
        self.filtered_tasks = filtered
        self.update_tasks_display()
        self.page.update()

    def view_task_details(self, task):
        """Visualiza detalhes da tarefa"""
        self.controller.current_task = task
        self.controller.show_page("DetalheTarefaAluno")

    def go_back(self, e):
        """Volta para o dashboard"""
        self.controller.show_page("DashboardAluno")