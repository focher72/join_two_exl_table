#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Программа для объединения двух CSV-файлов по колонке "client_id"
"""

import csv
import argparse
import os
from datetime import datetime


def parse_arguments():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description='Объединение CSV-файлов по указанной колонке'
    )
    parser.add_argument(
        'table_a',
        help='Путь к файлу table_a.csv'
    )
    parser.add_argument(
        'table_b',
        help='Путь к файлу table_b.csv'
    )
    parser.add_argument(
        '--join-column', '-j',
        required=True,
        help='Название колонки для соединения таблиц (обязательный параметр)'
    )
    return parser.parse_args()


def check_files_exist(table_a_path, table_b_path):
    """Проверка существования входных файлов"""
    if not os.path.exists(table_a_path):
        print(f"Ошибка: Файл {table_a_path} не существует")
        exit(1)
    
    if not os.path.exists(table_b_path):
        print(f"Ошибка: Файл {table_b_path} не существует")
        exit(1)


def read_csv_file(file_path):
    """Чтение CSV-файла и возврат данных"""
    try:
        with open(file_path, 'r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames
            data = list(reader)
            return headers, data
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        exit(1)


def validate_join_column(headers_a, headers_b, join_column, file_a_path, file_b_path):
    """Проверка наличия указанной колонки для соединения в обоих файлах (регистронезависимо)"""
    # Поиск колонки в headers_a с учетом регистра
    column_a = None
    for header in headers_a:
        if header.lower() == join_column.lower():
            column_a = header
            break
    
    if column_a is None:
        print(f'Ошибка: Колонка "{join_column}" не найдена в файле {file_a_path}')
        exit(1)
    
    # Поиск колонки в headers_b с учетом регистра
    column_b = None
    for header in headers_b:
        if header.lower() == join_column.lower():
            column_b = header
            break
    
    if column_b is None:
        print(f'Ошибка: Колонка "{join_column}" не найдена в файле {file_b_path}')
        exit(1)
    
    # Возвращаем найденные названия колонок из обоих файлов
    print(f'Найдена колонка для соединения: "{column_a}"')
    return column_a, column_b


def generate_output_filename():
    """Генерация имени выходного файла с текущей датой"""
    current_date = datetime.now().strftime("%Y-%m-%d")
    return f"merge_csv_{current_date}.csv"


def merge_data(data_a, data_b, headers_a, headers_b, join_column_a, join_column_b):
    """Объединение данных из двух таблиц по указанной колонке"""
    # Создаем словарь для хранения записей из table_b по указанной колонке
    # Ключ - значение join_column, значение - список записей с этим значением
    table_b_by_column = {}
    
    for row in data_b:
        column_value = row[join_column_b]
        if column_value not in table_b_by_column:
            table_b_by_column[column_value] = []
        table_b_by_column[column_value].append(row)
    
    # Объединяем заголовки
    all_headers = headers_a + [col for col in headers_b if col != join_column_b]
    
    # Объединяем данные
    merged_data = []
    
    for row_a in data_a:
        column_value = row_a[join_column_a]
        
        if column_value in table_b_by_column:
            # Если есть записи в table_b для этого значения колонки
            for row_b in table_b_by_column[column_value]:
                # Создаем объединенную запись
                merged_row = {}
                # Добавляем колонки из table_a
                for col in headers_a:
                    merged_row[col] = row_a[col]
                # Добавляем колонки из table_b (кроме join_column)
                for col in headers_b:
                    if col != join_column_b:
                        merged_row[col] = row_b[col]
                merged_data.append(merged_row)
        else:
            # Если нет записей в table_b для этого значения колонки
            # Создаем запись с пустыми значениями для колонок table_b
            merged_row = {}
            # Добавляем колонки из table_a
            for col in headers_a:
                merged_row[col] = row_a[col]
            # Добавляем пустые колонки из table_b (кроме join_column)
            for col in headers_b:
                if col != join_column_b:
                    merged_row[col] = ''
            merged_data.append(merged_row)
    
    return merged_data, all_headers


def write_csv_file(file_path, data, headers):
    """Запись данных в CSV-файл"""
    try:
        with open(file_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        print(f"Результат сохранен в файл: {file_path}")
    except Exception as e:
        print(f"Ошибка при записи файла {file_path}: {e}")
        exit(1)


def main():
    """Основная функция программы"""
    # Парсинг аргументов
    args = parse_arguments()
    
    # Проверка существования файлов
    check_files_exist(args.table_a, args.table_b)
    
    # Чтение CSV-файлов
    print(f"Чтение файла {args.table_a}...")
    headers_a, data_a = read_csv_file(args.table_a)
    
    print(f"Чтение файла {args.table_b}...")
    headers_b, data_b = read_csv_file(args.table_b)
    
    # Проверка наличия указанной колонки для соединения
    join_column_a, join_column_b = validate_join_column(headers_a, headers_b, args.join_column, args.table_a, args.table_b)
    
    print("Объединение данных...")
    merged_data, all_headers = merge_data(data_a, data_b, headers_a, headers_b, join_column_a, join_column_b)
    
    # Генерация имени выходного файла
    output_filename = generate_output_filename()
    
    # Запись результата
    write_csv_file(output_filename, merged_data, all_headers)
    
    print(f"Обработка завершена. Обработано {len(merged_data)} записей.")


if __name__ == "__main__":
    main()