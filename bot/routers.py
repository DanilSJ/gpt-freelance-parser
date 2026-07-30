from aiogram import Router
from bot.start.handler import router as start_router
from bot.parse.callbacks import router as callbacks_router
from bot.parse.accept import router as accept_router

router = Router()
router.include_router(start_router)
router.include_router(callbacks_router)
router.include_router(accept_router)
