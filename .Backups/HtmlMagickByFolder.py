# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认为 d:\\Works\\In\\）与目标文件夹位置（默认为 d:\\Works\\Out\\）。
# 依次读取源文件夹下的所有 html 文件，进行下列操作，放在目标文件夹位置，保持文件夹及子文件结构。。
# Html 文件内嵌的图片是（base64 格式）。我希望将它批量转成 html（zip）格式（要求生成的 html 还能被浏览器打开）。然后压缩图片。如果图片格式为 bmp、jpg、jpeg、png 或静态 webp 格式、或静态 avif 格式、静态 heic 格式、静态 heif 格式，则使用 magick 压缩成 avif 格式，使用类似命令：magick input.jpg -quality 50 output.avif。如果图片文件格式为 gif 或动态 webp 格式或 mp4 格式，则使用 magick 压缩成 gif 格式，类似命令：magick input.webp -fuzz 5% -quality 75 -layers Optimize output.gif。

# 导入模块
import os, re, base64, subprocess
from pathlib import Path
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog

# 提示选择文件夹
root = tk.Tk()
root.withdraw()
src_dir = Path(filedialog.askdirectory(
    initialdir=r"D:\Works\In", title="选择源 HTML 文件夹"))
dst_dir = Path(filedialog.askdirectory(
    initialdir=r"D:\Works\Out", title="选择目标输出文件夹"))

IMG_RE = re.compile(r'data:image/([^;]+);base64,([A-Za-z0-9+/=\n]+)', re.S)

def convert_with_magick(buf, orig_fmt):
    ext = orig_fmt.lower().replace('jpeg','jpg')
    tmp_in = Path("tmp_in." + ext)
    tmp_in.write_bytes(buf)
    if ext in ('bmp','jpg','jpeg','png','webp','avif','heic','heif'):
        tmp_out = tmp_in.with_suffix('.avif')
        cmd = ['magick', str(tmp_in), '-quality', '50', str(tmp_out)]
    elif ext=='gif' or ext=='webp':
        tmp_out = tmp_in.with_suffix('.gif')
        cmd = ['magick', str(tmp_in), '-fuzz', '5%', '-quality', '75',
               '-layers', 'Optimize', str(tmp_out)]
    else:
        tmp_in.unlink()
        return None, None
    subprocess.run(cmd, check=True)
    data = tmp_out.read_bytes()
    tmp_in.unlink()
    tmp_out.unlink()
    return data, tmp_out.suffix.lstrip('.')

def process_html_file(html_path, out_path):
    soup = BeautifulSoup(html_path.read_bytes(), 'html.parser')
    for img in soup.find_all('img'):
        src = img.get('src','')
        m = IMG_RE.match(src)
        if m:
            fmt, b64 = m.groups()
            data = base64.b64decode(b64)
            res = convert_with_magick(data, fmt)
            if res[0]:
                nb, new_fmt = res
                img['src'] = f"data:image/{new_fmt};base64," + base64.b64encode(nb).decode()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(str(soup), encoding='utf8')

def main():
    for html in src_dir.rglob('*.html'):
        rel = html.relative_to(src_dir)
        out_html = dst_dir / rel
        process_html_file(html, out_html)

if __name__ == '__main__':
    main()
    print("处理完成 ✅")
    
# 按下回车键退出。
input("按回车键退出...")