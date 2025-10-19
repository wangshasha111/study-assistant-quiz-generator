# 🚀 快速部署参考卡

## 📝 GitHub Desktop 操作步骤

### 1️⃣ 添加仓库到 GitHub Desktop

1. 打开 **GitHub Desktop**
2. 点击 `File` → `Add Local Repository`
3. 点击 `Choose...` 选择项目文件夹
4. 点击 `Add Repository`

### 2️⃣ 查看要提交的文件

左侧会显示所有更改，确认包含：
- ✅ app.py
- ✅ database.py  
- ✅ admin_auth.py
- ✅ requirements.txt
- ✅ .streamlit/config.toml
- ✅ 所有 .md 文档

确认排除（不应出现）：
- ❌ .env
- ❌ venv/
- ❌ __pycache__/

### 3️⃣ 提交到本地

在左下角填写：
```
Summary: Initial commit - Study Assistant v1.0

Description:
- AI-powered study assistant
- Admin dashboard with authentication  
- Multi-user session tracking
- Ready for Streamlit Cloud deployment
```

点击 `Commit to main`

### 4️⃣ 发布到 GitHub

1. 点击 `Publish repository`
2. Repository name: `study-assistant-quiz-generator`
3. Description: `AI-powered quiz generator with admin dashboard`
4. 选择 Public 或 Private
5. 点击 `Publish Repository`

---

## ☁️ Streamlit Cloud 部署

### 1️⃣ 登录
- 访问: https://share.streamlit.io/
- 使用 GitHub 登录

### 2️⃣ 创建应用
- 点击 `New app`
- Repository: `study-assistant-quiz-generator`
- Branch: `main`
- Main file: `app.py`

### 3️⃣ 配置 Secrets

点击 `Advanced settings`，在 Secrets 中添加：

```toml
ADMIN_PASSWORD = "您的强密码"
```

**示例强密码**：`Admin@2025!Quiz`

### 4️⃣ 部署
- 点击 `Deploy!`
- 等待 2-5 分钟
- 获得 URL: `https://your-app.streamlit.app`

---

## ✅ 部署后测试清单

访问您的应用 URL，测试：

- [ ] 上传 PDF 功能
- [ ] 生成摘要和测验
- [ ] 下载结果
- [ ] 访问 Admin Dashboard
- [ ] Admin 密码登录
- [ ] 查看用户数据

---

## 🔧 常用命令（可选）

如果需要手动操作：

```bash
# 查看状态
git status

# 提交更改
git add .
git commit -m "Your message"

# 推送到 GitHub
git push origin main
```

---

## 📞 需要帮助？

查看详细文档：
- 📖 `STREAMLIT_DEPLOYMENT.md` - 完整部署指南
- 📖 `用户指南.md` - 使用说明
- 📖 `技术文档.md` - 技术细节

---

**预计时间**: 
- GitHub 上传: 5 分钟
- Streamlit 部署: 3-5 分钟
- 总计: **10 分钟内完成**

祝部署顺利！🎉
