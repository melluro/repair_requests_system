from database import get_connection

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # Таблица пользователей
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL  -- 'admin', 'operator', 'specialist'
        )
    """)

    # Таблица клиентов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)

    # Таблица специалистов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS specialists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            specialization TEXT
        )
    """)

    # Таблица заявок
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_number TEXT NOT NULL UNIQUE,
            created_date TEXT NOT NULL,
            equipment_type TEXT NOT NULL,
            equipment_model TEXT NOT NULL,
            problem_description TEXT NOT NULL,
            status TEXT NOT NULL,
            client_id INTEGER NOT NULL,
            assigned_specialist_id INTEGER,
            start_repair_date TEXT,
            end_repair_date TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(id),
            FOREIGN KEY (assigned_specialist_id) REFERENCES specialists(id)
        )
    """)

    # Таблица комментариев
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER NOT NULL,
            comment_text TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (request_id) REFERENCES requests(id)
        )
    """)

    connection.commit()
    connection.close()
