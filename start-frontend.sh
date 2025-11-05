#!/bin/bash
# 启动前端服务
# 适用于 Linux/Ubuntu/macOS

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "\n${CYAN}========================================${NC}"
echo -e "${CYAN}启动前端服务${NC}"
echo -e "${CYAN}========================================${NC}\n"

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 进入前端目录
cd "$SCRIPT_DIR/frontend" || exit 1

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}⚠ 前端依赖未安装,请先运行 ./setup.sh${NC}"
    exit 1
fi

# 检查端口是否被占用
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠ 端口 3000 已被占用${NC}"
    echo -e "${CYAN}尝试停止旧进程...${NC}"
    lsof -ti:3000 | xargs kill -9 2>/dev/null
    sleep 2
fi

# 启动服务
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ 前端服务启动中...${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${CYAN}访问地址:${NC}"
echo -e "  前端: ${YELLOW}http://localhost:3000${NC}"
echo -e "  管理后台: ${YELLOW}http://localhost:3000/admin${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${YELLOW}按 Ctrl+C 停止服务${NC}\n"

# 启动开发服务器
npm run dev
