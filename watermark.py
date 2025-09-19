#!/usr/bin/env python3
"""
图片水印工具 - 基于EXIF拍摄时间添加日期水印
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ExifTags
import exifread


def get_date_from_exif(image_path):
    """
    从图片的EXIF信息中提取拍摄日期
    
    Args:
        image_path (str): 图片文件路径
        
    Returns:
        str: 格式化的日期字符串 (YYYY-MM-DD) 或 None
    """
    try:
        # 尝试使用PIL读取EXIF
        with Image.open(image_path) as img:
            exif_dict = img._getexif()
            if exif_dict:
                for tag_id, value in exif_dict.items():
                    tag = ExifTags.TAGS.get(tag_id, tag_id)
                    if tag == "DateTime" or tag == "DateTimeOriginal":
                        # 格式通常是 "YYYY:MM:DD HH:MM:SS"
                        date_str = str(value)
                        try:
                            date_obj = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
                            return date_obj.strftime("%Y-%m-%d")
                        except ValueError:
                            continue
        
        # 如果PIL方法失败，尝试使用exifread
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)
            date_tags = [
                'EXIF DateTimeOriginal',
                'EXIF DateTime',
                'Image DateTime'
            ]
            
            for tag_name in date_tags:
                if tag_name in tags:
                    date_str = str(tags[tag_name])
                    try:
                        date_obj = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
                        return date_obj.strftime("%Y-%m-%d")
                    except ValueError:
                        continue
                        
    except Exception as e:
        print(f"警告: 无法读取 {image_path} 的EXIF信息: {e}")
        
    return None


def get_watermark_position(image_size, text_bbox, position):
    """
    计算水印在图片上的位置坐标
    
    Args:
        image_size (tuple): 图片尺寸 (width, height)
        text_bbox (tuple): 文本边界框 (left, top, right, bottom)
        position (str): 位置选项
        
    Returns:
        tuple: (x, y) 坐标
    """
    img_width, img_height = image_size
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    margin = 20  # 边距
    
    position_map = {
        'top-left': (margin, margin),
        'top-center': ((img_width - text_width) // 2, margin),
        'top-right': (img_width - text_width - margin, margin),
        'center-left': (margin, (img_height - text_height) // 2),
        'center': ((img_width - text_width) // 2, (img_height - text_height) // 2),
        'center-right': (img_width - text_width - margin, (img_height - text_height) // 2),
        'bottom-left': (margin, img_height - text_height - margin),
        'bottom-center': ((img_width - text_width) // 2, img_height - text_height - margin),
        'bottom-right': (img_width - text_width - margin, img_height - text_height - margin)
    }
    
    return position_map.get(position, position_map['bottom-right'])


def hex_to_rgb(hex_color):
    """
    将十六进制颜色转换为RGB元组
    
    Args:
        hex_color (str): 十六进制颜色 (如 #FFFFFF)
        
    Returns:
        tuple: RGB元组
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def add_watermark(image_path, output_path, date_text, font_size, color, position):
    """
    在图片上添加日期水印
    
    Args:
        image_path (str): 输入图片路径
        output_path (str): 输出图片路径
        date_text (str): 日期文本
        font_size (int): 字体大小
        color (str): 颜色 (十六进制)
        position (str): 位置
    """
    try:
        with Image.open(image_path) as img:
            # 创建可绘制对象
            draw = ImageDraw.Draw(img)
            
            # 尝试使用系统字体
            try:
                # macOS和Linux系统字体
                font_paths = [
                    "/System/Library/Fonts/Arial.ttf",  # macOS
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
                    "/Windows/Fonts/arial.ttf",  # Windows
                ]
                
                font = None
                for font_path in font_paths:
                    if os.path.exists(font_path):
                        font = ImageFont.truetype(font_path, font_size)
                        break
                
                if font is None:
                    font = ImageFont.load_default()
                    
            except Exception:
                font = ImageFont.load_default()
            
            # 获取文本边界框
            text_bbox = draw.textbbox((0, 0), date_text, font=font)
            
            # 计算位置
            x, y = get_watermark_position(img.size, text_bbox, position)
            
            # 转换颜色
            rgb_color = hex_to_rgb(color)
            
            # 绘制文本
            draw.text((x, y), date_text, font=font, fill=rgb_color)
            
            # 保存图片
            img.save(output_path, quality=95)
            
    except Exception as e:
        print(f"错误: 处理图片 {image_path} 时发生错误: {e}")
        return False
    
    return True


def process_images(input_dir, font_size, color, position):
    """
    批量处理目录中的图片文件
    
    Args:
        input_dir (str): 输入目录路径
        font_size (int): 字体大小
        color (str): 水印颜色
        position (str): 水印位置
    """
    input_path = Path(input_dir)
    
    if not input_path.exists():
        print(f"错误: 目录 {input_dir} 不存在")
        sys.exit(1)
    
    if not input_path.is_dir():
        print(f"错误: {input_dir} 不是一个目录")
        sys.exit(1)
    
    # 创建输出目录
    output_dir = input_path / f"{input_path.name}_watermark"
    output_dir.mkdir(exist_ok=True)
    
    # 支持的图片格式
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    
    processed_count = 0
    skipped_count = 0
    
    print(f"开始处理目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    print("-" * 50)
    
    # 遍历目录中的所有文件
    for file_path in input_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            print(f"处理: {file_path.name}")
            
            # 提取日期
            date_text = get_date_from_exif(str(file_path))
            
            if date_text is None:
                print(f"  跳过: 无法获取拍摄日期")
                skipped_count += 1
                continue
            
            # 输出文件路径
            output_file = output_dir / file_path.name
            
            # 添加水印
            if add_watermark(str(file_path), str(output_file), date_text, 
                           font_size, color, position):
                print(f"  完成: 日期 {date_text} 已添加到 {output_file.name}")
                processed_count += 1
            else:
                print(f"  失败: 处理失败")
                skipped_count += 1
    
    print("-" * 50)
    print(f"处理完成! 成功: {processed_count} 张，跳过: {skipped_count} 张")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="基于EXIF拍摄时间为图片添加日期水印",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
位置选项:
  top-left, top-center, top-right
  center-left, center, center-right  
  bottom-left, bottom-center, bottom-right

颜色格式: 十六进制，如 #FFFFFF (白色), #000000 (黑色)

示例:
  python watermark.py /path/to/photos --size 36 --color "#FFFFFF" --position bottom-right
        """
    )
    
    parser.add_argument('directory', 
                       help='包含图片文件的目录路径')
    
    parser.add_argument('--size', '-s',
                       type=int, 
                       default=24,
                       help='字体大小 (默认: 24)')
    
    parser.add_argument('--color', '-c',
                       default='#FFFFFF',
                       help='水印颜色，十六进制格式 (默认: #FFFFFF 白色)')
    
    parser.add_argument('--position', '-p',
                       choices=['top-left', 'top-center', 'top-right',
                               'center-left', 'center', 'center-right',
                               'bottom-left', 'bottom-center', 'bottom-right'],
                       default='bottom-right',
                       help='水印位置 (默认: bottom-right)')
    
    args = parser.parse_args()
    
    # 验证颜色格式
    if not args.color.startswith('#') or len(args.color) != 7:
        print("错误: 颜色格式不正确，请使用十六进制格式如 #FFFFFF")
        sys.exit(1)
    
    try:
        hex_to_rgb(args.color)
    except ValueError:
        print("错误: 颜色格式不正确，请使用十六进制格式如 #FFFFFF")
        sys.exit(1)
    
    # 开始处理
    process_images(args.directory, args.size, args.color, args.position)


if __name__ == '__main__':
    main()