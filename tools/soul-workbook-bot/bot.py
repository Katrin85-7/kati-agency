# -*- coding: utf-8 -*-
"""
Soul Method Workbook — Telegram-бот выдачи PDF.
Один код доступа · один PDF на Telegram-аккаунт.
"""
from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from chs import ARCHETYPES, day_to_chs, format_birth_date_ru, parse_birth_date, pdf_filename
from config import (
    ACCESS_CODE,
    BOT_TOKEN,
    MAX_CODE_ATTEMPTS,
    PDF_DIR,
    PORT,
    WEBHOOK_PATH,
    WEBHOOK_SECRET_SAFE,
    WEBHOOK_URL,
    validate_config,
)
from db import get_redemption, has_redeemed, init_db, mark_redeemed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Flow(StatesGroup):
    waiting_birth_date = State()
    waiting_code = State()


def confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да, верно", callback_data="birth:yes"),
                InlineKeyboardButton(text="✏️ Исправить", callback_data="birth:fix"),
            ]
        ]
    )


async def already_done_message(message: Message) -> None:
    row = get_redemption(message.from_user.id)
    if row:
        archetype = ARCHETYPES.get(row["chs"], "")
        await message.answer(
            f"Ты уже получила свой воркбук <b>SOUL METHOD | {archetype}</b>.\n\n"
            "Один аккаунт — одна выдача. Файл остался в этом чате выше.\n"
            "Если PDF потерялся — напиши Катрин лично.",
            parse_mode=ParseMode.HTML,
        )
    else:
        await message.answer(
            "Ты уже получила воркбук ранее.\n"
            "Если файл потерялся — напиши Катрин лично."
        )


