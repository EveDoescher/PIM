#!/usr/bin/env python3
"""
Sistema de Estatísticas Real - Conecta ao MySQL via SQLAlchemy
"""
from sqlalchemy import text
from .database import get_db

class RealStatisticsSystem:
    """Sistema de estatísticas que executa queries reais no MySQL"""
    
    def __init__(self):
        self.lib = True
    
    def test_database_connection(self) -> bool:
        """Testa conexão real com o banco MySQL"""
        try:
            db = get_db()
            db.execute(text("SELECT 1"))
            db.close()
            return True
        except:
            return False
    
    def get_professor_active_tasks(self, professor_id: int) -> int:
        """Obtém total de tarefas ativas (não expiradas) do professor"""
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
        except:
            return 0
    
    def get_total_students(self) -> int:
        """Obtém número total de usuários com role 'aluno'"""
        try:
            db = get_db()
            query = text("SELECT COUNT(*) as count FROM users WHERE user_type = 'aluno'")
            result = db.execute(query)
            count = result.fetchone()[0]
            db.close()
            return count
        except:
            return 0
    
    def get_professor_evaluated_responses(self, professor_id: int) -> int:
        """Obtém total de respostas avaliadas pelo professor"""
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
        except:
            return 0
    
    def get_student_pending_tasks(self, student_id: int) -> int:
        """Obtém total de tarefas ativas pendentes do aluno"""
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
        except:
            return 0
    
    def get_student_completed_tasks(self, student_id: int) -> int:
        """Obtém total de tarefas concluídas do aluno"""
        try:
            db = get_db()
            query = text("SELECT COUNT(*) as count FROM task_responses WHERE student_id = :student_id")
            result = db.execute(query, {"student_id": student_id})
            count = result.fetchone()[0]
            db.close()
            return count
        except:
            return 0
    
    def get_student_average_grade(self, student_id: int) -> float:
        """Obtém média de notas do aluno"""
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
        except:
            return 0.0

_stats_system = None

def get_statistics_system():
    """Obtém a instância global do sistema de estatísticas"""
    global _stats_system
    if _stats_system is None:
        _stats_system = RealStatisticsSystem()
    return _stats_system