"""Page management utilities."""
from pathlib import Path
from typing import Iterable


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang=\"en\">
<head>
<meta charset=\"UTF-8\" />
<title>{title}</title>
<meta name=\"description\" content=\"{description}\" />
</head>
<body>
{body}
</body>
</html>
"""


def save_pages(output_dir: Path, articles: Iterable[str], keywords: Iterable[str]) -> None:
    """Save articles to HTML files in output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for keyword, article in zip(keywords, articles):
        title = keyword.title()
        description = f"Learn about {keyword} in this article."
        html = HTML_TEMPLATE.format(title=title, description=description, body=article)
        filename = output_dir / f"{keyword}.html"
        filename.write_text(html, encoding="utf-8")
