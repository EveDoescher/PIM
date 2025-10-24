#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mysql/mysql.h>

// Estrutura para configuração do banco de dados
typedef struct {
    char host[100];
    char user[50];
    char password[50];
    char database[50];
    int port;
} db_config_t;

// Configuração global do banco de dados
static db_config_t db_config = {
    .host = "localhost",
    .user = "app_user", 
    .password = "app_password",
    .database = "sistema_academico",
    .port = 3306
};

// Função para estabelecer conexão com MySQL
static MYSQL* connect_to_database() {
    MYSQL *conn = mysql_init(NULL);
    if (conn == NULL) {
        fprintf(stderr, "mysql_init() failed\n");
        return NULL;
    }

    if (mysql_real_connect(conn, db_config.host, db_config.user, 
                          db_config.password, db_config.database, 
                          db_config.port, NULL, 0) == NULL) {
        fprintf(stderr, "mysql_real_connect() failed: %s\n", mysql_error(conn));
        mysql_close(conn);
        return NULL;
    }

    return conn;
}

// Função para executar query e retornar resultado inteiro
static int execute_count_query(const char* query) {
    MYSQL *conn = connect_to_database();
    if (conn == NULL) {
        return -1;
    }

    if (mysql_query(conn, query)) {
        fprintf(stderr, "Query failed: %s\n", mysql_error(conn));
        mysql_close(conn);
        return -1;
    }

    MYSQL_RES *result = mysql_store_result(conn);
    if (result == NULL) {
        fprintf(stderr, "mysql_store_result() failed: %s\n", mysql_error(conn));
        mysql_close(conn);
        return -1;
    }

    MYSQL_ROW row = mysql_fetch_row(result);
    int count = 0;
    if (row && row[0]) {
        count = atoi(row[0]);
    }

    mysql_free_result(result);
    mysql_close(conn);
    return count;
}

// Função para executar query e retornar resultado double
static double execute_avg_query(const char* query) {
    MYSQL *conn = connect_to_database();
    if (conn == NULL) {
        return -1.0;
    }

    if (mysql_query(conn, query)) {
        fprintf(stderr, "Query failed: %s\n", mysql_error(conn));
        mysql_close(conn);
        return -1.0;
    }

    MYSQL_RES *result = mysql_store_result(conn);
    if (result == NULL) {
        fprintf(stderr, "mysql_store_result() failed: %s\n", mysql_error(conn));
        mysql_close(conn);
        return -1.0;
    }

    MYSQL_ROW row = mysql_fetch_row(result);
    double avg = 0.0;
    if (row && row[0]) {
        avg = atof(row[0]);
    }

    mysql_free_result(result);
    mysql_close(conn);
    return avg;
}

/* ========== FUNÇÕES PARA PROFESSORES ========== */

int obter_total_tarefas_ativas_professor(int professor_id) {
    char query[512];
    snprintf(query, sizeof(query), 
        "SELECT COUNT(*) FROM tasks WHERE creator_id = %d AND (due_date IS NULL OR due_date > NOW())", 
        professor_id);
    
    return execute_count_query(query);
}

int obter_numero_alunos_cadastrados() {
    const char* query = "SELECT COUNT(*) FROM users WHERE user_type = 'aluno'";
    return execute_count_query(query);
}

int obter_total_respostas_avaliadas_professor(int professor_id) {
    char query[512];
    snprintf(query, sizeof(query), 
        "SELECT COUNT(*) FROM task_responses tr "
        "INNER JOIN tasks t ON tr.task_id = t.id "
        "WHERE t.creator_id = %d AND tr.score IS NOT NULL", 
        professor_id);
    
    return execute_count_query(query);
}

/* ========== FUNÇÕES PARA ALUNOS ========== */

int obter_total_tarefas_pendentes_aluno(int aluno_id) {
    char query[512];
    snprintf(query, sizeof(query), 
        "SELECT COUNT(*) FROM tasks t "
        "LEFT JOIN task_responses tr ON t.id = tr.task_id AND tr.student_id = %d "
        "WHERE tr.id IS NULL AND (t.due_date IS NULL OR t.due_date > NOW())", 
        aluno_id);
    
    return execute_count_query(query);
}

int obter_total_tarefas_concluidas_aluno(int aluno_id) {
    char query[512];
    snprintf(query, sizeof(query), 
        "SELECT COUNT(*) FROM task_responses WHERE student_id = %d", 
        aluno_id);
    
    return execute_count_query(query);
}

double obter_media_notas_aluno(int aluno_id) {
    char query[512];
    snprintf(query, sizeof(query), 
        "SELECT AVG(score) FROM task_responses "
        "WHERE student_id = %d AND score IS NOT NULL", 
        aluno_id);
    
    return execute_avg_query(query);
}

/* ========== FUNÇÕES AUXILIARES ========== */

int testar_conexao_banco() {
    MYSQL *conn = connect_to_database();
    if (conn == NULL) {
        return 0;
    }
    
    // Testa com uma query simples
    if (mysql_query(conn, "SELECT 1")) {
        mysql_close(conn);
        return 0;
    }
    
    mysql_close(conn);
    return 1;
}

void configurar_banco(const char* host, const char* user, const char* password, 
                     const char* database, int port) {
    strncpy(db_config.host, host, sizeof(db_config.host) - 1);
    db_config.host[sizeof(db_config.host) - 1] = '\0';
    
    strncpy(db_config.user, user, sizeof(db_config.user) - 1);
    db_config.user[sizeof(db_config.user) - 1] = '\0';
    
    strncpy(db_config.password, password, sizeof(db_config.password) - 1);
    db_config.password[sizeof(db_config.password) - 1] = '\0';
    
    strncpy(db_config.database, database, sizeof(db_config.database) - 1);
    db_config.database[sizeof(db_config.database) - 1] = '\0';
    
    db_config.port = port;
}