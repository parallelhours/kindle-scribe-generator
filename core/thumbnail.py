# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
"""Embed a rendered cover thumbnail into a PDF file."""

import zlib
from pathlib import Path


def embed_cover_thumbnail(pdf_path: str) -> None:
    """Render page 0 to a pixmap and embed it as the PDF /Thumb entry.

    Requires pymupdf >= 1.23.
    """
    import fitz  # PyMuPDF

    path = Path(pdf_path)
    tmp = path.with_name(path.stem + "_thumb_tmp.pdf")
    try:
        doc = fitz.open(str(path))
        page = doc[0]
        mat = fitz.Matrix(0.25, 0.25)
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
        w, h = pix.width, pix.height
        compressed = zlib.compress(bytes(pix.samples))
        thumb_xref = doc.get_new_xref()
        doc.update_object(
            thumb_xref,
            f"<</Type /XObject /Subtype /Image /Width {w} /Height {h}"
            f" /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /FlateDecode>>",
        )
        doc.update_stream(thumb_xref, compressed)
        doc.xref_set_key(page.xref, "Thumb", f"{thumb_xref} 0 R")
        doc.save(str(tmp))
        doc.close()
        tmp.replace(path)
    except Exception:
        if tmp.exists():
            tmp.unlink(missing_ok=True)
        raise
