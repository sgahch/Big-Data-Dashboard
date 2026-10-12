# -*- coding: utf-8 -*-
"""把剪贴板 logo 复制进 assets，并裁出纯图标版（去掉下方文字）"""
import os, shutil
from PIL import Image, ImageChops

SRC = r"C:\Users\Ynchen\.workbuddy\clipboard-images\clipboard-2026-09-29T12-10-16-709Z-1f003753.jpg"
DST_DIR = r"C:\Users\Ynchen\Desktop\大数据看板\assets"
os.chdir(DST_DIR)

img = Image.open(SRC).convert("RGB")
w, h = img.size
print("original size:", w, h)

# 完整版（原样保存，供登录页等使用）
img.save(os.path.join(DST_DIR, "logo-full.jpg"), quality=95)

# 图标版：裁掉下方文字区域（文字大约从 63% 高度开始）
icon = img.crop((0, 0, w, int(h * 0.62)))

# 自动去白边：与白色背景做差分取包围盒
bg = Image.new("RGB", icon.size, (255, 255, 255))
diff = ImageChops.difference(icon, bg)
bbox = diff.getbbox()
if bbox:
    icon = icon.crop(bbox)
print("icon size:", icon.size)

# 转 RGBA 并把近白像素透明化，方便叠在任意底色上
icon = icon.convert("RGBA")
px = icon.getdata()
new_px = []
for r, g, b, a in px:
    if r > 240 and g > 240 and b > 240:
        new_px.append((r, g, b, 0))
    else:
        new_px.append((r, g, b, a))
icon.putdata(new_px)
icon.save(os.path.join(DST_DIR, "logo-icon.png"))
print("done: logo-full.jpg + logo-icon.png")
