"""Main orchestration for SEO generator."""
from pathlib import Path
from typing import List

from .keyword import fetch_keywords
from .content_generator import generate_articles
from .page_manager import save_pages
from .link_manager import generate_sitemap
from .monitor import log_generation


def generate_site(topic: str, output_dir: str) -> List[str]:
    """Generate a simple SEO site for the given topic."""
    keywords = fetch_keywords(topic)
    articles = generate_articles(keywords)
    output_path = Path(output_dir)
    save_pages(output_path, articles, keywords)
    generate_sitemap(output_path, keywords)
    log_generation(output_path, keywords)
    return keywords


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate a simple SEO site.")
    parser.add_argument("topic", help="Topic to generate content for")
    parser.add_argument("--output", default="site", help="Directory to output files")
    args = parser.parse_args()

    generate_site(args.topic, args.output)
    print(f"Site generated in {args.output}")
