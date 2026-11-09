# Запуск общего проекта

## Обновление и установка

Сначала сохранить свою незавершенную работу отдельным коммитом в своей ветке.
Основная ветка проекта называется `main`.

```powershell
git switch main
git pull --ff-only
.\setup.ps1
```

Скрипт создает `.venv`, устанавливает проект с инструментами разработки,
БД, Playwright и параллельного запуска, затем скачивает Chromium для Playwright.
Существующий `.env` сохраняется. При первом запуске создается копия `.env.example`.
Python 3.11+ с командой `py` должен быть установлен заранее.

После установки в этом терминале доступны обычные `python`, `pip`, `pytest` и `ruff`.
В VS Code новые терминалы также получают PATH виртуального окружения из настроек проекта.
В другом PowerShell перед работой выполнить `.\.venv\Scripts\Activate.ps1`.

Открыть `.env` и заполнить доступы к стенду. Для проверок БД добавить переменные
`ZAGS_DB_*` из актуального `.env.example`. Значения из окружения имеют приоритет.
Пароли в Git не добавлять.

## Первые проверки

```powershell
pytest
ruff check .
pytest --collect-only
```

Обычный `pytest` запускает локальные проверки без браузера и стенда.
Он не доказывает, что live-сценарии прошли. Для них нужны отдельные команды ниже.
Минимальная установка `pip install -e ".[dev]"` тоже поддерживается, но проверки,
требующие отсутствующих SQLAlchemy или Playwright, будут пропущены.

## Selenium

Нужны Chrome или Edge, VPN стенда и заполненная авторизация в `.env`.

```powershell
# Smoke администратора.
pytest tests/ui/test_admin.py -m ui -v

# Все Selenium-сценарии. Создающие заявки будут пропущены.
pytest tests/ui -m ui --headless -v

# Те же тесты через Edge.
pytest tests/ui -m ui --browser edge -v
```

Полные сценарии Романа и Даниила сохраняют заявки на общем стенде.
Запускать по одному, когда создание тестовой записи согласовано.

```powershell
# Роман — регистрация рождения.
pytest tests/ui/test_checkappreg.py -m ui --allow-defense-writes -v

# Даниил — регистрация брака.
pytest tests/ui/test_user.py -m ui --allow-defense-writes -v
```

## API

```powershell
# Чтение заявок, пагинация и авторизация. POST будет пропущен.
pytest tests/api -m api -v

# Отдельно работа Романа или Даниила.
pytest tests/api/test_roman_applications.py -m api -v
pytest tests/api/test_daniil_applications.py -m api -v
```

Необязательный пример создания администратора использует свой флаг разрешения.

```powershell
pytest tests/api/test_admin_write.py -m api --allow-api-writes -v
```

## БД и Playwright

```powershell
# Только чтение БД и сверка с API.
pytest tests/final/roman/test_database_roman.py tests/api/test_database_daniil.py -m "defense_live and not defense_write" -v

# Формы Playwright без отправки.
pytest tests/final/roman/test_playwright_roman.py tests/ui/test_playwright_daniil.py -m "defense_pw and not defense_write" -v
```

Для разрешенных полных сценариев выбрать один конкретный тест и добавить
`--allow-defense-writes`. Один этот флаг не меняет выбор тестов по маркеру.
Флаг `--allow-api-writes` относится только к `api_write`, а
`--allow-defense-writes` — только к `defense_write`.

## Allure

Результаты каждого нового прогона лучше очищать, чтобы не смешивать старые падения
с текущими проверками.

```powershell
pytest --alluredir=allure-results --clean-alluredir
allure generate allure-results --clean
allure open allure-report
```

Для этих команд отдельно нужен Allure CLI. Например, при установленном Node.js LTS
можно установить его командой `npm install -g allure`. Это отдельная программа,
а `allure-pytest` из Python-зависимостей только записывает результаты тестов.

## Docker и три браузера

Нужен запущенный Docker с Linux containers. Команды выполнять из корня проекта.
Образ браузера скачивается отдельно от Selenoid.

```powershell
docker pull selenoid/vnc_chrome:128.0
docker compose -f deploy/daniil/compose.yml up -d selenoid selenoid-ui
```

Проверить готовность Selenoid по `http://localhost:4445/status`.
Его интерфейс открыт на `http://localhost:8081`.
В `.env` указать `ZAGS_REMOTE_URL=http://localhost:4445/wd/hub`.
Запускать ровно этот файл отдельно с тремя worker-процессами.

```powershell
pytest tests/final/daniil/test_remote_daniil.py -m defense_remote -n 3 -v
```

Для конфигурации Романа заменить путь Compose на `deploy/roman/compose.yml`,
файл теста на `tests/final/roman/test_remote_roman.py`, порт Selenoid на `4444`,
порт интерфейса на `8080`. Перед этим обновить `ZAGS_REMOTE_URL` в `.env`.
Синхронизация демо рассчитана на три локальных worker-процесса с общей файловой системой.

Тесты внутри Docker по умолчанию выполняют локальные проверки фреймворка.

```powershell
docker compose --env-file .env -f deploy/daniil/compose.yml --profile tests run --build --rm tests
```

Для удаленных браузеров из контейнера тестов используется адрес
`http://selenoid:4444/wd/hub`, который уже передается Compose.
VPN должен обеспечивать доступ к ЗАГСу также из контейнеров браузера.
Для запуска браузеров Selenoid использует Docker socket хоста.

После работы остановить только нужную конфигурацию.

```powershell
docker compose -f deploy/daniil/compose.yml down
```

## CI

`Framework checks` запускает Ruff и локальные тесты при push и PR.
Персональные workflow запускаются вручную или по расписанию и сохраняют отчеты.
Live job включается переменной репозитория `DEFENSE_LIVE_ENABLED=true` и требует
self-hosted runner с метками `linux`, `zags-vpn` и доступами в GitHub Secrets.
Live job выполняет только чтение API/БД и заполнение форм без отправки.
Автоматическое создание записей в эти job не включено.
Отправка отчета по почте требует `DEFENSE_MAIL_ENABLED=true` и настроенных SMTP Secrets.

## Если запуск остановился

| Симптом | Что проверить |
| --- | --- |
| `pytest` не найден | Выполнить установку и открыть новый терминал VS Code или активировать `.venv` |
| `fixture not found`, неизвестный marker | Обновить `main`, повторить `pip install -e ".[dev,defense]"` |
| `403`, HTML с запретом сети | VPN и маршрут доступа к стенду. Не менять ожидаемый статус на 403 |
| `401` | Логин, пароль и переменные окружения, переопределяющие `.env` |
| `Executable doesn't exist` в Playwright | Выполнить `playwright install chromium` |
| Нет драйвера Selenium | Браузер установлен, Selenium Manager может скачать драйвер, нет устаревшего драйвера в PATH |
| Нет тестов в запуске | Сверить путь и маркер. `ui`, `api`, `defense_pw`, `defense_db` — разные группы |
| Три Selenoid-теста зависают | Файл запущен отдельно с `-n 3`, хватает трех браузерных слотов |
| Заявка № `null` | Изучить ответ отправки и скриншот. Такой результат не считается успешной регистрацией |
