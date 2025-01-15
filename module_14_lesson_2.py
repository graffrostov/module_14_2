import sqlite3

# Соединяемся с базой данных
connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

# --------------------------------------------------------------------------------------------------------
# Если таблица не существует, то создаём её согласно определённой структуре
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL, 
age INTEGER,
balance INTEGER NOT NULL)
""")

# --------------------------------------------------------------------------------------------------------
# Удаляем все данные от предыдущего запуска
cursor.execute("DELETE FROM Users")

# --------------------------------------------------------------------------------------------------------
# Заполняем таблицу данными согласно задания
for i in range(1, 11):
    cursor.execute("""
    INSERT INTO Users
     (username,
      email,
      age,
      balance)

      VALUES
      (?, ?, ?, ?)
      """,

                   (f"User{i}",
                    f"example{i}@gmail.com",
                    i * 10,
                    1000))

# --------------------------------------------------------------------------------------------------------

# Делаем выборку всех записей и распечатываем их

# cursor.execute("SELECT * FROM Users")
# users = cursor.fetchall()
#
# print('В базе данных созданы следующие записи:')
#
# for user in users:
#     id, username, email, age, balance = user
#     print(f'ID: {id} | Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}')

# --------------------------------------------------------------------------------------------------------
# Меняем баланс у каждой второй записи
cursor.execute('SELECT COUNT(*) FROM Users')
total_users = cursor.fetchone()[0]

for i in range(1, total_users + 1, 2):
    cursor.execute('UPDATE Users SET balance = ? WHERE id = ?', (500, i))

# cursor.execute("SELECT * FROM Users")
# users = cursor.fetchall()
#
# print()
# print('У каждой второй записи изменён баланс на 500:')
#
# for user in users:
#     id, username, email, age, balance = user
#     print(f'ID: {id} | Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}')

# --------------------------------------------------------------------------------------------------------
# Удаляем каждую 3 запись
for i in range(1, total_users + 1, 3):
    cursor.execute('DELETE FROM Users WHERE id = ?', (i,))

# cursor.execute("SELECT * FROM Users")
# users = cursor.fetchall()
#
# print()
# print('Удалена каждая 3 запись, начиная с первой:')
# for user in users:
#     id, username, email, age, balance = user
#     print(f'ID: {id} | Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}')

# --------------------------------------------------------------------------------------------------------
# Делаем выборку во возрасту
cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != ?", (60,))
# users = cursor.fetchall()
#
# print()
# print('Сделана выборка из оставшихся, чей возраст не равен 60:')
#
# for user in users:
#     username, email, age, balance = user
#     print(f'Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}')

# --------------------------------------------------------------------------------------------------------
# Удаляем запись с id=6
cursor.execute('DELETE FROM Users WHERE id = 6')

# Считаем количество оставшихся записей
cursor.execute('SELECT COUNT(*) FROM Users')
total_users = cursor.fetchone()[0]

# Считаем общий баланс пользователей
cursor.execute('SELECT SUM(balance) FROM Users')
all_balances = cursor.fetchone()[0]

# Выводим средний баланс
print(all_balances / total_users)

# Фиксируем изменения и закрываем соединение с базой данных
connection.commit()
connection.close()