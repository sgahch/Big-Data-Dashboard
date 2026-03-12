#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
清除 Python 缓存文件脚本
用于删除所有 .pyc 文件和 __pycache__ 目录
"""

import os
import shutil
import sys

def clear_python_cache(root_dir='.'):
    """
    递归删除所有 Python 缓存文件和目录
    
    Args:
        root_dir: 项目根目录路径
    """
    deleted_files = 0
    deleted_dirs = 0
    
    print(f"开始清除 Python 缓存文件...")
    print(f"扫描目录: {os.path.abspath(root_dir)}\n")
    
    # 遍历所有目录
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 跳过虚拟环境目录
        if 'venv' in dirpath or 'env' in dirpath or '.venv' in dirpath:
            continue
            
        # 删除 __pycache__ 目录
        if '__pycache__' in dirnames:
            cache_dir = os.path.join(dirpath, '__pycache__')
            try:
                shutil.rmtree(cache_dir)
                print(f"✓ 已删除目录: {cache_dir}")
                deleted_dirs += 1
            except Exception as e:
                print(f"✗ 删除目录失败: {cache_dir} - {e}")
        
        # 删除 .pyc 文件
        for filename in filenames:
            if filename.endswith('.pyc'):
                file_path = os.path.join(dirpath, filename)
                try:
                    os.remove(file_path)
                    print(f"✓ 已删除文件: {file_path}")
                    deleted_files += 1
                except Exception as e:
                    print(f"✗ 删除文件失败: {file_path} - {e}")
    
    print(f"\n清除完成！")
    print(f"删除了 {deleted_dirs} 个 __pycache__ 目录")
    print(f"删除了 {deleted_files} 个 .pyc 文件")
    
    return deleted_dirs, deleted_files

if __name__ == '__main__':
    try:
        # 获取项目根目录
        project_root = os.path.dirname(os.path.abspath(__file__))
        
        # 清除缓存
        dirs, files = clear_python_cache(project_root)
        
        if dirs == 0 and files == 0:
            print("\n没有找到需要清除的缓存文件。")
        else:
            print("\n✅ 缓存清除成功！")
            print("\n建议：")
            print("1. 重新启动 Django 服务器")
            print("2. 运行 python manage.py migrate 来应用数据库迁移")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ 清除缓存时发生错误: {e}")
        sys.exit(1)

