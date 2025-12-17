def start_interface():
    print("=== Добро пожаловать в систему учёта заявок ===")
    while True:
        choice = input("1 - Вход, 2 - Регистрация, 0 - Выход: ").strip()
        if choice == "1":
            username = input("Логин: ")
            password = input("Пароль: ")
            user = login_user(username, password)
            if user:
                print(f"Успешный вход! Ваша роль: {user['role']}")
                main_menu(user)
                break
            else:
                print("Неверный логин или пароль")
        elif choice == "2":
            username = input("Логин: ")
            password = input("Пароль: ")
            role = input("Роль (admin/operator/specialist): ")
            user_id = register_user(username, password, role)
            if user_id:
                print("Регистрация прошла успешно")
            else:
                print("Ошибка регистрации, возможно такой логин уже есть")
        elif choice == "0":
            print("Выход")
            break
        else:
            print("Неверный выбор")
