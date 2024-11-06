import sqlite3
import pandas as pd

# Загрузка файла Excel
file_path = '/Users/kalek/Desktop/Учеба/Информатика/Проект АЯП/transformed_data.xlsx' 
data = pd.read_excel(file_path)

# Подключение к базе данных SQLite
conn = sqlite3.connect('/Users/kalek/Desktop/Учеба/Информатика/Проект АЯП/database.db')
cursor = conn.cursor()

# Создание таблицы "Семестры"
cursor.execute('''
CREATE TABLE IF NOT EXISTS Семестры (
    id_семестра INTEGER PRIMARY KEY AUTOINCREMENT,
    название_семестра TEXT UNIQUE
)
''')

# Создание таблицы "Дисциплины"
cursor.execute('''
CREATE TABLE IF NOT EXISTS Дисциплины (
    id_дисциплины INTEGER PRIMARY KEY AUTOINCREMENT,
    название_дисциплины TEXT,
    id_семестра INTEGER,
    FOREIGN KEY (id_семестра) REFERENCES Семестры(id_семестра)
)
''')

# Создание таблицы "Группы" с дополнительными столбцами
cursor.execute('''
CREATE TABLE IF NOT EXISTS Группы (
    id_группы INTEGER PRIMARY KEY AUTOINCREMENT,
    название_группы TEXT,
    id_дисциплины INTEGER,
    "Сту\nден\nтов" INTEGER,
    Лекции REAL,
    Практические REAL,
    Лабы REAL,
    "Курс\nработа" REAL,
    "Курс\nпроект" REAL,
    "К\nо\nн\nс" REAL,
    "Р\nе\nй\nт\nи\nн\nг" REAL,
    "З\nа\nч\nё\nт" REAL,
    "Э\nк\nз\nа\nм" REAL,
    "С\nР\nС" REAL,
    "Прак\nтика" REAL,
    "Д\nи\nп\nл\nо\nм" REAL,
    "П\nр\nо\nч\nе\nе" REAL,
    "В\nс\nе\nг\nо" INTEGER,
    FOREIGN KEY (id_дисциплины) REFERENCES Дисциплины(id_дисциплины)
)
''')

# Вставка данных в таблицы "Семестры", "Дисциплины" и "Группы"
for index, row in data.iterrows():
    # Вставка в "Семестры"
    cursor.execute('''
    INSERT OR IGNORE INTO Семестры (название_семестра)
    VALUES (?)
    ''', (row['Семестр'],))
    
    # Получение id_семестра
    cursor.execute('''
    SELECT id_семестра FROM Семестры WHERE название_семестра = ?
    ''', (row['Семестр'],))
    id_семестра = cursor.fetchone()[0]
    
    # Вставка в "Дисциплины"
    cursor.execute('''
    INSERT OR IGNORE INTO Дисциплины (название_дисциплины, id_семестра)
    VALUES (?, ?)
    ''', (row['Дисциплина'], id_семестра))
    
    # Получение id_дисциплины
    cursor.execute('''
    SELECT id_дисциплины FROM Дисциплины WHERE название_дисциплины = ? AND id_семестра = ?
    ''', (row['Дисциплина'], id_семестра))
    id_дисциплины = cursor.fetchone()[0]
    
    # Вставка в "Группы"
    cursor.execute('''
    INSERT INTO Группы (название_группы, id_дисциплины, "Сту\nден\nтов", Лекции, Практические, Лабы, "Курс\nработа", 
                        "Курс\nпроект", "К\nо\nн\nс", "Р\nе\nй\nт\nи\nн\nг", "З\nа\nч\nё\nт", "Э\nк\nз\nа\nм", "С\nР\nС", 
                        "Прак\nтика", "Д\nи\nп\nл\nо\nм", "П\nр\nо\nч\nе\nе", "В\nс\nе\nг\nо")
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        row['Группа'], id_дисциплины, row['Сту\nден\nтов'], row['Лекции'], row['Практические'], row['Лабы'],
        row['Курс\nработа'], row['Курс\nпроект'], row['К\nо\nн\nс'], row['Р\nе\nй\nт\nи\nн\nг'], row['З\nа\nч\nё\nт'],
        row['Э\nк\nз\nа\nм'], row['С\nР\nС'], row['Прак\nтика'], row['Д\nи\nп\nл\nо\nм'], row['П\nр\nо\nч\nе\nе'],
        row['В\nс\nе\nг\nо']
    ))

# Подтверждение изменений и закрытие соединения
conn.commit()
conn.close()