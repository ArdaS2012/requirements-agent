import re


def chunking_page(page_text: str) -> tuple[list[str], list[str], list[int]]:
    """Split a Markdown page into heading-aligned chunks.

    The function walks each line looking for ATX headings (e.g. ``# Title``).
    When a heading is encountered while the current buffer contains content,
    the buffer is flushed as a new chunk and a fresh one is started under the
    new heading.  Consecutive headings with no intervening content are
    accumulated and joined with " / " to preserve hierarchy.

    Args:
        page_text: Raw Markdown text for a single PDF page.

    Returns:
        A 3-tuple of parallel lists:
        - section_titles: human-readable label for each chunk
        - chunk_contents: the actual text of each chunk
        - chunk_ids: zero-based sequential index for each chunk
    """
    if not page_text.strip():
        return [], [], []

    section_titles: list[str] = []
    chunk_contents: list[str] = []
    chunk_ids: list[int] = []
    pending_titles: list[str] = []  # headings seen but not yet attached to a chunk
    buffer: list[str] = []          # lines accumulated for the current chunk

    def clean_title(raw: str) -> str:
        """Strip Markdown emphasis markers and normalise whitespace."""
        title = re.sub(r"[*_`]+", "", raw).strip()
        return re.sub(r"\s+", " ", title)

    def flush_chunk() -> None:
        """Save the current buffer as a finished chunk."""
        chunk = "\n".join(buffer).strip()
        if chunk:
            title = " / ".join(pending_titles) if pending_titles else "Untitled"
            section_titles.append(title)
            chunk_contents.append(chunk)
            chunk_ids.append(len(chunk_ids))

    for line in page_text.splitlines():
        # Detect ATX headings: up to 3 leading spaces, 1-6 '#' chars, then text
        match = re.match(r"^\s{0,3}#{1,6}\s+(.*?)\s*$", line)
        if match:
            title = clean_title(match.group(1))
            if any(item.strip() for item in buffer):
                # Buffer has real content — flush it before starting a new chunk
                flush_chunk()
                buffer = []
                pending_titles = [title] if title else []
            elif title:
                # Consecutive headings with no body — accumulate them
                buffer = []
                pending_titles.append(title)
            continue
        buffer.append(line)

    # Flush whatever remains after the last heading
    flush_chunk()
    return section_titles, chunk_contents, chunk_ids
