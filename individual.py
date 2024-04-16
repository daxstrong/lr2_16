#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from datetime import datetime


def exit_program():
    """
    Выход из программы.
    """
    sys.exit()


def add_person(people):
    """
    Добавление информации о человеке.
    """
    last_name = input("Фамилия: ")
    first_name = input("Имя: ")
    phone_number = input("Номер телефона: ")
    birthdate_str = input("Дата рождения (в формате ДД.ММ.ГГГГ): ")
    birthdate = datetime.strptime(birthdate_str, "%d.%m.%Y")

    person = {
        'фамилия': last_name,
        'имя': first_name,
        'номер телефона': phone_number,
        'дата рождения': birthdate,
    }

    people.append(person)
    people.sort(key=lambda x: x['фамилия'])


def list_people(people):
    """
    Вывод списка всех людей.
    """
    line = f'+-{"-" * 25}-+-{"-" * 15}-+-{"-" * 25}-+'
    print(line)
    print(f"| {'Фамилия':^25} | {'Имя':^15} | {'Дата рождения':^25} |")

    for person in people:
        print(line)
        print(f"| {person['фамилия']:^25} | {person['имя']:^15} | {person['дата рождения'].strftime('%d.%m.%Y'):^25} |")
    print(line)


def select_people_by_month(people, month_to_search):
    """
    Вывод людей с днем рождения в указанном месяце.
    """
    found = False

    print(f"Люди с днем рождения в месяце {month_to_search}:")
    for person in people:
        if person['дата рождения'].month == month_to_search:
            print(
                f"Фамилия: {person['фамилия']}, Имя: {person['имя']}, Дата рождения: {person['дата рождения'].strftime('%d.%m.%Y')}")
            found = True

    if not found:
        print("Нет людей с днем рождения в указанном месяце.")


def help_info():
    """
    Вывод справочной информации о командах.
    """
    print("Список команд:\n")
    print("add - добавить информацию о человеке;")
    print("list - вывести список всех людей;")
    print("select <месяц> - вывести людей с днем рождения в указанном месяце;")
    print("save - сохранить данные в файл JSON;")
    print("load - загрузить данные из файла JSON;")
    print("exit - завершить работу с программой.")


def save_people(file_name, people):
    """
    Сохранить всех людей в файл JSON.
    """
    # Преобразуем объекты datetime в строки
    for person in people:
        person['дата рождения'] = person['дата рождения'].strftime('%d.%m.%Y')

    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(people, fout, ensure_ascii=False, indent=4)


def load_people(file_name):
    """
    Загрузить всех людей из файла JSON.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as fin:
            people_data = json.load(fin)
            for person in people_data:
                person['дата рождения'] = datetime.strptime(person['дата рождения'], '%d.%m.%Y')
            return people_data
    except FileNotFoundError:
        return []


if __name__ == '__main__':
    file_name = 'people.json'  # Имя файла для сохранения данных

    people = load_people(file_name)

    while True:
        command = input(">>> ").lower()

        match command:
            case 'exit':
                save_people(file_name, people)  # Сохраняем данные перед выходом
                exit_program()
            case 'add':
                add_person(people)
            case 'list':
                list_people(people)
            case command if command.startswith('select '):
                month_to_search = int(command.split(' ')[1])
                select_people_by_month(people, month_to_search)
            case command if command.startswith('save '):
                save_file_name = command.split(' ')[1]
                save_people(save_file_name, people)
            case command if command.startswith('load '):
                load_file_name = command.split(' ')[1]
                people = load_people(load_file_name)
            case 'help':
                help_info()
            case _:
                print(f"Неизвестная команда {command}", file=sys.stderr)
