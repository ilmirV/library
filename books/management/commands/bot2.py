import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, InlineQueryHandler

from django.core.management.base import BaseCommand, CommandError

from books.models import Book, Author

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def get_books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    all_books = []
    async for book in Book.objects.all():
        all_books.append(book.title)
    response = "\n".join(book for book in all_books)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)


class Command(BaseCommand):
    help = "Telegram Bot"

    def handle(self, *args, **options):
        application = ApplicationBuilder().token("6093647563:AAFdrnSvUZI9y7IyDW2F1nA2McFNdODy81c").build()

        start_handler = CommandHandler("start", start)
        get_books_handler = CommandHandler("get_books", get_books)
        inline_caps_handler = InlineQueryHandler(inline_caps)

        application.add_handler(start_handler)
        application.add_handler(get_books_handler)
        application.add_handler(inline_caps_handler)

        application.run_polling()
