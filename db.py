import sqlite3


POST_DB = 'posts.db'

def create_db():
    conn = sqlite3.connect(POST_DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()


def save_post_id(post_id):
    conn = sqlite3.connect(POST_DB)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO posts (id) VALUES (?)', (post_id,))
    conn.commit()
    conn.close()


def is_post_published(post_id):
    conn = sqlite3.connect(POST_DB)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM posts WHERE id = ?', (post_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def count_posts():
    conn = sqlite3.connect(POST_DB)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM posts')
    result = cursor.fetchone()
    conn.close()
    if result is not None:
        return result[0]
    else:
        return 0
