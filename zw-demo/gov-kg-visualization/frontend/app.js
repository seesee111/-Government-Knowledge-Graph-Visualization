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

    // 头像与侧边栏逻辑
    const avatar = document.getElementById('user-avatar');
    const sidePanel = document.getElementById('user-side-panel');
    const closeBtn = document.getElementById('side-close-btn');
    // 设置头像下方用户名
    const loginUser = localStorage.getItem("loginUser") || "未登录";
    document.getElementById('avatar-username').textContent = loginUser;
    document.getElementById('user-name').textContent = loginUser;
    document.getElementById('side-user-name').textContent = loginUser;

    // 点击头像显示侧边栏
    avatar.onclick = function(e) {
        sidePanel.classList.add('active');
        e.stopPropagation();
    };
    // 关闭按钮
    closeBtn.onclick = function(e) {
        sidePanel.classList.remove('active');
        e.stopPropagation();
    };
    // 点击侧边栏外部关闭
    document.body.addEventListener('click', function(e) {
        if (sidePanel.classList.contains('active') && !sidePanel.contains(e.target) && e.target !== avatar) {
            sidePanel.classList.remove('active');
        }
    });
    sidePanel.onclick = function(e) { e.stopPropagation(); };

    // 修改密码
    document.getElementById('change-password-btn').onclick = async function() {
        const newPwd = document.getElementById('new-password').value.trim();
        const msg = document.getElementById('change-msg');
        if (!newPwd) {
            msg.textContent = "新密码不能为空";
            msg.style.color = "red";
            return;
        }
        const username = localStorage.getItem("loginUser");
        const res = await fetch('http://localhost:5000/api/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password: newPwd})
        });
        const data = await res.json();
        if (data.success) {
            msg.style.color = "green";
            msg.textContent = "密码修改成功";
        } else {
            msg.style.color = "red";
            msg.textContent = data.msg || "修改失败";
        }
    };

    // 退出登录
    document.getElementById('logout-btn').onclick = function() {
        localStorage.removeItem("loginUser");
        window.location.href = "login.html";
    };
});