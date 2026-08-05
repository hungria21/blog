import sqlite3
import os

DB_FILE = "cache.db"

def init_db():
    """Inicializa o banco de dados e cria a tabela de cache se ela não existir."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS video_cache (
            url TEXT PRIMARY KEY,
            document_id INTEGER,
            access_hash INTEGER,
            file_reference BLOB,
            mime_type TEXT,
            size INTEGER,
            title TEXT,
            caption TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_cached_video(url):
    """
    Retorna os dados do vídeo em cache para a URL fornecida.
    Retorna um dicionário ou None se não encontrado.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT document_id, access_hash, file_reference, mime_type, size, title, caption
        FROM video_cache WHERE url = ?
    """, (url,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def save_cached_video(url, document_id, access_hash, file_reference, mime_type, size, title, caption):
    """Salva os dados de um vídeo no cache."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO video_cache (
            url, document_id, access_hash, file_reference, mime_type, size, title, caption
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (url, document_id, access_hash, file_reference, mime_type, size, title, caption))
    conn.commit()
    conn.close()
