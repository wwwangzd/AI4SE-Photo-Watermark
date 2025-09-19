#!/bin/bash

# 图片水印工具使用示例脚本

echo "=== 图片水印工具使用示例 ==="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python"
    exit 1
fi

# 检查是否安装了依赖
echo "1. 安装依赖包..."
pip3 install -r requirements.txt

echo ""
echo "2. 使用示例："
echo ""

# 创建测试目录结构
echo "创建示例目录结构..."
mkdir -p example_photos

echo ""
echo "=== 基本使用方法 ==="
echo ""
echo "# 使用默认设置处理图片（白色水印，24号字体，右下角）"
echo "python3 watermark.py ./example_photos"
echo ""

echo "# 自定义字体大小和颜色"
echo "python3 watermark.py ./example_photos --size 36 --color \"#FFFFFF\""
echo ""

echo "# 设置水印位置"
echo "python3 watermark.py ./example_photos --position top-left"
echo ""

echo "# 完整自定义参数"
echo "python3 watermark.py ./example_photos --size 48 --color \"#FFD700\" --position center"
echo ""

echo "=== 更多位置选项 ==="
echo "top-left, top-center, top-right"
echo "center-left, center, center-right"
echo "bottom-left, bottom-center, bottom-right"
echo ""

echo "=== 常用颜色 ==="
echo "白色: #FFFFFF"
echo "黑色: #000000"
echo "红色: #FF0000"
echo "蓝色: #0000FF"
echo "黄色: #FFFF00"
echo "金色: #FFD700"
echo ""

echo "=== 注意事项 ==="
echo "1. 确保图片包含EXIF拍摄时间信息"
echo "2. 输出图片保存在 {原目录名}_watermark 子目录中"
echo "3. 原始图片不会被修改"
echo ""

echo "请将您的图片放入一个目录，然后运行："
echo "python3 watermark.py /path/to/your/photos"