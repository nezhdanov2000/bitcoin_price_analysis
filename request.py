import requests
import psycopg2
from config import host, port, database, user, password
# ----------------------------------------------------------------------------------------------------------
url = 'https://api.exchangerate.host/timeseries'
parameters = {
    'symbols': 'RUB',
    'base': 'BTC',
    'start_date': 'YYYY-MM-DD',
    'end_date': 'YYYY-MM-DD'
}

# Обновление значений словаря
new_start_date = input("Введите начальную дату формата (2023-07-01): ")
new_end_date = input("Введите конечную дату формата (2023-07-31): ")
parameters['start_date'] = new_start_date
parameters['end_date'] = new_end_date
print()

try:
    response = requests.get(url, params=parameters)
    response.raise_for_status()
    data = response.json()

    # Создаем пустой словарь, в который будем добавлять значения курса биткоина по датам
    bitcoin_rates_by_date = {}
    # Извлекаем значения курса биткоина из ключей 'rates' и сохраняем их в словарь
    for date, rate_info in data['rates'].items():
        bitcoin_rates_by_date[date] = rate_info['RUB']

    bitcoin_rate_during = [
        (date, rate) for date, rate in bitcoin_rates_by_date.items()
    ]

except requests.exceptions.RequestException as e:
    print("Ошибка при выполнении запроса:", e)
except requests.exceptions.JSONDecodeError as e:
    print("Ошибка при разборе JSON:", e)
except KeyError as e:
    print("Ошибка в структуре данных:", e)

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
    drop_table_query = "DROP TABLE IF EXISTS bitcoin_rate_during;"
    cursor.execute(drop_table_query)

    # Создание новой таблицы
    create_table_query = """
        CREATE TABLE IF NOT EXISTS bitcoin_rate_during (
            id SERIAL PRIMARY KEY,
            currency_code VARCHAR(10) NOT NULL,
            rate FLOAT NOT NULL
        );
    """
    cursor.execute(create_table_query)
    print("Таблица 'bitcoin_rate_during' успешно создана.")

    # Вставка данных в таблицу
    insert_query = "INSERT INTO bitcoin_rate_during (currency_code, rate) VALUES (%s, %s);"
    cursor.executemany(insert_query, bitcoin_rate_during)
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