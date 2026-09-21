from maxapi import Router
from max.start.handler import router as start_router
from max.parse.callbacks import router as callbacks_router
from max.parse.accept import router as accept_router

router = Router()
router.include_routers(start_router, callbacks_router, accept_router)
