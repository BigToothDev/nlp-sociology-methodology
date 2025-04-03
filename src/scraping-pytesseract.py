#Image source https://x.com/Bykvu/status/1905901772465377428
from dotenv import load_dotenv
from pathlib import Path
import os
import pytesseract
from pytesseract import image_to_string
from PIL import Image

load_dotenv()
base_path = Path(__file__).parent.parent
tesseract_cmd = os.environ.get("tesseract_path")
img_path = os.environ.get("img_path")

if not tesseract_cmd:
    raise ValueError("Tesseract path not found")
if (os.name) == "nt":
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

img_content = image_to_string(Image.open(base_path / img_path), lang="ukr")

with open (base_path / 'data/pytesseract_data.txt', 'w', encoding='utf-8') as file:
    file.write(img_content)