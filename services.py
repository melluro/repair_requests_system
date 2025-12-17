from database import get_connection
from datetime import datetime

# ------------------ Клиенты ------------------
def add_client(full_name, phone):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO clients (full_name, phone) VALUES (?, ?)",
        (full_name, phone)
    )

    client_id = cursor.lastrowid
    connection.commit()
    connection.close()

    return client_id

# ------------------ Заявки ------------------
def add_request(request_number, equipment_type, equipment_model, problem_description, client_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO requests (
                request_number,
                created_date,
                equipment_type,
                equipment_model,
                problem_description,
                status,
                client_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                request_number,
                datetime.now().isoformat(),
                equipment_type,
                equipment_model,
                problem_description,
                "Открыта",
                client_id
            )
        )

        connection.commit()

    except Exception as error:
        print("Ошибка при добавлении заявки:", error)

    finally:
        connection.close()

def get_all_requests():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT 
            requests.id,
            requests.request_number,
            requests.equipment_type,
            requests.equipment_model,
            requests.problem_description,
            requests.status,
            clients.full_name
        FROM requests
        JOIN clients ON requests.client_id = clients.id
        """
    )

    rows = cursor.fetchall()
    connection.close()

    return rows

def update_request_status(request_number, new_status):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE requests
            SET status = ?
            WHERE request_number = ?
            """,
            (new_status, request_number)
        )
        if cursor.rowcount == 0:
            print(f"Заявка с номером {request_number} не найдена")
        else:
            print(f"Статус заявки {request_number} обновлен на {new_status}")

        connection.commit()

    except Exception as error:
        print("Ошибка при обновлении статуса:", error)

    finally:
        connection.close()

def assign_specialist(request_number, specialist_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE requests
            SET assigned_specialist_id = ?
            WHERE request_number = ?
            """,
            (specialist_id, request_number)
        )
        if cursor.rowcount == 0:
            print(f"Заявка с номером {request_number} не найдена")
        else:
            print(f"Специалист {specialist_id} назначен на заявку {request_number}")

        connection.commit()

    except Exception as error:
        print("Ошибка при назначении специалиста:", error)

    finally:
        connection.close()

def complete_request(request_number, start_date, end_date):
    """Завершает заявку, устанавливая статус и даты ремонта"""
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE requests
            SET status = 'Завершена', start_repair_date = ?, end_repair_date = ?
            WHERE request_number = ?
            """,
            (start_date, end_date, request_number)
        )
        if cursor.rowcount == 0:
            print(f"Заявка {request_number} не найдена")
        else:
            print(f"Заявка {request_number} успешно завершена")

        connection.commit()

    except Exception as error:
        print("Ошибка при завершении заявки:", error)

    finally:
        connection.close()

# ------------------ Статистика ------------------
def calculate_statistics():
    connection = get_connection()
    cursor = connection.cursor()

    # Выбираем все завершённые заявки
    cursor.execute(
        """
        SELECT start_repair_date, end_repair_date, problem_description
        FROM requests
        WHERE status = 'Завершена'
        """
    )

    rows = cursor.fetchall()
    connection.close()

    completed_count = len(rows)           # количество завершённых заявок
    total_days = 0                        # суммарное время ремонта в днях
    problem_types = {}                     # статистика по типам неисправностей

    for start, end, problem in rows:
        if start and end:
            start_date = datetime.fromisoformat(start)
            end_date = datetime.fromisoformat(end)
            total_days += (end_date - start_date).days

        if problem in problem_types:
            problem_types[problem] += 1
        else:
            problem_types[problem] = 1

    average_days = total_days / completed_count if completed_count > 0 else 0

    return {
        "completed_count": completed_count,
        "average_days": average_days,
        "problem_types": problem_types
    }

# ------------------ Специалисты ------------------
def add_specialist(full_name, specialization=None):
    """Добавляет нового специалиста и возвращает его id"""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO specialists (full_name, specialization) VALUES (?, ?)",
        (full_name, specialization)
    )

    specialist_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return specialist_id

# ------------------ Пользователи ------------------
def register_user(username, password, role):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password, role)
        )
        connection.commit()
        user_id = cursor.lastrowid
    except Exception as e:
        print("Ошибка регистрации:", e)
        user_id = None
    finally:
        connection.close()
    return user_id

def login_user(username, password):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id, role FROM users WHERE username=? AND password=?",
        (username, password)
    )
    row = cursor.fetchone()
    connection.close()
    if row:
        return {"id": row[0], "role": row[1]}
    else:
        return None

# ------------------ Получение заявок по роли ------------------
def get_requests_by_user(user):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        if user['role'] == 'specialist':
            cursor.execute("""
                SELECT r.id, r.request_number, r.equipment_type, r.equipment_model,
                       r.problem_description, r.status, c.full_name
                FROM requests r
                JOIN clients c ON r.client_id = c.id
                WHERE r.specialist_id = ?
            """, (user['id'],))
        else:
            cursor.execute("""
                SELECT r.id, r.request_number, r.equipment_type, r.equipment_model,
                       r.problem_description, r.status, c.full_name
                FROM requests r
                JOIN clients c ON r.client_id = c.id
            """)
        rows = cursor.fetchall()
        return rows
    finally:
        connection.close()

