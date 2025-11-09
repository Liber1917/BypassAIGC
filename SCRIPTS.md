# 脚本使用指南

本文档列出了项目中所有可用的脚本及其用途。

## 📋 目录

- [统一启动脚本（推荐）](#统一启动脚本推荐)
- [传统独立脚本](#传统独立脚本)
  - [安装脚本](#安装脚本)
  - [启动脚本](#启动脚本)
  - [验证脚本](#验证脚本)
  - [维护脚本](#维护脚本)
- [平台特定脚本](#平台特定脚本)

---

## 统一启动脚本（推荐）

### `start.ps1` (Windows)
### `start.sh` (Linux/Ubuntu)
### `start-macos.sh` (macOS)

**用途**: 统一的交互式管理脚本，整合了所有常用功能

**功能菜单**:
1. **环境安装配置** - 一键安装和配置所有依赖
2. **启动所有服务** - 同时启动前端和后端服务
3. **仅启动后端服务** - 启动 FastAPI 后端（端口 8000）
4. **仅启动前端服务** - 启动 React 前端（端口 3000）
5. **停止所有服务** - 停止所有正在运行的服务
6. **验证安装** - 检查环境配置和依赖安装情况
7. **验证数据库** - 检查数据库配置和连接状态
8. **故障排查** - 生成诊断报告（Linux/macOS）
9. **清理环境** - 清理临时文件或重置环境（Linux/macOS）
0. **退出**

**特性**:
- **Windows 版本**: 自动检测并优先使用 PowerShell 7+ (pwsh.exe) 以避免 PowerShell 5.1 兼容性问题
- **Linux/macOS 版本**: 自动检测 tmux/screen 实现后台运行
- **交互式菜单**: 友好的用户界面，提供详细的选项说明
- **智能检测**: 自动检查依赖和环境状态
- **命令行模式**: 支持直接传入选项编号，如 `./start.sh 2` 直接启动所有服务

**使用示例**:

```bash
# macOS
./start-macos.sh        # 交互式菜单
./start-macos.sh 1      # 直接执行环境配置
./start-macos.sh 2      # 直接启动所有服务

# Linux/Ubuntu  
./start.sh              # 交互式菜单
./start.sh 2            # 直接启动所有服务

# Windows
.\start.ps1             # 交互式菜单
.\start.ps1 -Option 2   # 直接启动所有服务
```

**推荐模型配置**: 
- 所有新生成的配置文件默认使用 `gemini-2.5-pro` 模型
- 推荐使用 Google Gemini 以获得更好的性能和成本效益

---

## 传统独立脚本

以下脚本仍然可用，适合需要单独功能或脚本化操作的场景。

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

### 首次安装（推荐使用统一脚本）

```bash
# macOS
./start-macos.sh
# 选择选项 1 进行环境配置

# Linux/Ubuntu
./start.sh
# 选择选项 1 进行环境配置

# Windows
.\start.ps1
# 选择选项 1 进行环境配置
```

配置完成后，编辑 `backend/.env` 填入 API 密钥（推荐使用 gemini-2.5-pro）。

### 日常使用

```bash
# 启动服务 - 使用统一脚本
./start-macos.sh  # 或 ./start.sh (Linux) 或 .\start.ps1 (Windows)
# 选择选项 2 启动所有服务
# 选择选项 5 停止所有服务

# 或使用传统脚本
./start-all-macos.sh   # macOS
./start-all.sh         # Linux/Ubuntu
.\start-all.ps1        # Windows (注意：可能有 PowerShell 5.1 兼容性问题)
```

### 故障排查

```bash
# 使用统一脚本
./start.sh
# 选择选项 8 进行故障排查
# 选择选项 6 验证安装
# 选择选项 7 验证数据库

# 或使用传统脚本
./troubleshoot.sh      # 生成诊断报告
./verify-installation.sh
./verify-database.sh
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

1. **首次使用**: 推荐使用统一脚本（start.ps1 / start.sh / start-macos.sh），选择菜单选项 1 进行环境配置
2. **Windows 用户**: 统一脚本会自动检测并优先使用 PowerShell 7+ 以避免兼容性问题
3. **验证安装**: 使用统一脚本的选项 6 确保一切正常
4. **后台运行**: Linux/macOS 推荐安装 tmux 以便更好地管理服务
5. **故障排查**: 遇到问题使用统一脚本的选项 8 获取诊断信息
6. **定期清理**: 使用统一脚本的选项 9 清理临时文件和缓存
7. **模型推荐**: 新配置文件默认使用 gemini-2.5-pro 模型，性能更优且成本更低

---

**最后更新**: 2025-01-09
