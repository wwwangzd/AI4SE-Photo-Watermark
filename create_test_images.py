#!/usr/bin/env python3
"""
创建带有EXIF信息的测试图片
"""

import os
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import piexif

def create_test_image_with_exif(output_path, width=800, height=600, date_taken=None):
    """
    创建一个带有EXIF拍摄时间信息的测试图片
    
    Args:
        output_path (str): 输出图片路径
        width (int): 图片宽度
        height (int): 图片高度  
        date_taken (str): 拍摄时间，格式为 "YYYY:MM:DD HH:MM:SS"
    """
    if date_taken is None:
        date_taken = "2024:03:15 14:30:22"
    
    # 创建一个简单的测试图片
    img = Image.new('RGB', (width, height), color='lightblue')
    
    # 添加一些图形元素
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(img)
    
    # 绘制一些简单的图形
    draw.rectangle([50, 50, width-50, height-50], outline='navy', width=3)
    draw.ellipse([width//4, height//4, 3*width//4, 3*height//4], outline='darkblue', width=2)
    
    # 添加文本
    try:
        font = ImageFont.load_default()
        text = f"Test Photo\nSize: {width}x{height}\nDate: {date_taken}"
        draw.text((width//2-100, height//2-20), text, fill='navy', font=font)
    except:
        pass
    
    # 创建EXIF数据
    exif_dict = {
        "0th": {
            piexif.ImageIFD.Make: "Test Camera",
            piexif.ImageIFD.Model: "Test Model",
            piexif.ImageIFD.Software: "Test Script",
            piexif.ImageIFD.DateTime: date_taken,
        },
        "Exif": {
            piexif.ExifIFD.DateTimeOriginal: date_taken,
            piexif.ExifIFD.DateTimeDigitized: date_taken,
            piexif.ExifIFD.ExifVersion: b"0220",
        },
        "GPS": {},
        "1st": {},
        "thumbnail": None
    }
    
    # 生成EXIF字节数据
    exif_bytes = piexif.dump(exif_dict)
    
    # 保存图片
    img.save(output_path, "JPEG", quality=95, exif=exif_bytes)
    print(f"已创建测试图片: {output_path}")
    print(f"拍摄时间: {date_taken}")

def create_sample_photos():
    """创建一些示例照片用于测试"""
    # 创建示例目录
    sample_dir = "sample_photos"
    os.makedirs(sample_dir, exist_ok=True)
    
    # 创建不同日期的测试图片
    test_dates = [
        "2024:01:15 10:30:45",
        "2024:02:20 15:22:10", 
        "2024:03:25 09:15:33",
        "2023:12:31 23:59:59",
        "2024:06:01 12:00:00"
    ]
    
    for i, date in enumerate(test_dates, 1):
        filename = os.path.join(sample_dir, f"photo_{i:02d}.jpg")
        create_test_image_with_exif(filename, 1024, 768, date)
    
    print(f"\n已在 {sample_dir} 目录中创建 {len(test_dates)} 张测试图片")
    print("\n现在可以运行水印程序:")
    print(f"python3 watermark.py {sample_dir}")
    print(f"python3 watermark.py {sample_dir} --size 32 --color '#FF0000' --position center")

if __name__ == "__main__":
    try:
        import piexif
    except ImportError:
        print("正在安装 piexif 库...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "piexif"])
        import piexif
    
    create_sample_photos()