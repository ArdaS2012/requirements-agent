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
    """
    process pdfs for LLM
    """
    def process_vlm(path):
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()

        img = f"data:image/png;base64,{b64}"
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
        content = out.choices[0].message.content
        return content
    reader = PdfReader(path)
    doc = fitz.open(path)
    img_paths = os.listdir("extracted_images")
    for page_nr, page in enumerate(reader.pages):
        page_text = pymupdf4llm.to_markdown(doc, pages=[page_nr], header=False, footer=False)
        page_txtimg_content = []
        for img in img_paths:
            m = re.match(r"img-(\d+)", os.path.splitext(img)[0])
            if m and int(m.group(1)) == page_nr:
                #page_txtimg_content = process_vlm(f"extracted_images/{img}")
                pass
        #page_txt_content = page.extract_text()
        image_desc = f"Image description on page {page_nr}: {page_txtimg_content}" if page_txtimg_content != [] else ""
        section_title, chunks, chunk_ids = chunking_page(page_text)
        embeddings = create_embedding(chunks)
        yield {
            "source_path": path,
            "page_nr": page_nr,
            "image": image_desc,
            "section_title": section_title,
            "chunk_id": chunk_ids,
            "chunk_content": chunks,
            "metadata": {"page_start": page_nr},
            "embeddings": embeddings,
        }
