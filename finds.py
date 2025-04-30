import pymupdf
import fitz # 导入 PyMuPDF 库
import os
import unicodedata
import shutil
import pytesseract
import re
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
try:
    from PIL import Image
except ImportError:
    import Image




