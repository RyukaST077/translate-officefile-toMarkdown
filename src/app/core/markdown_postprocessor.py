"""Markdown post-processing utilities."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Sequence


_IMAGE_MARKDOWN_PATTERN = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_IMAGE_REFERENCE_PATTERN = re.compile(r"!\[[^\]]*\]\[[^\]]*\]")


@dataclass(frozen=True)
class MarkdownPostprocessResult:
    """Result of post-processing markdown."""

    markdown: str
    warnings: list[str]


def remove_image_markdown(markdown: str) -> str:
    """Remove Markdown image embeds from text."""
    has_trailing_newline = markdown.endswith("\n")
    cleaned = _IMAGE_MARKDOWN_PATTERN.sub("", markdown)
    cleaned = _IMAGE_REFERENCE_PATTERN.sub("", cleaned)
    cleaned = re.sub(r"[ \t]+\n", "\n", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    if has_trailing_newline and not cleaned.endswith("\n"):
        cleaned += "\n"
    return cleaned


def normalize_excel_markdown(
    markdown: str,
    sheet_names: Sequence[str],
    image_sheet_names: Iterable[str],
) -> MarkdownPostprocessResult:
    """Normalize Excel markdown by ensuring sheet headings and annotations."""
    warnings: list[str] = []
    image_set = {name.strip() for name in image_sheet_names}
    sheet_set = {name.strip() for name in sheet_names}
    found: set[str] = set()

    lines = markdown.splitlines()
    normalized_lines: list[str] = []

    for line in lines:
        updated = _normalize_sheet_heading(line, sheet_set, image_set, found)
        normalized_lines.append(updated)

    missing = [name for name in sheet_names if name.strip() not in found]
    if missing:
        warnings.append(
            f"Excelシート見出しが検出できませんでした: {', '.join(missing)}"
        )
        if len(sheet_names) == 1:
            heading = _sheet_heading(sheet_names[0], sheet_names[0] in image_set)
            normalized_lines.insert(0, heading)

    normalized = "\n".join(normalized_lines)
    return MarkdownPostprocessResult(markdown=normalized, warnings=warnings)


def _normalize_sheet_heading(
    line: str,
    sheet_names: set[str],
    image_sheet_names: set[str],
    found: set[str],
) -> str:
    match = re.match(r"^(#{1,6})\s+(.*)$", line)
    if not match:
        stripped = line.strip()
        if stripped in sheet_names:
            found.add(stripped)
            return _sheet_heading(stripped, stripped in image_sheet_names)
        return line

    _, title = match.groups()
    title = title.strip()
    base_title = title.replace("（画像あり）", "").strip()
    if base_title not in sheet_names:
        return line

    found.add(base_title)
    return _sheet_heading(base_title, base_title in image_sheet_names)


def _sheet_heading(sheet_name: str, has_image: bool) -> str:
    suffix = "（画像あり）" if has_image else ""
    return f"## {sheet_name}{suffix}"
