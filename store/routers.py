from fastapi import APIRouter
from store.controllers.product import router

api_router = APIRouter()
api_router.include_router(router, prefix="/products")
