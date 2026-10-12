# -*- coding: utf-8 -*-
import codecs

# 读取乱码文件（以GBK读取，因为乱码是UTF-8被当作GBK显示）
try:
    with open('index.html', 'r', encoding='gbk', errors='ignore') as f:
        content = f.read()
    
    # 保存为正确的UTF-8
    with open('index_fixed.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 修复完成！已保存到 index_fixed.html")
    print("请检查文件，如果正确，执行：")
    print("  del index.html")
    print("  ren index_fixed.html index.html")
    
except Exception as e:
    print(f"❌ 修复失败: {e}")
    print("\n尝试方案2...")
    
    # 方案2：尝试用latin1读取再转UTF-8
    try:
        with open('index.html', 'r', encoding='latin1') as f:
            content = f.read()
        
        # 尝试将乱码转回UTF-8
        content_bytes = content.encode('latin1')
        content_fixed = content_bytes.decode('utf-8', errors='ignore')
        
        with open('index_fixed.html', 'w', encoding='utf-8') as f:
            f.write(content_fixed)
        
        print("✅ 方案2修复完成！")
    except Exception as e2:
        print(f"❌ 方案2也失败: {e2}")

