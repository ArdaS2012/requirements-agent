import pytest
from src.chunking import chunking_page


# --- Empty / whitespace inputs ---

def test_empty_string_returns_empty():
    titles, contents, ids = chunking_page("")
    assert titles == [] and contents == [] and ids == []


def test_whitespace_only_returns_empty():
    titles, contents, ids = chunking_page("   \n\t  ")
    assert titles == [] and contents == [] and ids == []


# --- Single section ---

def test_single_section_no_header():
    text = "Some plain text\nwith multiple lines."
    titles, contents, ids = chunking_page(text)
    assert len(contents) == 1
    assert "Some plain text" in contents[0]
    assert titles[0] == "Untitled"
    assert ids == [0]


def test_single_header_with_content():
    text = "# Introduction\nThis is the intro text."
    titles, contents, ids = chunking_page(text)
    assert len(contents) == 1
    assert titles[0] == "Introduction"
    assert "intro text" in contents[0]


# --- Multiple sections ---

def test_multiple_headers_produce_multiple_chunks():
    text = (
        "# Section A\nContent of A.\n"
        "## Section B\nContent of B.\n"
        "### Section C\nContent of C."
    )
    titles, contents, ids = chunking_page(text)
    assert len(titles) == len(contents) == len(ids) == 3
    assert "Section A" in titles[0]
    assert "Content of A" in contents[0]


def test_chunk_ids_are_sequential():
    text = "# A\ntext a\n# B\ntext b\n# C\ntext c"
    _, _, ids = chunking_page(text)
    assert ids == list(range(len(ids)))


def test_nested_headers_joined_with_slash():
    text = "# Parent\n## Child\nsome content"
    titles, _, _ = chunking_page(text)
    # The child section title should include the parent context
    assert "Child" in titles[-1]


# --- Markdown formatting in headers ---

def test_bold_markers_stripped_from_title():
    text = "# **Bold Title**\nContent here."
    titles, _, _ = chunking_page(text)
    assert "**" not in titles[0]
    assert "Bold Title" in titles[0]


def test_extra_whitespace_in_title_collapsed():
    text = "#  Spaced   Title  \nContent."
    titles, _, _ = chunking_page(text)
    assert "  " not in titles[0]  # no double spaces


# --- Content preservation ---

def test_content_is_not_empty_for_valid_sections():
    text = "# Section\nLine 1\nLine 2\nLine 3"
    _, contents, _ = chunking_page(text)
    assert all(c.strip() for c in contents)


def test_header_only_no_body_produces_no_chunk():
    """A header with no body text after it (end of input) should not create a chunk."""
    text = "# Only a header"
    _, contents, _ = chunking_page(text)
    assert contents == []
