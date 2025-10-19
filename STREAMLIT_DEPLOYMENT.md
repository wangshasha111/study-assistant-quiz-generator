# 🚀 Streamlit Cloud 部署指南

## 📋 部署前准备

### ✅ 已完成项
- [x] Git 仓库已初始化
- [x] .gitignore 配置完成
- [x] .streamlit/config.toml 创建完成
- [x] requirements.txt 准备就绪
- [x] 代码测试通过

---

## 📖 完整部署步骤

### 步骤 1: 提交代码到 Git 仓库

#### 使用 Git Desktop：

1. **打开 GitHub Desktop**
2. **添加本地仓库**：
   - 点击 `File` → `Add Local Repository`
   - 选择项目文件夹：
     ```
     /Users/wss2023/Dropbox/documents/gen AI curriculum/agentic/5_Introduction_to_Langchain_for_Agentic/project_study_assistant_quiz_generation
     ```
   - 点击 `Add Repository`

3. **查看更改**：
   - 左侧会显示所有更改的文件
   - 确认以下关键文件已包含：
     - ✅ `app.py`
     - ✅ `database.py`
     - ✅ `admin_auth.py`
     - ✅ `session_utils.py`
     - ✅ `requirements.txt`
     - ✅ `.streamlit/config.toml`
     - ✅ `pages/` 文件夹
     - ✅ 所有 `.md` 文档
   
   - 确认以下文件**未被包含**（被 .gitignore 排除）：
     - ❌ `.env` (敏感信息)
     - ❌ `venv/` (虚拟环境)
     - ❌ `__pycache__/`
     - ❌ `.DS_Store`
     - ❌ `.streamlit/secrets.toml`

4. **提交更改**：
   - 左下角输入提交信息：
     ```
     Initial commit - Study Assistant v1.0
     
     - AI-powered study assistant with quiz generation
     - Admin dashboard with authentication
     - Multi-user session tracking
     - PDF/Text processing support
     ```
   - 点击 `Commit to main`

5. **发布到 GitHub**：
   - 点击 `Publish repository`
   - 设置仓库名称（建议）：`study-assistant-quiz-generator`
   - **重要**：选择 `Public` 或 `Private`（Streamlit Cloud 两者都支持）
   - 取消勾选 `Keep this code private`（如果想公开）
   - 点击 `Publish Repository`

---

### 步骤 2: 部署到 Streamlit Cloud

#### 2.1 登录 Streamlit Cloud

1. 访问：https://share.streamlit.io/
2. 使用 GitHub 账号登录
3. 授权 Streamlit Cloud 访问您的 GitHub 仓库

#### 2.2 创建新应用

1. 点击 `New app` 按钮
2. 填写部署信息：
   - **Repository**: 选择您刚才上传的仓库（如：`study-assistant-quiz-generator`）
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (可选): 自定义域名前缀，如 `study-assistant`

3. 点击 `Advanced settings`（高级设置）

#### 2.3 配置环境变量（Secrets）

在 `Secrets` 区域，添加以下内容：

```toml
# Admin Password (必须)
ADMIN_PASSWORD = "您的强密码"

# OpenAI API Key (可选，也可以在应用中输入)
# OPENAI_API_KEY = "sk-your-api-key-here"
```

**重要提示**：
- 使用强密码（8+字符，包含大小写、数字、符号）
- 不要使用引号内的示例密码
- 如果不设置 OPENAI_API_KEY，用户可以在应用中手动输入

#### 2.4 配置 Python 版本（可选）

如果需要指定 Python 版本，在 `Python version` 下拉菜单选择：
- 推荐：`3.12` 或 `3.11`

#### 2.5 部署应用

1. 点击 `Deploy!` 按钮
2. 等待部署完成（通常需要 2-5 分钟）
3. 部署日志会实时显示在屏幕上

---

### 步骤 3: 验证部署

#### 3.1 检查部署状态

部署成功后，您会看到：
- ✅ 绿色的 `Running` 状态
- 🔗 应用 URL（如：`https://study-assistant.streamlit.app`）

#### 3.2 测试功能

访问您的应用 URL，测试以下功能：

1. **主应用测试**：
   - [ ] 上传 PDF 文件
   - [ ] 输入文本内容
   - [ ] 生成摘要和测验
   - [ ] 交互式答题
   - [ ] 下载结果（PDF/TXT）

2. **Admin Dashboard 测试**：
   - [ ] 访问 Admin Dashboard 页面
   - [ ] 输入密码登录
   - [ ] 查看用户会话数据
   - [ ] 查看生成记录
   - [ ] 查看测验结果

3. **调试模式测试**：
   - [ ] 启用调试模式
   - [ ] 测试无 API 调用功能

---

### 步骤 4: 配置自定义域名（可选）

