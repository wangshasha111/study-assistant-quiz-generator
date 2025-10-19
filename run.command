#!/bin/bash

# Study Assistant Quiz Generator - macOS Launch Script
# 双击此文件即可启动应用

# 获取脚本所在目录
cd "$(dirname "$0")"

echo "================================================"
echo "  📚 Study Assistant - Quiz Generator"
echo "================================================"
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    echo "请先安装 Python 3: https://www.python.org/downloads/"
    echo ""
    read -p "按 Enter 键退出..."
    exit 1
fi

echo "✓ Python 版本: $(python3 --version)"
echo ""

# 检查是否存在虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 首次运行：创建虚拟环境..."
    python3 -m venv venv
    
    if [ $? -eq 0 ]; then
        echo "✓ 虚拟环境创建成功"
    else
        echo "❌ 虚拟环境创建失败"
        read -p "按 Enter 键退出..."
        exit 1
    fi
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 检查是否需要安装依赖
if [ ! -f "venv/.dependencies_installed" ]; then
    echo "📥 安装依赖包（首次运行可能需要几分钟）..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo "✓ 依赖包安装成功"
        touch venv/.dependencies_installed
    else
        echo "❌ 依赖包安装失败"
        read -p "按 Enter 键退出..."
        exit 1
    fi
else
    echo "✓ 依赖包已安装"
fi

echo ""
echo "================================================"
echo "  🚀 启动 Study Assistant..."
echo "================================================"
echo ""
echo "应用将在浏览器中自动打开"
echo "如果没有自动打开，请访问: http://localhost:8501"
echo ""
echo "⚠️  关闭此窗口将停止应用"
echo "================================================"
echo ""

# 启动 Streamlit 应用
streamlit run app.py

# 如果应用关闭，等待用户确认
echo ""
echo "应用已关闭"
read -p "按 Enter 键退出..."
