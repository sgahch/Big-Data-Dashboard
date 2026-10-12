#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试报告导出功能
"""
import os
import sys
import django

# 设置Django环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supervision.settings')
django.setup()

from apps.stats.report import generate_report, get_report_data


def test_export_word():
    """测试Word导出"""
    print("=" * 50)
    print("测试Word报告导出...")
    print("=" * 50)
    
    try:
        # 获取报告数据
        data = get_report_data()
        print(f"✓ 获取报告数据成功")
        print(f"  - 总新闻数: {data['summary']['total_news']}")
        print(f"  - 违规类型: {len(data['violations'])} 种")
        print(f"  - 地区数: {len(data['regions'])} 个")
        
        # 生成Word报告
        output = generate_report(report_type='word', data=data)
        
        # 保存到文件
        filename = 'test_report.docx'
        with open(filename, 'wb') as f:
            f.write(output.getvalue())
        
        print(f"✓ Word报告生成成功: {filename}")
        print(f"  文件大小: {os.path.getsize(filename)} 字节")
        
    except Exception as e:
        print(f"✗ Word报告生成失败: {e}")
        import traceback
        traceback.print_exc()


def test_export_excel():
    """测试Excel导出"""
    print("\n" + "=" * 50)
    print("测试Excel报告导出...")
    print("=" * 50)
    
    try:
        # 获取报告数据
        data = get_report_data()
        
        # 生成Excel报告
        output = generate_report(report_type='excel', data=data)
        
        # 保存到文件
        filename = 'test_report.xlsx'
        with open(filename, 'wb') as f:
            f.write(output.getvalue())
        
        print(f"✓ Excel报告生成成功: {filename}")
        print(f"  文件大小: {os.path.getsize(filename)} 字节")
        
    except Exception as e:
        print(f"✗ Excel报告生成失败: {e}")
        import traceback
        traceback.print_exc()


def test_export_pdf():
    """测试PDF导出"""
    print("\n" + "=" * 50)
    print("测试PDF报告导出...")
    print("=" * 50)
    
    try:
        # 获取报告数据
        data = get_report_data()
        
        # 生成PDF报告
        output = generate_report(report_type='pdf', data=data)
        
        # 保存到文件
        filename = 'test_report.pdf'
        with open(filename, 'wb') as f:
            f.write(output.getvalue())
        
        print(f"✓ PDF报告生成成功: {filename}")
        print(f"  文件大小: {os.path.getsize(filename)} 字节")
        
    except Exception as e:
        print(f"✗ PDF报告生成失败: {e}")
        print(f"  提示: PDF生成需要安装 weasyprint 或 xhtml2pdf")
        print(f"  安装命令: pip install weasyprint xhtml2pdf reportlab")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    print("\n开始测试报告导出功能...\n")
    
    # 测试Word导出
    test_export_word()
    
    # 测试Excel导出
    test_export_excel()
    
    # 测试PDF导出
    test_export_pdf()
    
    print("\n" + "=" * 50)
    print("测试完成！")
    print("=" * 50)

