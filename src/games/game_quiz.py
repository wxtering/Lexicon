from database.session import AsyncSessionLocal
from database.models.models_list import QuizQuestions
from random import randint, choice
from database.repos.chat.gamesession_repo import (
    add_game_session,
    get_game_session,
    clear_game_session,
    update_game_session,
)
from database.repos.chat.gamehistory_repo import add_game_to_history


async def get_random_question():
    async with AsyncSessionLocal() as session:
        question_id = randint(1, 30847)
        question: QuizQuestions = await session.get(QuizQuestions, question_id)
        return question.word, question.definition


async def start_quiz(chat_id: int):
    word, definition = await get_random_question()
    await clear_game_session(chat_id=chat_id, game_type="quiz")
    await add_game_session(
        chat_id=chat_id,
        game_type="quiz",
        session_info={
            "word": word,
            "definition": definition,
            "hint": list(len(word) * "_"),
            "attempts": 0,
        },
    )
    return word, definition


async def check_answer(answer: str, chat_id: int, user_id: int):
    game_session = await get_game_session(chat_id=chat_id, game_type="quiz")
    word = game_session["word"]
    print(word, answer, game_session["attempts"])

    if game_session["word"] == answer:
        await add_game_to_history(
            user_id=user_id,
            game_type="quiz",
            game_result=True,
            chat_id=chat_id,
        )
        await clear_game_session(chat_id=chat_id, game_type="quiz")

        return ("Correct", word)
    else:
        game_session["attempts"] += 1
        await update_game_session(
            chat_id=chat_id, game_type="quiz", session_info=game_session
        )
        if (game_session["attempts"] - 3) % 3 == 0:
            hint = game_session["hint"]
            closed = [i for i, ch in enumerate(hint) if ch == "_"]
            rnd = choice(closed)
            hint[rnd] = word[rnd]
            game_session["hint"] = hint
            await update_game_session(
                chat_id=chat_id, game_type="quiz", session_info=game_session
            )
            return ("Incorrect", "".join(game_session["hint"]))
        else:
            return "Continue"


async def get_hint(chat_id: int):
    game_session = await get_game_session(chat_id=chat_id, game_type="quiz")
    hint = game_session["hint"]
    word = game_session["word"]
    closed = [i for i, ch in enumerate(hint) if ch == "_"]
    rnd = choice(closed)
    hint[rnd] = word[rnd]
    game_session["hint"] = hint
    await update_game_session(
        chat_id=chat_id, game_type="quiz", session_info=game_session
    )
    return "".join(game_session["hint"])
