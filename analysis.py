import psycopg2
from config import host, port, database, user, password
# ----------------------------------------------------------------------------------------------------------

# Подключение к БД
try:
    # Установка соединения с БД
    connection = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

    # Создание курсора
    cursor = connection.cursor()

    # SQL-запрос для выборки данных
    query = "SELECT * FROM bitcoin_rate_during;"  # Замените "your_table" на имя вашей таблицы

    # Выполнение SQL-запроса
    cursor.execute(query)

    # Получение результатов
    rows = cursor.fetchall()

    data = []

    # Вывод полученных данных
    for row in rows:
        # print(row) ЗДЕСЬ ВЫВОДЯТСЯ КУРСЫ
        data += tuple(row)

    # Закрытие курсора и соединения
    cursor.close()
    connection.close()

except (Exception, psycopg2.Error) as error:
    print("Ошибка при работе с PostgreSQL:", error)

# ----------------------------------------------------------------------------------------------------------

# Инициализация переменных для хранения максимального значения курса и соответствующего дня
max_value = None
day = None

# Перебор элементов списка с шагом 3 (потому что у вас данные кортежей вида [номер, дата, значение])
for i in range(2, len(data), 3):
    # Получение значения курса из текущего кортежа
    value = data[i]

    # Сравнение с текущим максимальным значением
    if max_value is None or value > max_value:
        max_value = value
        day = data[i - 1]  # День соответствующий этому значению

print("\n"f"День с максимальным значением курса: {day}")
max_value_date=day
print(f"Максимальное значение курса: {max_value}""\n")
max_value=max_value
# ----------------------------------------------------------------------------------------------------------

# Инициализация переменных для хранения максимального значения курса и соответствующего дня
min_value = None
day = None

# Перебор элементов списка с шагом 3 (потому что у вас данные кортежей вида [номер, дата, значение])
for i in range(2, len(data), 3):
    # Получение значения курса из текущего кортежа
    value = data[i]

    # Сравнение с текущим максимальным значением
    if min_value is None or value < min_value:
        min_value = value
        day = data[i - 1]  # День соответствующий этому значению

print(f"День с минимальным значением курса: {day}")
min_value_date=day
print(f"Минимальное значение курса: {min_value}""\n")
min_value=min_value
# ----------------------------------------------------------------------------------------------------------

# Инициализация переменных для хранения максимального значения курса и соответствующего дня
sum_values = 0
amount = len(data)

# Перебор элементов списка с шагом 3 (потому что у вас данные кортежей вида [номер, дата, значение])
for i in range(2, len(data), 3):
    sum_values += data[i]
print(f"Среднее значение курса за интервал: ", sum_values / (len(data)//3))
average_value=sum_values / (len(data)//3)
# ----------------------------------------------------------------------------------------------------------
last_date_value=data[len(data)-1]
print("\n"f"Значение курса биткоина на последний день месяца: ", data[len(data)-1])
# ----------------------------------------------------------------------------------------------------------

try:
    # Подключение к PostgreSQL
    connection = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

    # Установка уровня изоляции транзакций в "AUTOCOMMIT"
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    # Создание объекта-курсора
    cursor = connection.cursor()

    # Удаление таблицы, если она существует
    drop_table_query = "DROP TABLE IF EXISTS main_table;"
    cursor.execute(drop_table_query)

    # Создание новой таблицы
    create_table_query = """
        CREATE TABLE IF NOT EXISTS main_table (
        id SERIAL PRIMARY KEY,
        max_value_date VARCHAR(10) NOT NULL,
        max_value FLOAT NOT NULL,
        min_value_date VARCHAR(10) NOT NULL,
        min_value FLOAT NOT NULL,
        average_value FLOAT NOT NULL,
        last_date_value FLOAT NOT NULL
        );
    """

    cursor.execute(create_table_query)
    print("Таблица 'main_table' успешно создана.")

    # Вставка данных в таблицу
    insert_query = "INSERT INTO main_table (max_value_date, max_value, min_value_date, min_value, average_value, last_date_value) VALUES (%s, %s, %s, %s, %s, %s);"

    data_to_insert = (max_value_date, max_value, min_value_date, min_value, average_value, last_date_value)
    cursor.execute(insert_query, data_to_insert)

    connection.commit()

    print("Данные успешно сохранены в базу данных.", "\n")

except (Exception, psycopg2.Error) as error:
    print("Ошибка при работе с PostgreSQL:", error)

finally:
    # Закрытие соединения
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто.")

print('=======================================================================')