from dishka import Provider, Scope, provide

from market_bot.application.greetings import GreetingService


class ApplicationProvider(Provider):
    greeting_service = provide(GreetingService, scope=Scope.APP)
