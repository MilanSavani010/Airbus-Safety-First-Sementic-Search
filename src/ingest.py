# src/pdf_ingest.py
from pathlib import Path
import sqlite3
from pdf2image import convert_from_path
from PIL import Image
import json

from src.config import RAW_DIR, DB_PATH, POPPLER_BIN


