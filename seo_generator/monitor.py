"""Monitoring placeholder."""
from pathlib import Path


def log_generation(output_dir: Path, keywords):
    """Log generated pages."""
    log_file = output_dir / "log.txt"
    with log_file.open("w", encoding="utf-8") as f:
        for kw in keywords:
            f.write(f"Generated page for {kw}\n")
