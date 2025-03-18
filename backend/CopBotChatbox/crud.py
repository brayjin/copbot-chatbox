from CopBotChatbox.database import get_db_connection

def create_procedure(title: str, description: str) -> int:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO procedures (title, description) VALUES (?, ?)", (title, description))
        conn.commit()
        return cursor.lastrowid

def read_procedures():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM procedures")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def update_procedure(proc_id: int, title: str, description: str) -> bool:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE procedures SET title = ?, description = ? WHERE id = ?", (title, description, proc_id))
        conn.commit()
        return cursor.rowcount > 0

def delete_procedure(proc_id: int) -> bool:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM procedures WHERE id = ?", (proc_id,))
        conn.commit()
        return cursor.rowcount > 0
