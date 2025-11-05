# 脚本使用指南

本文档列出了项目中所有可用的脚本及其用途。

## 📋 目录

- [安装脚本](#安装脚本)
- [启动脚本](#启动脚本)
- [验证脚本](#验证脚本)
- [维护脚本](#维护脚本)
- [平台特定脚本](#平台特定脚本)

---

## 安装脚本

### `setup.sh` (Linux/Ubuntu)
**用途**: 在 Linux/Ubuntu 系统上安装和配置环境

**功能**:
- 检查 Python 3.10+ 和 Node.js 16+
- 创建 Python 虚拟环境
- 安装后端和前端依赖
- 生成 .env 配置文件（如果不存在）
- 验证数据库配置

**使用**:
```bash
chmod +x setup.sh
./setup.sh
```

---

### `setup-macos.sh` (macOS)
**用途**: 在 macOS 系统上安装和配置环境

**功能**:
- 自动安装 Homebrew（如果需要）
- 通过 Homebrew 安装 Python 和 Node.js
- 创建虚拟环境并安装依赖
- 生成配置文件
- 验证数据库

**使用**:
```bash
chmod +x setup-macos.sh
./setup-macos.sh
```

---

### `setup.ps1` (Windows)
**用途**: 在 Windows 系统上安装和配置环境

**功能**:
- 检查 Python 和 Node.js
- 创建虚拟环境
- 安装依赖
- 生成配置文件

**使用**:
```powershell
.\setup.ps1
```

---

## 启动脚本

### `start-backend.sh` (Linux/macOS)
**用途**: 启动后端服务

**功能**:
- 检查虚拟环境和配置文件
- 检测并清理端口占用
- 启动 FastAPI 后端服务（端口 8000）

**使用**:
```bash
./start-backend.sh
```

---

### `start-frontend.sh` (Linux/macOS)
**用途**: 启动前端服务

**功能**:
- 检查 node_modules
- 检测并清理端口占用
- 启动前端开发服务器（端口 3000）

**使用**:
```bash
./start-frontend.sh
```

---

### `start-all.sh` (Linux/Ubuntu)
**用途**: 一键启动所有服务（使用 tmux/screen 或后台运行）

**功能**:
- 检查环境配置
- 自动选择 tmux、screen 或 nohup 方式运行
- 同时启动后端和前端服务
- 提供服务管理说明

**使用**:
```bash
./start-all.sh
```

**会话管理**:
```bash
# 查看 tmux 会话
tmux ls

# 进入后端会话
tmux attach -t bypassaigc-backend

# 进入前端会话
tmux attach -t bypassaigc-frontend

# 退出会话（不停止服务）
Ctrl+B, D
```

---

### `start-all-macos.sh` (macOS)
**用途**: macOS 专用的一键启动脚本

**功能**:
- 优先使用 tmux 管理服务
- 自动在浏览器打开前端页面
- 提供 macOS 特定的管理说明

**使用**:
```bash
./start-all-macos.sh
```

---

### `start-backend.ps1` (Windows)
**用途**: Windows 系统启动后端服务

**使用**:
```powershell
.\start-backend.ps1
```

---

### `start-frontend.ps1` (Windows)
**用途**: Windows 系统启动前端服务

**使用**:
```powershell
.\start-frontend.ps1
```

---

### `start-all.ps1` (Windows)
**用途**: Windows 系统一键启动

**功能**:
- 在新窗口中启动后端和前端
- 显示访问地址

**使用**:
```powershell
.\start-all.ps1
```

---

### `stop-all.sh` (Linux/macOS)
**用途**: 停止所有运行中的服务

**功能**:
- 停止 tmux/screen 会话
- 通过 PID 文件停止进程
- 清理端口占用

**使用**:
```bash
./stop-all.sh
```

---

## 验证脚本

### `verify-installation.sh` (Linux/macOS)
**用途**: 全面验证安装状态

**检查项**:
- Python 和 Node.js 版本
- 虚拟环境和依赖包
- 前端依赖
- 配置文件完整性
- 数据库状态
- 端口占用情况
- 脚本权限

**使用**:
```bash
./verify-installation.sh
```

**输出示例**:
```
[1/8] 检查 Python...
✓ Python 3.11.5
[2/8] 检查 Node.js...
✓ Node.js v18.17.0
...
✓ 所有检查通过!
```

---

### `verify-installation.ps1` (Windows)
**用途**: Windows 系统的安装验证

**使用**:
```powershell
.\verify-installation.ps1
```

---

### `verify-database.sh` (Linux/macOS)
**用途**: 专门验证数据库配置

**功能**:
- 运行数据库初始化脚本
- 检查数据库连接
- 验证表结构
- 测试 CRUD 操作

**使用**:
```bash
./verify-database.sh
```

---

### `verify-database.ps1` (Windows)
**用途**: Windows 数据库验证

**使用**:
```powershell
.\verify-database.ps1
```

---

### `backend/init_db.py`
**用途**: 数据库初始化和健康检查工具

**功能**:
- 创建数据库表结构
- 迁移数据库架构
- 检查数据完整性
- 测试数据库操作
- 生成诊断报告

**使用**:
```bash
cd backend
source venv/bin/activate
python init_db.py
```

---

## 维护脚本

### `troubleshoot.sh` (Linux/macOS)
**用途**: 故障排查和诊断工具

**功能**:
- 收集系统信息
- 检查运行中的进程
- 显示最近的日志
- 检查配置文件
- 验证数据库状态
- 测试网络连接
- 检查依赖包
- 生成诊断报告

**使用**:
```bash
./troubleshoot.sh
```

**生成报告位置**: `/tmp/bypassaigc-diagnostic-YYYYMMDD-HHMMSS.txt`

---

### `cleanup.sh` (Linux/Ubuntu)
**用途**: 清理临时文件和重置环境

**选项**:
1. 清理临时文件和日志
2. 停止所有服务
3. 删除数据库（保留配置）
4. 完全重置（删除虚拟环境和依赖）
5. 清理编译文件和缓存

**使用**:
```bash
./cleanup.sh
```

**示例场景**:
```bash
# 场景 1: 清理日志
./cleanup.sh
# 选择: 1

# 场景 2: 完全重置后重新安装
./cleanup.sh
# 选择: 4
./setup.sh
```

---

### `cleanup-macos.sh` (macOS)
**用途**: macOS 专用清理工具

**额外功能**:
- 清理 .DS_Store 文件
- 卸载 launchd 服务

**使用**:
```bash
./cleanup-macos.sh
```

---

## 平台特定脚本

### Linux/Ubuntu 脚本
- `setup.sh` - 安装配置
- `start-all.sh` - 一键启动（支持 tmux/screen/nohup）
- `start-backend.sh` - 启动后端
- `start-frontend.sh` - 启动前端
- `stop-all.sh` - 停止服务
- `verify-installation.sh` - 验证安装
- `verify-database.sh` - 验证数据库
- `troubleshoot.sh` - 故障排查
- `cleanup.sh` - 清理工具

### macOS 脚本
- `setup-macos.sh` - macOS 安装（自动安装 Homebrew）
- `start-all-macos.sh` - macOS 一键启动（优化的 tmux 支持）
- `start-backend.sh` - 启动后端（通用）
- `start-frontend.sh` - 启动前端（通用）
- `stop-all.sh` - 停止服务（通用）
- `verify-installation.sh` - 验证安装（通用）
- `verify-database.sh` - 验证数据库（通用）
- `troubleshoot.sh` - 故障排查（通用）
- `cleanup-macos.sh` - macOS 清理工具

### Windows 脚本
- `setup.ps1` - 安装配置
- `start-all.ps1` - 一键启动
- `start-backend.ps1` - 启动后端
- `start-frontend.ps1` - 启动前端
- `verify-installation.ps1` - 验证安装
- `verify-database.ps1` - 验证数据库

---

## 📖 使用流程

### 首次安装
```bash
# 1. 选择对应平台的安装脚本
./setup.sh              # Linux/Ubuntu
./setup-macos.sh        # macOS
.\setup.ps1             # Windows

# 2. 配置 API 密钥
nano backend/.env       # Linux/macOS
notepad backend\.env    # Windows

# 3. 验证安装（可选）
./verify-installation.sh     # Linux/macOS
.\verify-installation.ps1    # Windows
```

### 日常使用
```bash
# 启动服务
./start-all.sh          # Linux/Ubuntu
./start-all-macos.sh    # macOS
.\start-all.ps1         # Windows

# 停止服务
./stop-all.sh           # Linux/macOS
# Windows: 直接关闭窗口或 Ctrl+C
```

### 故障排查
```bash
# 1. 运行诊断
./troubleshoot.sh

# 2. 查看日志
tail -f backend/backend.log
tail -f frontend/frontend.log

# 3. 验证数据库
./verify-database.sh

# 4. 如果需要，清理并重装
./cleanup.sh            # 选择清理选项
./setup.sh              # 重新安装
```

### 维护和更新
```bash
# 清理临时文件
./cleanup.sh            # 选择 1

# 更新代码后重新安装依赖
git pull
./setup.sh              # 或 setup-macos.sh / setup.ps1

# 重启服务
./stop-all.sh
./start-all.sh
```

---

## 🔧 脚本权限

Linux/macOS 脚本需要执行权限：

```bash
# 一次性添加所有脚本的执行权限
chmod +x *.sh
```

Windows PowerShell 脚本可能需要执行策略调整：

```powershell
# 允许执行脚本（以管理员身份运行）
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📚 相关文档

- [README.md](README.md) - 项目概览和快速开始
- [DEPLOY.md](DEPLOY.md) - 详细的部署指南
- [DATABASE_SETUP.md](DATABASE_SETUP.md) - 数据库配置说明

---

## 💡 提示

1. **首次使用**: 始终从安装脚本开始（setup.sh / setup-macos.sh / setup.ps1）
2. **验证安装**: 使用 verify-installation 脚本确保一切正常
3. **后台运行**: Linux/macOS 推荐安装 tmux 以便更好地管理服务
4. **故障排查**: 遇到问题先运行 troubleshoot.sh 获取诊断信息
5. **定期清理**: 使用 cleanup 脚本清理临时文件和缓存

---

**最后更新**: 2024-11-05
