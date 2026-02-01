# -*- coding: utf-8 -*-
import logging
import pandas as pd
import io
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from datetime import timedelta
from .models import Region, TagCategory, Tag, News, CrawlLog, CrawlTask, AuditLog, SupervisionItem
from .serializers import (
    RegionSerializer, TagCategorySerializer, TagSerializer,
    NewsSerializer, CrawlLogSerializer, CrawlTaskSerializer, AuditLogSerializer,
    SupervisionItemSerializer
)

logger = logging.getLogger(__name__)


class RegionViewSet(viewsets.ModelViewSet):
    """地区API"""
    queryset = Region.objects.filter(is_active=True)
    serializer_class = RegionSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by('sort')


class TagCategoryViewSet(viewsets.ModelViewSet):
    """标签分类API"""
    queryset = TagCategory.objects.all()
    serializer_class = TagCategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    """标签API"""
    queryset = Tag.objects.filter(is_active=True)
    serializer_class = TagSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category_id=category)
        return qs.select_related('category')


class NewsViewSet(viewsets.ModelViewSet):
    """新闻API"""
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        # 筛选地区（支持代码如 'xian' 或 ID）
        region = self.request.query_params.get('region')
        if region and region != 'all':
            # 尝试用代码匹配
            qs = qs.filter(region__code=region)
            # 如果没有匹配，尝试用ID匹配
            if not qs.exists():
                qs = super().get_queryset().filter(region_id=region)

        # 筛选标签
        tag = self.request.query_params.get('tag')
        if tag:
            qs = qs.filter(tag_names__contains=tag)

        # 筛选日期范围
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)

        # 关键词搜索
        keyword = self.request.query_params.get('keyword')
        if keyword:
            qs = qs.filter(title__icontains=keyword)

        return qs.select_related('region').prefetch_related('tags')

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """获取最新新闻"""
        limit = int(request.query_params.get('limit', 20))
        news = self.get_queryset()[:limit]
        serializer = self.get_serializer(news, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': len(serializer.data)
        })

    @action(detail=False, methods=['get'])
    def by_region(self, request):
        """按地区分组统计"""
        stats = self.get_queryset().values('region__name').annotate(
            count=Count('id')
        ).order_by('-count')
        return Response({
            'code': 0,
            'data': list(stats)
        })

    @action(detail=True, methods=['get'])
    def info(self, request, pk=None):
        """获取新闻详情"""
        news = self.get_object()

        # 获取相关文章（相同标签）
        related_news = News.objects.filter(
            tags__in=news.tags.all()
        ).exclude(id=news.id).distinct()[:5]

        return Response({
            'code': 0,
            'data': {
                'news': NewsSerializer(news).data,
                'related': NewsSerializer(related_news, many=True).data
            }
        })

    @action(detail=True, methods=['get'])
    def related(self, request, pk=None):
        """获取相关文章"""
        news = self.get_object()
        limit = int(request.query_params.get('limit', 5))

        related_news = News.objects.filter(
            tags__in=news.tags.all()
        ).exclude(id=news.id).distinct()[:limit]

        return Response({
            'code': 0,
            'data': NewsSerializer(related_news, many=True).data
        })


class CrawlLogViewSet(viewsets.ReadOnlyModelViewSet):
    """爬取日志API"""
    queryset = CrawlLog.objects.all()
    serializer_class = CrawlLogSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        region = self.request.query_params.get('region')
        if region:
            qs = qs.filter(region_id=region)
        return qs[:100]


