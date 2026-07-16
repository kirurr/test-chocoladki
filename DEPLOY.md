# Деплой на PythonAnywhere

Фронт собирается локально, на сервер заливаются готовые файлы — на PythonAnywhere
ничего собирать не нужно. На сервере достаточно двух папок: `backend/` и
`frontend/dist/`. Итоговая структура на PA:

```
python-react-chocolatki/
  backend/
  frontend/dist/
```

## На своём компе

### 1. Собрать фронт
```powershell
cd D:\code\python-react-chocolatki\frontend
npm run build
```
Появится `frontend/dist`.

### 2. Собрать zip только из нужного
Вставить целиком в PowerShell:
```powershell
cd D:\code\python-react-chocolatki
$stage = "$env:TEMP\choco_deploy\python-react-chocolatki"
Remove-Item "$env:TEMP\choco_deploy" -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force "$stage\frontend" | Out-Null
Copy-Item backend "$stage\backend" -Recurse
Copy-Item frontend\dist "$stage\frontend\dist" -Recurse
Remove-Item "$stage\backend\venv","$stage\backend\dev.db","$stage\backend\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Compress-Archive -Path "$env:TEMP\choco_deploy\python-react-chocolatki" -DestinationPath D:\code\choco_deploy.zip -Force
```
Результат — `D:\code\choco_deploy.zip`.

## На PythonAnywhere

### 3. Загрузить архив
Вкладка **Files** → загрузить `choco_deploy.zip` в домашнюю папку.

### 4. Распаковать
Вкладка **Consoles** → **Bash**:
```bash
cd ~
unzip choco_deploy.zip
```

### 5. Создать виртуальное окружение
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

### 6. Поставить зависимости
```bash
pip install Flask flask-cors python-dotenv
```
На free-тарифе БД — локальный SQLite, поэтому `libsql-experimental` не нужен.

### 7. Создать web app
Вкладка **Web** → **Add a new web app** → **Manual configuration** → **Python 3.10**.

### 8. Настроить web app
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

### 9. Запустить
Зелёная кнопка **Reload** → открыть `ЛОГИН.pythonanywhere.com`.
Страница метрик — `/metrics`.

## База данных

- **Free-тариф:** всё пишется в файл `backend/dev.db` на диске PA. Настраивать
  ничего не нужно — работает само.
- **Turso:** нужен платный тариф (на free-тарифе закрыт исходящий интернет).
  Тогда: `pip install libsql-experimental`, задать `TURSO_DATABASE_URL` и
  `TURSO_AUTH_TOKEN` (в WSGI-файле через `os.environ` или в `backend/.env`).

## Обновление сайта

Повторить шаги 1–2, залить новый zip, распаковать с заменой и нажать **Reload**.

## Реальные фото товаров

Заменить SVG в `frontend/public/images/` на фото с теми же именами
(`choco_01…choco_10`), затем пересобрать фронт (шаг 1) и перезалить.
