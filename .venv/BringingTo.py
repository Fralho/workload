import pandas as pd

# Load both files to analyze their structures
input_file_path = '/Users/kalek/Desktop/Учеба/Информатика/Проект АЯП/formatted_нагрузка.xlsx'


# Load the input and example Excel files
input_data = pd.read_excel(input_file_path)


# Display the first few rows to understand the structure of the input and the desired output
input_data.head()

# Extract necessary columns for transformation
data = input_data.iloc[:, :]  # Take all columns

# Initialize lists to hold the final transformed data
semesters = []
disciplines = []
groups = []
other_columns = []  # Добавляем список для остальных столбцов

# Variables to store current semester and discipline
current_semester = ""
current_group = ""

# Loop through the data to structure it in the required format
for index, row in data.iterrows():
    value = row.iloc[0]
    
    # If it's a semester
    if "семестр" in str(value):
        current_semester = value
    
    # If it's a discipline name (it appears after the semester row)
    elif value.count('-') < 2:  # Проверка на наличие менее двух '-' в строке
        current_group = value
    
    # Otherwise, it's a group name
    else:
        semesters.append(current_semester)
        disciplines.append(current_group)
        groups.append(value)
        other_columns.append(list(row[1:]))  # Сохраняем остальные столбцы в список

# Create a DataFrame with the desired structure
output_data = pd.DataFrame({
    'Семестр': semesters,
    'Дисциплина': disciplines,
    'Группа': groups
})

# Добавляем остальные столбцы в output_data
for i, column_name in enumerate(input_data.columns[1:]):  # Проходим по остальным столбцам
    output_data[column_name] = [row[i] for row in other_columns]  # Добавляем столбец

# Переименовываем нужные столбцы
output_data.rename(columns={output_data.columns[5]: 'Лекции', 
                            output_data.columns[7]: 'Практические', 
                            output_data.columns[8]: 'Лабы'}, inplace=True)

# Удаляем 5 и 7 столбцы
output_data.drop(columns=[output_data.columns[4], output_data.columns[6]], inplace=True)

# Сохраняем
output_file_path = '/Users/kalek/Desktop/Учеба/Информатика/Проект АЯП/transformed_data.xlsx'
output_data.to_excel(output_file_path, index=False)