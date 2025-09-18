from fastapi import FastAPI
from app.modules.category.category_model import CategoryModule
from app.modules.products.products_model import ProductsModule

from app.modules.admin.admin_module import AdminModule
from app.core.database import start_connection

app = FastAPI()
AdminModule.register(app)
ProductsModule.register(app)
CategoryModule.register(app)

@app.on_event("startup")
async def startup_event():
    start_connection()

@app.get("/")
async def root():
    return {"message": "Hello World"}