#!/bin/bash
# 停止所有服务脚本

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "\n${CYAN}========================================${NC}"
echo -e "${CYAN}停止 AI 学术写作助手服务${NC}"
echo -e "${CYAN}========================================${NC}\n"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STOPPED_COUNT=0

# 停止 tmux 会话
if command -v tmux &> /dev/null; then
    if tmux has-session -t bypassaigc-backend 2>/dev/null; then
        tmux kill-session -t bypassaigc-backend
        echo -e "${GREEN}✓ 已停止后端 tmux 会话${NC}"
        STOPPED_COUNT=$((STOPPED_COUNT + 1))
    fi
    
    if tmux has-session -t bypassaigc-frontend 2>/dev/null; then
        tmux kill-session -t bypassaigc-frontend
        echo -e "${GREEN}✓ 已停止前端 tmux 会话${NC}"
        STOPPED_COUNT=$((STOPPED_COUNT + 1))
    fi
fi

# 停止 screen 会话
if command -v screen &> /dev/null; then
    if screen -ls | grep -q bypassaigc-backend; then
        screen -X -S bypassaigc-backend quit
        echo -e "${GREEN}✓ 已停止后端 screen 会话${NC}"
        STOPPED_COUNT=$((STOPPED_COUNT + 1))
    fi
    
    if screen -ls | grep -q bypassaigc-frontend; then
        screen -X -S bypassaigc-frontend quit
        echo -e "${GREEN}✓ 已停止前端 screen 会话${NC}"
        STOPPED_COUNT=$((STOPPED_COUNT + 1))
    fi
fi

# 通过 PID 文件停止
if [ -f "$SCRIPT_DIR/backend.pid" ]; then
    BACKEND_PID=$(cat "$SCRIPT_DIR/backend.pid")
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID
        echo -e "${GREEN}✓ 已停止后端服务 (PID: $BACKEND_PID)${NC}"
        STOPPED_COUNT=$((STOPPED_COUNT + 1))
    fi
    rm "$SCRIPT_DIR/backend.pid"
fi

if [ -f "$SCRIPT_DIR/frontend.pid" ]; then
    FRONTEND_PID=$(cat "$SCRIPT_DIR/frontend.pid")
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID
        echo -e "${GREEN}✓ 已停止前端服务 (PID: $FRONTEND_PID)${NC}"
        STOPPED_COUNT=$((STOPPED_COUNT + 1))
    fi
    rm "$SCRIPT_DIR/frontend.pid"
fi

# 通过端口停止进程（后备方案）
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}发现端口 8000 上有进程运行${NC}"
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    echo -e "${GREEN}✓ 已停止端口 8000 上的进程${NC}"
    STOPPED_COUNT=$((STOPPED_COUNT + 1))
fi

if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}发现端口 3000 上有进程运行${NC}"
    lsof -ti:3000 | xargs kill -9 2>/dev/null
    echo -e "${GREEN}✓ 已停止端口 3000 上的进程${NC}"
    STOPPED_COUNT=$((STOPPED_COUNT + 1))
fi

# 显示结果
echo -e "\n${GREEN}========================================${NC}"
if [ $STOPPED_COUNT -gt 0 ]; then
    echo -e "${GREEN}✓ 已停止 $STOPPED_COUNT 个服务${NC}"
else
    echo -e "${YELLOW}⚠ 未发现运行中的服务${NC}"
fi
echo -e "${GREEN}========================================${NC}\n"
