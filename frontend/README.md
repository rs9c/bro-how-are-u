# 前端部分开发说明

## 所需环境

[![node](https://img.shields.io/badge/node-v26.3.0-5FA04E?style=flat-square&logo=nodedotjs&logoColor=white)](https://nodejs.org/)

## 目录结构

```sh
frontend/
├── index.html          # 入口 HTML 文件
├── jsconfig.json       # JavaScript 配置文件
├── package-lock.json   # 依赖锁定文件
├── package.json        # 项目配置文件
├── public/             # 静态资源
│   └── favicon.ico
├── README.md           # 前端部分开发说明
├── src/
│   ├── App.vue         # 根组件
│   ├── assets/         # 静态资源
│   ├── main.js         # 入口文件
│   ├── router/         # 路由相关
│   ├── stores/         # Pinia 状态管理相关
│   └── views/          # 页面组件
├── vite.config.js      # Vite 配置文件
└── vitest.config.js    # Vitest 配置文件
```

## 本地开发

### 1. 初次部署

```sh
# 安装所需依赖
cd frontend
npm install
```

### 2. 后续开发

```sh
# 启动开发服务器
npm run dev
# http://localhost:5501
```

### 3. 构建

```sh
npm run build
```
