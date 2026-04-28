"""Generate llms.txt and llms-full.txt from the zensical navigation."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, TypedDict

try:
    import tomllib
except ImportError:  # pragma: no cover
    import tomli as tomllib

ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT_DIR / "docs"
ZENSICAL_TOML = ROOT_DIR / "zensical.toml"
OPTIONAL_PATTERNS = ("development-contributing.md",)
SKIP_PREFIXES = ("```", "!!!", "[![", "![", "<", "---")
MAX_DESC_LINES = 2
MAX_DESC_LEN = 150
EMOJI_RE = re.compile(
    r"[\U0001F300-\U0001F9FF\U0001FA00-\U0001FAFF\U00002702-\U000027B0"
    r"\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002600-\U000026FF"
    r"\U00002300-\U000023FF\U0000FE00-\U0000FE0F\U0000200D]+",
)


class SiteConfig(TypedDict):
    """Configuration extracted from zensical.toml."""

    site_name: str
    site_description: str
    site_url: str
    nav: list[dict[str, Any]]


@dataclass
class PageInfo:
    """Information about a documentation page."""

    title: str
    path: str
    url: str
    description: str
    content: str
    depth: int = 0


@dataclass
class NavSection:
    """A navigation section with optional children."""

    title: str
    path: str | None = None
    children: list["NavSection"] = field(default_factory=list)
    depth: int = 0


def parse_zensical_toml(path: Path) -> SiteConfig:
    """Parse zensical.toml and extract project configuration."""
    if not path.exists():
        raise FileNotFoundError(path)
    try:
        with path.open("rb") as file:
            project = tomllib.load(file).get("project", {})
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f"Error parsing {path}: {exc}") from exc
    return SiteConfig(
        site_name=project.get("site_name", ""),
        site_description=project.get("site_description", ""),
        site_url=project.get("site_url", "").rstrip("/"),
        nav=project.get("nav", []),
    )


def flatten_nav(nav: list[dict[str, Any]], depth: int = 0) -> list[NavSection]:
    """Recursively flatten the zensical nav structure."""
    sections: list[NavSection] = []
    for item in nav:
        for title, value in item.items():
            if isinstance(value, str):
                sections.append(NavSection(title=title, path=value, depth=depth))
            elif isinstance(value, list):
                sections.append(
                    NavSection(
                        title=title,
                        children=flatten_nav(value, depth + 1),
                        depth=depth,
                    )
                )
    return sections


def extract_page_info(md_path: Path, url: str, depth: int = 0) -> PageInfo | None:
    """Extract title and description from a Markdown file."""
    if not md_path.exists():
        print(f"Warning: {md_path} not found, skipping", file=sys.stderr)
        return None
    try:
        content = md_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Warning: Cannot read {md_path}: {exc}", file=sys.stderr)
        return None

    title = md_path.stem.replace("-", " ").replace("_", " ").title()
    desc_lines: list[str] = []
    in_code = False
    found_h1 = False

    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if stripped.startswith("# ") and not found_h1:
            title = EMOJI_RE.sub("", stripped[2:]).strip()
            found_h1 = True
            continue
        if not found_h1:
            continue
        if stripped.startswith("## "):
            break
        if stripped.startswith(SKIP_PREFIXES):
            continue
        if not stripped and desc_lines:
            break
        if stripped:
            desc_lines.append(stripped)
            if len(desc_lines) >= MAX_DESC_LINES:
                break

    description = EMOJI_RE.sub("", " ".join(desc_lines)).strip()
    if len(description) > MAX_DESC_LEN:
        description = description[: MAX_DESC_LEN - 3] + "..."
    return PageInfo(
        title=title,
        path=str(md_path.relative_to(DOCS_DIR)),
        url=url,
        description=description,
        content=content,
        depth=depth,
    )


def collect_pages(
    sections: list[NavSection],
    site_url: str,
    depth: int = 0,
    seen: set[str] | None = None,
) -> list[PageInfo]:
    """Collect page metadata from the nav structure."""
    if seen is None:
        seen = set()
    pages: list[PageInfo] = []
    for section in sections:
        if section.path and section.path not in seen:
            base = section.path.rsplit(".", 1)[0]
            url = (
                f"{site_url}/"
                if base == "index"
                else f"{site_url}/{base.removesuffix('/index')}/"
            )
            page = extract_page_info(DOCS_DIR / section.path, url, depth)
            if page is not None:
                seen.add(section.path)
                pages.append(page)
        if section.children:
            pages.extend(collect_pages(section.children, site_url, depth + 1, seen))
    return pages


def generate_llms_txt(
    config: SiteConfig, sections: list[NavSection], pages: list[PageInfo]
) -> str:
    """Generate llms.txt content from page metadata."""
    page_map = {page.path: page for page in pages}

    def format_page(page: PageInfo) -> str:
        line = f"- [{page.title}]({page.url})"
        if page.description:
            line += f": {page.description}"
        return line

    def is_optional(path: str | None) -> bool:
        return path is not None and any(
            fnmatch(path, pattern) for pattern in OPTIONAL_PATTERNS
        )

    def section_is_optional(section: NavSection) -> bool:
        if section.path:
            return is_optional(section.path)
        return bool(section.children) and all(
            section_is_optional(child) for child in section.children
        )

    def iter_section_pages(section: NavSection) -> list[PageInfo]:
        if section.path:
            page = page_map.get(section.path)
            return [page] if page is not None else []
        pages: list[PageInfo] = []
        for child in section.children:
            pages.extend(iter_section_pages(child))
        return pages

    def render(section: NavSection) -> list[str]:
        if section.path:
            page = page_map.get(section.path)
            return [format_page(page)] if page is not None else []
        if not section.children:
            return []
        header = "##" if section.depth == 0 else "###"
        lines = [f"{header} {section.title}", ""]
        for child in section.children:
            lines.extend(render(child))
        return [*lines, ""]

    main_sections: list[NavSection] = []
    optional_sections: list[NavSection] = []
    for section in sections:
        if section_is_optional(section):
            optional_sections.append(section)
        else:
            main_sections.append(section)

    lines = [
        f"# {config['site_name']}",
        "",
        f"> {config['site_description']}",
        "",
    ]
    for section in main_sections:
        lines.extend(render(section))
    if optional_sections:
        lines.extend(["## Optional", ""])
        for section in optional_sections:
            for page in iter_section_pages(section):
                lines.append(format_page(page))
        lines.append("")

    while lines and not lines[-1]:
        lines.pop()
    return "\n".join([*lines, ""])


def generate_llms_full_txt(pages: list[PageInfo]) -> str:
    """Generate llms-full.txt with the full docs content."""
    blocks: list[str] = []
    for page in pages:
        content = page.content.strip()
        if content.startswith("# "):
            first_newline = content.find("\n")
            if first_newline != -1:
                content = content[first_newline + 1 :].strip()
        blocks.append(f"# {page.title}\n\nSource: {page.url}\n\n{content}")
    return "\n---\n\n".join(blocks) + "\n"


def check_files(expected_files: dict[Path, str]) -> int:
    """Check whether the generated files are up to date."""
    errors = []
    for path, expected in expected_files.items():
        if not path.exists():
            errors.append(f"{path} does not exist")
        elif path.read_text(encoding="utf-8") != expected:
            errors.append(f"{path} is out of date")
    if errors:
        for error in errors:
            print(f"Error: {error}", file=sys.stderr)
        print("\nRun 'python scripts/build_llms_txt.py' to regenerate.", file=sys.stderr)
        return 1
    print("llms.txt files are up to date")
    return 0


def main() -> int:
    """Run the llms.txt generator."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check whether the generated files are up to date.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DOCS_DIR,
        help="Output directory for llms files.",
    )
    args = parser.parse_args()

    try:
        config = parse_zensical_toml(ZENSICAL_TOML)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    sections = flatten_nav(config["nav"])
    pages = collect_pages(sections, config["site_url"])
    expected_files = {
        args.output_dir / "llms.txt": generate_llms_txt(config, sections, pages),
        args.output_dir / "llms-full.txt": generate_llms_full_txt(pages),
    }

    if args.check:
        return check_files(expected_files)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for path, content in expected_files.items():
        path.write_text(content, encoding="utf-8")
        print(f"Generated {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
