# AI4SE Photo Watermark Tool

一个基于Python的图片水印工具，可以自动读取图片的EXIF信息中的拍摄时间，并将日期作为水印添加到图片上。

## 功能特性

- 🔍 自动读取图片EXIF信息中的拍摄时间
- 📅 将拍摄日期（年-月-日格式）作为水印添加到图片
- 🎨 支持自定义字体大小、颜色和位置
- 📁 批量处理目录中的所有图片文件
- 💾 保存到原目录的子目录中，保持原文件不变
- 🖼️ 支持多种图片格式：JPG, PNG, BMP, TIFF, WebP

## 安装依赖

```bash
pip install -r requirements.txt
```

或者手动安装：

```bash
pip install Pillow>=10.0.0 exifread>=3.0.0
```

## 使用方法

### 基本用法

```bash
python watermark.py /path/to/your/photos
```

### 自定义参数

```bash
python watermark.py /path/to/your/photos --size 36 --color "#FFFFFF" --position bottom-right
```

### 参数说明

- `directory`: **必需参数**，包含图片文件的目录路径
- `--size, -s`: 字体大小（默认：24）
- `--color, -c`: 水印颜色，十六进制格式（默认：#FFFFFF 白色）
- `--position, -p`: 水印位置（默认：bottom-right）

### 支持的位置选项

```
top-left        top-center        top-right
center-left     center            center-right  
bottom-left     bottom-center     bottom-right
```

### 颜色示例

- 白色：`#FFFFFF`
- 黑色：`#000000`
- 红色：`#FF0000`
- 蓝色：`#0000FF`
- 黄色：`#FFFF00`

## 使用示例

### 示例1：使用默认设置
```bash
python watermark.py ./my_photos
```

### 示例2：大字体白色水印在右下角
```bash
python watermark.py ./my_photos --size 48 --color "#FFFFFF" --position bottom-right
```

### 示例3：小字体黑色水印在左上角
```bash
python watermark.py ./my_photos --size 18 --color "#000000" --position top-left
```

### 示例4：居中的金色水印
```bash
python watermark.py ./my_photos --size 32 --color "#FFD700" --position center
```

## 输出说明

程序会在原目录下创建一个名为 `{原目录名}_watermark` 的子目录，所有添加了水印的图片都保存在这个新目录中。原始图片保持不变。

例如：
- 原目录：`/Users/john/vacation_photos/`
- 输出目录：`/Users/john/vacation_photos/vacation_photos_watermark/`

## 技术特性

- **智能EXIF读取**：程序会尝试多种方式读取EXIF信息，确保最大兼容性
- **错误处理**：对于无法读取EXIF信息的图片，程序会跳过并给出提示
- **字体处理**：自动选择系统可用的字体，在macOS、Linux和Windows上都能正常工作
- **阴影效果**：为水印文字添加阴影，提高可读性
- **批量处理**：一次性处理整个目录中的所有图片

## 注意事项

1. 确保图片文件包含EXIF信息（通常由数码相机拍摄的照片都包含）
2. 对于没有EXIF信息或无法读取拍摄时间的图片，程序会跳过处理
3. 程序保持原文件不变，所有输出都保存在新目录中
4. 支持的图片格式：.jpg, .jpeg, .png, .bmp, .tiff, .webp

## 故障排除

### 问题：程序显示"无法获取拍摄日期"
**解决方案**：
- 检查图片是否包含EXIF信息
- 确认图片不是截图或编辑过的图片（可能丢失了EXIF信息）
- 尝试使用数码相机直接拍摄的原始照片

### 问题：字体显示不正确
**解决方案**：
- 程序会自动选择系统字体
- 在不同操作系统上字体可能略有不同，这是正常现象

### 问题：水印位置不理想
**解决方案**：
- 尝试不同的位置参数：top-left, center, bottom-right等
- 调整字体大小以获得更好的视觉效果

## 许可证

此项目仅供学习和个人使用。