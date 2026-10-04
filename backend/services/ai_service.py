import os
from google import genai

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Chưa cấu hình GEMINI_API_KEY trong file .env")
    return genai.Client(api_key=api_key)

async def analyze_symptoms_with_ai(symptom_description: str) -> str:
    """
    Dùng Gemini để phân tích mô tả triệu chứng bệnh và đưa ra gợi ý sơ bộ
    """
    client = get_gemini_client()
    
    prompt = (
        "Bạn là một trợ lý y tế. Người dùng đang gặp các triệu chứng sau: "
        f"'{symptom_description}'. Hãy phân tích các nguyên nhân tiềm năng "
        "và đưa ra lời khuyên y tế chung (nhớ đính kèm khuyến cáo đi khám bác sĩ)."
    )
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    return response.text