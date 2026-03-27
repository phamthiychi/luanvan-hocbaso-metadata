import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    WORD2NUM = {
        "Một": 1,
        "Hai": 2,
        "Ba": 3,
        "Bốn": 4,
        "Năm": 5
    }
    WORD2SHORTCUT = {
        "Một": "Mo",
        "Hai": "Ha",
        "Ba": "Ba",
        "Bốn": "Bo",
        "Năm": "Na"
    }
    SUBJECT2SHORTCUT = {
        "Tiểu học": [
            {"code": "TV", "name": "Tiếng Việt"},
            {"code": "T", "name": "Toán"},
            {"code": "TNXH", "name": "Tự nhiên vầ xã hội"},
            {"code": "HDTN", "name": "Hoạt động trải nghiệm"},
            {"code": "DD", "name": "Đạo đức"},
            {"code": "CN", "name": "Công nghệ"},
            {"code": "KH", "name": "Khoa học"},
            {"code": "LSDL", "name": "Lịch sự & Địa lý"}
        ],
        "Âm nhạc": "AN",
        "Thể dục": "TD",
        "Tin học": "TH",
        "Tiếng Anh": "TA",
        "Mỹ thuật": "MT"
    }
    SHORTCUT2WORD = {v: k for k, v in WORD2SHORTCUT.items()}
    NUM2WORD = {v: k for k, v in WORD2NUM.items()}

settings = Settings()