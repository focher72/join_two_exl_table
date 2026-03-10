# Программа объединения CSV-файлов

Программа для объединения двух CSV-файлов по указанной колонке с использованием только стандартной библиотеки Python 3.12.

## Требования

- Python 3.12
- Только стандартная библиотека (никаких сторонних зависимостей)

## Использование

```bash
python merge_csv.py table_a.csv table_b.csv --join-column НАЗВАНИЕ_КОЛОНКИ
```

### Обязательные аргументы

- `table_a.csv` - путь к первому CSV-файлу (основной)
- `table_b.csv` - путь ко второму CSV-файлу
- `--join-column` (или `-j`) - название колонки для соединения таблиц

## Примеры

### Объединение по колонке client_id

```bash
python merge_csv.py table_a.csv table_b.csv --join-column client_id
```

или с коротким вариантом:

```bash
python merge_csv.py table_a.csv table_b.csv -j client_id
```

### Объединение по другой колонке

```bash
python merge_csv.py users.csv orders.csv --join-column user_id
```

## Выходные данные

Программа создает файл с именем формата: `merge_csv_YYYY-MM-DD.csv` в текущей директории.

## Особенности работы

- **Дубликаты**: Если в table_b.csv несколько записей с одинаковым значением колонки соединения, записи из table_a.csv дублируются
- **Отсутствующие записи**: Если в table_b.csv нет записей с определенным значением колонки, в результирующем файле для этих колонок будут пустые значения
- **Все колонки**: В выходном файле сохраняются все колонки из обеих таблиц (кроме колонки соединения из table_b.csv)

## Ошибки и обработка

### Колонка не найдена

```bash
python merge_csv.py table_a.csv table_b.csv --join-column nonexistent_column
# Ошибка: Колонка "nonexistent_column" не найдена в table_a.csv
```

### Обязательный параметр

```bash
python merge_csv.py table_a.csv table_b.csv
# usage: merge_csv.py [-h] --join-column JOIN_COLUMN table_a table_b
# merge_csv.py: error: the following arguments are required: --join-column/-j
```

## Безопасность

Программа проверяет существование входных файлов и указанной колонки, что предотвращает распространенные ошибки при работе с CSV-файлами.