class StatsView(APIView):
    """统计数据API"""

    def get(self, request):
        # 违规事项分布统计
        violations = self.get_violation_stats()

        # 案件查处统计（按月）
        months = int(request.query_params.get('months', 12))
        cases = self.get_case_stats(months)

        # 地区统计
        regions = self.get_region_stats()

        return Response({
            'code': 0,
            'data': {
                'violations': violations,
                'cases': cases,
                'regions': regions
            }
        })

    def get_violation_stats(self):
        """获取违规事项分布"""
        news = News.objects.filter(status='published')
        stats = {}

        for n in news:
            tags = n.get_tag_names_list()
            for tag in tags:
                stats[tag] = stats.get(tag, 0) + 1

        # 排序并返回
        result = [{'name': k, 'value': v} for k, v in sorted(stats.items(), key=lambda x: x[1], reverse=True)]
        return result[:20]

    def get_case_stats(self, months):
        """获取案件查处统计（按月）"""
        from django.db.models import Count
        from django.db.models.functions import TruncMonth

        start_date = timezone.now() - timedelta(days=months * 30)
        stats = (News.objects
                 .filter(status='published', crawl_time__gte=start_date)
                 .annotate(month=TruncMonth('crawl_time'))
                 .values('month')
                 .annotate(count=Count('id'))
                 .order_by('month'))

        months_list = []
        values_list = []

        for item in stats:
            months_list.append(item['month'].strftime('%Y-%m'))
            values_list.append(item['count'])

        return {
            'months': months_list,
            'values': values_list
        }

    def get_region_stats(self):
        """获取地区统计"""
        stats = (News.objects
                 .filter(status='published')
                 .values('region__name', 'region__code')
                 .annotate(count=Count('id'))
                 .order_by('-count'))

        return list(stats)


