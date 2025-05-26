# 政务知识图谱可视化

本项目旨在利用 Neo4j 构建政务信息知识图谱，并实现可视化系统。系统通过网络爬虫技术采集数据，构建知识图谱，并提供前端界面进行数据可视化。

## 项目结构

- **crawler/spider.py**：实现网络爬虫，从指定网站抓取政务信息。
- **kg/build_kg.py**：使用爬虫采集的数据构建知识图谱。
- **kg/schema.py**：定义知识图谱的模式，包括节点和关系类型。
- **neo4j/cypher_queries.cypher**：包含与 Neo4j 数据库交互的 Cypher 查询语句。
- **frontend/index.html**：前端应用的主 HTML 文件。
- **frontend/app.js**：处理前端的用户交互和 API 调用。
- **frontend/d3-visualization.js**：使用 D3.js 实现知识图谱的可视化。
- **backend/app.py**：后端应用入口，负责启动 Web 服务器。
- **backend/api/neo4j_api.py**：包含与 Neo4j 数据库交互的 API 接口。
- **requirements.txt**：项目所需依赖列表。

## 安装说明

1. **克隆仓库**：
   ```
   git clone <repository-url>
   cd zw-demo\gov-kg-visualization
   ```

2. **安装依赖**：
   ```
   pip install -r requirements.txt
   ```

3. **运行后端服务器**：
   ```
   python backend/app.py
   ```

4. **打开前端页面**：
   在浏览器中打开 `frontend/index.html` 以访问可视化界面。

## 使用指南

- 执行 `spider.py` 后，网络爬虫会自动从指定政务网站抓取数据。
- 数据采集完成后，运行 `build_kg.py` 构建知识图谱。
- 使用 `cypher_queries.cypher` 中的 Cypher 查询与 Neo4j 数据库交互。
- 前端界面支持知识图谱的可视化和数据交互。

## 项目简介

本项目集成了网页爬取、知识图谱构建和数据可视化，旨在为政务信息提供洞察。通过 Neo4j 和 D3.js，用户可以高效地探索数据关系和信息点。

# Government Knowledge Graph Visualization

This project aims to create a visualization system for government information using a knowledge graph built with Neo4j. The system utilizes web crawling techniques to gather data, constructs a knowledge graph, and provides a frontend interface for visualizing the data.

## Project Structure

- **crawler/spider.py**: Implements the web crawler to fetch government information from specified websites.
- **kg/build_kg.py**: Constructs the knowledge graph using the data collected by the web crawler.
- **kg/schema.py**: Defines the schema for the knowledge graph, including node and relationship types.
- **neo4j/cypher_queries.cypher**: Contains Cypher queries for interacting with the Neo4j database.
- **frontend/index.html**: Main HTML file for the frontend application.
- **frontend/app.js**: Handles user interactions and API calls for the frontend.
- **frontend/d3-visualization.js**: Uses D3.js to visualize the knowledge graph.
- **backend/app.py**: Entry point for the backend application, setting up the web server.
- **backend/api/neo4j_api.py**: Contains API endpoints for interacting with the Neo4j database.
- **requirements.txt**: Lists the dependencies required for the project.

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd zw-demo\gov-kg-visualization
   ```

2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Run the backend server**:
   ```
   python backend/app.py
   ```

4. **Open the frontend**:
   Open `frontend/index.html` in a web browser to access the visualization interface.

## Usage Guidelines

- The web crawler will automatically fetch data from the specified government websites when `spider.py` is executed.
- The knowledge graph can be built by running `build_kg.py` after data collection.
- Use the provided Cypher queries in `cypher_queries.cypher` to interact with the Neo4j database.
- The frontend allows users to visualize the knowledge graph and interact with the data.

## Overview

This project integrates web scraping, knowledge graph construction, and data visualization to provide insights into government information. By leveraging Neo4j and D3.js, users can explore relationships and data points effectively.
