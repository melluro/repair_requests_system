from models import create_tables
from services import (
    add_client, add_request, get_all_requests,
    update_request_status, assign_specialist,
    add_specialist, complete_request
)
from stats_module import calculate_statistics
from datetime import datetime, timedelta

# Создаём таблицы
create_tables()

# Добавляем клиента
client_id = add_client("Иванов Иван Иванович", "+79991234567")

# Добавляем заявку (уникальный номер)
add_request("REQ-004", "Кондиционер", "LG S09", "Не включается", client_id)

# Добавляем специалиста
specialist_id = add_specialist("Петров Петр Петрович", "Кондиционеры")

# Просмотр списка заявок до изменений
print("Список заявок до изменений:")
requests = get_all_requests()
for request in requests:
    print(request)

# Изменяем статус заявки
update_request_status("REQ-004", "В процессе ремонта")

# Назначаем специалиста
assign_specialist("REQ-004", specialist_id)

# Завершаем заявку (пример: ремонт длился 3 дня)
start = datetime.now() - timedelta(days=3)
end = datetime.now()
complete_request("REQ-004", start.isoformat(), end.isoformat())

# Просмотр списка заявок после изменений
print("\nСписок заявок после изменений:")
requests = get_all_requests()
for request in requests:
    print(request)

# Расчёт статистики
stats = calculate_statistics()
print("\nСтатистика по завершённым заявкам:")
print(f"Количество выполненных заявок: {stats['completed_count']}")
print(f"Среднее время ремонта (дней): {stats['average_days']:.2f}")
print("Статистика по типам неисправностей:")
for problem, count in stats['problem_types'].items():
    print(f"  {problem}: {count}")
