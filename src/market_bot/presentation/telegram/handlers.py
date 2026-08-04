from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from dishka.integrations.aiogram import FromDishka, inject

from market_bot.application.greetings import GreetingService

router = Router(name=__name__)


@router.message(CommandStart())
@inject
async def start(message: Message, service: FromDishka[GreetingService]) -> None:
    first_name = message.from_user.first_name if message.from_user else None
    await message.answer(service.start_message(first_name))


@router.message(Command("help"))
@inject
async def help_command(message: Message, service: FromDishka[GreetingService]) -> None:
    await message.answer(service.help_message())
