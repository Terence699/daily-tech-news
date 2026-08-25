#!/usr/bin/env python3
import json
import re
import math
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import pytz

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = Path(__file__).with_name("config.json")
DATE_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})\.md$")
PAGE_SIZE = 10

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Tech News</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        :root {{
            --bg-primary: #f3f4f6;
            --bg-secondary: #ffffff;
            --border: #e5e7eb;
            --text-primary: #111827;
            --text-secondary: #4b5563;
            --text-tertiary: #9ca3af;
            --accent: #f97316;
            --accent-hover: #ea580c;
        }}

        body {{
            font-family: 'Inter', 'Noto Sans SC', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 0 20px;
            width: 100%;
        }}

        header {{
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--border);
            padding: 20px 0;
            position: sticky;
            top: 0;
            z-index: 100;
        }}

        .header-content {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo {{
            font-size: 20px;
            font-weight: 700;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .logo-icon {{
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, #f97316, #fb923c);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }}

        .github-link {{
            color: var(--text-secondary);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 14px;
            transition: color 0.2s;
        }}

        .github-link:hover {{
            color: var(--text-primary);
        }}

        main {{
            flex: 1;
            padding: 40px 0;
        }}

        .digest-list {{
            display: grid;
            gap: 16px;
        }}

        .digest-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            text-decoration: none;
            color: inherit;
            transition: all 0.2s;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .digest-card:hover {{
            transform: translateY(-2px);
            border-color: var(--accent);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}

        .card-title {{
            font-size: 16px;
            font-weight: 600;
            color: var(--text-primary);
        }}

        .card-date {{
            font-size: 14px;
            color: var(--text-tertiary);
            font-family: monospace;
        }}

        .pagination {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            margin-top: 24px;
            flex-wrap: wrap;
        }}

        .page-links {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .page-link {{
            padding: 6px 12px;
            border-radius: 999px;
            border: 1px solid var(--border);
            text-decoration: none;
            color: var(--text-secondary);
            font-size: 14px;
            background: var(--bg-secondary);
            transition: all 0.2s;
            font-family: inherit;
            appearance: none;
            cursor: pointer;
        }}

        .page-link:hover {{
            color: var(--text-primary);
            border-color: var(--accent);
        }}

        .page-link.active {{
            background: var(--accent);
            border-color: var(--accent);
            color: #fff;
        }}

        .page-link.disabled {{
            color: var(--text-tertiary);
            border-color: var(--border);
            cursor: not-allowed;
        }}

        .page-ellipsis {{
            color: var(--text-tertiary);
            font-size: 14px;
            padding: 0 4px;
        }}

        footer {{
            padding: 32px 0;
            text-align: center;
            color: var(--text-secondary);
            font-size: 13px;
            border-top: 1px solid var(--border);
            background: var(--bg-secondary);
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <div class="logo">
                    <div class="logo-icon">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                            <polyline points="14 2 14 8 20 8"></polyline>
                            <line x1="16" y1="13" x2="8" y2="13"></line>
                            <line x1="16" y1="17" x2="8" y2="17"></line>
                            <line x1="10" y1="9" x2="8" y2="9"></line>
                        </svg>
                    </div>
                    Daily Tech News
                </div>
                <a href="https://github.com/Terence699" class="github-link" target="_blank">
                    <svg height="20" width="20" viewBox="0 0 16 16" fill="currentColor">
                        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
                    </svg>
                    GitHub
                </a>
            </div>
        </div>
    </header>

    <main>
        <div class="container">
            <div class="digest-list">
                {list_html}
            </div>
            {pagination_html}
        </div>
    </main>

    <footer>
        <div class="container">
            Daily Tech News · 由 GLM-5.2 自动生成
        </div>
    </footer>
</body>
</html>
"""


def load_config():
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def list_digest_files(digests_dir: Path) -> List[Tuple[str, Path]]:
    items: List[Tuple[str, Path]] = []
    for path in digests_dir.glob("*.md"):
        match = DATE_PATTERN.match(path.name)
        if not match:
            continue
        items.append((match.group(1), path))
    items.sort(key=lambda x: x[0], reverse=True)
    return items


def page_filename(page: int) -> str:
    return "index.html" if page == 1 else f"page-{page}.html"


def build_list_html(entries: List[Tuple[str, Path]]) -> str:
    if not entries:
        return '<div style="text-align:center; color:#666;">暂无简报</div>'

    list_items = []
    for date_str, _ in entries:
        list_items.append(f"""
            <a href="digests/{date_str}.html" class="digest-card">
                <span class="card-title">Daily Tech News | {date_str}</span>
                <span class="card-date">{date_str}</span>
            </a>
            """)
    return "\n".join(list_items)


def build_page_links(current_page: int, total_pages: int) -> List[int | None]:
    if total_pages <= 7:
        return list(range(1, total_pages + 1))

    pages: List[int | None] = [1]
    if current_page > 4:
        pages.append(None)

    if current_page <= 4:
        start = 2
        end = 4
    elif current_page >= total_pages - 3:
        start = total_pages - 3
        end = total_pages - 1
    else:
        start = current_page - 1
        end = current_page + 1

    pages.extend(range(start, end + 1))

    if current_page < total_pages - 3:
        pages.append(None)

    pages.append(total_pages)
    return pages


def build_pagination(current_page: int, total_pages: int) -> str:
    prev_link = (
        f'<a href="{page_filename(current_page - 1)}" class="page-link">上一页</a>'
        if current_page > 1
        else '<button type="button" class="page-link disabled" disabled>上一页</button>'
    )
    next_link = (
        f'<a href="{page_filename(current_page + 1)}" class="page-link">下一页</a>'
        if current_page < total_pages
        else '<button type="button" class="page-link disabled" disabled>下一页</button>'
    )
    page_links = []
    for page in build_page_links(current_page, total_pages):
        if page is None:
            page_links.append('<span class="page-ellipsis">...</span>')
            continue
        class_name = "page-link active" if page == current_page else "page-link"
        page_links.append(f'<a href="{page_filename(page)}" class="{class_name}">{page}</a>')
    return f"""
            <nav class="pagination" aria-label="分页导航">
                {prev_link}
                <div class="page-links">
                    {''.join(page_links)}
                </div>
                {next_link}
            </nav>
    """


def main() -> None:
    config = load_config()
    digests_dir = PROJECT_ROOT / config["output"]["output_dir"]
    entries = list_digest_files(digests_dir)
    total_pages = max(1, math.ceil(len(entries) / PAGE_SIZE))

    for page in range(1, total_pages + 1):
        start = (page - 1) * PAGE_SIZE
        page_entries = entries[start : start + PAGE_SIZE]
        list_html = build_list_html(page_entries)
        pagination_html = build_pagination(page, total_pages)
        index_html = INDEX_TEMPLATE.format(
            list_html=list_html,
            pagination_html=pagination_html,
        )

        output_path = PROJECT_ROOT / page_filename(page)
        output_path.write_text(index_html, encoding="utf-8")
        print(f"已生成首页列表: {output_path}")


if __name__ == "__main__":
    main()