async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    if has_redeemed(message.from_user.id):
        await already_done_message(message)
        return

    await message.answer(
        "🌿 <b>Твоя персональная распаковка по дате рождения</b>\n\n"
        "Внутри тебя уже есть ответы на многие вопросы. Иногда нужно лишь увидеть их под правильным углом.\n\n"
        "По дате рождения я определю твой природный тип личности и подберу воркбук, который поможет понять:\n\n"
        "✨ как ты принимаешь решения\n"
        "✨ где находятся твои сильные стороны\n"
        "✨ что мешает двигаться вперёд\n"
        "✨ как раскрыть свой потенциал\n"
        "✨ через что к тебе приходят деньги, отношения и самореализация\n\n"
        "Чтобы получить свой персональный воркбук, напиши дату рождения.\n\n"
        "📅 Формат:\n<code>25.06.1988</code>\nили\n<code>25/06/1988</code>",
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(Flow.waiting_birth_date)


async def cmd_cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Остановила. Когда будешь готова — /start")


async def on_birth_date(message: Message, state: FSMContext) -> None:
    if has_redeemed(message.from_user.id):
        await already_done_message(message)
        await state.clear()
        return

    parsed = parse_birth_date(message.text or "")
    if not parsed:
        await message.answer(
            "Не могу разобрать дату. Попробуй так:\n"
            "<code>25.06.1988</code>",
            parse_mode=ParseMode.HTML,
        )
        return

    chs = day_to_chs(parsed.day)
    if chs is None:
        await message.answer(
            "Что-то не так с днём рождения. Проверь дату и отправь ещё раз."
        )
        return

    archetype = ARCHETYPES[chs]
    await state.update_data(
        birth_iso=parsed.isoformat(),
        birth_display=format_birth_date_ru(parsed),
        chs=chs,
        code_attempts=0,
    )

    await message.answer(
        f"Ты родилась <b>{format_birth_date_ru(parsed)}</b>.\n"
        f"Твой архетип: <b>{archetype}</b> (число сознания {chs}).\n\n"
        "Всё верно?",
        parse_mode=ParseMode.HTML,
        reply_markup=confirm_keyboard(),
    )


async def on_birth_fix(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(Flow.waiting_birth_date)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        "Хорошо. Напиши дату рождения заново.\n"
        "Формат: <code>25.06.1988</code>",
        parse_mode=ParseMode.HTML,
    )


async def on_birth_yes(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    data = await state.get_data()
    if "chs" not in data:
        await state.set_state(Flow.waiting_birth_date)
        await callback.message.answer("Давай сначала — напиши дату рождения.")
        return

    await callback.message.edit_reply_markup(reply_markup=None)
    await state.set_state(Flow.waiting_code)
    await callback.message.answer(
        "Отлично.\n\n"
        "Теперь введи <b>код доступа</b>, который ты получила после оплаты.",
        parse_mode=ParseMode.HTML,
    )


async def on_access_code(message: Message, state: FSMContext, bot: Bot) -> None:
    if has_redeemed(message.from_user.id):
        await already_done_message(message)
        await state.clear()
        return

    data = await state.get_data()
    chs = data.get("chs")
    if chs is None:
        await state.set_state(Flow.waiting_birth_date)
        await message.answer("Сначала дата рождения — /start")
        return

    entered = (message.text or "").strip().upper()
    attempts = int(data.get("code_attempts", 0))

    if entered != ACCESS_CODE:
        attempts += 1
        await state.update_data(code_attempts=attempts)
        if attempts >= MAX_CODE_ATTEMPTS:
            await state.clear()
            await message.answer(
                "Слишком много неверных попыток. Начни заново: /start\n"
                "Если код точно верный — напиши Катрин."
            )
            return
        left = MAX_CODE_ATTEMPTS - attempts
        await message.answer(
            f"Код не подходит. Осталось попыток: {left}.\n"
            "Проверь регистр и пробелы — код чувствителен к написанию."
        )
        return

    pdf_path = PDF_DIR / pdf_filename(chs)
    if not pdf_path.is_file():
        logger.error("PDF missing: %s", pdf_path)
        await message.answer(
            "Файл воркбука временно недоступен. Напиши Катрин — она поможет."
        )
        return

    archetype = ARCHETYPES[chs]
    user = message.from_user

    mark_redeemed(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
        birth_date=data["birth_iso"],
        chs=chs,
    )

    await message.answer(
        f"✅ Код принят. Отправляю твой воркбук <b>SOUL METHOD | {archetype}</b>…",
        parse_mode=ParseMode.HTML,
    )

    await bot.send_document(
        chat_id=message.chat.id,
        document=FSInputFile(pdf_path),
        caption=(
            f"SOUL METHOD | {archetype}\n"
            "Сохрани файл — он останется в этом чате."
        ),
    )

    await state.clear()
    logger.info(
        "Delivered CHS%s to user %s (@%s)",
        chs,
        user.id,
        user.username,
    )


async def run_polling(dp: Dispatcher, bot: Bot) -> None:
    logger.info("Polling mode. PDF dir: %s", PDF_DIR)
    await dp.start_polling(bot)


async def run_webhook(dp: Dispatcher, bot: Bot) -> None:
    from aiohttp import web
    from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

    base = WEBHOOK_URL.rstrip("/")
    if not base.startswith("http"):
        base = f"https://{base}"
    webhook_url = f"{base}{WEBHOOK_PATH}"
    logger.info("Webhook mode: %s", webhook_url)

    app = web.Application()
    app.router.add_get("/", lambda _r: web.Response(text="Soul Method bot OK"))
    app.router.add_get("/health", lambda _r: web.Response(text="ok"))

    handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET_SAFE,
    )
    handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    await bot.set_webhook(
        webhook_url,
        secret_token=WEBHOOK_SECRET_SAFE,
        drop_pending_updates=True,
    )

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logger.info("Listening on 0.0.0.0:%s", PORT)

    await asyncio.Event().wait()


async def main() -> None:
    validate_config()
    init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.register(cmd_start, CommandStart())
    dp.message.register(cmd_cancel, Command("cancel"))
    dp.message.register(on_birth_date, Flow.waiting_birth_date)
    dp.message.register(on_access_code, Flow.waiting_code)

    dp.callback_query.register(on_birth_yes, F.data == "birth:yes")
    dp.callback_query.register(on_birth_fix, F.data == "birth:fix")

    if WEBHOOK_URL:
        await run_webhook(dp, bot)
    else:
        await run_polling(dp, bot)


if __name__ == "__main__":
    asyncio.run(main())
