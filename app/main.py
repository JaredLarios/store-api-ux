from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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


app.add_middleware(
    # type: ignore[arg-type]
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "HEAD", "OPTIONS"],
    allow_headers=[
        "Access-Control-Allow-Headers",
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Origin",
        "Set-Cookie",
    ],
)
