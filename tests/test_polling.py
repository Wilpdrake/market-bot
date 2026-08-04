from dataclasses import dataclass

import pytest

from market_bot.bootstrap.polling import WebhookConfiguredError, ensure_polling_available


@dataclass
class WebhookInfo:
    url: str


class BotStub:
    def __init__(self, webhook_url: str) -> None:
        self.webhook_url = webhook_url

    async def get_webhook_info(self) -> WebhookInfo:
        return WebhookInfo(url=self.webhook_url)


async def test_polling_starts_when_webhook_is_not_configured() -> None:
    await ensure_polling_available(BotStub(""))


async def test_polling_fails_without_mutating_configured_webhook() -> None:
    with pytest.raises(WebhookConfiguredError, match="webhook"):
        await ensure_polling_available(BotStub("https://example.com/telegram"))
