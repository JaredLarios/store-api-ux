from fastapi import FastAPI
from app.modules.products import products_controller


class ProductsModule:
    @staticmethod
    def register(app: FastAPI):
        app.include_router(
            products_controller.router, prefix="/product", tags=["Product"]
        )
