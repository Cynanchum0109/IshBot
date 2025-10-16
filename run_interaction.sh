#!/bin/bash
# 运行 Sphero 互动程序（抑制后台错误）

cd "$(dirname "$0")"
source sphero_env/bin/activate

echo "正在启动 Sphero 互动程序..."
echo "（后台线程错误已被抑制）"
echo ""

python3 Sphero_Interaction.py 2>/dev/null

echo ""
echo "程序已退出"

