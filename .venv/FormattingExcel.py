import pandas as pd

start_1={
    'Осенний семестр': 1, 
}
start_2={
    'Весенний семестр': 1, 
}

stop_marker_1 = {
  'Факультет 1': 0,
  'очная форма обучения, Бакалавриат': 0,
  'очная форма обучения, Специализированное высшее образование': 0,
  'очная форма обучения, Специалитет': 0,
  'Факультет 3': 0,
  'очная форма обучения, Аспирантура': 0,
  'очная форма обучения, Базовое высшее образование': 0,
  'Факультет 6': 0,
  'Факультет 7': 0,
  'очно-заочная форма обучения, Специалитет': 0,
  'Факультет 9': 0,
  'Весенний семестр': 0
}

stop_marker_2 = {
  'Факультет 1': 0,
  'очная форма обучения, Бакалавриат': 0,
  'очная форма обучения, Специализированное высшее образование': 0,
  'очная форма обучения, Специалитет': 0,
  'Факультет 3': 0,
  'очная форма обучения, Аспирантура': 0,
  'очная форма обучения, Базовое высшее образование': 0,
  'Факультет 6': 0,
  'Факультет 7': 0,
  'очно-заочная форма обучения, Специалитет': 0,
  'Факультет 9': 0,
  'Осенний семестр': 0
}


def format_excel_file(filename, start_1, start_2, stop_marker_1, stop_marker_2):

  # Загрузка Excel файла в DataFrame
  df = pd.read_excel(filename, skiprows = 6)
  
  columns_to_drop = [i for i in range(1, 14)] + [15, 17, 19, 22, 23, 25, 27, 29, 30, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 50, 51]
    
  num_rows = df.shape[0]
  formatted_rows = [] # Список для хранения отформатированных строк
  
  in_block = False # Начало блока
  is_marker = False
  
  for index in range(num_rows):
   
    current_row = df.iloc[index]
    current_value = current_row[df.columns[0]] # Значение в первом столбце

    if current_value in start_1:
      in_block = True # Начало блока
      if is_marker == False:
        formatted_rows.append(current_row.tolist()) # Добавляем строку с start_marker
        is_marker = True
      continue

    if current_value in stop_marker_1:
      in_block = False # Конец блока
      continue # Пропускаем строку с stop_marker или пустую строку

    if in_block: # Записываем строку, если находимся в блоке
      if pd.isnull(current_value):
        continue
      formatted_rows.append(current_row.tolist())
  
  in_block = False
  is_marker = False
  
  for index in range(num_rows):
   
    current_row = df.iloc[index]
    current_value = current_row[df.columns[0]] # Значение в первом столбце

    if current_value in start_2:
      in_block = True # Начало блока
      if is_marker == False:
        formatted_rows.append(current_row.tolist()) # Добавляем строку с start_marker
        is_marker = True
      continue

    if current_value in stop_marker_2:
      in_block = False # Конец блока
      continue # Пропускаем строку с stop_marker или пустую строку

    if in_block: # Записываем строку, если находимся в блоке
      if pd.isnull(current_value):
        continue
      formatted_rows.append(current_row.tolist())
      

  # Создание DataFrame из отформатированных данных
  formatted_df = pd.DataFrame(formatted_rows, columns=df.columns)
  
  for index, row in formatted_df.iterrows():
    # Assuming group names have a specific format (with hyphens) and are not NaN
    if isinstance(row['Unnamed: 0'], str) and row['Unnamed: 0'].count('-') >= 2:
        # Check the conditions: column 15 > 20 and column 25 < 20
      if row[formatted_df.columns[14]] > 20 and row[formatted_df.columns[24]] < 20:
          print("Ошибка несоотсвие нагрузки лабораторных в ",index+2, "строке. Проверить на несоответсвие количества нагрузки у лабораторных работ")
          
          
  column_17 = formatted_df.columns[16]  # 17th column (index 16 in Python)
  # Initialize variables
  current_discipline = None
  first_group_value = None
  error_messages = []

  # Loop through the data to process each block of groups
  for index, row in formatted_df.iterrows():
    first_column_value = row['Unnamed: 0']
    
    # Check if the row is a new semester or discipline
    if isinstance(first_column_value, str) and ("семестр" in first_column_value.lower() or first_column_value.count('-') < 2):
        # Reset discipline and first group value for a new block
        current_discipline = first_column_value
        first_group_value = None  # Reset the comparison value for a new block
    
    # Process group rows within the same discipline
    elif current_discipline and isinstance(first_column_value, str) and first_column_value.count('-') >= 2:
        # Capture the first group's value in column 17 as the comparison reference
        if first_group_value is None:
            first_group_value = row[column_17]  # Store the first group's 17th column value for comparison
        
        # Compare subsequent group's column 17 values within the same block
        elif pd.notna(row[column_17]) and row[column_17] != first_group_value:
          print(f"Ошибка, непраивльно разделение потоков. Проверьте {index + 2} строку")        
    
      
  formatted_df.drop(df.columns[columns_to_drop], axis=1, inplace=True)


  return formatted_df

filename = '/Users/kalek/Desktop/Учеба/Информатика/Проект АЯП/Нагрузка кафедра.xlsx'

formatted_df = format_excel_file(filename, start_1, start_2, stop_marker_1, stop_marker_2 )

# Сохранение отформатированного DataFrame в новый файл Excel
formatted_df.to_excel('formatted_нагрузка.xlsx', index=False)

#print(grouped_data)