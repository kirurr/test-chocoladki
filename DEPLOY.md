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
Подождать ~минуту, не прерывать. Когда окружение создано и активно, в начале
строки в консоли появится префикс `(chocolatki)`.

Окружение окажется в `/home/ЛОГИН/.virtualenvs/chocolatki`.

> Если `mkvirtualenv: command not found` — создать окружение вручную и активировать:
> ```bash
> cd ~/python-react-chocolatki/backend
> python3.10 -m venv venv
> source venv/bin/activate
> ```
> (создание может занять 30–60 сек, это не зависание). Путь окружения тогда
> `/home/ЛОГИН/python-react-chocolatki/backend/venv` — его же указать в шаге 6.

## 4. Поставить зависимости
```bash
cd ~/python-react-chocolatki/backend
pip install -r requirements.txt
```

## 5. Создать web app
Вкладка **Web** → **Add a new web app** → **Manual configuration** → **Python 3.10**.

## 6. Настроить web app
- **Virtualenv**: `/home/ЛОГИН/.virtualenvs/chocolatki`
  (если ставил через fallback — `/home/ЛОГИН/python-react-chocolatki/backend/venv`)
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

Всё пишется в файл `backend/dev.db` (SQLite) прямо на диске PA. Настраивать
ничего не нужно — работает само.

## Обновление сайта

Загрузить новую версию архива, распаковать с заменой файлов (`unzip -o <архив>.zip`)
и нажать **Reload**.
