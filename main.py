import os
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response
from starlette.routing import Route
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

telegram = (
    Application.builder()
    .token(os.environ["TOKEN"])
    .updater(None)
    .build()
)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)


telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


async def root(request: Request) -> Response:
    await telegram.update_queue.put(
        Update.de_json(data=await request.json(), bot=telegram.bot)
    )
    telegram.run_webhook()
    return Response()


app = Starlette(
    routes=[
        Route("/", root, methods=["POST"]),
    ]
)
