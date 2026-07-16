# Деплой на PythonAnywhere

Готовые файлы проекта уже собраны — на PythonAnywhere ничего собирать не нужно.
Структура проекта на сервере:

```
python-react-chocolatki/
  backend/
  frontend/dist/
```

## 1. Загрузить проект
Вкладка **Files** → загрузить присланный архив проекта в домашнюю папку.

## 2. Распаковать
Вкладка **Consoles** → **Bash**:
```bash
cd ~
unzip <имя-архива>.zip
```

## 3. Создать виртуальное окружение
На PA надёжнее их встроенный `mkvirtualenv` (обычный `python -m venv` часто
подолгу настраивает pip и кажется зависшим):
```bash
mkvirtualenv --python=/usr/bin/python3.10 chocolatki
```
Подождать ~минуту, не прерывать. Приглашение станет вида `(chocolatki) ~ $`.

Окружение окажется в `/home/ЛОГИН/.virtualenvs/chocolatki`.

> Если `mkvirtualenv: command not found` — тогда `python3.10 -m venv venv` и дать
> ему доработать (30–60 сек, это не зависание); путь окружения тогда
> `/home/ЛОГИН/python-react-chocolatki/backend/venv`.

## 4. Поставить зависимости
```bash
pip install Flask flask-cors python-dotenv
```
На free-тарифе БД — локальный SQLite, поэтому `libsql-experimental` не нужен.

## 5. Создать web app
Вкладка **Web** → **Add a new web app** → **Manual configuration** → **Python 3.10**.

## 6. Настроить web app
- **Virtualenv**: `/home/ЛОГИН/.virtualenvs/chocolatki`
- **WSGI configuration file** (ссылка вверху страницы) → стереть всё, вставить:
  ```python
  import sys
  project = "/home/ЛОГИН/python-react-chocolatki/backend"
  if project not in sys.path:
      sys.path.insert(0, project)
  from app import app as application
  ```
  (везде заменить `ЛОГИН` на свой ник PA)

## 7. Запустить
Зелёная кнопка **Reload** → открыть `ЛОГИН.pythonanywhere.com`.
Страница метрик — `/metrics`.

## База данных

- **Free-тариф:** всё пишется в файл `backend/dev.db` на диске PA. Настраивать
  ничего не нужно — работает само.
- **Turso:** нужен платный тариф (на free-тарифе закрыт исходящий интернет).
  Тогда: `pip install libsql-experimental`, задать `TURSO_DATABASE_URL` и
  `TURSO_AUTH_TOKEN` (в WSGI-файле через `os.environ` или в `backend/.env`).

## Обновление сайта

Загрузить новую версию проекта, распаковать с заменой файлов и нажать **Reload**.
