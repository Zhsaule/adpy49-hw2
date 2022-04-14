# Домашнее задание к лекции 2.«Regular expressions»
# Ваша задача: починить адресную книгу, используя регулярные выражения.
# Структура данных будет всегда:
# lastname,firstname,surname,organization,position,phone,email
# Предполагается, что телефон и e-mail у человека может быть только один.
# Необходимо:
# 1. поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно.
#    В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О;
# 2. привести все телефоны в формат +7(999)999-99-99. Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999;
# 3. объединить все дублирующиеся записи о человеке в одну.
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re

with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# TODO 1: пункты 1-3 ДЗ
contacts_list_new = list()
name_list = list()
for _row in contacts_list:
    # TODO 1: пункт 1 ДЗ
    __row = " ".join(_row[0:3]).split()
    if len(__row) < 3:
        __row.insert(2, "")
    __row.extend(_row[3:7])
    # TODO 1: пункт 2 ДЗ
    # Удаление символов в телефоне
    __row[5] = re.sub(r"[\s*|\-|\(|\)]", "", _row[5])
    # Приведение к требуемому формату
    __row[5] = re.sub(r"\A\+?[78]\s*(\d{3})\s*(\d{3})\s*(\d{2})\s*(\d{2})", r"+7(\1)\2-\3-\4 ", __row[5]).strip()
    # TODO 1: пункт 3 ДЗ (При полном совпадении Фамилии+Имя = все данные сливаются, без учета Отчества)
    if ' '.join(__row[0:2]).strip() in name_list:
        i = name_list.index(' '.join(__row[0:2]).strip())
        for j in range(2, 7):
            if __row[j].strip() not in contacts_list_new[i][j]:
                contacts_list_new[i][j] = (contacts_list_new[i][j] + ' ' + __row[j]).strip()
    else:
        name_list.append(' '.join(__row[0:2]).strip())
        contacts_list_new.append(__row)

# TODO 2: сохраняем получившиеся данные в другой файл
# код для записи файла в формате CSV
with open('phonebook.csv', 'w', encoding='utf-8', newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list_new)
