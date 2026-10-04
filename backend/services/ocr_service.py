import os
import requests
import base64
import time
import re
from typing import List
from sqlalchemy import text

def get_available_gemini_models(api_key: str) -> List[str]:
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        resp = requests.get(list_url, timeout=10)
        if resp.status_code == 200:
            models_data = resp.json().get("models", [])
            valid_models = []
            for m in models_data:
                methods = m.get("supportedGenerationMethods", [])
                if "generateContent" in methods:
                    name = m.get("name", "").replace("models/", "")
                    valid_models.append(name)
            valid_models.sort(key=lambda x: ("flash" not in x, x), reverse=False)
            if valid_models:
                return valid_models
    except Exception:
        pass
    
    # Fallback chuẩn với các model hiện hành để tránh lỗi 404 Not Found
    return [
        "gemini-3.8-flash",
        "gemini-2.5-flash",
        "gemini-1.5-flash"
    ]

async def process_prescription_image(image_path: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Chưa cấu hình GEMINI_API_KEY trong file .env")
    
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    
    ext = image_path.split(".")[-1].lower()
    mime_type = "image/jpeg"
    if ext == "png":
        mime_type = "image/png"
    elif ext == "webp":
        mime_type = "image/webp"

    models_to_try = get_available_gemini_models(api_key)
    prescription_text = ""
    last_error = ""

    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Bạn là một trợ lý y tế thông minh. Hãy đọc ảnh đơn thuốc này và trích xuất danh sách các loại thuốc, hàm lượng, số lượng và cách dùng."},
                    {"inline_data": {"mime_type": mime_type, "data": image_base64}}
                ]
            }]
        }
        
        try:
            response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=30)
            try:
                res_json = response.json()
            except ValueError:
                res_json = {}

            if response.status_code == 200:
                candidates = res_json.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        prescription_text = parts[0].get("text", "").strip()
                        if prescription_text:
                            break

            last_error = res_json.get("error", {}).get("message", response.text or f"HTTP {response.status_code}")
            if response.status_code in [404, 429, 503] or "high demand" in last_error.lower() or "not found" in last_error.lower():
                continue
        except requests.RequestException as e:
            last_error = str(e)
            continue

    if not prescription_text:
        raise Exception(f"Lỗi gọi Gemini API xử lý OCR đơn thuốc: {last_error}")
    
    return prescription_text


async def identify_medicine_image_logic(image_bytes: bytes, content_type: str, db) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Chưa cấu hình GEMINI_API_KEY trong file .env!")

    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    payload = {
        "contents": [{
            "parts": [
                {"text": "Đây là ảnh vỏ hộp hoặc vỉ thuốc. Hãy đọc và trích xuất duy nhất TÊN THUỐC chính và HÀM LƯỢNG (ví dụ: Hapacol 500, Panadol Extra, Augmentin 625mg). Chỉ trả về tên thuốc, không trả về văn bản thừa."},
                {"inline_data": {"mime_type": content_type, "data": base64_image}}
            ]
        }]
    }

    models_to_try = get_available_gemini_models(api_key)
    detected_name = ""
    last_error = ""

    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        for attempt in range(2):
            try:
                response = requests.post(url, json=payload, timeout=60)
                try:
                    res_json = response.json()
                except ValueError:
                    res_json = {}

                if response.status_code == 200:
                    candidates = res_json.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            detected_name = parts[0].get("text", "").strip()
                            if detected_name:
                                break

                last_error = res_json.get("error", {}).get("message", response.text or f"HTTP {response.status_code}")
                if response.status_code in [404, 429, 503] or "high demand" in last_error.lower() or "not found" in last_error.lower():
                    break
                time.sleep(1)
            except requests.RequestException as e:
                last_error = str(e)
                time.sleep(1)

        if detected_name:
            break

    if not detected_name:
        raise Exception(f"Gemini API không nhận diện được vỏ hộp thuốc: {last_error}")

    all_medicines = db.execute(text("""
        SELECT m.id, m.name, m.sdk_code, m.strength, m.dosage_form, m.manufacturer, 
               m.indication, m.contraindication, m.side_effect, m.warning,
               a.name as active_ingredient
        FROM medicines m
        LEFT JOIN active_ingredients a ON m.active_ingredient_id = a.id
    """)).mappings().all()
    
    matched_medicine = None
    for med in all_medicines:
        if re.search(r'\b' + re.escape(med['name']) + r'\b', detected_name, re.IGNORECASE) or \
           re.search(r'\b' + re.escape(detected_name) + r'\b', med['name'], re.IGNORECASE):
            matched_medicine = dict(med)
            break

    return {
        "status": "success",
        "detected_medicine_name_from_image": detected_name,
        "is_found_in_database": matched_medicine is not None,
        "medicine_details": matched_medicine
    }