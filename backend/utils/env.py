import os
from dotenv import load_dotenv

load_dotenv()

def check_environment():
    required_vars = ["GEMINI_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"Thiếu các biến môi trường bắt buộc: {', ' .join(missing)}")
    return True