import base64
import os
import re

import fitz
import pymupdf4llm
import pytesseract
from PIL import Image
from pypdf import PdfReader

from .chunking import chunking_page
from .config import client


def process_pdfs(path: str):
    """
    process pdfs for LLM
    """
    def process_ocr_imgs(path,page_nr):
        doc = fitz.open(path)
        pix = doc[page_nr].get_pixmap(matrix=fitz.Matrix(2,2))
        pix.save("temp_page.png")
        page_to_str = pytesseract.image_to_string(Image.open("temp_page.png"))
        return page_to_str
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
    content = {
        "source_path": path,
        "images": [],
        "chunk_id": [],
        "chunk_content": [],
        "page_nr": 0,
        "section_title": [],
        "metadata": {"page_start": 0},
        "embeddings": []
    }
    reader = PdfReader(path)
    doc = fitz.open(path)
    img_paths = os.listdir("extracted_images")
    for page_nr, page in enumerate(reader.pages):
        page_text = pymupdf4llm.to_markdown(doc, pages=[page_nr], header=False, footer=False)
        page_txtimg_content = ""
        for img in img_paths:
            m = re.match(r"img-(\d+)", os.path.splitext(img)[0])
            if m and int(m.group(1)) == page_nr:
                #page_txtimg_content = process_vlm(f"extracted_images/{img}")
                pass
        #page_txt_content = page.extract_text()
        content["images"].append(f"Image description on page {page_nr}: {page_txtimg_content}" if page_txtimg_content!="" else "")
        content["section_title"], content["chunk_content"], content["chunk_id"] = chunking_page(page_text)
        content["metadata"]["page_start"] = page_nr
        content["embeddings"].append("") #TODO: add embedding for the chunk content here, so we have all data for one chunk ready at the end of processing one page, and can insert it into db right after processing one page, instead of waiting for the whole document to be processed and then inserting all chunks at once.
#TODO: return the content of one page and iterate somewhere else over all pages,
# so we insert the chunks and all of its data into db right after processing one page, instead of waiting for the whole document to be processed and then inserting all chunks at once.
# This way we can also handle bigger documents that might cause memory issues if we process the whole document at once and keep all chunks in memory until the end.
    return content
