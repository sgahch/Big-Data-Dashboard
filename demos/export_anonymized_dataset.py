# -*- coding: utf-8 -*-
"""
导出脱敏演示数据集
用途：为竞赛演示/前端 Demo 生成不含真实自然人姓名的案件数据。
安全策略：保留「单位+职务+处置方式」结构，遮蔽姓名与原文链接，避免巡展公开展示真实个人信息。
"""
import os
import sys
import re
import json
import django

BASE = r'C:\Users\Ynchen\Desktop\大数据看板'
sys.path.insert(0, BASE)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supervision.settings')
os.chdir(BASE)
django.setup()

from apps.news.models import News  # noqa: E402

# 职务词锚点：中文通报结构通常为「单位 + 职务 + 姓名 + 处置动作」
TITLE_WORDS = (
    r'(书记|局长|主任|经理|董事|委员|巡视员|院长|县长|主席|部长|厅长|省长|市长|'
    r'所长|站长|队长|科长|处长|行长|检察长|秘书长|组长|总裁|总工|监事)'
)
NAME_RE = re.compile(
    TITLE_WORDS + r'([\u4e00-\u9fa5]{2,3})(?=接受|涉嫌|严重违纪|被开除|被取消|被移送|，|。)'
)


def mask_person(title: str) -> str:
    """将职务之后的自然人姓名替换为脱敏标记。"""
    return NAME_RE.sub(lambda m: m.group(1) + '\u3010姓名脱敏\u3011', title)


def main():
    qs = [x for x in News.objects.all() if x.url and 'qinfeng.gov.cn' in x.url]
    rows = []
    for x in qs:
        rows.append({
            'title': mask_person(x.title or ''),
            'date': str(x.date) if x.date else None,
            'region': x.region_name or '未知',
            'source': x.source or '',
            'tags': x.tag_names or '',
        })
    rows.sort(key=lambda r: r['date'] or '')

    out_dir = os.path.join(BASE, 'demos', 'data')
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, 'cases_anonymized.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)

    print(f'导出完成: {out}')
    print(f'案件记录数: {len(rows)}')
    if rows:
        print(f'时间范围: {rows[0]["date"]} ~ {rows[-1]["date"]}')


if __name__ == '__main__':
    main()
