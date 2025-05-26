// This file contains the main logic for the frontend application.
// It handles user interactions, makes API calls to the backend, and processes the data for visualization.

document.addEventListener('DOMContentLoaded', function() {

    document.getElementById('load-data').addEventListener('click', async () => {
        try {
            const response = await fetch('http://localhost:5000/api/graph');
            if (!response.ok) {
                alert('后端接口请求失败');
                return;
            }
            const data = await response.json();
            renderGraph(data.nodes, data.links);
        } catch (e) {
            alert('加载或解析数据出错');
            console.error(e);
        }
    });

    document.getElementById('search-btn').addEventListener('click', () => {
        const name = document.getElementById('search-input').value.trim();
        if (name) {
            highlightNode(name);
        }
    });
});