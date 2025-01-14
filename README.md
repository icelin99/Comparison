# 图文问答多模态模型效果比较系统
前端+后段
## 技术栈
- tortoise-orm
- sqlite3
- Vue.js

### 打开服务
在网页端运行`http://101.230.144.192:10069/mllm_evaluation/`


### 开启后端
进入backend目录
`tmux attach -t mllm_evaluation`
进去tmux后运行`uvicorn app.main:app --reload --port 8002`重启后端
#### 开发版本
`cd backend/app/dev` & `uvicorn main_dev:app --port 8003 --workers 8`

### 重启数据库
使用`@app.on_event("startup")`函数，注释掉`register_tortoise()`函数
重启后（更新完db.sqlite3）恢复，即注释掉`@app.on_event("startup")`，使用`register_tortoise()`。

## 开发版本转测试
`main_dev`中的`app.include_router(api_router)`加上`prefix="/api"`
frontend的api中URl改成'http://101.230.144.192:10069/api/'

## 前端打包
`sudo env "PATH=$PATH" npm run build`
