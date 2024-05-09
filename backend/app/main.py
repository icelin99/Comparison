from fastapi import FastAPI
from app.routes import router as api_router
from fastapi.middleware.cors import CORSMiddleware
from app.database import model_run, init_db
from tortoise import run_async
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8082'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)

# 假设数据库已经建好
register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['app.database']}, 
    generate_schemas=False, 
    add_exception_handlers=True
)

# 若要修改数据库，使用下面的函数
# @app.on_event("startup")
# async def startup_event():
#     await model_run()
