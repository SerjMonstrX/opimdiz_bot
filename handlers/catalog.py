from aiogram import F, Router, types

from keyboards.catalog import generate_catalog_kb, CategoryCBData, generate_books_kb, BookCBData, back_to_category_books

router = Router()

CATALOG = {
    "romans": {
        "text": "Романы",
        "description": "Книги романы",
        "books": [
            {
                "id": 1,
                "name": "Гордость и предубеждение",
                "description": "Роман о любви и социальных предрассудках.",
                "price": 350,
            },
            {
                "id": 2,
                "name": "Анна Каренина",
                "description": "История трагической любви и судьбы женщины.",
                "price": 500,
            },
        ],
    },
    "fantasy": {
        "text": "Фэнтези",
        "description": "Книги фэнтези",
        "books": [
            {
                "id": 3,
                "name": "Властелин колец",
                "description": "Эпическая история борьбы за Средиземье.",
                "price": 700,
            },
            {
                "id": 4,
                "name": "Гарри Поттер и философский камень",
                "description": "Первая книга о юном волшебнике.",
                "price": 400,
            },
        ],
    },
    "horror": {
        "text": "Ужасы",
        "description": "Книги ужасов",
        "books": [
            {
                "id": 5,
                "name": "Оно",
                "description": "Мистическая история о зловещем клоуне.",
                "price": 450,
            },
            {
                "id": 6,
                "name": "Сияние",
                "description": "Психологический хоррор в уединённом отеле.",
                "price": 380,
            },
        ],
    },
    "detectives": {
        "text": "Детективы",
        "description": "Книги детективы",
        "books": [
            {
                "id": 7,
                "name": "Шерлок Холмс: Этюд в багровых тонах",
                "description": "Первое расследование Шерлока Холмса.",
                "price": 300,
            },
            {
                "id": 8,
                "name": "Убийство в Восточном экспрессе",
                "description": "Знаменитое дело Эркюля Пуаро.",
                "price": 320,
            },
        ],
    },
    "documentaries": {
        "text": "Документальные",
        "description": "Документальная литература",
        "books": [
            {
                "id": 9,
                "name": "Краткая история времени",
                "description": "Объяснение устройства Вселенной простым языком.",
                "price": 550,
            },
            {
                "id": 10,
                "name": "Sapiens: Краткая история человечества",
                "description": "История развития человека как вида.",
                "price": 600,
            },
        ],
    },
}


@router.callback_query(F.data == "catalog")
@router.message(F.text == "Каталог")
async def catalog(update: types.Message | types.CallbackQuery):
    if isinstance(update, types.Message):
        await update.answer(
        "Наш каталог:",
        reply_markup=generate_catalog_kb(CATALOG)
    )
    else:
        await update.message.edit_text(
        "Наш каталог:",
        reply_markup=generate_catalog_kb(CATALOG)
        )


@router.callback_query(CategoryCBData.filter())
async  def category_info(callback: types.CallbackQuery, callback_data: CategoryCBData):
    category = CATALOG.get(callback_data.category)

    await callback.message.edit_text(
        text=category["description"],
        reply_markup=generate_books_kb(
            category["books"],
            callback_data.category
        )
    )

@router.callback_query(BookCBData.filter())
async def book_info(callback: types.CallbackQuery, callback_data: BookCBData):
    book_id = callback_data.id
    category = CATALOG.get(callback_data.category)

    book = None

    for bk  in category["books"]:
        if bk["id"] == book_id:
            book = bk
            break

    if not book:
        return await callback.answer("Не нашел книгу")

    await callback.message.edit_text(
        f"Название - {book['name']}\n"
        f"Описание - {book['description']}\n"
        f"Стоимость - {book['price']}\n\n"
        "Хотите приобрести?",
        reply_markup=back_to_category_books(callback_data.category)
    )