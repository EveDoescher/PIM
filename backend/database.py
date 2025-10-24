# Importações necessárias para o banco de dados
import os
from datetime import datetime  # Para trabalhar com datas e horários
import pytz  # Para trabalhar com fusos horários
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, LargeBinary
from sqlalchemy.ext.declarative import declarative_base  # Base para modelos ORM
from sqlalchemy.orm import sessionmaker, relationship  # Para sessões e relacionamentos
from .config import Config  # Importa as configurações do sistema

# Define o fuso horário de Brasília para timestamps corretos
BRASILIA_TZ = pytz.timezone('America/Sao_Paulo')

# Cria a classe base para todos os modelos do banco de dados
Base = declarative_base()

# Cria o engine de conexão com o banco usando as configurações
engine = create_engine(Config.DATABASE_URL, echo=Config.DEBUG)

# Cria a fábrica de sessões para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    """Modelo que representa os usuários do sistema (professores e alunos)"""
    __tablename__ = "users"  # Nome da tabela no banco
    
    # Definição das colunas da tabela
    id = Column(Integer, primary_key=True, index=True)  # Chave primária auto-incremento
    username = Column(String(50), unique=True, index=True, nullable=False)  # RA único
    password = Column(String(255), nullable=False)  # Senha do usuário
    full_name = Column(String(100), nullable=False)  # Nome completo
    user_type = Column(String(20), nullable=False)  # Tipo: 'professor' ou 'aluno'
    created_at = Column(DateTime, default=lambda: datetime.now(BRASILIA_TZ))  # Data de criação

    # Relacionamentos com outras tabelas
    tasks_created = relationship("Task", back_populates="creator", foreign_keys="Task.creator_id")
    responses = relationship("TaskResponse", back_populates="student")

class Task(Base):
    """Modelo que representa as tarefas criadas pelos professores"""
    __tablename__ = "tasks"  # Nome da tabela no banco
    
    # Definição das colunas da tabela
    id = Column(Integer, primary_key=True, index=True)  # Chave primária
    title = Column(String(200), nullable=False)  # Título da tarefa
    description = Column(Text, nullable=False)  # Descrição detalhada
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ID do professor criador
    created_at = Column(DateTime, default=lambda: datetime.now(BRASILIA_TZ))  # Data de criação
    due_date = Column(DateTime, nullable=True)  # Data limite (opcional)
    max_score = Column(Integer, default=100)  # Pontuação máxima (padrão 100)
    
    # Relacionamentos
    creator = relationship("User", back_populates="tasks_created", foreign_keys=[creator_id])
    responses = relationship("TaskResponse", back_populates="task")

class TaskResponse(Base):
    """Modelo que representa as respostas dos alunos às tarefas"""
    __tablename__ = "task_responses"  # Nome da tabela no banco
    
    # Definição das colunas da tabela
    id = Column(Integer, primary_key=True, index=True)  # Chave primária
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)  # ID da tarefa
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ID do aluno
    response_text = Column(Text, nullable=True)  # Resposta em texto (opcional)
    file_data = Column(LargeBinary(length=(10*1024*1024)), nullable=True)  # Arquivo até 10MB
    file_name = Column(String(255), nullable=True)  # Nome do arquivo enviado
    submitted_at = Column(DateTime, default=lambda: datetime.now(BRASILIA_TZ))  # Data de envio
    score = Column(Integer, nullable=True)  # Nota atribuída (opcional)
    feedback = Column(Text, nullable=True)  # Comentário do professor (opcional)
    
    # Relacionamentos
    task = relationship("Task", back_populates="responses")
    student = relationship("User", back_populates="responses")

def init_database():
    """Cria todas as tabelas no banco de dados se elas não existirem"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Retorna uma nova sessão de conexão com o banco de dados"""
    db = SessionLocal()
    try:
        return db
    finally:
        pass  # Sessão será fechada manualmente nas funções que a utilizam

def authenticate_user(username: str, password: str):
    """Autentica um usuário verificando suas credenciais no banco"""
    db = get_db()
    try:
        # Busca usuário com username e senha correspondentes
        user = db.query(User).filter(User.username == username, User.password == password).first()
        if user:
            # Retorna dicionário com dados do usuário para sessão
            return {
                'id': user.id,
                'username': user.username,
                'ra': user.username,  # RA é o mesmo que username
                'role': user.user_type,
                'full_name': user.full_name
            }
        return None  # Credenciais inválidas
    finally:
        db.close()  # Sempre fecha a conexão

def insert_user(name: str, ra: str, password: str, role: str):
    """Cadastra um novo usuário no sistema verificando se o RA já existe"""
    db = get_db()
    try:
        # Verifica se já existe usuário com este RA
        existing_user = db.query(User).filter(User.username == ra).first()
        
        if existing_user:
            return False  # RA já cadastrado
        
        # Cria novo usuário
        user = User(
            username=ra,
            password=password,
            full_name=name,
            user_type=role
        )
        
        # Salva no banco
        db.add(user)
        db.commit()
        return True  # Cadastro realizado com sucesso
    except:
        return False  # Erro durante o cadastro
    finally:
        db.close()

def get_user_id(ra: str):
    """Busca o ID interno de um usuário usando seu RA"""
    db = get_db()
    try:
        user = db.query(User).filter(User.username == ra).first()
        return user.id if user else None
    finally:
        db.close()

