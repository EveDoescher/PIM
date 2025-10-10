import sqlite3
import hashlib
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

def get_connection():
    """Retorna uma conexão com o banco de dados SQLite."""
    return sqlite3.connect("db/database.db")

# Criar tabelas se não existirem
conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
               id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL,
               ra TEXT UNIQUE NOT NULL,
               encrypted_password TEXT NOT NULL,
               role TEXT CHECK(role IN ('aluno', 'professor')) NOT NULL
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATETIME NOT NULL,
    expiration_date DATETIME NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS student_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    filename TEXT NOT NULL,
    file_data BLOB NOT NULL,
    upload_date DATETIME NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

# Adicionar colunas rating e comment se não existirem
try:
    cursor.execute("ALTER TABLE student_responses ADD COLUMN rating INTEGER")
except sqlite3.OperationalError:
    pass  # Coluna já existe

try:
    cursor.execute("ALTER TABLE student_responses ADD COLUMN comment TEXT")
except sqlite3.OperationalError:
    pass  # Coluna já existe

conn.commit()
conn.close()

logging.info("Tabelas criadas com sucesso")

def insert_user(username, ra, password, role):
    """Insere um novo usuário no banco de dados."""
    hash_pass = hashlib.sha256(password.encode()).hexdigest()
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, ra, encrypted_password, role) VALUES (?, ?, ?, ?)", (username, ra, hash_pass, role))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            logging.error(f"Erro ao inserir usuário: {e}")
            return False

def authenticate_user(ra, password):
    """Autentica um usuário com RA e senha."""
    hash_pass = hashlib.sha256(password.encode()).hexdigest()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, ra, role FROM users WHERE ra = ? AND encrypted_password = ?", (ra, hash_pass))
        user = cursor.fetchone()
        if user:
            return {"id": user[0], "username": user[1], "ra": user[2], "role": user[3]}
        return None

def insert_task(title, description, expiration_date_str, user_id):
    """Insere uma nova tarefa no banco de dados."""
    creation_date = datetime.now()
    try:
        if isinstance(expiration_date_str, datetime):
            expiration_date = expiration_date_str
        else:
            expiration_date = datetime.strptime(expiration_date_str, '%d/%m/%Y %H:%M')
    except ValueError:
        logging.error("Formato de data/hora inválido")
        return False
    
    if not user_id:
        logging.error("user_id é obrigatório")
        return False
        
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO tasks (title, description, creation_date, expiration_date, user_id) VALUES (?, ?, ?, ?, ?)",
                (title, description, creation_date, expiration_date, user_id)
            )
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Erro ao inserir tarefa: {e}")
            return False

def get_user_id(ra):
    """Retorna o ID do usuário com base no RA."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE ra = ?", (ra,))
        result = cursor.fetchone()
        return result[0] if result else None

def get_tasks_by_user_id(user_id):
    """Retorna todas as tarefas de um usuário específico."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description, creation_date, expiration_date FROM tasks WHERE user_id = ? ORDER BY creation_date DESC", (user_id,))
        return cursor.fetchall()

def get_all_tasks():
    """Retorna todas as tarefas cadastradas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description, creation_date, expiration_date FROM tasks ORDER BY creation_date DESC")
        return cursor.fetchall()

def delete_task(task_id):
    """Deleta uma tarefa pelo ID."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            # Primeiro, deletar as respostas dos alunos associadas à tarefa
            cursor.execute("DELETE FROM student_responses WHERE task_id = ?", (task_id,))
            # Depois, deletar a tarefa
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return True
    except Exception as e:
        logging.error(f"Erro ao deletar tarefa: {e}")
        return False

def update_task(task_id, title, description, expiration_date_str):
    """Atualiza uma tarefa existente."""
    try:
        if isinstance(expiration_date_str, datetime):
            expiration_date = expiration_date_str
        else:
            expiration_date = datetime.strptime(expiration_date_str, '%d/%m/%Y %H:%M')
    except ValueError:
        logging.error("Formato de data/hora inválido")
        return False
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tasks SET title = ?, description = ?, expiration_date = ? WHERE id = ?",
                (title, description, expiration_date, task_id)
            )
            conn.commit()
            return True
    except Exception as e:
        logging.error(f"Erro ao atualizar tarefa: {e}")
        return False

def insert_student_response(task_id, user_id, filename, file_data):
    """Insere a resposta de um aluno para uma tarefa."""
    upload_date = datetime.now()
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO student_responses (task_id, user_id, filename, file_data, upload_date) VALUES (?, ?, ?, ?, ?)",
                (task_id, user_id, filename, file_data, upload_date)
            )
            conn.commit()
            return True
    except Exception as e:
        logging.error(f"Erro ao inserir resposta do aluno: {e}")
        return False

def get_student_response(task_id, user_id):
    """Retorna a resposta de um aluno para uma tarefa."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT filename, file_data, upload_date, rating, comment FROM student_responses WHERE task_id = ? AND user_id = ?",
                (task_id, user_id)
            )
            return cursor.fetchone()
    except Exception as e:
        logging.error(f"Erro ao buscar resposta do aluno: {e}")
        return None

def get_students_who_responded(task_id):
    """Retorna a lista de tuplas (nome, id, has_rating, rating, comment, upload_date, filename) de alunos que responderam a uma tarefa."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT u.username, u.id, 
                   CASE WHEN sr.rating IS NOT NULL THEN 1 ELSE 0 END as has_rating,
                   sr.rating, sr.comment, sr.upload_date, sr.filename
                   FROM users u 
                   INNER JOIN student_responses sr ON u.id = sr.user_id 
                   WHERE sr.task_id = ? 
                   ORDER BY sr.upload_date DESC""",
                (task_id,)
            )
            return cursor.fetchall()
    except Exception as e:
        logging.error(f"Erro ao buscar alunos que responderam: {e}")
        return []

def update_student_response_rating(task_id, user_id, rating, comment):
    """Atualiza a nota e comentário de uma resposta de aluno."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE student_responses SET rating = ?, comment = ? WHERE task_id = ? AND user_id = ?",
                (rating, comment, task_id, user_id)
            )
            conn.commit()
            return True
    except Exception as e:
        logging.error(f"Erro ao atualizar nota e comentário: {e}")
        return False