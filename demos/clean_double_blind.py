# -*- coding: utf-8 -*-
"""
iCAN 双盲合规清洗工具

针对创新赛道规则：所有赛程材料禁止出现院校、指导教师、单位名称，每出现一处扣 5 分。

功能：
  1. 全项目扫描院校标识（校名 / 校域名 / 校 Logo 引用）
  2. 默认「试运行」只出报告不动文件；加 --apply 才实际修改
  3. 修改前自动生成带时间戳的备份，绝不裸改

用法：
    python clean_double_blind.py            # 试运行，只扫描出报告
    python clean_double_blind.py --apply    # 实际清洗（自动备份）
"""
import os
import re
import sys
import shutil
import argparse
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── 违规标识表：如需覆盖自己院校，改这里即可 ──────────────────────
SCHOOL_NAMES = ['西安文理学院']
SCHOOL_DOMAINS = ['xawl.edu.cn', 'dis.xawl.edu.cn', 'www.xawl.edu.cn']
# 替换为中性文案（严禁改成其它院校/单位名）
REPLACE_NAME = '廉智通'

SKIP_DIRS = {'venv', '.git', 'node_modules', '__pycache__', '.idea', 'media', 'staticfiles'}
SCAN_EXT = {'.html', '.htm', '.md', '.js', '.css', '.json', '.py', '.txt', '.vue'}

# 匹配整条引用了院校域名的 <img ...> 标签
IMG_TAG_RE = re.compile(
    r'<img\b[^>]*?(?:' + '|'.join(re.escape(d) for d in SCHOOL_DOMAINS) + r')[^>]*>',
    re.IGNORECASE,
)
DOMAIN_URL_RE = re.compile(
    r'https?://(?:www\.|dis\.)?[^/\s"\']*' + re.escape('xawl.edu.cn') + r'[^"\'\s]*'
)


def iter_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if os.path.splitext(fn)[1].lower() in SCAN_EXT:
                yield os.path.join(dirpath, fn)


def scan_file(path):
    """返回该文件命中的行数列表 [(行号, 内容片段, 类型)]"""
    hits = []
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
    except Exception as e:
        return hits, f'读取失败: {e}'
    for i, line in enumerate(lines, 1):
        for name in SCHOOL_NAMES:
            if name in line:
                hits.append((i, line.strip()[:150], f'院校名 {name}'))
                break
        else:
            for d in SCHOOL_DOMAINS:
                if d in line:
                    hits.append((i, line.strip()[:150], f'校域名 {d}'))
                    break
    return hits, None


def clean_text(text):
    """对单文件内容做清洗"""
    # 1) 移除引用院校 Logo 的整条 img 标签
    text = IMG_TAG_RE.sub('<!-- 院校 Logo 已按双盲要求移除 -->', text)
    # 2) 移除校域名 URL
    text = DOMAIN_URL_RE.sub('', text)
    # 3) 替换院校名为中性文案
    for name in SCHOOL_NAMES:
        text = text.replace(name, REPLACE_NAME)
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true', help='实际执行清洗（默认仅试运行）')
    args = ap.parse_args()

    total_hits = 0
    touched = []
    errors = []

    print(f'扫描根目录: {BASE}')
    print(f'模式      : {"实际清洗(会备份)" if args.apply else "试运行(不改动任何文件)"}')
    print('=' * 72)

    for path in iter_files(BASE):
        hits, err = scan_file(path)
        if err:
            errors.append((path, err))
            continue
        if hits:
            rel = os.path.relpath(path, BASE)
            print(f'\n[命中 {len(hits)} 处] {rel}')
            for ln, snippet, kind in hits[:5]:
                print(f'    L{ln} <{kind}>')
                print(f'      {snippet}')
            if len(hits) > 5:
                print(f'    ... 其余 {len(hits) - 5} 处略')
            total_hits += len(hits)
            touched.append(path)

    print('\n' + '=' * 72)
    print(f'命中文件数: {len(touched)}   命中总处数: {total_hits}')
    if total_hits:
        print(f'按规则预估扣分: {total_hits * 5} 分（每处 5 分）')
    if errors:
        print(f'\n读取异常 {len(errors)} 个文件:')
        for p, e in errors[:5]:
            print(f'    {os.path.relpath(p, BASE)}: {e}')

    if not args.apply:
        print('\n【试运行结束】未修改任何文件。确认无误后加 --apply 执行清洗。')
        return

    if not touched:
        print('\n无需清洗：未发现违规标识。')
        return

    stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    bak_root = os.path.join(BASE, f'.doubleblind_backup_{stamp}')
    print(f'\n备份目录: {bak_root}')

    done = 0
    for path in touched:
        rel = os.path.relpath(path, BASE)
        bak = os.path.join(bak_root, rel)
        os.makedirs(os.path.dirname(bak), exist_ok=True)
        shutil.copy2(path, bak)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                src = f.read()
            out = clean_text(src)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(out)
            done += 1
        except Exception as e:
            print(f'    清洗失败 {rel}: {e}')

    print(f'清洗完成 {done}/{len(touched)} 个文件')

    # 清洗后复查
    remain = 0
    for path in touched:
        hits, _ = scan_file(path)
        remain += len(hits)
    print(f'复查残留: {remain} 处')


if __name__ == '__main__':
    main()
