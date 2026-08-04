import pytest
from pydantic import ValidationError

from market_bot.infrastructure.config import Settings


def test_settings_require_non_empty_bot_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_settings_load_token_without_exposing_it_in_repr(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:synthetic-test-token")

    settings = Settings(_env_file=None)

    assert settings.telegram_bot_token.get_secret_value() == "123456:synthetic-test-token"
    assert "synthetic-test-token" not in repr(settings)


def test_settings_reject_whitespace_only_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "   ")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_settings_reject_unknown_log_level(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:synthetic-test-token")
    monkeypatch.setenv("LOG_LEVEL", "verbose")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)
