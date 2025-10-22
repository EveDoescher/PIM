#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Estrutura para configuração do banco de dados
typedef struct {
    char host[100];
    char user[50];
    char password[50];
    char database[50];
    int port;
} db_config_t;

// Configuração padrão do banco de dados
static db_config_t db_config = {
    .host = "localhost",
    .user = "app_user", 
    .password = "app_password",
    .database = "sistema_academico",
    .port = 3306
};

// Simular conexão com banco (para funcionar sem MySQL instalado)
// Em produção, substituir por mysql_real_connect
static int simulate_db_connection() {
    return 1; // Simula conexão bem-sucedida
}

// Simular query no banco (para funcionar sem MySQL instalado)
// Em produção, substituir por mysql_query + mysql_store_result
static int simulate_query_result(const char* query) {
    // Simula resultados baseados no tipo de query
    if (strstr(query, "COUNT(*) FROM tasks WHERE creator_id")) {
        return 8; // Tarefas ativas do professor
    }
    if (strstr(query, "COUNT(*) FROM users WHERE user_type = 'aluno'")) {
        return 45; // Total de alunos
    }
    if (strstr(query, "COUNT(*) FROM task_responses") && strstr(query, "score IS NOT NULL")) {
        return 23; // Respostas avaliadas
    }
    if (strstr(query, "LEFT JOIN task_responses") && strstr(query, "IS NULL")) {
        return 5; // Tarefas pendentes do aluno
    }
    if (strstr(query, "COUNT(*) FROM task_responses WHERE student_id")) {
        return 12; // Tarefas concluídas do aluno
    }
    return 0;
}

static double simulate_avg_query(const char* query) {
    if (strstr(query, "AVG(score)")) {
        return 8.5; // Média de notas do aluno
    }
    return 0.0;
}

/* ========== FUNÇÕES PARA PROFESSORES ========== */

int obter_total_tarefas_ativas_professor(int professor_id) {
    if (!simulate_db_connection()) {
        return -1;
    }
    
    char query[512];
    snprintf(query, sizeof(query), 
        "SELECT COUNT(*) FROM tasks WHERE creator_id = %d", 
        professor_id);
    
    return simulate_query_result(query);
}

int obter_numero_alunos_cadastrados() {
    if (!simulate_db_connection()) {
        return -1;
    }
    
    char query[] = "SELECT COUNT(*) FROM users WHERE user_type = 'aluno'";
    return simulate_query_result(query);
}

int obter_total_respostas_avaliadas_professor(int professor_id) {
    if (!simulate_db_connection()) {
        return -1;
    }
    
    char query[512];
    snprintf(query, sizeof(query), 
        "SELECT COUNT(*) FROM task_responses tr "
        "INNER JOIN tasks t ON tr.task_id = t.id "
        "WHERE t.creator_id = %d AND tr.score IS NOT NULL", 
        professor_id);
    
    return simulate_query_result(query);
}

/* ========== FUNÇÕES PARA ALUNOS ========== */

int obter_total_tarefas_pendentes_aluno(int aluno_id) {
    if (!simulate_db_connection()) {
        return -1;
    }
    
    char query[512];
    snprintf(query, sizeof(query), 
        "SELECT COUNT(*) FROM tasks t "
        "LEFT JOIN task_responses tr ON t.id = tr.task_id AND tr.student_id = %d "
        "WHERE tr.id IS NULL", 
        aluno_id);
    
    return simulate_query_result(query);
}

int obter_total_tarefas_concluidas_aluno(int aluno_id) {
    if (!simulate_db_connection()) {
        return -1;
    }
    
    char query[512];
    snprintf(query, sizeof(query), 
        "SELECT COUNT(*) FROM task_responses WHERE student_id = %d", 
        aluno_id);
    
    return simulate_query_result(query);
}

double obter_media_notas_aluno(int aluno_id) {
    if (!simulate_db_connection()) {
        return -1.0;
    }
    
    char query[512];
    snprintf(query, sizeof(query), 
        "SELECT AVG(score) FROM task_responses "
        "WHERE student_id = %d AND score IS NOT NULL", 
        aluno_id);
    
    return simulate_avg_query(query);
}

/* ========== FUNÇÕES AUXILIARES ========== */

int testar_conexao_banco() {
    return simulate_db_connection();
}

void configurar_banco(const char* host, const char* user, const char* password, 
                     const char* database, int port) {
    strncpy(db_config.host, host, sizeof(db_config.host) - 1);
    strncpy(db_config.user, user, sizeof(db_config.user) - 1);
    strncpy(db_config.password, password, sizeof(db_config.password) - 1);
    strncpy(db_config.database, database, sizeof(db_config.database) - 1);
    db_config.port = port;
}

// Função principal para testar as funções
int main() {
    printf("=== Teste das Funções de Estatísticas ===\n\n");
    
    // Testar conexão
    if (testar_conexao_banco()) {
        printf("✓ Conexão com banco simulada com sucesso\n\n");
    } else {
        printf("✗ Falha na conexão\n");
        return 1;
    }
    
    // Testar funções do professor
    printf("--- Estatísticas do Professor (ID: 1) ---\n");
    printf("Tarefas ativas: %d\n", obter_total_tarefas_ativas_professor(1));
    printf("Total de alunos: %d\n", obter_numero_alunos_cadastrados());
    printf("Respostas avaliadas: %d\n", obter_total_respostas_avaliadas_professor(1));
    
    printf("\n--- Estatísticas do Aluno (ID: 1) ---\n");
    printf("Tarefas pendentes: %d\n", obter_total_tarefas_pendentes_aluno(1));
    printf("Tarefas concluídas: %d\n", obter_total_tarefas_concluidas_aluno(1));
    printf("Média de notas: %.1f\n", obter_media_notas_aluno(1));
    
    printf("\n=== Teste concluído com sucesso! ===\n");
    return 0;
}