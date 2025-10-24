#!/usr/bin/env python3

from sqlalchemy import text
from .database import get_db

class StatisticsWrapper:
    """Sistema de estatísticas usando a conexão de banco existente"""
    
    def __init__(self):
        """Inicializa o sistema"""
        self.lib = True  # Marca como disponível
        print("✓ Sistema de estatísticas inicializado com conexão existente")

    def configure_database(self, host: str, user: str, password: str, database: str, port: int = 3306):
        """Configura parâmetros de conexão"""
        return True

    def test_database_connection(self) -> bool:
        """Testa conexão com banco usando SQLAlchemy"""
        try:
            db = get_db()
            db.execute(text("SELECT 1"))
            db.close()
            return True
        except:
            return False

    def get_professor_active_tasks(self, professor_id: int):
        """Obtém número de tarefas ativas do professor"""
        try:
            db = get_db()
            query = text("""
                SELECT COUNT(*) as count 
                FROM tasks 
                WHERE creator_id = :professor_id 
                AND (due_date IS NULL OR due_date > NOW())
            """)
            result = db.execute(query, {"professor_id": professor_id})
            count = result.fetchone()[0]
            db.close()
            return count
        except Exception as e:
            print(f"Erro ao obter tarefas ativas: {e}")
            return 0

    def get_total_students(self):
        """Obtém total de estudantes"""
        try:
            db = get_db()
            query = text("SELECT COUNT(*) as count FROM users WHERE user_type = 'aluno'")
            result = db.execute(query)
            count = result.fetchone()[0]
            db.close()
            return count
        except Exception as e:
            print(f"Erro ao obter total de alunos: {e}")
            return 0

    def get_professor_evaluated_responses(self, professor_id: int):
        """Obtém número de respostas avaliadas pelo professor"""
        try:
            db = get_db()
            query = text("""
                SELECT COUNT(*) as count 
                FROM task_responses tr 
                INNER JOIN tasks t ON tr.task_id = t.id 
                WHERE t.creator_id = :professor_id AND tr.score IS NOT NULL
            """)
            result = db.execute(query, {"professor_id": professor_id})
            count = result.fetchone()[0]
            db.close()
            return count
        except Exception as e:
            print(f"Erro ao obter respostas avaliadas: {e}")
            return 0

    def get_student_pending_tasks(self, student_id: int):
        """Obtém número de tarefas pendentes do aluno"""
        try:
            db = get_db()
            query = text("""
                SELECT COUNT(*) as count 
                FROM tasks t 
                LEFT JOIN task_responses tr ON t.id = tr.task_id AND tr.student_id = :student_id 
                WHERE tr.id IS NULL 
                AND (t.due_date IS NULL OR t.due_date > NOW())
            """)
            result = db.execute(query, {"student_id": student_id})
            count = result.fetchone()[0]
            db.close()
            return count
        except Exception as e:
            print(f"Erro ao obter tarefas pendentes: {e}")
            return 0

    def get_student_completed_tasks(self, student_id: int):
        """Obtém número de tarefas completadas pelo aluno"""
        try:
            db = get_db()
            query = text("SELECT COUNT(*) as count FROM task_responses WHERE student_id = :student_id")
            result = db.execute(query, {"student_id": student_id})
            count = result.fetchone()[0]
            db.close()
            return count
        except Exception as e:
            print(f"Erro ao obter tarefas completadas: {e}")
            return 0

    def get_student_average_grade(self, student_id: int):
        """Calcula média de notas do aluno"""
        try:
            db = get_db()
            query = text("""
                SELECT AVG(score) as avg_score 
                FROM task_responses 
                WHERE student_id = :student_id AND score IS NOT NULL
            """)
            result = db.execute(query, {"student_id": student_id})
            avg_score = result.fetchone()[0]
            db.close()
            
            if avg_score is None:
                return 0.0
            
            return float(avg_score)
        except Exception as e:
            print(f"Erro ao obter média de notas: {e}")
            return 0.0

# Singleton
_stats_wrapper = None

def get_statistics_wrapper():
    """Retorna instância única do wrapper de estatísticas"""
    global _stats_wrapper
    if _stats_wrapper is None:
        _stats_wrapper = StatisticsWrapper()
    return _stats_wrapper