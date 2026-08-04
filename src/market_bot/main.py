import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka

from market_bot.bootstrap.ioc import ApplicationProvider
from market_bot.bootstrap.polling import ensure_polling_available
from market_bot.infrastructure.config import Settings
from market_bot.presentation.telegram.handlers import router

logger = logging.getLogger(__name__)


async def serve() -> None:
    # BaseSettings supplies required fields from environment variables at runtime.
    settings = Settings()  # type: ignore[call-arg]
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    bot = Bot(token=settings.telegram_bot_token.get_secret_value())
    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    container = make_async_container(ApplicationProvider())
    setup_dishka(container, dispatcher)

    try:
        await ensure_polling_available(bot)
        await bot.set_my_commands(
            [
                BotCommand(command="start", description="Начать работу"),
                BotCommand(command="help", description="Справка"),
            ]
        )
        identity = await bot.get_me()
        logger.info(
            "Starting Telegram polling for bot id=%s username=%s",
            identity.id,
            identity.username,
        )
        await dispatcher.start_polling(
            bot,
            allowed_updates=dispatcher.resolve_used_update_types(),
        )
    finally:
        await container.close()
        await bot.session.close()


def run() -> None:
    asyncio.run(serve())


if __name__ == "__main__":
    run()
