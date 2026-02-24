from aiogram import F, Router, types

router = Router()


@router.message(F.text == "О нас")
async def info(message: types.Message):
    await message.answer(
        (
            f"Я бот для покупки книг.\n"
            f"Ты можешь посмотреть весь "
            f"мой каталог и купить понравившуюся кжинку.\n\n"
            f"Хорошего чтения!"
        )
    )
