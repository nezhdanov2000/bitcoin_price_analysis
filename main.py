while True:
    print('1 - Создание таблицы курса биткоина за указанный период')
    print('2 - Подключение, анализ данных, создание таблицы результатов')
    print('0 - Завершение работы')
    choice = input('Выберите пункт меню: ')
    if choice == '1':
        import request
    elif choice == '2':
        import analysis
    elif choice == '0':
        break
    else:
        print('Неверный ввод данных!')