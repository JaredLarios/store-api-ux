from fastapi import FastAPI

from app.modules.admin.admin_module import AdminModule

app = FastAPI()
AdminModule.register(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}