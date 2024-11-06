def group_data_by_symbol(df):
  
 grouped_data = {}
 current_discipline = None
 first_group = None # Первая группа в блоке дисциплины
 first_group_data = {} # Данные первой группы каждой дисциплины
 other_group_data = {} # Данные групп с разными 7, 8, 9 символами

 for index in range(len(df)):
  row = df.iloc[index]
  value = row.iloc[0] # Значение в первом столбце

  # Пропускаем строку, если она содержит 'Осенний семестр'
  #if value == ('Осенний семестр' or 'Весенний семестр'):
  # continue

  
  if value.startswith('М') or value.startswith('M') and value != 'Осенний семестр':
   # Название группы
   if current_discipline is None:
    # Если предыдущей дисциплины не было, записываем текущую
    if index > 0: # Проверяем, есть ли предыдущая строка
     current_discipline = df.iloc[index - 1].iloc[1] # Используйте iloc для получения названия дисциплины из второго столбца
    else:
     # Если это первая строка, то нет предыдущей дисциплины
     continue

   if first_group is None:
    # Запоминаем первую группу в блоке дисциплины
    first_group = value
    first_group_data[current_discipline] = {first_group: row.iloc[2]}

   symbol_group = value[7:10]
   if symbol_group == first_group[7:10]:
    # Группа совпадает по 7, 8, 9 символам с первой группой
    first_group_data[current_discipline][value] = row.iloc[2]
   else:
    # Группа отличается по 7, 8, 9 символам, создаем новый словарь для нее
    if current_discipline not in other_group_data:
     other_group_data[current_discipline] = {}
    other_group_data[current_discipline][value] = row.iloc[2]

  else:
   # Название дисциплины
   if current_discipline is not None:
    # Добавляем группы текущей дисциплины в общий словарь
    if current_discipline in first_group_data: # Проверяем, есть ли данные для текущей дисциплины
     grouped_data[current_discipline].append(first_group_data[current_discipline])
    if current_discipline in other_group_data:
     grouped_data[current_discipline].append(other_group_data[current_discipline])
   # Получаем текущую дисциплину из строки
   current_discipline = value 
   grouped_data[current_discipline] = [] # Создаем новый список для новой дисциплины
   first_group = None # Сбрасываем первую группу
   first_group_data = {} # Сбрасываем словарь данных первой группы
   other_group_data = {} # Сбрасываем словарь данных групп с разными символами

 # Добавляем группы последней дисциплины
 if current_discipline is not None:
  if current_discipline in first_group_data: # Проверяем, есть ли данные для текущей дисциплины
   grouped_data[current_discipline].append(first_group_data[current_discipline])
  if current_discipline in other_group_data:
   grouped_data[current_discipline].append(other_group_data[current_discipline])

# Обновляем значения в группах, присваивая максимальное значение
 for discipline, groups_list in grouped_data.items():
  for group_dict in groups_list:
   max_value = max(group_dict.values()) # Находим максимальное значение в словаре
   for group_name, value in group_dict.items():
    group_dict[group_name] = max_value # Присваиваем максимальное значение всем группам
 return grouped_data
