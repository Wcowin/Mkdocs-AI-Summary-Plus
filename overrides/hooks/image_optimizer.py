import re
import os
from PIL import Image
from pathlib import Path

class ImageOptimizer:
    def __init__(self):
        self.optimized_images = set()
        self.target_sizes = {
            'thumbnail': (300, 200),
            'medium': (800, 600),
            'large': (1200, 900)
        }
    
    def optimize_image(self, image_path, max_width=1200, quality=85):
        """优化单个图片"""
        if image_path in self.optimized_images:
            return
        
        try:
            with Image.open(image_path) as img:
                # 如果图片宽度超过最大宽度，进行缩放
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
                # 保存优化后的图片
                img.save(image_path, optimize=True, quality=quality)
                self.optimized_images.add(image_path)
                print(f"✅ 图片已优化: {image_path}")
                
        except Exception as e:
            print(f"❌ 图片优化失败 {image_path}: {e}")
    
    def process_markdown_images(self, markdown, page):
        """处理Markdown中的图片"""
        # 匹配图片链接
        image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        images = re.findall(image_pattern, markdown)
        
        for alt_text, src in images:
            # 处理相对路径
            if not src.startswith(('http://', 'https://', '//')):
                image_path = Path(page.file.abs_src_path).parent / src
                if image_path.exists():
                    self.optimize_image(str(image_path))
        
        return markdown

image_optimizer = ImageOptimizer()

def on_page_markdown(markdown, page, config, files):
    """处理页面中的图片"""
    return image_optimizer.process_markdown_images(markdown, page)