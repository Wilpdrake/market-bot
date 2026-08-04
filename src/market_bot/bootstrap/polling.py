from collections.abc import Awaitable
from typing import Protocol


class WebhookInfo(Protocol):
    url: str


class WebhookAwareBot(Protocol):
    def get_webhook_info(self) -> Awaitable[WebhookInfo]: ...


class WebhookConfiguredError(RuntimeError):
    pass


async def ensure_polling_available(bot: WebhookAwareBot) -> None:
    """Refuse to steal updates from an explicitly configured webhook."""
    webhook = await bot.get_webhook_info()
    if webhook.url:
        raise WebhookConfiguredError(
            "Telegram webhook is configured; remove it explicitly before enabling polling"
        )
