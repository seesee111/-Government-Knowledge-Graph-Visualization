// 本文件为前端主逻辑，处理用户交互、调用后端API并处理可视化数据。

document.addEventListener('DOMContentLoaded', function() {

    // “加载知识图谱”按钮点击事件
    document.getElementById('load-data').addEventListener('click', async () => {
        try {
            // 向后端请求知识图谱数据
            const response = await fetch('http://localhost:5000/api/graph');
            if (!response.ok) {
                alert('后端接口请求失败');
                return;
            }
            const data = await response.json();
            // 渲染知识图谱
            renderGraph(data.nodes, data.links);
        } catch (e) {
            alert('加载或解析数据出错');
            console.error(e);
        }
    });

    // “查询”按钮点击事件
    document.getElementById('search-btn').addEventListener('click', () => {
        const name = document.getElementById('search-input').value.trim();
        if (name) {
            highlightNode(name); // 高亮查询到的节点
        }
    });

    // 初始化右侧信息面板
    document.getElementById('info-panel').innerHTML = "<p>点击节点查看详细信息</p>";
});