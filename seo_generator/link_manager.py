"""Link management utilities."""
from typing import List
from pathlib import Path


def generate_sitemap(output_dir: Path, keywords: List[str]) -> None:
    """Generate a simple sitemap.xml file."""
    sitemap_entries = [
        f"  <url><loc>{keyword}.html</loc></url>" for keyword in keywords
    ]
    content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" "<urlset>\n" + "\n".join(sitemap_entries) + "\n</urlset>"
    (output_dir / "sitemap.xml").write_text(content, encoding="utf-8")
