from fastapi import FastAPI
from app.modules.admin import admin_controller

class AdminModule:
    @staticmethod
    def register(app: FastAPI):
        app.include_router(admin_controller.router, prefix="/admin", tags=["Admin", "Security"])
