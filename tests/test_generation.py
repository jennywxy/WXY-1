import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from seo_generator import generate_site
from pathlib import Path


def test_generate_site(tmp_path: Path):
    keywords = generate_site("demo topic", tmp_path)
    assert (tmp_path / "demo-topic.html").exists()
    assert (tmp_path / "sitemap.xml").exists()
    assert (tmp_path / "log.txt").exists()
    assert "demo-topic" in keywords[0]
