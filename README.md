### 打开服务
在网页端运行`http://101.230.144.192:10069/mllm_evaluation/`


### 开启后端
进入backend目录
`tmux attach -t mllm_evaluation`
进去tmux后运行`uvicorn app.main:app --reload --port 8002`重启后端


### 重启数据库
使用`@app.on_event("startup")`函数，注释掉`register_tortoise()`函数
重启后（更新完db.sqlite3）恢复，即注释掉`@app.on_event("startup")`，使用`register_tortoise()`。

## 开发版本转测试
`main_dev`中的`app.include_router(api_router)`加上`prefix="/api"`
frontend的api中URl改成'http://101.230.144.192:10069/api/'