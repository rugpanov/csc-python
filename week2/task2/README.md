## Форматирование и файлы

**Краткое описания:**

Выполнение форматирование файла на псевдо-латыни.
Функция:
- читает из input_file (например, из sys.stdin)
- и выводит в output_file (например, в sys.stdout)
- абзацы заявленной ширины desired_width,
- выполняя переносы латинских слов по слогам, если use_hyphens = True,
- расширяя пробелы, если expand_spaces = True