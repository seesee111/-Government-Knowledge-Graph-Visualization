# 政务知识图谱可视化项目

本项目基于 Neo4j、Flask 和 D3.js，实现了政务信息的自动采集、知识图谱构建与前端可视化。适合政务数据的结构化管理、关系分析与交互式展示。

---

## 项目结构

```
gov-kg-visualization/
├── crawler/           # 爬虫模块，采集政务数据
│   └── spider.py
├── kg/                # 知识图谱构建模块
│   └── build_kg.py
├── neo4j/             # Neo4j相关脚本和Cypher语句
│   ├── cypher_queries.cypher
│   └── from neo4j import GraphDatabase.py
├── backend/           # 后端API服务
│   ├── app.py
│   └── api/
│       ├── api.py
│       └── neo4j_api.py
├── frontend/          # 前端可视化
│   ├── index.html
│   ├── login.html
│   ├── app.js
│   ├── d3-visualization.js
│   └── styles.css
├── requirements.txt   # Python依赖
└── government_data.json # 爬取后的原始数据
```

---

## 安装与运行

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **运行爬虫采集数据**
   ```bash
   python crawler/spider.py
   ```
   采集结果会保存在 `government_data.json`。

3. **构建知识图谱（写入Neo4j）**
   ```bash
   python kg/build_kg.py
   ```

4. **启动后端服务**
   ```bash
   python backend/app.py
   ```
   默认监听 `http://localhost:5000`。

5. **启动前端本地服务器并访问**
   ```bash
   cd frontend
   python -m http.server 8000
   ```
   在浏览器访问 [http://localhost:8000/zw-demo/gov-kg-visualization/frontend/login.html]，登录后自动跳转到主页面。

---

## 功能说明

- **数据采集**：`crawler/spider.py` 自动抓取政务事项数据，保存为 JSON。
- **知识图谱构建**：`kg/build_kg.py` 读取 JSON，批量写入 Neo4j，形成“部门-事项”结构。
- **后端API**：`backend/app.py` 提供 RESTful 接口，前端可动态获取图谱数据，并支持用户注册、登录、密码修改等功能。
- **前端可视化**：`frontend/` 目录下用 D3.js 实现图谱展示，支持缩放、拖拽、节点高亮查询等交互。右上角为圆形SVG头像，点击弹出用户信息侧边栏，可修改密码和退出登录。

---

## 主要依赖

- Python 3.x
- requests
- beautifulsoup4
- neo4j
- flask
- flask-cors
- D3.js (v6)

---

## 典型流程

1. 运行爬虫采集数据
2. 构建知识图谱写入 Neo4j
3. 启动后端 Flask 服务
4. 启动前端本地服务器，浏览器访问登录页，登录后进入主页面
5. 点击“加载知识图谱”按钮，浏览和查询政务知识图谱

---

## 说明

- Neo4j 默认连接 `bolt://localhost:7687`，用户名密码请在相关脚本中自行修改。
- 若需清空数据库，可运行 `neo4j/from neo4j import GraphDatabase.py`。
- 所有代码和数据仅供学习和研究使用。

---

## 联系

如有问题或建议，请通过 GitHub Issue 反馈。