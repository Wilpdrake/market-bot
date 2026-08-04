# Market Bot

Отдельный production-сервис Telegram-бота проекта Market.

## Что реализовано

- long polling на `aiogram 3`;
- dependency injection через Dishka;
- команды `/start` и `/help`;
- строгая конфигурация из environment/`.env` через `pydantic-settings`;
- токен хранится как `SecretStr` и не выводится в логах;
- fail-fast при уже настроенном Telegram webhook — бот не удаляет webhook сам;
- отдельный `uv.lock`, тесты, Ruff, mypy и multi-stage Docker image;
- непривилегированный пользователь в production-контейнере.

База данных текущим функциям не нужна, поэтому SQLAlchemy/Alembic намеренно не добавлены. При появлении постоянного состояния следует добавить отдельный infrastructure-adapter и Alembic-миграции, не хранить состояние в handlers.

## Локальный запуск

```bash
cp .env.example .env
# Заполнить TELEGRAM_BOT_TOKEN в .env
uv sync --all-groups
uv run market-bot
```

`.env` исключён из Git и Docker build context.

## Проверки

```bash
uv lock --check
uv run pytest -q
uv run ruff check src tests
uv run ruff format --check src tests
uv run mypy
```

## Docker

```bash
docker build --target development -t market-bot-ci .
docker run --rm market-bot-ci
docker compose up -d --build
```

## Production

В общей инфраструктуре токен передаётся из Jenkins Secret text credential с точным ID `telegram-bot-token`. Один токен может отправлять Jenkins-уведомления и работать в polling-боте, но Telegram updates должен потреблять только один topology: либо polling, либо webhook.

Если у токена уже зарегистрирован webhook, процесс завершится с ошибкой и ничего не изменит. Для перехода на polling webhook нужно удалить осознанно отдельно, после чего перезапустить сервис.
