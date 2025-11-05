#!/bin/bash
# 数据库验证脚本

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "\n${CYAN}========================================${NC}"
echo -e "${CYAN}数据库验证和健康检查${NC}"
echo -e "${CYAN}========================================${NC}\n"

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 检查虚拟环境
if [ ! -d "$SCRIPT_DIR/backend/venv" ]; then
    echo -e "${RED}× 后端虚拟环境不存在${NC}"
    echo -e "${YELLOW}请先运行: ./setup.sh${NC}\n"
    exit 1
fi

# 检查 .env 文件
if [ ! -f "$SCRIPT_DIR/backend/.env" ]; then
    echo -e "${RED}× 配置文件不存在${NC}"
    echo -e "${YELLOW}请先运行: ./setup.sh${NC}\n"
    exit 1
fi

# 激活虚拟环境并运行数据库检查
cd "$SCRIPT_DIR/backend"
source venv/bin/activate

echo -e "${CYAN}运行数据库初始化和检查...${NC}\n"
python init_db.py

EXIT_CODE=$?

deactivate

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "\n${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ 数据库验证成功!${NC}"
    echo -e "${GREEN}========================================${NC}\n"
else
    echo -e "\n${RED}========================================${NC}"
    echo -e "${RED}✗ 数据库验证失败${NC}"
    echo -e "${RED}========================================${NC}\n"
    exit 1
fi
