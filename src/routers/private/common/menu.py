from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from aiogram.types import CallbackQuery
from keyboards import menu_keyboard as mk
from middlewares.private_middleware import PrivateChatMiddleware
from database.repos.user_repo import add_user
from aiogram.filters import StateFilter

router = Router()
router.message.middleware(PrivateChatMiddleware())
router.callback_query.middleware(PrivateChatMiddleware())


@router.message(Command("start"), StateFilter(None))
async def start_command(message: Message):
    await message.answer(
        text="👋 Привет!\n\nЯ бот для словесных игр. Выбери игру в меню ниже.",
        reply_markup=mk.back_to_menu_keyboard(),
    )
    await add_user(message.from_user.id, message.from_user.username)


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu_command(callback: CallbackQuery):
    await callback.message.edit_text(
        text="📋 Главное меню", reply_markup=mk.get_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "game_selection")
async def game_selection_command(callback: CallbackQuery):
    await callback.message.edit_text(
        text="🎮 Выберите игру:",
        reply_markup=mk.game_selection_keyboard(),
    )
    await callback.answer()
