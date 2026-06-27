from PIL import Image, ImageDraw, ImageFont
import os
import math

def combine_raw_blots_uniform_3x2():
    # --- 1. 路径设置 ---
    base_path = r"D:\reDraw\JYSZrawBlots"
    
    # 自动获取该文件夹下的所有图片文件，并按文件名排序
    valid_extensions = ('.png', '.jpg', '.jpeg', '.tif', '.tiff')
    all_files = sorted([os.path.join(base_path, f) for f in os.listdir(base_path) 
                 if f.lower().endswith(valid_extensions)])
    
    num_imgs = len(all_files)
    if num_imgs == 0:
        print(f"错误: 在 {base_path} 中没有找到任何图片！")
        return
        
    output_path = os.path.join(base_path, f"Supplementary_Raw_Blots_{num_imgs}Panels_3x2.tiff")

    # --- 2. 网格设定与独立宽度 ---
    # ================= 关键修改 =================
    cols = 2  # 将列数改为 2，如果有6张图，rows会自动计算为3
    # ============================================
    rows = math.ceil(num_imgs / cols)
    
    # 调大宽度，充分利用 2 列排版时的横向空间
    target_cell_w = 1800  
    
    # --- 3. 智能两阶段缩放与白底填充 (保证子图尺寸完全相同) ---
    max_cell_h = 0
    temp_resized_data = []
    
    # 阶段一：计算所有图片按等比例缩放后的最大高度
    for img_path in all_files:
        img = Image.open(img_path).convert("RGB")
        w, h = img.size
        aspect_ratio = h / w
        new_h = int(target_cell_w * aspect_ratio)
        
        if new_h > max_cell_h:
            max_cell_h = new_h
        temp_resized_data.append((img, new_h))
        
    # 阶段二：将所有子图片无损嵌入统一大小的画布中
    processed_imgs = []
    for img, new_h in temp_resized_data:
        # 高质量缩放原始图片
        img_scaled = img.resize((target_cell_w, new_h), Image.Resampling.LANCZOS)
        
        # 创建一个规整的、大小完全相同的高清纯白子画布
        uniform_tile = Image.new("RGB", (target_cell_w, max_cell_h), "white")
        
        # 将图片垂直居中贴入子画布
        paste_y = (max_cell_h - new_h) // 2
        uniform_tile.paste(img_scaled, (0, paste_y))
        
        processed_imgs.append(uniform_tile)

    # --- 4. 动态画布计算 ---
    margin = 300    # 外部留白
    gap_x = 250     # 列间距 (稍微拉宽了一点，配合放大的图片)
    gap_y = 450     # 行间距
    
    # 总宽 = 左右留白 + 2列*子图宽 + 列间距
    canvas_w = margin * 2 + target_cell_w * cols + gap_x * (cols - 1)
    # 总高 = 上下留白 + 3行*子图最大高 + 行间距
    canvas_h = margin * 2 + max_cell_h * rows + gap_y * (rows - 1)
    
    combined = Image.new("RGB", (canvas_w, canvas_h), "white")
    draw = ImageDraw.Draw(combined)

    try:
        # 配合调大的宽度，字体也适当放大，保证醒目
        font_panel = ImageFont.truetype("arialbd.ttf", 200)
    except:
        font_panel = ImageFont.load_default()

    # --- 5. 坐标计算与精准粘贴 ---
    labels = [chr(65 + i) for i in range(num_imgs)]
    
    for i, img in enumerate(processed_imgs):
        row = i // cols
        col = i % cols
        
        x = margin + col * (target_cell_w + gap_x)
        y = margin + row * (max_cell_h + gap_y)
            
        combined.paste(img, (x, y))
        
        # 绘制字母标签
        label_x = x
        label_y = y - 250
        draw.text((label_x, label_y), labels[i], fill="black", font=font_panel)

    # --- 6. 导出投稿级高清图片 ---
    combined.save(output_path, format="TIFF", compression="tiff_lzw", dpi=(300, 300))
    
    print("-" * 40)
    print(f"成功拼合 {num_imgs} 张规整化 Raw Blots 图！")
    print(f"已采用 {rows} 行 x {cols} 列 的规整对称网格排布。")
    print(f"输出文件路径: {output_path}")
    print("-" * 40)

if __name__ == "__main__":
    combine_raw_blots_uniform_3x2()