class ForceCrawlView(APIView):
    """手动触发爬取"""

    def post(self, request):
        from apps.crawler.tasks import crawl_all_regions

        try:
            result = crawl_all_regions()
            return Response({
                'code': 0,
                'message': '爬取完成',
                'data': result
            })
        except Exception as e:
            logger.exception('手动爬取失败')
            return Response({
                'code': -1,
                'message': f'爬取失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CrawlTaskViewSet(viewsets.ModelViewSet):
    """爬虫任务API"""
    queryset = CrawlTask.objects.all()
    serializer_class = CrawlTaskSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs[:100]


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """审计日志API"""
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        # 筛选操作类型
        action = self.request.query_params.get('action')
        if action:
            qs = qs.filter(action=action)

        # 筛选内容类型
        content_type = self.request.query_params.get('content_type')
        if content_type:
            qs = qs.filter(content_type=content_type)

        # 筛选用户
        user_id = self.request.query_params.get('user')
        if user_id:
            qs = qs.filter(user_id=user_id)

        # 日期范围
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            qs = qs.filter(created_at__date__gte=start_date)
        if end_date:
            qs = qs.filter(created_at__date__lte=end_date)

        return qs.select_related('user')[:200]


class SupervisionItemViewSet(viewsets.ModelViewSet):
    """监督事项清单API"""
    queryset = SupervisionItem.objects.all()
    serializer_class = SupervisionItemSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        # 按年份筛选
        year = self.request.query_params.get('year')
        if year:
            qs = qs.filter(year=year)

        # 按月份筛选
        month = self.request.query_params.get('month')
        if month:
            qs = qs.filter(month=month)

        # 按分类筛选
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category_id=category)

        # 按启用状态筛选
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')

        return qs.select_related('category')

    @action(detail=False, methods=['get'])
    def by_period(self, request):
        """按年月分组获取监督事项"""
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        qs = self.get_queryset()
        if year:
            qs = qs.filter(year=year)
        if month:
            qs = qs.filter(month=month)

        # 按分类分组
        from django.db.models import Count
        stats = qs.values('category__name').annotate(
            count=Count('id')
        ).order_by('category__name')

        return Response({
            'code': 0,
            'data': {
                'items': SupervisionItemSerializer(qs, many=True).data,
                'stats': list(stats)
            }
        })

    @action(detail=False, methods=['post'])
    def import_excel(self, request):
        """从Excel导入监督事项"""
        import pandas as pd
        import io

        excel_file = request.FILES.get('file')
        if not excel_file:
            return Response({
                'code': -1,
                'message': '请上传Excel文件'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 读取Excel
            df = pd.read_excel(excel_file)

            # 验证必要列
            required_cols = ['事项名称', '年份', '月份', '监督分类', '核心关键词']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                return Response({
                    'code': -1,
                    'message': f'Excel缺少必要列: {", ".join(missing_cols)}'
                }, status=status.HTTP_400_BAD_REQUEST)

            imported_count = 0
            errors = []

            for idx, row in df.iterrows():
                try:
                    # 获取分类
                    category_name = str(row['监督分类']).strip()
                    try:
                        category = TagCategory.objects.get(name=category_name)
                    except TagCategory.DoesNotExist:
                        # 创建新分类
                        category = TagCategory.objects.create(name=category_name)

                    # 检查年份月份格式
                    year = str(int(row['年份']))
                    month = str(int(row['月份'])).zfill(2)

                    # 创建或更新监督事项
                    item, created = SupervisionItem.objects.update_or_create(
                        name=str(row['事项名称']).strip(),
                        year=year,
                        month=month,
                        defaults={
                            'category': category,
                            'core_keywords': str(row.get('核心关键词', '')).strip(),
                            'synonyms': str(row.get('近义词', '')).strip(),
                            'context_words': str(row.get('上下文行动词', '')).strip(),
                            'description': str(row.get('事项描述', '')).strip(),
                            'standard': str(row.get('判定标准', '')).strip(),
                            'is_active': True,
                        }
                    )
                    imported_count += 1

                except Exception as e:
                    errors.append(f'第{idx+2}行错误: {str(e)}')

            return Response({
                'code': 0,
                'message': f'成功导入 {imported_count} 条监督事项',
                'errors': errors if errors else None
            })

        except Exception as e:
            logger.exception('导入Excel失败')
            return Response({
                'code': -1,
                'message': f'导入失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """导出监督事项为Excel"""
        qs = self.get_queryset()

        # 构建DataFrame
        data = []
        for item in qs:
            data.append({
                '事项名称': item.name,
                '年份': item.year,
                '月份': item.month,
                '监督分类': item.category.name if item.category else '',
                '核心关键词': item.core_keywords,
                '近义词': item.synonyms,
                '上下文行动词': item.context_words,
                '事项描述': item.description,
                '判定标准': item.standard,
                '是否启用': '是' if item.is_active else '否',
            })

        df = pd.DataFrame(data)

        # 生成Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='监督事项清单')

        output.seek(0)

        from django.http import HttpResponse
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="监督事项清单_{timezone.now().strftime("%Y%m%d")}.xlsx"'
        return response


class NewsCorrectionView(APIView):
    """新闻手动修正分类API"""

    def post(self, request, pk):
        """手动修正文章分类"""
        news = News.objects.get(pk=pk)
        data = request.data

        try:
            # 获取手动修正的标签
            tag_ids = data.get('manual_tags', [])
            if isinstance(tag_ids, str):
                tag_ids = [int(t.strip()) for t in tag_ids.split(',') if t.strip()]

            # 清除现有手动标签
            news.manual_tags.clear()

            # 设置新标签
            for tag_id in tag_ids:
                try:
                    tag = Tag.objects.get(id=tag_id)
                    news.manual_tags.add(tag)
                except Tag.DoesNotExist:
                    pass

            # 更新手动标签名称
            news.manual_tag_names = ','.join([t.name for t in news.manual_tags.all()])

            # 更新修正信息
            news.is_manual_corrected = True
            news.correction_reason = data.get('correction_reason', '')
            news.corrected_by = request.user if request.user.is_authenticated else None
            news.corrected_at = timezone.now()
            news.save()

            return Response({
                'code': 0,
                'message': '修正成功',
                'data': {
                    'manual_tags': news.manual_tag_names,
                    'corrected_at': news.corrected_at.isoformat() if news.corrected_at else None
                }
            })

        except Exception as e:
            logger.exception('修正分类失败')
            return Response({
                'code': -1,
                'message': f'修正失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """取消手动修正，恢复自动分类"""
        news = News.objects.get(pk=pk)

        try:
            news.manual_tags.clear()
            news.manual_tag_names = ''
            news.is_manual_corrected = False
            news.correction_reason = ''
            news.corrected_by = None
            news.corrected_at = None
            news.save()

            return Response({
                'code': 0,
                'message': '已取消手动修正'
            })

        except Exception as e:
            logger.exception('取消修正失败')
            return Response({
                'code': -1,
                'message': f'操作失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
