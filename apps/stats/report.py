# -*- coding: utf-8 -*-
"""
报告生成模块
支持 Word、PDF、Excel 格式的报告导出
"""
import io
import logging
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

logger = logging.getLogger(__name__)


class ReportGenerator:
    """报告生成器基类"""

    def __init__(self, title=None, subtitle=None):
        self.title = title or '纪检监察数据分析报告'
        self.subtitle = subtitle or ''
        self.generated_at = timezone.now()
        self.data = {}

    def generate(self, **kwargs):
        """生成报告，子类实现"""
        raise NotImplementedError


class WordReportGenerator(ReportGenerator):
    """Word报告生成器"""

    def generate(self, data=None, **kwargs):
        """生成Word报告"""
        doc = Document()

        # 设置中文字体
        self._setup_chinese_fonts(doc)

        # 添加标题
        self._add_title(doc)

        # 添加生成时间
        self._add_meta(doc)

        # 添加报告内容
        if data:
            self._add_summary(doc, data.get('summary', {}))
            self._add_violations_chart(doc, data.get('violations', []))
            self._add_cases_chart(doc, data.get('cases', {}))
            self._add_regions_table(doc, data.get('regions', []))
            self._add_recent_news(doc, data.get('recent_news', []))

        # 保存到内存
        output = io.BytesIO()
        doc.save(output)
        output.seek(0)

        return output

    def _setup_chinese_fonts(self, doc):
        """设置中文字体"""
        # 为整个文档设置默认字体
        doc.styles['Normal'].font.name = '宋体'
        doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        doc.styles['Normal'].font.size = Pt(12)

    def _add_title(self, doc):
        """添加标题"""
        title = doc.add_heading(self.title, 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER

        if self.subtitle:
            subtitle = doc.add_paragraph(self.subtitle)
            subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

    def _add_meta(self, doc):
        """添加元信息"""
        meta = doc.add_paragraph()
        meta.add_run(f'生成时间：{self.generated_at.strftime("%Y-%m-%d %H:%M:%S")}').font.size = Pt(10)
        meta.add_run('\n')
        meta.add_run(f'数据来源：清风网').font.size = Pt(10)

    def _add_summary(self, doc, summary):
        """添加统计摘要"""
        doc.add_heading('一、数据概览', level=1)

        table = doc.add_table(rows=1, cols=2)
        table.style = 'Table Grid'

        # 表头
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = '指标'
        hdr_cells[1].text = '数值'

        # 数据行
        data = [
            ('总新闻数', str(summary.get('total_news', 0))),
            ('今日新增', str(summary.get('today_news', 0))),
            ('昨日新增', str(summary.get('yesterday_news', 0))),
            ('活跃地区', str(summary.get('active_regions', 0))),
            ('今日爬取', str(summary.get('today_crawled', 0))),
            ('今日新增', str(summary.get('today_new', 0))),
        ]

        for metric, value in data:
            row = table.add_row().cells
            row[0].text = metric
            row[1].text = value

    def _add_violations_chart(self, doc, violations):
        """添加违规事项统计"""
        doc.add_heading('二、违规事项分布', level=1)

        if violations:
            # 创建表格
            table = doc.add_table(rows=1, cols=3)
            table.style = 'Table Grid'

            hdr_cells = table.rows[0].cells
            hdr_cells[0].text = '排名'
            hdr_cells[1].text = '违规类型'
            hdr_cells[2].text = '数量'

            for i, item in enumerate(violations[:15], 1):
                row = table.add_row().cells
                row[0].text = str(i)
                row[1].text = item.get('name', '')
                row[2].text = str(item.get('value', 0))

    def _add_cases_chart(self, doc, cases):
        """添加案件统计"""
        doc.add_heading('三、案件查处趋势', level=1)

        months = cases.get('months', [])
        values = cases.get('values', [])

        if months and values:
            table = doc.add_table(rows=1, cols=3)
            table.style = 'Table Grid'

            hdr_cells = table.rows[0].cells
            hdr_cells[0].text = '月份'
            hdr_cells[1].text = '案件数'
            hdr_cells[2].text = '环比变化'

            for i, (month, value) in enumerate(zip(months, values)):
                row = table.add_row().cells
                row[0].text = month
                row[1].text = str(value)

                # 计算环比变化
                if i > 0 and values[i-1] > 0:
                    change = ((value - values[i-1]) / values[i-1] * 100)
                    row[2].text = f'{change:+.1f}%'
                else:
                    row[2].text = '-'

    def _add_regions_table(self, doc, regions):
        """添加地区统计表格"""
        doc.add_heading('四、地区分布统计', level=1)

        if regions:
            table = doc.add_table(rows=1, cols=3)
            table.style = 'Table Grid'

            hdr_cells = table.rows[0].cells
            hdr_cells[0].text = '地区'
            hdr_cells[1].text = '新闻数量'
            hdr_cells[2].text = '占比'

            total = sum(r.get('count', 0) for r in regions)

            for region in regions:
                row = table.add_row().cells
                row[0].text = region.get('region__name', region.get('name', ''))
                row[1].text = str(region.get('count', 0))

                percentage = (region.get('count', 0) / total * 100) if total > 0 else 0
                row[2].text = f'{percentage:.1f}%'

    def _add_recent_news(self, doc, news_list):
        """添加最新新闻列表"""
        doc.add_heading('五、最新通报案例', level=1)

        for i, news in enumerate(news_list[:20], 1):
            p = doc.add_paragraph()
            p.add_run(f'{i}. ').bold = True
            p.add_run(news.get('title', ''))

            p.add_run(f'\n    来源：{news.get("region_name", "")} | '
                      f'日期：{news.get("date", "")}').font.size = Pt(10)


class ExcelReportGenerator(ReportGenerator):
    """Excel报告生成器"""

    def generate(self, data=None, **kwargs):
        """生成Excel报告"""
        import openpyxl
        from openpyxl.styles import Font, Alignment, PatternFill
        from openpyxl.utils import get_column_letter

        wb = openpyxl.Workbook()

        # Sheet 1: 统计概览
        ws1 = wb.active
        ws1.title = '统计概览'

        self._setup_sheet(ws1)
        self._fill_summary(ws1, data.get('summary', {}))

        # Sheet 2: 违规事项
        ws2 = wb.create_sheet('违规事项分布')
        self._setup_sheet(ws2)
        self._fill_list(ws2, data.get('violations', []), ['违规类型', '数量'])

        # Sheet 3: 案件趋势
        ws3 = wb.create_sheet('案件趋势')
        self._setup_sheet(ws3)

        cases = data.get('cases', {})
        months = cases.get('months', [])
        values = cases.get('values', [])

        ws3['A1'] = '月份'
        ws3['B1'] = '案件数'
        ws3['C1'] = '环比变化'

        for i, (month, value) in enumerate(zip(months, values), 2):
            ws3[f'A{i}'] = month
            ws3[f'B{i}'] = value
            if i > 2 and values[i-3] > 0:
                change = ((value - values[i-3]) / values[i-3] * 100)
                ws3[f'C{i}'] = f'{change:+.1f}%'

        # Sheet 4: 地区统计
        ws4 = wb.create_sheet('地区统计')
        self._setup_sheet(ws4)
        self._fill_regions(ws4, data.get('regions', []))

        # Sheet 5: 最新新闻
        ws5 = wb.create_sheet('最新新闻')
        self._setup_sheet(ws5)
        self._fill_news(ws5, data.get('recent_news', []))

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        return output

    def _setup_sheet(self, ws):
        """设置工作表样式"""
        header_font = Font(bold=True)
        header_fill = PatternFill(start_color='00D2FF', end_color='00D2FF', fill_type='solid')

        for cell in ws[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center')

        # 设置列宽
        ws.column_dimensions['A'].width = 30
        ws.column_dimensions['B'].width = 20
        ws.column_dimensions['C'].width = 20

    def _fill_summary(self, ws, summary):
        """填充统计摘要"""
        data = [
            ('总新闻数', summary.get('total_news', 0)),
            ('今日新增', summary.get('today_news', 0)),
            ('昨日新增', summary.get('yesterday_news', 0)),
            ('活跃地区', summary.get('active_regions', 0)),
            ('今日爬取', summary.get('today_crawled', 0)),
            ('今日新增', summary.get('today_new', 0)),
        ]

        for i, (metric, value) in enumerate(data, 1):
            ws[f'A{i}'] = metric
            ws[f'B{i}'] = value

    def _fill_list(self, ws, items, headers):
        """填充列表数据"""
        ws['A1'] = headers[0]
        ws['B1'] = headers[1]

        for i, item in enumerate(items, 2):
            ws[f'A{i}'] = item.get('name', '')
            ws[f'B{i}'] = item.get('value', 0) or item.get('count', 0)

    def _fill_regions(self, ws, regions):
        """填充地区统计"""
        ws['A1'] = '地区'
        ws['B1'] = '数量'
        ws['C1'] = '占比'

        total = sum(r.get('count', 0) for r in regions)

        for i, region in enumerate(regions, 2):
            ws[f'A{i}'] = region.get('region__name', region.get('name', ''))
            ws[f'B{i}'] = region.get('count', 0)
            percentage = (region.get('count', 0) / total * 100) if total > 0 else 0
            ws[f'C{i}'] = f'{percentage:.1f}%'

    def _fill_news(self, ws, news_list):
        """填充新闻列表"""
        ws['A1'] = '序号'
        ws['B1'] = '标题'
        ws['C1'] = '地区'
        ws['D1'] = '日期'
        ws['E1'] = '标签'

        for i, news in enumerate(news_list, 2):
            ws[f'A{i}'] = i - 1
            ws[f'B{i}'] = news.get('title', '')
            ws[f'C{i}'] = news.get('region_name', '')
            ws[f'D{i}'] = str(news.get('date', ''))
            ws[f'E{i}'] = news.get('tag_names', '')


def generate_report(report_type='word', data=None, **kwargs):
    """
    生成报告的统一入口

    Args:
        report_type: 报告类型 ('word', 'excel')
        data: 报告数据
        **kwargs: 其他参数

    Returns:
        文件流
    """
    generators = {
        'word': WordReportGenerator,
        'excel': ExcelReportGenerator,
    }

    generator_class = generators.get(report_type, WordReportGenerator)
    generator = generator_class(
        title=kwargs.get('title', '纪检监察数据分析报告'),
        subtitle=kwargs.get('subtitle', '')
    )

    return generator.generate(data)


def get_report_data(start_date=None, end_date=None, region=None):
    """
    获取报告所需数据

    Args:
        start_date: 开始日期
        end_date: 结束日期
        region: 地区筛选

    Returns:
        报告数据字典
    """
    from apps.news.models import News, Region, Tag, CrawlLog
    from apps.crawler.crawler import REGIONS

    today = timezone.now().date()

    # 统计摘要
    total_news = News.objects.filter(status='published').count()
    today_news = News.objects.filter(crawl_time__date=today).count()
    yesterday_news = News.objects.filter(
        crawl_time__date=today - timedelta(days=1)
    ).count()

    today_logs = CrawlLog.objects.filter(crawl_time__date=today)
    today_crawled = today_logs.aggregate(total=Count('total_crawled'))['total'] or 0
    today_new = today_logs.aggregate(total=Count('new_count'))['total'] or 0

    # 违规事项
    violations = {}
    news_qs = News.objects.filter(status='published')
    for n in news_qs:
        tags = n.get_tag_names_list()
        for tag in tags:
            violations[tag] = violations.get(tag, 0) + 1
    violations_list = [
        {'name': k, 'value': v}
        for k, v in sorted(violations.items(), key=lambda x: x[1], reverse=True)
    ]

    # 案件趋势（近12月）
    cases_stats = (News.objects
                   .filter(status='published')
                   .annotate(month=TruncMonth('crawl_time'))
                   .values('month')
                   .annotate(count=Count('id'))
                   .order_by('month')[-12:])

    cases = {
        'months': [item['month'].strftime('%Y-%m') for item in cases_stats],
        'values': [item['count'] for item in cases_stats]
    }

    # 地区统计
    regions_stats = (News.objects
                     .filter(status='published')
                     .values('region__name', 'region__code')
                     .annotate(count=Count('id'))
                     .order_by('-count'))

    regions_list = list(regions_stats)

    # 最新新闻
    recent_news = News.objects.filter(
        status='published'
    ).select_related('region').prefetch_related('tags')[:50]

    recent_news_data = [
        {
            'title': n.title,
            'region_name': n.region_name,
            'date': str(n.date) if n.date else '',
            'tag_names': n.tag_names,
            'url': n.url
        }
        for n in recent_news
    ]

    return {
        'summary': {
            'total_news': total_news,
            'today_news': today_news,
            'yesterday_news': yesterday_news,
            'active_regions': regions_stats.values('region').distinct().count(),
            'today_crawled': today_crawled,
            'today_new': today_new,
        },
        'violations': violations_list,
        'cases': cases,
        'regions': regions_list,
        'recent_news': recent_news_data
    }
