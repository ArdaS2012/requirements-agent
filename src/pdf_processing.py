import base64
import os
import re

import fitz
import pymupdf4llm
import pytesseract
from PIL import Image
from pypdf import PdfReader
from .embeddings import create_embedding
from .chunking import chunking_page
from .config import client


def process_page(path: str):
    """Yield per-page processing results for a single PDF file.

    Each iteration converts one PDF page to Markdown (via pymupdf4llm),
    splits it into heading-aligned chunks, embeds every chunk, and yields
    a dict ready to be inserted into PostgreSQL by ingestion.py.

    Image handling:
        Extracted images are matched to their page by the ``img-<page_nr>``
        filename convention.  VLM description via process_vlm() is currently
        disabled (commented out) to save API quota — re-enable it when
        accurate figure descriptions are needed.

    Args:
        path: Absolute or relative path to the source PDF.

    Yields:
        dict with keys: source_path, page_nr, image, section_title,
        chunk_id, chunk_content, metadata, embeddings.
    """
    def process_vlm(path: str) -> str:
        """Send an image to a multimodal LLM and return its description.

        Uses the HuggingFace-routed Llama-4-Scout model.  The image is
        base64-encoded and passed inline as a data-URL to avoid storing
        temporary files.

        Args:
            path: Path to the PNG image extracted from the PDF.

        Returns:
            A detailed natural-language description of the figure.
        """
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()

        out = client.chat.completions.create(
            model="meta-llama/Llama-4-Scout-17B-16E-Instruct:groq",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Describe the figure as precisely and completely as possible. Identify what the figure shows, all visible components, labels, symbols, arrows, axes, values, relationships, and layout. Preserve technical meaning. Do not guess hidden details.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{b64}"},
                        },
                    ],
                }
            ],
        )
        return out.choices[0].message.content

    # Open the PDF with both pypdf (page iterator) and fitz (Markdown extraction)
    reader = PdfReader(path)
    doc = fitz.open(path)

    # Collect extracted image filenames once for the whole document
    img_paths = os.listdir("extracted_images")

    for page_nr, page in enumerate(reader.pages):
        # Convert the page to Markdown; suppress header/footer noise
        page_text = pymupdf4llm.to_markdown(doc, pages=[page_nr], header=False, footer=False)

        page_txtimg_content = []
        for img in img_paths:
            # Image filenames follow the pattern img-<page_nr>.<ext>
            m = re.match(r"img-(\d+)", os.path.splitext(img)[0])
            if m and int(m.group(1)) == page_nr:
                # Disabled: uncomment the line below to enable VLM descriptions
                # page_txtimg_content = process_vlm(f"extracted_images/{img}")
                pass

        # Build a human-readable image annotation string, or leave empty
        image_desc = (
            f"Image description on page {page_nr}: {page_txtimg_content}"
            if page_txtimg_content != []
            else ""
        )

        # Split Markdown text into heading-aligned chunks
        section_title, chunks, chunk_ids = chunking_page(page_text)

        # Embed all chunks from this page in a single batch call
        embeddings = create_embedding(chunks)

        yield {
            "source_path": path,
            "page_nr": page_nr,
            "image": image_desc,
            "section_title": section_title,
            "chunk_id": chunk_ids,
            "chunk_content": chunks,
            "metadata": {"page_start": page_nr},  # 0-based; callers add 1 for display
            "embeddings": embeddings,
        }
