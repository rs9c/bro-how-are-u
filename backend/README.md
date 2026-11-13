# 后端部分开发说明

## 所需环境

[![python](https://img.shields.io/badge/python-v3.13.15-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)

## 目录结构

```sh
backend/
├── app/                # 应用主目录
│   ├── api/            # API
│   └── main.py         # 主入口
├── .gitignore
├── README.md           # 后端开发说明
└── requirements.txt    # 依赖清单
```

## 本地开发

### 1. 安装依赖

```sh
# 创建并进入虚拟环境
# Python 3.13.15
cd backend && python3.13 -m venv venv
source venv/bin/activate    # macOS/Linux
.\venv\Scripts\activate     # Windows

# 安装依赖
# 到 https://pytorch.org/get-started/locally 找到适合自己系统的安装命令
# 类似于下面这行命令
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu132
# 安装Ultralytics
pip install ultralytics
# 补齐依赖
pip install -r requirements.txt
```

### 2. 后续开发与调试

```sh
cd backend

source venv/bin/activate    # macOS/Linux
.\venv\Scripts\activate     # Windows

uvicorn app.main:app --reload --port 5502 # 启动FastAPI服务
# 请求地址：http://127.0.0.1:5502
# API文档与调试：http://127.0.0.1:5502/docs
```
