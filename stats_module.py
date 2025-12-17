from database import get_connection
from datetime import datetime

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
