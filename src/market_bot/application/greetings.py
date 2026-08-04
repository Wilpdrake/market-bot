class GreetingService:
    """Build user-facing text independently from the Telegram transport."""

    def start_message(self, first_name: str | None) -> str:
        name = first_name.strip() if first_name and first_name.strip() else "друг"
        return (
            f"Привет, {name}! Это бот Market.\n\n"
            "Пока я умею только знакомиться и показывать справку. "
            "Новые возможности появятся позже."
        )

    def help_message(self) -> str:
        return "Доступные команды:\n/start — начать работу\n/help — показать эту справку"
