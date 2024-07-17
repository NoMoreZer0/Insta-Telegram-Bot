import sqlite3


def create_db():
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

def save_post_id(post_id):
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO posts (id) VALUES (?)', (post_id,))
    conn.commit()
    conn.close()

def is_post_published(post_id):
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM posts WHERE id = ?', (post_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None