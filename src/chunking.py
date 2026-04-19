import re


def chunking_page(page_text: str) -> tuple[list[str], list[str], list[int]]:
    if not page_text.strip():
        return [], [], []

    section_titles: list[str] = []
    chunk_contents: list[str] = []
    chunk_ids: list[int] = []
    pending_titles: list[str] = []
    buffer: list[str] = []

    def clean_title(raw: str) -> str:
        title = re.sub(r"[*_`]+", "", raw).strip()
        return re.sub(r"\s+", " ", title)

    def flush_chunk() -> None:
        chunk = "\n".join(buffer).strip()
        if chunk:
            title = " / ".join(pending_titles) if pending_titles else "Untitled"
            section_titles.append(title)
            chunk_contents.append(chunk)
            chunk_ids.append(len(chunk_ids))

    for line in page_text.splitlines():
        match = re.match(r"^\s{0,3}#{1,6}\s+(.*?)\s*$", line)
        if match:
            title = clean_title(match.group(1))
            if any(item.strip() for item in buffer):
                flush_chunk()
                buffer = []
                pending_titles = [title] if title else []
            elif title:
                buffer = []
                pending_titles.append(title)
            continue
        buffer.append(line)

    flush_chunk()
    return section_titles, chunk_contents, chunk_ids
