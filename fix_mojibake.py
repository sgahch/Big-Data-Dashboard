# -*- coding: utf-8 -*-
"""
智能修复UTF-8乱码
原理：UTF-8文本被错误地以GBK/GB2312编码保存后，再以UTF-8读取会产生乱码
"""

def fix_mojibake(text):
    """修复mojibake（文字化け）乱码"""
    try:
        # 尝试将文本编码为latin-1，然后解码为GBK
        fixed = text.encode('latin-1').decode('gbk', errors='ignore')
        return fixed
    except:
        try:
            # 备用方案：尝试UTF-8 -> GBK
            fixed = text.encode('utf-8').decode('gbk', errors='ignore')
            return fixed
        except:
            return text

# 读取乱码文件
print("正在读取文件...")
with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

print(f"文件大小: {len(content)} 字符")

# 修复乱码
print("正在修复乱码...")
fixed_content = fix_mojibake(content)

# 保存修复后的文件
print("正在保存...")
with open('index_recovered.html', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("✅ 修复完成！已保存到 index_recovered.html")
print("\n请检查文件前几行：")

# 显示前10行
lines = fixed_content.split('\n')[:10]
for i, line in enumerate(lines, 1):
    print(f"{i}: {line[:80]}")

