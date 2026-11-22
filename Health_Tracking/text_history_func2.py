import sqlite3

conn = sqlite3.connect('my_db.db')
cursor = conn.cursor()

# Создаем таблицу
cursor.execute('CREATE TABLE IF NOT EXISTS test_table (id INTEGER PRIMARY KEY, name TEXT, age TEXT NOT NULL)')

# Пытаемся прочитать данные, хотя мы ничего не вставляли
cursor.execute("INSERT INTO test_table (name) VALUES (?)", ("Петя",))
conn.commit()
cursor.execute("SELECT * FROM test_table")
row = cursor.fetchall()

print(row)  # None