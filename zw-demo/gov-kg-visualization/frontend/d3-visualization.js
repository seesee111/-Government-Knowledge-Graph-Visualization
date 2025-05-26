let currentNodes = [];
let currentLinks = [];
let svg, node, link, label, simulation, g;

function renderGraph(nodes, links) {
    currentNodes = nodes;
    currentLinks = links;

    d3.select("#visualization").selectAll("*").remove();

    const width = 900, height = 600;

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

    simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id).distance(120))
        .force("charge", d3.forceManyBody().strength(-400))
        .force("center", d3.forceCenter(width / 2, height / 2));

    link = g.append("g")
        .attr("stroke", "#aaa")
        .selectAll("line")
        .data(links)
        .join("line")
        .attr("stroke-width", 2);

    node = g.append("g")
        .selectAll("circle")
        .data(nodes)
        .join("circle")
        .attr("r", 18)
        .attr("fill", d => d.group === "department" ? "#1f77b4" : "#ff7f0e")
        .attr("stroke", "#fff")
        .attr("stroke-width", 2)
        .call(drag(simulation));

    label = g.append("g")
        .selectAll("text")
        .data(nodes)
        .join("text")
        .text(d => d.id)
        .attr("font-size", 12)
        .attr("dy", 4)
        .attr("text-anchor", "middle");

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