#### 4.1 Streamlit Cloud 提供的域名
默认域名格式：`https://your-app-name.streamlit.app`

#### 4.2 自定义域名
1. 在 Streamlit Cloud 应用设置中点击 `Settings`
2. 选择 `General` → `Custom domain`
3. 按照指引配置 DNS 记录

---

## 🔧 部署后管理

### 查看日志
1. 登录 Streamlit Cloud
2. 选择您的应用
3. 点击 `Manage app` → `Logs`

### 更新应用
当您在 GitHub 上更新代码后：
1. 使用 Git Desktop 提交并推送更改
2. Streamlit Cloud 会**自动检测并重新部署**
3. 无需手动操作

### 重启应用
如果应用出现问题：
1. 点击 `Manage app` → `Reboot app`
2. 或修改代码触发自动重新部署

### 修改 Secrets
1. 点击 `Manage app` → `Settings`
2. 编辑 `Secrets` 区域
3. 点击 `Save`
4. 应用会自动重启

---

## 📊 资源限制（免费版）

Streamlit Cloud 免费版限制：
- ✅ 1 个公开应用
- ✅ 无限访客
- ⚠️ 1 GB 内存
- ⚠️ 1 个 CPU 核心
- ⚠️ 应用闲置后会休眠（首次访问需要唤醒，约10-30秒）

如需更多资源，可升级到付费版。

---

## 🔒 安全建议

### 生产环境检查清单
- [ ] 使用强 Admin 密码
- [ ] OpenAI API Key 仅在 Secrets 中配置
- [ ] 不要在代码中硬编码敏感信息
- [ ] 定期备份数据库（如需要）
- [ ] 监控 API 使用量和成本
- [ ] 启用 GitHub 仓库的分支保护

### 数据库注意事项
- Streamlit Cloud 的文件系统是**临时的**
- 应用重启后，`study_assistant.db` 会丢失
- 如需持久化数据，考虑使用：
  - ✅ 外部数据库（PostgreSQL, MySQL）
  - ✅ Streamlit 的数据连接功能
  - ✅ 云存储（AWS S3, Google Cloud Storage）

---

## 🐛 常见问题

### Q1: 应用部署失败
**A**: 检查部署日志，常见原因：
- 依赖包版本冲突
- Python 版本不兼容
- 文件路径错误

**解决方法**：
```bash
# 本地测试依赖
pip install -r requirements.txt
python3 -m py_compile app.py
```

### Q2: 应用加载缓慢
**A**: 免费版应用闲置后会休眠
- 首次访问需要唤醒（10-30秒）
- 考虑使用付费版保持常驻

### Q3: 数据库数据丢失
**A**: Streamlit Cloud 文件系统是临时的
- 每次重启会重置
- 使用外部数据库解决持久化问题

### Q4: OpenAI API 错误
**A**: 检查：
- API Key 是否正确配置在 Secrets 中
- API Key 格式：`OPENAI_API_KEY = "sk-..."`（注意大写）
- OpenAI 账户是否有余额

### Q5: 无法访问 Admin Dashboard
**A**: 检查：
- Secrets 中是否配置了 `ADMIN_PASSWORD`
- 密码格式正确（不要有额外的引号或空格）
- 清除浏览器缓存后重试

---

## 📞 获取帮助

### 官方资源
- Streamlit 文档：https://docs.streamlit.io/
- Streamlit 社区论坛：https://discuss.streamlit.io/
- Streamlit Cloud 文档：https://docs.streamlit.io/streamlit-community-cloud

### 项目文档
- 用户指南：`用户指南.md` / `USER_GUIDE_EN.md`
- 技术文档：`技术文档.md` / `TECHNICAL_GUIDE_EN.md`

---

## ✅ 部署检查清单

部署前：
- [x] Git 仓库初始化
- [x] 代码提交到 GitHub
- [x] requirements.txt 准备就绪
- [x] .gitignore 配置正确
- [x] .streamlit/config.toml 创建

部署时：
- [ ] Streamlit Cloud 账号登录
- [ ] GitHub 仓库连接
- [ ] Secrets 配置（ADMIN_PASSWORD）
- [ ] 应用成功部署

部署后：
- [ ] 测试主要功能
- [ ] 测试 Admin Dashboard
- [ ] 验证密码保护
- [ ] 检查日志无错误

---

## 🎉 恭喜！

完成上述步骤后，您的 Study Assistant 应用就成功部署到云端了！

您的应用将可以：
- ✅ 24/7 在线访问
- ✅ 自动扩展支持多用户
- ✅ 自动更新（当您推送代码到 GitHub）
- ✅ 安全的密码保护
- ✅ 全球访问速度优化

享受您的 AI 学习助手吧！🚀

---

**文档版本**: 1.0  
**更新日期**: 2025-10-19  
**适用平台**: Streamlit Cloud (Community/Free Tier)
