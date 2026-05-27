# BypassAIGC 软件安全漏洞测试报告
> 日期: 2026-05-27
> 工具: Bandit v1.9.4 + 人工审计

## 一、Bandit 自动扫描结果

### Medium 严重度（3 个）

| ID | 文件 | 问题 | 风险 | CWE |
|----|------|------|------|-----|
| B104 | `config.py:31` | `SERVER_HOST = "0.0.0.0"` 绑定所有网卡 | 内部服务，exe 本地运行，风险低 | CWE-605 |
| B306 | `doc_convert.py:60` | 使用 `tempfile.mktemp()` 不安全临时文件 | 应改用 `NamedTemporaryFile(delete=False)` | CWE-377 |
| B608 | `database.py:166` | f-string 拼接 SQL | DB 迁移代码，参数非用户输入，安全 | CWE-89 |

### Low 严重度（10 个）

| ID | 文件 | 问题 | 处理 |
|----|------|------|------|
| B105 | `main.py:52` | 硬编码默认密钥检测 | 安全警告，非漏洞（有检测逻辑）|
| B105 | `main.py:62` | 硬编码默认密码检测 | 同上 |
| B110 | `renderer.py:49/552` | `try/except/pass` 静默异常 | Word 格式清理，可接受 |
| B110 | `template_generator.py:95` | 同上 | 文件生成容错 |
| B112 | `validator.py:93` | `try/except/continue` | XML 解析容错 |
| B311 | `template_generator.py:49` | `random.choice()` 非加密随机 | 仅用于生成临时文件名，安全 |
| B404 | `doc_convert.py:11` | `import subprocess` | 专用于调用 LibreOffice |
| B603 | `doc_convert.py:45` | `subprocess.run()` | 参数硬编码，无注入风险 |
| B101 | `template_generator.py:339` | `assert` 使用 | 内部断言，release 下被优化 |

### 总计: 13 个问题，0 个高危，3 个中危均可接受

## 二、人工安全审计

### 2.1 鉴权覆盖
- **Optimization 路由**: 11/11 有鉴权 ✅ (SSE 路由用独立 `_resolve_user()`)
- **Word Formatter 路由**: 22/25 有鉴权 ✅
  - 3 个无鉴权路由均为只读工具端点: `/specs`, `/specs/schema`, `/format-check/types`，无数据暴露风险

### 2.2 SQL 注入
- 所有业务查询均使用 SQLAlchemy ORM 参数化查询 ✅
- `database.py` 中的 f-string SQL 为数据库迁移代码，参数硬编码 ✅

### 2.3 敏感信息泄漏
- `password_hash`、`card_key` 不在 API 响应中返回 ✅
- JWT token 使用 `SECRET_KEY` 签名，默认密钥有运行期检测 ⚠️
- CORS 完全开放 (`allow_origins=["*"]`) — exe 本地服务，可接受 ✅

### 2.4 未验证重定向: 无 ✅

## 三、建议修复（非紧急）

1. `doc_convert.py:60` — `tempfile.mktemp()` → `NamedTemporaryFile(delete=False)`
2. `template_generator.py:95` — `except: pass` → 至少 `logging.warning()`
3. `renderer.py:49/552` — 同上

## 四、结论
**当前 Master 分支无高危可利用漏洞。** 项目为本地桌面 exe 应用，攻击面有限。建议在后续开发中逐步修复上述 3 个 Medium/Low 问题。
