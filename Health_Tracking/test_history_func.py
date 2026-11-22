import sqlite3
import json

conn = sqlite3.connect('my_db.db')
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS mixed_data (id INTEGER PRIMARY KEY, data TEXT)')

# Смешанный массив с разными типами
my_mixed_array = [42,"Hello, World!", True,  None,[1, 2, 3],{"name": "Alice", "age": 30}]

# Сохраняем в JSON
json_string = json.dumps(my_mixed_array, ensure_ascii=False)
cursor.execute("INSERT INTO mixed_data (data) VALUES (?)", (json_string,))
conn.commit()

# Читаем обратно
cursor.execute("SELECT data FROM mixed_data WHERE id=1")
row = cursor.fetchone()
restored_array = json.loads(row[0])

print(restored_array)
# [42, 'Hello, World!', True, None, [1, 2, 3], {'name': 'Alice', 'age': 30}]
print(type(restored_array))  # <class 'list'>
print(restored_array[3])     # None (сохранился корректно)