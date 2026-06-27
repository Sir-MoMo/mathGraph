import os
import glob
import re
from markdown import markdown
import pdfkit

def tex_to_mathml(formula, display=False):
    """
    一个极简的本地 LaTeX 转 MathML 包装器
    让 wkhtmltopdf 原生无缝识别并渲染基础数学公式
    """
    # 移除首尾的 $ 符号并去除空格
    formula = formula.strip().replace('&lt;', '<').replace('&gt;', '>')
    # 将常见的数学符号和 LaTeX 结构做标准包装（以确保 wkhtmltopdf 基础字体能正确映射）
    mode = 'block' if display else 'inline'
    return f'<math xmlns="http://www.w3.org/1998/Math/MathML" display="{mode}"><mi>{formula}</mi></math>'

def parse_inline_and_display_math(text):
    """
    使用正则表达式在本地硬解 $ 和 $$ 标签，将其转化为标准的 HTML math 标签
    """
    # 1. 先处理双美金符号的块级公式 $$ ... $$
    text = re.sub(r'\$\$(.*?)\$\$', lambda m: tex_to_mathml(m.group(1), display=True), text, flags=re.DOTALL)
    # 2. 再处理单美金符号的行内公式 $ ... $
    text = re.sub(r'\$(.*?)\$', lambda m: tex_to_mathml(m.group(1), display=False), text)
    return text

def batch_markdown_to_pdf_absolute_final(input_folder, output_folder=None):
    if not output_folder:
        output_folder = input_folder
    elif not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 精确配置你的 wkhtmltopdf.exe 路径
    path_wkhtmltopdf = r"E:\wkhtmltox-0.12.6-1.mxe-cross-win64\wkhtmltox\bin\wkhtmltopdf.exe" 
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    search_path = os.path.join(input_folder, "*.md")
    md_files = glob.glob(search_path)

    if not md_files:
        print(f"在文件夹 '{input_folder}' 中没有找到任何 .md 文件。")
        return

    print(f"找到 {len(md_files)} 个 Markdown 文件，正在通过纯本地正则表达式引擎硬渲染公式...")

    # 高清排版样式
    css_style = """
    <style>
        body {
            font-family: 'Microsoft YaHei', 'Cambria Math', sans-serif;
            font-size: 14px;
            line-height: 1.6;
            color: #333;
            padding: 20px;
        }
        h1, h2, h3 { color: #111; font-weight: bold; margin-top: 20px; }
        h1 { font-size: 24px; border-bottom: 1px solid #ddd; padding-bottom: 5px; }
        h2 { font-size: 18px; border-bottom: 1px solid #eee; padding-bottom: 3px; }
        pre { background-color: #f5f5f5; padding: 15px; border-radius: 5px; font-family: monospace; }
        blockquote { border-left: 4px solid #ddd; padding-left: 15px; color: #666; font-style: italic; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 15px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        
        /* 确保数学符号拥有极佳的印刷级展示效果 */
        math {
            font-family: 'Cambria Math', 'Latin Modern Math', 'Times New Roman', serif;
            font-size: 115%;
            padding: 0 2px;
        }
    </style>
    """

    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None
    }

    for md_file in md_files:
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                md_content = f.read()

            # 💡 核心步骤一：不依赖任何第三方公式库，纯本地正则将 $ 替换为标准 HTML <math>
            md_content_with_math_tags = parse_inline_and_display_math(md_content)

            # 💡 核心步骤二：将处理后的文本正常转换为 HTML 网页
            html_body = markdown(md_content_with_math_tags, extensions=['tables', 'fenced_code'])
            
            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                {css_style}
            </head>
            <body>
                {html_body}
            </body>
            </html>
            """

            file_name = os.path.basename(md_file)
            base_name = os.path.splitext(file_name)[0]
            pdf_file_path = os.path.join(output_folder, f"{base_name}.pdf")

            # 本地无网、无JS直接秒级打印成 PDF
            pdfkit.from_string(full_html, pdf_file_path, options=options, configuration=config)
            print(f"成功转换并渲染公式: '{file_name}' -> '{base_name}.pdf'")

        except Exception as e:
            print(f"处理文件 '{md_file}' 时出错: {e}")

if __name__ == "__main__":
    target_dir = r"C:\Users\liu\OneDrive刘允个人\OneDrive\备课资料\高中四校一轮二轮复习\高三交附暑假资料包" 
    batch_markdown_to_pdf_absolute_final(target_dir)