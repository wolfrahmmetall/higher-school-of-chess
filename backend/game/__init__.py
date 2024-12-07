from fastapi import APIRouter
from .move_handler import router as move_router

router = APIRouter()
router.include_router(move_router, prefix='/chess')