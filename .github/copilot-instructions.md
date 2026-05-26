# Copilot Review Instructions — BypassAIGC

## 审查重点

### 1. SSE/EventSource 路由
- `?token=` query param 必须能被实际使用，不能有死代码
- `Depends(get_current_user)` 在 SSE 路由中会先于 `token` 检查执行 → 必须用 `_resolve_user()` 或等效逻辑
- 前端 `getStreamUrl()` 生成的 URL 必须与后端路由签名匹配

### 2. 参数传递完整性
- 任何 `Query(None)` 声明的参数（token, card_key 等），在调用 `get_current_user()` 时必须实际传递
- grep 检查点：`grep -n "get_current_user("` 确认每个调用都传了对应参数

### 3. GBK 兼容性（Windows 中文系统）
- 所有 `print()` / `logging` 调用中禁止使用 emoji（⚠️ ✅ ❌ 🚀 🌐 🛑 ✓ ✗ 等）
- 统一使用纯文本替代：[安全警告] [成功] [失败] [停止] [OK]
- emoji 在 Windows GBK 控制台会触发 `UnicodeEncodeError` 导致 exe 崩溃

### 4. 前端-后端一致性
- API token 必须统一使用 `sessionStorage`（禁止 `localStorage`）
- SSE URL 使用 `?token=`（EventSource 不支持自定义 Header）
- 普通 API 请求使用 `Authorization: Bearer`

### 5. 测试覆盖
- 每个 Bug 修复必须有对应的回归测试
- 测试必须能复现原 bug 并证明已修复
- 新增路由必须有对应的 API 测试

## 禁止模式
- 禁止在 `Depends()` 后面跟不可达的 `if token` 判断
- 禁止使用 `pass` 代替 `raise NotImplementedError` 或实际实现
- 禁止 hardcode 版本号不一致（保持 `package/main.py` / `frontend/package.json` / `backend/main.py` 同步）

## Python 规范
- 遵循 isort + black 导包规范：标准库 → 第三方 → 本地模块
- 禁止使用已废弃 API：`datetime.utcnow()` → `datetime.now(datetime.UTC)`，`@app.on_event` → lifespan handlers
- 所有 print() 日志必须前缀命名空间，如 `[WORD-FORMATTER]`, `[AI]`, `[DB]`
