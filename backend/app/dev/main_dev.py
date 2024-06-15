from fastapi import FastAPI
from routes_dev import router as api_router
from fastapi.middleware.cors import CORSMiddleware
from database_dev import model_run
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8082', 'http://101.230.144.192:10069/mllm_evaluation','http://localhost:8083'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
# app.include_router(api_router, prefix="/api")


# 若要修改数据库，使用下面的函数
# @app.on_event("startup")
# async def startup_event():
#     await model_run()

@app.on_event("shutdown")
async def shutdown_event():
    await Tortoise.close_connections()


# 假设数据库已经建好
register_tortoise(
    app,
    db_url='sqlite://db-607.sqlite3',
    modules={'models': ['database_dev']}, 
    generate_schemas=False, 
    add_exception_handlers=True
)
