#!/bin/bash
# Sphero虚拟环境激活脚本
# 使用方法: source activate.sh

cd "$(dirname "$0")"
source sphero_env/bin/activate

echo "✅ Sphero虚拟环境已激活"
echo "📍 工作目录: $(pwd)"
echo "🐍 Python版本: $(python3 --version)"
echo "⚠️  注意: 使用 Python 3.12，spherov2 在 3.13+ 有兼容性问题"
echo ""
echo "可用命令："
echo "  python3 Interactive_Sphero.py      # 运行交互式控制"
echo "  python3 test_pattern_module.py     # 测试图案模块"
echo "  deactivate                         # 退出虚拟环境"
echo ""

