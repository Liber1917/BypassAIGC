# 脚本使用指南

本文档介绍项目中可用的统一启动脚本及其用途。

## 📋 统一启动脚本

项目已整合为统一的交互式管理脚本，所有功能通过菜单访问。

---

## 统一启动脚本

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

## 📖 使用流程

### 首次安装

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
```

### 故障排查

```bash
# 使用统一脚本
./start.sh
# 选择选项 8 进行故障排查
# 选择选项 6 验证安装
# 选择选项 7 验证数据库
```

### 维护和更新

```bash
# 清理临时文件
./start.sh            # 选择选项 9

# 更新代码后重新安装依赖
git pull
./start.sh            # 选择选项 1

# 重启服务
./start.sh            # 选择选项 5（停止），然后选项 2（启动）
```

---

## 🔧 脚本权限

Linux/macOS 脚本需要执行权限：

```bash
# 添加执行权限
chmod +x start.sh start-macos.sh
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

---

## 💡 提示

1. **首次使用**: 运行统一脚本，选择菜单选项 1 进行环境配置
2. **Windows 用户**: 统一脚本会自动检测并优先使用 PowerShell 7+ 以避免兼容性问题
3. **验证安装**: 使用统一脚本的选项 6 确保一切正常
4. **后台运行**: Linux/macOS 推荐安装 tmux 以便更好地管理服务
5. **故障排查**: 遇到问题使用统一脚本的选项 8 获取诊断信息
6. **定期清理**: 使用统一脚本的选项 9 清理临时文件和缓存
7. **模型推荐**: 新配置文件默认使用 gemini-2.5-pro 模型，性能更优且成本更低

---

**最后更新**: 2025-01-09
