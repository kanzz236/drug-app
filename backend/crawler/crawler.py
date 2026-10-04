import requests
import json
import os
import time

from parser import parse_drug_page


# ============================================================
# DANH SÁCH URL TEST
# ============================================================

URLS = [
    "https://thuocbietduoc.com.vn/thuoc-2696/sanlitor-20.aspx",
    "https://thuocbietduoc.com.vn/thuoc-10229/daiticol.aspx",
    "https://thuocbietduoc.com.vn/thuoc-10329/daiticol.aspx",
    "https://thuocbietduoc.com.vn/thuoc-10129/daiticol.aspx",
    "https://thuocbietduoc.com.vn/thuoc-55952/domela.aspx",
]


# ============================================================
# CONFIG
# ============================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/153.0.0.0 "
        "Safari/537.36"
    )
}


OUTPUT_FILE = "data/raw/drugs.json"


# ============================================================
# LẤY HTML
# ============================================================

def fetch_page(url):

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    # ThuocBietDuoc là tiếng Việt
    response.encoding = response.apparent_encoding

    return response.text


# ============================================================
# MAIN
# ============================================================

def main():

    # Tạo thư mục output nếu chưa tồn tại
    os.makedirs(
        "data/raw",
        exist_ok=True
    )

    results = []

    for url in URLS:

        print(f"Đang lấy: {url}")

        try:

            html = fetch_page(url)

            data = parse_drug_page(html)

            results.append(data)

            print(
                f"OK: {data['drug']['name']}"
            )

            print(
                f"   Hoạt chất: {len(data['ingredients'])}"
            )

            for ingredient in data["ingredients"]:

                print(
                    f"   - {ingredient['name']} "
                    f"({ingredient['strength']})"
                )

        except Exception as e:

            print(
                f"ERROR: {e}"
            )

        # Nghỉ giữa các request
        time.sleep(1)

    # ========================================================
    # GHI JSON
    # ========================================================

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            results,
            f,
            ensure_ascii=False,
            indent=4
        )

    print()
    print(
        f"Đã lưu {len(results)} thuốc."
    )

    print(
        f"File: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
