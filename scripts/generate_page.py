#!/usr/bin/env python3
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import markdown
import pytz

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = Path(__file__).with_name("config.json")
DATE_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})\.md$")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Tech News | {date_str}</title>
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
            --bg-tertiary: #f9fafb;
            --border: #e5e7eb;
            --text-primary: #111827;
            --text-secondary: #4b5563;
            --accent: #f97316;
            --accent-hover: #ea580c;
        }}

        body {{
            font-family: 'Inter', 'Noto Sans SC', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
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

        /* Header */
        header {{
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
        }}

        .header-inner {{
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .back-link {{
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 4px;
            transition: color 0.2s;
        }}

        .back-link:hover {{
            color: var(--accent);
        }}

        .header-date {{
            font-size: 14px;
            color: var(--text-secondary);
            font-family: monospace;
        }}

        /* Main */
        main {{
            flex: 1;
            padding: 40px 0;
        }}

        .digest-item {{
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}

        .digest-content {{
            padding: 32px;
        }}

        /* Content Styles */
        .digest-content h1 {{
            font-size: 24px;
            margin-bottom: 16px;
            color: var(--text-primary);
        }}

        .digest-content h2 {{
            font-size: 18px;
            margin: 32px 0 16px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border);
            color: var(--text-primary);
        }}

        .digest-content p {{
            margin-bottom: 16px;
            color: var(--text-secondary);
        }}

        .digest-content ul {{
            padding-left: 20px;
            margin-bottom: 24px;
        }}

        .digest-content li {{
            margin-bottom: 12px;
            color: var(--text-secondary);
        }}

        .digest-content a {{
            color: var(--accent);
            text-decoration: none;
        }}

        .digest-content a:hover {{
            text-decoration: underline;
        }}

        /* Footer */
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
            <div class="header-inner">
                <a href="../index.html" class="back-link">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M19 12H5M12 19l-7-7 7-7"/>
                    </svg>
                    Daily Tech News
                </a>
                <span class="header-date">{date_str}</span>
            </div>
        </div>
    </header>

    <main>
        <div class="container">
            <article class="digest-item">
                <div class="digest-content">
                    {html_content}
                </div>
            </article>
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
    return items


def main() -> None:
    config = load_config()
    digests_dir = PROJECT_ROOT / config["output"]["output_dir"]
    digests_dir.mkdir(parents=True, exist_ok=True)

    entries = list_digest_files(digests_dir)
    
    for date_str, path in entries:
        md_text = path.read_text(encoding="utf-8")
        html_content = markdown.markdown(md_text, extensions=["extra", "tables"])
        
        page_html = HTML_TEMPLATE.format(
            date_str=date_str,
            html_content=html_content
        )
        
        output_path = digests_dir / f"{date_str}.html"
        output_path.write_text(page_html, encoding="utf-8")
        print(f"已生成详情页: {output_path}")


if __name__ == "__main__":
    main()
