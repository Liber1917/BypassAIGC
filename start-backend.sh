#!/bin/bash
# 启动后端服务
# 适用于 Linux/Ubuntu/macOS

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "\n${CYAN}========================================${NC}"
echo -e "${CYAN}启动后端服务${NC}"
echo -e "${CYAN}========================================${NC}\n"

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 进入后端目录
cd "$SCRIPT_DIR/backend" || exit 1

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠ 虚拟环境不存在,请先运行 ./setup.sh${NC}"
    exit 1
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠ 配置文件不存在,请先运行 ./setup.sh${NC}"
    exit 1
fi

# 激活虚拟环境
source venv/bin/activate

# 检查端口是否被占用
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠ 端口 8000 已被占用${NC}"
    echo -e "${CYAN}尝试停止旧进程...${NC}"
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    sleep 2
fi

# 初始化数据库（如果不存在）
if [ ! -f "ai_polish.db" ]; then
    echo -e "${CYAN}首次运行，正在初始化数据库...${NC}"
    echo -e "${CYAN}数据库将在后端服务启动时自动创建${NC}"
fi

# 启动服务
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ 后端服务启动中...${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${CYAN}访问地址:${NC}"
echo -e "  API: ${YELLOW}http://localhost:8000${NC}"
echo -e "  文档: ${YELLOW}http://localhost:8000/docs${NC}"
echo -e "  健康检查: ${YELLOW}http://localhost:8000/health${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${YELLOW}按 Ctrl+C 停止服务${NC}\n"

# 启动 uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
