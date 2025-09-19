#!/usr/bin/env python3
"""
测试脚本 - 验证水印程序的基本功能
"""

import os
import sys
import tempfile
import shutil
from datetime import datetime
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS

def create_test_image_with_exif(filename, date_str="2024:01:15 14:30:00"):
    """创建一个带有EXIF信息的测试图片"""
    # 创建一个简单的测试图片
    img = Image.new('RGB', (800, 600), color='lightblue')
    
    # 添加一些基本的EXIF信息
    # 注意：PIL对EXIF写入的支持有限，这里我们创建一个简单的图片用于测试
    img.save(filename, 'JPEG', quality=95)
    print(f"创建测试图片: {filename}")
    
    return filename

def test_watermark_program():
    """测试水印程序的主要功能"""
    print("=== 开始测试图片水印程序 ===")
    
    # 创建临时测试目录
    test_dir = tempfile.mkdtemp(prefix="watermark_test_")
    print(f"测试目录: {test_dir}")
    
    try:
        # 创建测试图片
        test_image = os.path.join(test_dir, "test_photo.jpg")
        create_test_image_with_exif(test_image)
        
        # 测试程序是否能正常运行（即使没有EXIF信息）
        import subprocess
        
        print("\n1. 测试程序基本运行...")
        result = subprocess.run([
            sys.executable, 
            "watermark.py", 
            test_dir,
            "--size", "24",
            "--color", "#FF0000",
            "--position", "bottom-right"
        ], capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"返回码: {result.returncode}")
        
        # 检查输出目录是否创建
        output_dir = os.path.join(test_dir, f"{os.path.basename(test_dir)}_watermark")
        if os.path.exists(output_dir):
            print(f"✓ 输出目录创建成功: {output_dir}")
            
            # 列出输出文件
            output_files = os.listdir(output_dir)
            print(f"输出文件: {output_files}")
        else:
            print("✗ 输出目录未创建")
        
        print("\n2. 测试不同参数...")
        
        # 测试不同位置
        positions = ["top-left", "center", "bottom-right"]
        for pos in positions:
            print(f"测试位置: {pos}")
            result = subprocess.run([
                sys.executable, 
                "watermark.py", 
                test_dir,
                "--position", pos,
                "--size", "20"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✓ 位置 {pos} 测试通过")
            else:
                print(f"✗ 位置 {pos} 测试失败")
        
        print("\n3. 测试错误处理...")
        
        # 测试不存在的目录
        result = subprocess.run([
            sys.executable, 
            "watermark.py", 
            "/nonexistent/directory"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("✓ 正确处理了不存在的目录")
        else:
            print("✗ 没有正确处理不存在的目录")
        
        # 测试无效的颜色格式
        result = subprocess.run([
            sys.executable, 
            "watermark.py", 
            test_dir,
            "--color", "invalid_color"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("✓ 正确处理了无效的颜色格式")
        else:
            print("✗ 没有正确处理无效的颜色格式")
            
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        
    finally:
        # 清理测试目录
        try:
            shutil.rmtree(test_dir)
            print(f"\n清理测试目录: {test_dir}")
        except Exception as e:
            print(f"清理目录时出错: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    # 切换到脚本目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    test_watermark_program()