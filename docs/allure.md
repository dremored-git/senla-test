# Allure в нашем проекте

Allure — отчет о выполнении тестов. Он показывает сценарий, параметры, шаг падения,
ожидаемое и фактическое состояние из assertion и приложенные скриншоты.
Он не выполняет тесты и не заменяет проверки: тесты запускает Pytest.

## Обновить свою ветку

Сначала сохранить работу коммитом и убедиться через `git status`, что рабочая папка чистая.
Находясь в своей `homework/...` ветке:

```powershell
git fetch origin
git merge origin/main
pip install -e ".[dev]"
```

Основная ветка репозитория называется `main`. Не пересоздавать проект и окружение.
При конфликте `tests/ui/conftest.py` сохранить и настройки своего браузера, и прикрепление
скриншота из обновленной базы. Если неясно, показать конфликт ментору до его разрешения.

## Установить просмотрщик

Python-зависимость `allure-pytest` уже включена в `pyproject.toml`. Она пишет результаты.
Allure CLI отдельно превращает их в HTML. Для нового окружения используем Allure Report 3.

1. Установить Node.js LTS: https://nodejs.org/
2. Открыть новый терминал. Выполнить:

```powershell
npm install -g allure
allure --version
```

Если PowerShell запрещает запуск `npm.ps1`, использовать `npm.cmd install -g allure`.
Если не найдена команда `allure`, открыть новый терминал и проверить npm prefix:
`npm config get prefix`. Каталог глобальных команд npm должен быть в PATH.

## Запустить тесты и открыть отчет

Из корня проекта в терминале VS Code с настроенной `.venv`:

```powershell
# Без стенда: проверить установку и сформировать первый набор результатов.
pytest tests/unit --alluredir=allure-results --clean-alluredir

# UI без создания заявок: включить VPN и заполнить локальный .env.
pytest tests/ui/test_admin.py -m ui -v --alluredir=allure-results --clean-alluredir

# Команды Allure 3: сформировать и открыть HTML.
allure generate allure-results --clean
allure open allure-report
```

`--clean-alluredir` очищает прежние результаты перед этим запуском.
Без него в отчет могут попасть тесты из нескольких запусков.
`allure open` поднимает локальный сервер; остановить его можно Ctrl+C.
Не открывать каталог `allure-results` как HTML: это JSON и вложения, а не готовый сайт.

Если уже стоит Allure 2, не переустанавливать его ради этой домашки:

```powershell
allure generate allure-results --clean -o allure-report
allure open allure-report
```

Allure 2 требует Java; Allure 3 запускается через Node.js. Не смешивать инструкции установки.

## Как оформлены наши тесты

В `tests/ui/test_admin.py` есть `epic`, `feature`, `story`, `title`.
Они задают разделы отчета и читаемое название сценария; на проверки не влияют.
В `zags/steps/admin.py` и `navigation.py` функции помечены `@allure.step`.
Их можно импортировать как раньше: параметры, возвращаемые страницы и assertions сохранены.

Пример для нового шага в своей ветке (названия методов сверить со своим Page Object):

```python
import allure


@allure.step("Ввести фамилию заявителя: {value}")
def fill_applicant_surname(page, value: str) -> None:
    page.set_surname(value)
```

Локаторы и работа с WebDriver остаются в `pages`, последовательность действий — в тесте.
Не нужно повторно оборачивать каждый вызов уже декорированного шага в `with allure.step`.
`with allure.step(...)` полезен для отдельного блока внутри составного шага.

## Скриншоты и статусы

При падении UI-теста с `--alluredir` фикстура автоматически прикладывает скриншот
перед закрытием браузера. Для дополнительного PNG на диске добавить `--screenshot-on-failure`.
Если браузер не создался или уже аварийно завершился, скриншот может быть недоступен:
в таком случае сохраняется исходная ошибка, а не искусственный успешный результат.

- Passed: тест завершился успешно.
- Failed: не прошла проверка, например `assert actual == expected`.
- Broken: ошибка выполнения, например отсутствующий метод или сбой WebDriver.
- Skipped: сценарий пропущен с указанной причиной.

Статус показывает способ завершения теста; `Failed` сам по себе не доказывает баг продукта.
Нужно отличить дефект стенда, неверное ожидание и ошибку теста. Не перехватывать исключения
ради зеленого отчета и не добавлять retries для скрытия проблемы.

`allure-results`, `allure-report`, `artifacts` исключены из Git. В PR добавляется код,
в описание — команда запуска и проверенные скриншоты отчета. Не прикладывать `.env`,
креды, URL с Basic Auth и реальные персональные данные. HTML страницы и URL браузера
автоматически не прикрепляются.

## Источники

https://allurereport.org/docs/pytest/
https://allurereport.org/docs/pytest-reference/
https://allurereport.org/docs/guides/pytest-selenium-screenshots/
https://allurereport.org/docs/v3/install/
https://allurereport.org/docs/v3/generate-report/
