let currentNodes = [];
let currentLinks = [];
let svg, node, link, label, simulation, g;

// 颜色映射，不同类型节点不同颜色
const colorMap = {
    department: "#1f77b4", // 部门-蓝色
    matter: "#2ca02c",     // 事项-绿色
    content: "#ff7f0e",    // 内容-橙色
    other: "#888"          // 其他-灰色
};

// 渲染知识图谱主函数
function renderGraph(nodes, links) {
    currentNodes = nodes;
    currentLinks = links;

    // 清空原有内容
    d3.select("#visualization").selectAll("*").remove();

    const width = 900, height = 600;

    // 创建SVG画布
    svg = d3.select("#visualization")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    // 支持缩放和平移
    g = svg.append("g");
    svg.call(
        d3.zoom()
            .scaleExtent([0.2, 4])
            .on("zoom", (event) => {
                g.attr("transform", event.transform);
            })
    );

    // 力导向布局设置
    simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id).distance(180)) // 连线长度
        .force("charge", d3.forceManyBody().strength(-900)) // 斥力
        .force("center", d3.forceCenter(width / 2, height / 2)) // 居中
        .force("collide", d3.forceCollide(30)); // 防止节点重叠

    // 绘制连线
    link = g.append("g")
        .attr("stroke", "#aaa")
        .selectAll("line")
        .data(links)
        .join("line")
        .attr("stroke-width", 2);

    // 绘制节点标签
    label = g.append("g")
        .selectAll("text")
        .data(nodes)
        .join("text")
        .text(d => d.name)
        .attr("font-size", 16)
        .attr("dy", 5)
        .attr("text-anchor", "middle")
        .attr("pointer-events", "none"); // 标签不拦截鼠标事件

    // 绘制节点
    node = g.append("g")
        .selectAll("circle")
        .data(nodes)
        .join("circle")
        .attr("r", 22)
        .attr("fill", d => colorMap[d.group] || "#ccc")
        .attr("stroke", "#fff")
        .attr("stroke-width", 2)
        // 鼠标悬停高亮
        .on("mouseover", function(event, d) {
            d3.select(this).attr("stroke", "#ff0").attr("stroke-width", 5);
        })
        .on("mouseout", function(event, d) {
            d3.select(this).attr("stroke", "#fff").attr("stroke-width", 2);
        })
        // 点击节点显示详细信息
        .on("click", function(event, d) {
            showNodeInfo(d);
        })
        .call(drag(simulation)); // 支持拖拽

    // tick事件：每次仿真迭代更新节点和连线位置
    simulation.on("tick", () => {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node
            .attr("cx", d => d.x)
            .attr("cy", d => d.y);

        label
            .attr("x", d => d.x)
            .attr("y", d => d.y);
    });

    // 拖拽行为定义
    function drag(simulation) {
        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }
        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }
        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }
        return d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
    }
}

// 查询并高亮节点
function highlightNode(name) {
    if (!svg || !currentNodes.length) return;
    // 取消所有高亮
    node.attr("stroke", "#fff").attr("stroke-width", 2);
    link.attr("stroke", "#aaa").attr("stroke-width", 2);
    label.attr("fill", "#222");

    // 找到目标节点
    const target = currentNodes.find(n => n.id === name);
    if (!target) return;

    // 高亮节点
    node.filter(d => d.id === name)
        .attr("stroke", "#ff0")
        .attr("stroke-width", 5);

    // 高亮相关连线
    link.filter(d => d.source.id === name || d.target.id === name)
        .attr("stroke", "#f00")
        .attr("stroke-width", 4);

    // 高亮标签
    label.filter(d => d.id === name)
        .attr("fill", "#d62728");
}

// 显示节点详细信息到右侧面板
function showNodeInfo(d) {
    const panel = document.getElementById('info-panel');
    if (!d) {
        panel.innerHTML = "<p>未选择节点</p>";
        return;
    }
    // 类型中英文映射
    const groupMap = {
        department: "部门",
        matter: "事项",
        content: "内容",
        other: "其他"
    };
    let html = `<h2>${d.name || d.id}</h2>`;
    html += `<div class="info-row"><span class="info-label">类型:</span>${groupMap[d.group] || d.group}</div>`;
    if (d.id) html += `<div class="info-row"><span class="info-label">ID:</span>${d.id}</div>`;
    // 新增：显示授权部门、事项类型、实施层级（如果有）
    if (d.dept) html += `<div class="info-row"><span class="info-label">授权部门:</span>${d.dept}</div>`;
    if (d.kind) html += `<div class="info-row"><span class="info-label">事项类型:</span>${d.kind}</div>`;
    if (d.level) html += `<div class="info-row"><span class="info-label">实施层级:</span>${d.level}</div>`;
    panel.innerHTML = html;
}
