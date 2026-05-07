# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
# Kindle Scribe native resolution: 1404 × 1872 px at 300 DPI
PAGE_WIDTH_PX  = 1404
PAGE_HEIGHT_PX = 1872
DPI = 300

PX_TO_PT = 72 / DPI   # 0.24 pt per pixel
PAGE_W = PAGE_WIDTH_PX  * PX_TO_PT   # 336.96 pt
PAGE_H = PAGE_HEIGHT_PX * PX_TO_PT   # 449.28 pt
MARGIN = 6.0  # pt, all sides