def insert_task(title: str, description: str, due_date, creator_id: int):
    """Cria uma nova tarefa no sistema convertendo data se necessário"""
    db = get_db()
    try:
        # Converte string de data para datetime se necessário
        if isinstance(due_date, str):
            due_date = datetime.strptime(due_date, '%d/%m/%Y %H:%M')

        # Cria nova tarefa
        task = Task(
            title=title,
            description=description,
            creator_id=creator_id,
            due_date=due_date
        )

        # Salva no banco
        db.add(task)
        db.commit()
        return True
    except Exception as e:
        print(f"Erro ao inserir tarefa: {e}")
        return False
    finally:
        db.close()

def get_tasks_by_user_id(user_id: int):
    """Busca todas as tarefas criadas por um professor específico"""
    db = get_db()
    try:
        # Busca tarefas do professor ordenadas por data de criação (mais recentes primeiro)
        tasks = db.query(Task).filter(Task.creator_id == user_id).order_by(Task.created_at.desc()).all()
        # Retorna lista de tuplas com dados das tarefas
        return [(t.id, t.title, t.description, str(t.created_at), str(t.due_date)) for t in tasks]
    finally:
        db.close()

def get_all_tasks():
    """Busca todas as tarefas do sistema incluindo nome do professor criador"""
    db = get_db()
    try:
        # Faz join entre Task e User para pegar nome do professor
        tasks = db.query(Task, User.full_name).join(User, Task.creator_id == User.id).order_by(Task.created_at.desc()).all()
        # Retorna lista incluindo nome do professor
        return [(t.id, t.title, t.description, str(t.created_at), str(t.due_date), user_full_name) for t, user_full_name in tasks]
    finally:
        db.close()

def update_task(task_id: int, title: str, description: str, due_date):
    """Atualiza os dados de uma tarefa existente"""
    db = get_db()
    try:
        # Busca a tarefa pelo ID
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            # Atualiza os campos
            task.title = title
            task.description = description
            task.due_date = due_date
            db.commit()
            return True
        return False  # Tarefa não encontrada
    finally:
        db.close()

def delete_task(task_id: int):
    """Remove uma tarefa e todas as suas respostas do sistema"""
    db = get_db()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            # Primeiro remove todas as respostas relacionadas
            db.query(TaskResponse).filter(TaskResponse.task_id == task_id).delete()
            # Depois remove a tarefa
            db.delete(task)
            db.commit()
            return True
        return False
    finally:
        db.close()

def insert_student_response(task_id: int, student_id: int, filename: str, file_data: bytes):
    """Salva ou atualiza a resposta de um aluno para uma tarefa"""
    db = get_db()
    try:
        # Verifica se já existe resposta deste aluno para esta tarefa
        existing_response = db.query(TaskResponse).filter(
            TaskResponse.task_id == task_id,
            TaskResponse.student_id == student_id
        ).first()

        if existing_response:
            # Atualiza resposta existente
            existing_response.file_data = file_data
            existing_response.file_name = filename
            existing_response.submitted_at = datetime.now(BRASILIA_TZ)
        else:
            # Cria nova resposta
            response = TaskResponse(
                task_id=task_id,
                student_id=student_id,
                file_data=file_data,
                file_name=filename
            )
            db.add(response)

        db.commit()
        print(f"Resposta inserida/atualizada com sucesso para task_id={task_id}, student_id={student_id}")
        return True
    except Exception as e:
        print(f"Erro ao inserir resposta: {e}")
        return False
    finally:
        db.close()

def get_student_response(task_id: int, student_id: int):
    """Busca a resposta de um aluno específico para uma tarefa"""
    db = get_db()
    try:
        response = db.query(TaskResponse).filter(
            TaskResponse.task_id == task_id,
            TaskResponse.student_id == student_id
        ).first()
        if response:
            # Retorna tupla com dados da resposta
            return (response.file_name, response.file_data, str(response.submitted_at), response.score, response.feedback)
        return None
    finally:
        db.close()

def get_students_who_responded(task_id: int):
    """Lista todos os alunos que enviaram respostas para uma tarefa específica"""
    db = get_db()
    try:
        # Faz join entre TaskResponse e User para pegar dados dos alunos
        responses = db.query(TaskResponse, User).join(User, TaskResponse.student_id == User.id).filter(
            TaskResponse.task_id == task_id
        ).all()
        
        result = []
        for response, user in responses:
            # Verifica se a resposta já foi avaliada
            has_rating = response.score is not None
            result.append((
                user.full_name,  # Nome do aluno
                user.id,  # ID do aluno
                has_rating,  # Se já foi avaliado
                response.score,  # Nota (se houver)
                response.feedback,  # Comentário (se houver)
                str(response.submitted_at),  # Data de envio
                response.file_name  # Nome do arquivo
            ))
        return result
    finally:
        db.close()

def update_student_response_rating(task_id: int, student_id: int, rating: int, comment: str):
    """Atualiza a nota e comentário de uma resposta de aluno"""
    db = get_db()
    try:
        # Busca a resposta específica
        response = db.query(TaskResponse).filter(
            TaskResponse.task_id == task_id,
            TaskResponse.student_id == student_id
        ).first()
        
        if response:
            # Atualiza nota e feedback
            response.score = rating
            response.feedback = comment
            db.commit()
            return True
        return False
    finally:
        db.close()