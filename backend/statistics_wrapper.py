"""
Wrapper de estatísticas - Interface para o sistema real
"""
from .statistics import get_statistics_system

class StatisticsWrapper:
    """Wrapper que usa o sistema de estatísticas real"""
    
    def __init__(self):
        self.stats_system = get_statistics_system()
        self.lib = self.stats_system.lib
    
    def configure_database(self, host: str, user: str, password: str, database: str, port: int = 3306):
        return True
    
    def test_database_connection(self) -> bool:
        return self.stats_system.test_database_connection()
    
    def get_professor_active_tasks(self, professor_id: int):
        return self.stats_system.get_professor_active_tasks(professor_id)
    
    def get_total_students(self):
        return self.stats_system.get_total_students()
    
    def get_professor_evaluated_responses(self, professor_id: int):
        return self.stats_system.get_professor_evaluated_responses(professor_id)
    
    def get_student_pending_tasks(self, student_id: int):
        return self.stats_system.get_student_pending_tasks(student_id)
    
    def get_student_completed_tasks(self, student_id: int):
        return self.stats_system.get_student_completed_tasks(student_id)
    
    def get_student_average_grade(self, student_id: int):
        return self.stats_system.get_student_average_grade(student_id)

_stats_wrapper = None

def get_statistics_wrapper():
    global _stats_wrapper
    if _stats_wrapper is None:
        _stats_wrapper = StatisticsWrapper()
    return _stats_wrapper