from market_bot.application.greetings import GreetingService


def test_start_message_addresses_known_user() -> None:
    service = GreetingService()

    text = service.start_message("Алексей")

    assert "Алексей" in text
    assert "Market" in text


def test_start_message_has_safe_fallback_for_missing_name() -> None:
    service = GreetingService()

    text = service.start_message(None)

    assert "Market" in text
    assert "None" not in text


def test_help_message_lists_available_commands() -> None:
    service = GreetingService()

    text = service.help_message()

    assert "/start" in text
    assert "/help" in text
