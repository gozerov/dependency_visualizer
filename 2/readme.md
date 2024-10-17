Вот пример файла `README.md` на русском языке, который описывает вашу работу и инструкцию по использованию:

```markdown
# Визуализатор зависимостей для пакетов Homebrew

Этот проект представляет собой инструмент командной строки для визуализации графа зависимостей пакетов Homebrew, используя синтаксис Mermaid для отображения графа зависимостей. Программа анализирует зависимости пакетов, включая транзитивные зависимости, и сохраняет результат в виде кода в формате Mermaid.

## Установка и запуск

### Требования

- Python 3.6 или новее
- Homebrew, установленный на вашем устройстве
- Установленный пакет, зависимости которого вы хотите анализировать

### Установка

1. Склонируйте репозиторий или скопируйте файлы проекта в нужную директорию.

2. Убедитесь, что у вас установлен Python. Для проверки версии выполните:

   ```bash
   python3 --version
   ```

3. Установите необходимые зависимости (если они есть) с помощью `pip`:

   ```bash
   pip install -r requirements.txt
   ```

4. Убедитесь, что у вас установлен Homebrew. Если Homebrew не установлен, его можно установить командой:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

### Запуск программы

1. Создайте файл конфигурации в формате JSON, например, `config.json`, который будет содержать следующие параметры:

   ```json
   {
       "package": "curl",
       "max_depth": 2,
       "output_path": "./output.mermaid",
       "visualization_program": "/usr/bin/mermaid",
       "repository_url": "http://archive.ubuntu.com/ubuntu/"
   }
   ```

   - `package`: Имя пакета Homebrew, который вы хотите проанализировать.
   - `max_depth`: Максимальная глубина анализа зависимостей.
   - `output_path`: Путь для сохранения результата в формате Mermaid.
   - `visualization_program`: Путь к программе для визуализации (если есть).
   - `repository_url`: URL-адрес репозитория для получения данных о пакетах.

2. Запустите программу командой:

   ```bash
   python3 dependency_visualizer.py config.json
   ```

3. После выполнения программы результат будет сохранен в указанный файл в формате Mermaid и выведен на экран.

### Запуск тестов

Тесты написаны с использованием библиотеки `unittest`. Чтобы запустить тесты, выполните следующую команду:

```bash
python3 -m unittest discover
```

Это запустит все тесты и проверит корректность работы программы.

## Структура проекта

- `dependency_visualizer.py` — основной скрипт программы для анализа зависимостей пакетов.
- `test.py` — модуль с тестами для проверки функций программы.
- `config.json` — пример конфигурационного файла.
- `output.mermaid` — файл, в который сохраняется результат работы программы в формате Mermaid.

## Пример вывода

Пример вывода графа зависимостей пакета `curl` в формате Mermaid:

```
graph TD
curl --> brotli
curl --> libnghttp2
curl --> libssh2
curl --> openssl@3
curl --> rtmpdump
curl --> zstd
```