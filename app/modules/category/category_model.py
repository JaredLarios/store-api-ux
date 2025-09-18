from fastapi import FastAPI
from app.modules.category import category_controller

class CategoryModule:
    @staticmethod
    def register(app: FastAPI):
        app.include_router(category_controller.router, prefix="/category", tags=["Category"])
