"""
Módulo de banco de dados para o Sistema Acadêmico Colaborativo
Gerencia conexões, modelos e operações do banco de dados
"""
import os
from datetime import datetime
import pytz
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from .config import Config

# Definir timezone de Brasília
BRASILIA_TZ = pytz.timezone('America/Sao_Paulo')

# Base para os modelos
Base = declarative_base()

# Configuração do banco de dados
engine = create_engine(Config.DATABASE_URL, echo=Config.DEBUG)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    """Modelo de usuário"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)  # RA
    password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    user_type = Column(String(20), nullable=False)  # 'professor' ou 'aluno'
    created_at = Column(DateTime, default=lambda: datetime.now(BRASILIA_TZ))

    # Relacionamentos
    tasks_created = relationship("Task", back_populates="creator", foreign_keys="Task.creator_id")
    responses = relationship("TaskResponse", back_populates="student")

class Task(Base):
    """Modelo de tarefa"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(BRASILIA_TZ))
    due_date = Column(DateTime, nullable=True)
    max_score = Column(Integer, default=100)
    
    # Relacionamentos
    creator = relationship("User", back_populates="tasks_created", foreign_keys=[creator_id])
    responses = relationship("TaskResponse", back_populates="task")

class TaskResponse(Base):
    """Modelo de resposta de tarefa"""
    __tablename__ = "task_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    response_text = Column(Text, nullable=True)
    file_data = Column(LargeBinary(length=(10*1024*1024)), nullable=True)  # 10MB limit
    file_name = Column(String(255), nullable=True)
    submitted_at = Column(DateTime, default=lambda: datetime.now(BRASILIA_TZ))
    score = Column(Integer, nullable=True)
    feedback = Column(Text, nullable=True)
    
    # Relacionamentos
    task = relationship("Task", back_populates="responses")
    student = relationship("User", back_populates="responses")

def init_database():
    """Inicializa o banco de dados criando as tabelas"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Obtém uma sessão do banco de dados"""
    db = SessionLocal()
    try:
        return db
    finally:
        pass

def authenticate_user(username: str, password: str):
    """Autentica um usuário - usado pelo login.py"""
    db = get_db()
    try:
        user = db.query(User).filter(User.username == username, User.password == password).first()
        if user:
            return {
                'id': user.id,
                'username': user.username,
                'ra': user.username,
                'role': user.user_type,
                'full_name': user.full_name
            }
        return None
    finally:
        db.close()

def insert_user(name: str, ra: str, password: str, role: str):
    """Insere um novo usuário - usado pelo register.py"""
    db = get_db()
    try:
        # Verificar se usuário já existe
        existing_user = db.query(User).filter(User.username == ra).first()
        
        if existing_user:
            return False
        
        # Criar novo usuário
        user = User(
            username=ra,
            password=password,
            full_name=name,
            user_type=role
        )
        
        db.add(user)
        db.commit()
        return True
    except:
        return False
    finally:
        db.close()

def get_user_id(ra: str):
    """Obtém o ID de um usuário pelo RA - usado por vários arquivos"""
    db = get_db()
    try:
        user = db.query(User).filter(User.username == ra).first()
        return user.id if user else None
    finally:
        db.close()

def insert_task(title: str, description: str, due_date, creator_id: int):
    """Insere uma nova tarefa - usado pelo criar_tarefa.py"""
    db = get_db()
    try:
        # Converter string de data para datetime se necessário
        if isinstance(due_date, str):
            due_date = datetime.strptime(due_date, '%d/%m/%Y %H:%M')

        task = Task(
            title=title,
            description=description,
            creator_id=creator_id,
            due_date=due_date
        )

        db.add(task)
        db.commit()
        return True
    except Exception as e:
        print(f"Erro ao inserir tarefa: {e}")
        return False
    finally:
        db.close()

def get_tasks_by_user_id(user_id: int):
    """Obtém tarefas criadas por um professor - usado pelo ver_tarefa.py"""
    db = get_db()
    try:
        tasks = db.query(Task).filter(Task.creator_id == user_id).order_by(Task.created_at.desc()).all()
        return [(t.id, t.title, t.description, str(t.created_at), str(t.due_date)) for t in tasks]
    finally:
        db.close()

def get_all_tasks():
    """Obtém todas as tarefas - usado pelos alunos"""
    db = get_db()
    try:
        tasks = db.query(Task, User.full_name).join(User, Task.creator_id == User.id).order_by(Task.created_at.desc()).all()
        return [(t.id, t.title, t.description, str(t.created_at), str(t.due_date), user_full_name) for t, user_full_name in tasks]
    finally:
        db.close()

def update_task(task_id: int, title: str, description: str, due_date):
    """Atualiza uma tarefa - usado pelo editar_tarefa.py"""
    db = get_db()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            task.title = title
            task.description = description
            task.due_date = due_date
            db.commit()
            return True
        return False
    finally:
        db.close()

def delete_task(task_id: int):
    """Deleta uma tarefa - usado pelo detalhe_tarefa.py"""
    db = get_db()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            # Primeiro deletar todas as respostas relacionadas
            db.query(TaskResponse).filter(TaskResponse.task_id == task_id).delete()
            # Depois deletar a tarefa
            db.delete(task)
            db.commit()
            return True
        return False
    finally:
        db.close()

def insert_student_response(task_id: int, student_id: int, filename: str, file_data: bytes):
    """Insere resposta de aluno - usado pelo detalhe_tarefa_aluno.py"""
    db = get_db()
    try:
        # Verificar se já existe uma resposta
        existing_response = db.query(TaskResponse).filter(
            TaskResponse.task_id == task_id,
            TaskResponse.student_id == student_id
        ).first()

        if existing_response:
            # Atualizar resposta existente
            existing_response.file_data = file_data
            existing_response.file_name = filename
            existing_response.submitted_at = datetime.now(BRASILIA_TZ)
        else:
            # Criar nova resposta
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
    """Obtém resposta de um aluno para uma tarefa - usado por vários arquivos"""
    db = get_db()
    try:
        response = db.query(TaskResponse).filter(
            TaskResponse.task_id == task_id,
            TaskResponse.student_id == student_id
        ).first()
        if response:
            return (response.file_name, response.file_data, str(response.submitted_at), response.score, response.feedback)
        return None
    finally:
        db.close()

def get_students_who_responded(task_id: int):
    """Obtém lista de alunos que responderam uma tarefa - usado pelo detalhe_tarefa.py"""
    db = get_db()
    try:
        responses = db.query(TaskResponse, User).join(User, TaskResponse.student_id == User.id).filter(
            TaskResponse.task_id == task_id
        ).all()
        
        result = []
        for response, user in responses:
            has_rating = response.score is not None
            result.append((
                user.full_name,        # username
                user.id,               # user_id
                has_rating,            # has_rating
                response.score,        # rating
                response.feedback,     # comment
                str(response.submitted_at),  # upload_date
                response.file_name     # filename
            ))
        return result
    finally:
        db.close()

def update_student_response_rating(task_id: int, student_id: int, rating: int, comment: str):
    """Atualiza nota e comentário de uma resposta - usado pelo detalhe_resposta_aluno.py"""
    db = get_db()
    try:
        response = db.query(TaskResponse).filter(
            TaskResponse.task_id == task_id,
            TaskResponse.student_id == student_id
        ).first()
        
        if response:
            response.score = rating
            response.feedback = comment
            db.commit()
            return True
        return False
    finally:
        db.close()