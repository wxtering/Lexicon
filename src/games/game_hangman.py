from database.session import AsyncSessionLocal
from database.models.models_list import HangmanWords
from sqlalchemy import select, func
from random import randint, choice
from database.repos.private.gamesession_repo import (
    add_game_session,
    get_game_session,
    clear_game_session,
    update_game_session,
)
from re import finditer

HANGMANPICS = [
    """
  +---+
  |   |
      |
      |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========""",
]


async def hangman_game_start(difficulty: str, user_id: int) -> str:
    word = await get_random_word(difficulty)
    opened_letters = list("_" * len(word))
    session_info = {"word": word, "attempt": 0, "opened_letters": opened_letters}  # type: ignore
    await clear_game_session(user_id, "hangman")
    await add_game_session(
        user_id=user_id, game_type="hangman", session_info=session_info
    )
    return "".join(opened_letters)


async def get_random_word(difficulty: str) -> str:  # type: ignore
    async with AsyncSessionLocal() as session:
        if difficulty == "easy":
            result = await session.execute(
                select(HangmanWords.word).where(func.length(HangmanWords.word) == 5)
            )
            return choice(result.scalars().all())

        elif difficulty == "medium":
            result = await session.execute(
                select(HangmanWords.word).where(
                    func.length(HangmanWords.word) == randint(6, 8)
                )
            )
            return choice(result.scalars().all())

        elif difficulty == "hard":
            result = await session.execute(
                select(HangmanWords.word).where(
                    func.length(HangmanWords.word) == randint(9, 14)
                )
            )
            return choice(result.scalars().all())


async def game_hangman_gameplay(user_id: int, message: str) -> tuple[str, str, str]:
    game_session = await get_game_session(user_id=user_id, game_type="hangman")
    word, attempt, opened_letters = game_session.values()
    message = message.lower()
    print(word, attempt, opened_letters, message)
    if len(message) == 1:
        matches = [
            m.start()
            for m in finditer(
                message,
                word,
            )
        ]
        print(matches)
        if message in opened_letters:
            return ("already_opened", HANGMANPICS[attempt], "".join(opened_letters))
        if matches:
            for match in matches:
                opened_letters[match] = message
            await update_game_session(
                user_id=user_id,
                game_type="hangman",
                session_info={
                    "word": word,
                    "attempt": attempt,
                    "opened_letters": opened_letters,
                },
            )
            if "".join(opened_letters) == word:
                await clear_game_session(user_id, "hangman")
                return ("win", HANGMANPICS[attempt], word)
            return (
                "Yes letter match",
                HANGMANPICS[attempt],
                "".join(opened_letters),
            )

        else:
            attempt += 1
            if attempt == 6:
                await clear_game_session(user_id, "hangman")
                return ("lose", HANGMANPICS[attempt], word)
            await update_game_session(
                user_id=user_id,
                game_type="hangman",
                session_info={
                    "word": word,
                    "attempt": attempt,
                    "opened_letters": opened_letters,
                },
            )
            return ("No letter match", HANGMANPICS[attempt], "".join(opened_letters))
    else:
        if message == word:
            await clear_game_session(user_id, "hangman")
            return ("win", HANGMANPICS[attempt], word)
        else:
            attempt += 1
            if attempt == 6:
                await clear_game_session(user_id, "hangman")
                return ("lose", HANGMANPICS[attempt], "".join(opened_letters))
            await update_game_session(
                user_id=user_id,
                game_type="hangman",
                session_info={
                    "word": word,
                    "attempt": attempt,
                    "opened_letters": opened_letters,
                },
            )
            return ("No word match", HANGMANPICS[attempt], "".join(opened_letters))
    return "smth wrong"
