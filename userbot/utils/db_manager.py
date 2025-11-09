# coding: utf-8
import sqlite3
import time
from userbot import logger

DB_FILE = "userbot/database/userbot.db"

def init_db():
    """Inicializa o banco de dados e cria as tabelas se não existirem."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            # Tabela de estatísticas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS statistics (
                    key TEXT PRIMARY KEY,
                    value INTEGER
                )
            """)
            # Tabela de histórico de comandos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS command_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command TEXT,
                    timestamp REAL
                )
            """)
            # Tabela de logs de download
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS downloads_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    size INTEGER,
                    duration REAL,
                    status TEXT
                )
            """)

            # Inicializa as estatísticas se não existirem
            initial_stats = {
                "uptime": 0,
                "comandos_executados": 0,
                "downloads_realizados": 0,
                "uploads_realizados": 0,
                "espaco_usado": 0
            }
            for key, value in initial_stats.items():
                cursor.execute("INSERT OR IGNORE INTO statistics (key, value) VALUES (?, ?)", (key, value))

            conn.commit()
            logger.info("Banco de dados inicializado com sucesso.")
    except sqlite3.Error as e:
        logger.error(f"Erro ao inicializar o banco de dados: {e}")

def get_stat(key):
    """Obtém o valor de uma estatística."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM statistics WHERE key = ?", (key,))
            result = cursor.fetchone()
            return result[0] if result else 0
    except sqlite3.Error as e:
        logger.error(f"Erro ao obter estatística '{key}': {e}")
        return 0

def update_stat(key, value):
    """Atualiza o valor de uma estatística."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE statistics SET value = ? WHERE key = ?", (value, key))
            conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Erro ao atualizar estatística '{key}': {e}")

def increment_stat(key, amount=1):
    """Incrementa o valor de uma estatística."""
    current_value = get_stat(key)
    update_stat(key, current_value + amount)

def reset_stats():
    """Reseta todas as estatísticas para zero."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE statistics SET value = 0")
            cursor.execute("DELETE FROM command_history")
            conn.commit()
            logger.info("Estatísticas resetadas com sucesso.")
    except sqlite3.Error as e:
        logger.error(f"Erro ao resetar estatísticas: {e}")

def log_command(command):
    """Registra um comando executado no histórico."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO command_history (command, timestamp) VALUES (?, ?)", (command, time.time()))
            conn.commit()
        increment_stat("comandos_executados")
    except sqlite3.Error as e:
        logger.error(f"Erro ao registrar comando: {e}")

def get_command_usage():
    """Obtém a contagem de uso de cada comando."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT command, COUNT(*) FROM command_history GROUP BY command ORDER BY COUNT(*) DESC")
            return cursor.fetchall()
    except sqlite3.Error as e:
        logger.error(f"Erro ao obter uso de comandos: {e}")
        return []

# Inicializa o DB na importação
init_db()
