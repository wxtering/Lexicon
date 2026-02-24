from aiogram import Router
from aiogram.types import Message
from middlewares.group_chat_middleware import GroupChatMiddleware
from aiogram.filters import Command
from games.game_quiz import start_quiz, check_answer
from states.quiz_states import QuizState
from aiogram.fsm.context import FSMContext
from aiogram import F
from database.repos.chat.gamesession_repo import clear_game_session
from games.game_quiz import get_hint
from middlewares.add_user_middleware import AddUserMiddleware

router = Router()
router.message.middleware(AddUserMiddleware())
router.message.middleware(GroupChatMiddleware())
router.callback_query.middleware(GroupChatMiddleware())


@router.message(Command("quiz"))
async def quiz_start(message: Message, state: FSMContext):
    await state.set_state(QuizState.ingame)
    word, definition = await start_quiz(message.chat.id)
    await message.answer(
        text=(
            f"📖 Новый вопрос!\n\n"
            f"{definition}\n\n"
            f"🔤 Слово из {len(word)} букв\n"
            f"💡 Напишите ответ в формате: 'слово'\n"
            f"🔍 Подсказка: напишите hint"
        ),
    )


@router.message(QuizState.ingame, Command("quit"))
async def quiz_quit(message: Message, state: FSMContext):
    await state.clear()
    await clear_game_session(chat_id=message.chat.id, game_type="quiz")
    await message.answer(text="🛑 Игра завершена. До встречи!")


@router.message(QuizState.ingame, F.text.startswith("hint"))
async def quiz_hint(message: Message, state: FSMContext):
    hint = await get_hint(message.chat.id)
    await message.answer(
        text=f"🔍 Подсказка:\n\n{hint}",
    )


@router.message(QuizState.ingame)
async def quiz_answer(message: Message, state: FSMContext):
    answer = message.text.lower()
    result = await check_answer(answer, message.chat.id, message.from_user.id)
    if result == "Continue":
        pass
    if result[0] == "Correct":
        await message.answer(
            text=f"✅ Правильно!\n\nСлово: {answer}",
        )
        await quiz_start(message, state)

    elif result[0] == "Incorrect":
        await message.answer(
            text=f"❌ Неверно!\n\n🔍 Открытые буквы: {result[1]}",
        )
