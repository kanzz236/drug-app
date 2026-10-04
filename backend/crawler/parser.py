from bs4 import BeautifulSoup, Tag
import re


# ============================================================
# CONFIG
# ============================================================

SECTION_NAMES = {
    "indication": [
        "chỉ định"
    ],

    "usage": [
        "liều lượng - cách dùng",
        "liều lượng và cách dùng",
        "liều lượng cách dùng",
        "liều dùng",
        "cách dùng"
    ],

    "contraindication": [
        "chống chỉ định"
    ],

    "side_effect": [
        "tác dụng phụ",
        "tác dụng không mong muốn"
    ],

    "interaction": [
        "tương tác thuốc",
        "tương tác"
    ],

    "warning": [
        "thận trọng lúc dùng",
        "thận trọng",
        "lưu ý"
    ],

    "storage": [
        "bảo quản"
    ]
}


HEADING_TAGS = [
    "h1",
    "h2",
    "h3",
    "h4",
    "h5"
]


# ============================================================
# LABEL
# ============================================================

LABEL_MAP = {
    "số đăng ký": "registration_number",
    "dạng bào chế": "dosage_form",
    "quy cách đóng gói": "packaging",
    "quy cách": "packaging"
}


# ============================================================
# CONTACT / WEBSITE GARBAGE
# ============================================================

CONTACT_WORDS = [
    "chọn hình thức liên hệ",
    "chọn cách bạn muốn được tư vấn",
    "gọi điện thoại",
    "chat zalo",
    "nhắn tin qua zalo",
    "chat facebook",
    "nhắn tin qua messenger",
    "hỗ trợ khách hàng",
    "tư vấn mua hàng",
    "gửi đơn thuốc",
    "hỗ trợ 24/7",
    "hotline"
]


GARBAGE_WORDS = [
    "lượt xem",
    "danh mục",
    "thông tin từ hoạt chất",
    "các thông tin dược lý",
    "thông tin chi tiết về",
    "công dụng"
]


# ============================================================
# TEXT
# ============================================================

def clean_text(text):
    if not text:
        return ""

    text = text.replace("\xa0", " ")
    text = text.replace("\u200b", "")
    text = text.replace("\ufeff", "")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize(text):
    text = clean_text(text).lower()

    text = (
        text
        .replace("–", "-")
        .replace("—", "-")
        .replace("−", "-")
    )

    return text


def text_of(tag):
    if not isinstance(tag, Tag):
        return ""

    return clean_text(
        tag.get_text(
            " ",
            strip=True
        )
    )


def heading_text(tag):
    return normalize(
        text_of(tag)
    )


def is_heading(tag):
    return (
        isinstance(tag, Tag)
        and tag.name in HEADING_TAGS
    )


def heading_level(tag):
    if not is_heading(tag):
        return 99

    return int(tag.name[1])


# ============================================================
# CUT TEXT
# ============================================================

def cut_at_words(text, words):

    if not text:
        return ""

    lower = normalize(text)

    positions = []

    for word in words:

        word = normalize(word)

        if not word:
            continue

        pos = lower.find(word)

        if pos >= 0:
            positions.append(pos)

    if positions:
        text = text[:min(positions)]

    return clean_text(text)


def remove_website_garbage(text):

    if not text:
        return ""

    text = cut_at_words(
        text,
        CONTACT_WORDS
    )

    return clean_text(text)


# ============================================================
# SECTION
# ============================================================

def match_section_type(text):

    text = normalize(text)

    for field, keywords in SECTION_NAMES.items():

        for keyword in keywords:

            keyword = normalize(keyword)

            if (
                text == keyword
                or text.startswith(
                    keyword + " "
                )
                or text.startswith(
                    keyword + ":"
                )
            ):
                return field

    return None


def is_section_heading(tag):

    return (
        is_heading(tag)
        and match_section_type(
            heading_text(tag)
        ) is not None
    )


def get_section_type(tag):

    if not is_heading(tag):
        return None

    return match_section_type(
        heading_text(tag)
    )


def find_section_heading(
    soup,
    keywords
):

    keywords = [
        normalize(x)
        for x in keywords
    ]

    for tag in soup.find_all(
        HEADING_TAGS
    ):

        text = heading_text(tag)

        for keyword in keywords:

            if (
                text == keyword
                or text.startswith(
                    keyword + " "
                )
                or text.startswith(
                    keyword + ":"
                )
            ):
                return tag

    return None


# ============================================================
# DUPLICATE
# ============================================================

def remove_duplicate_texts(texts):

    result = []
    seen = set()

    for text in texts:

        text = clean_text(text)

        if not text:
            continue

        key = normalize(text)

        if key in seen:
            continue

        seen.add(key)

        result.append(text)

    return result


def remove_repeated_blocks(text):

    """
    Xử lý trường hợp website lặp nguyên block:
        Công dụng ...
        Công dụng ...
        Công dụng ...

    Không xoá các câu giống nhau nhỏ bên trong.
    """

    text = clean_text(text)

    if not text:
        return ""

    parts = re.split(
        r"(?=Công dụng\s+)",
        text,
        flags=re.IGNORECASE
    )

    parts = [
        clean_text(x)
        for x in parts
        if clean_text(x)
    ]

    if len(parts) <= 1:
        return text

    result = []
    seen = set()

    for part in parts:

        key = normalize(part)

        if key in seen:
            continue

        seen.add(key)
        result.append(part)

    return " ".join(result)


# ============================================================
# CONTENT NODE
# ============================================================

def collect_element_text(element):

    if not isinstance(element, Tag):
        return ""

    if element.name in {
        "script",
        "style",
        "noscript",
        "svg"
    }:
        return ""

    return text_of(element)


# ============================================================
# SECTION EXTRACTION
# ============================================================

def extract_section_from_heading(
    heading
):

    if heading is None:
        return ""

    level = heading_level(
        heading
    )

    content = []

    # ========================================================
    # 1. SIBLING
    # ========================================================

    current = heading.find_next_sibling()

    while current:

        # Gặp heading cùng cấp / lớn hơn
        if is_heading(current):

            current_level = heading_level(
                current
            )

            if current_level <= level:
                break

            current = current.find_next_sibling()
            continue

        text = collect_element_text(
            current
        )

        if text:
            content.append(text)

        current = current.find_next_sibling()

    if content:

        content = remove_duplicate_texts(
            content
        )

        return clean_text(
            " ".join(content)
        )

    # ========================================================
    # 2. WRAPPER DIV
    # ========================================================

    content = []

    for element in heading.find_all_next():

        if element is heading:
            continue

        if is_heading(element):

            element_level = heading_level(
                element
            )

            if element_level <= level:
                break

            continue

        if element.name not in {
            "p",
            "li",
            "td",
            "th"
        }:
            continue

        text = collect_element_text(
            element
        )

        if text:
            content.append(text)

    content = remove_duplicate_texts(
        content
    )

    return clean_text(
        " ".join(content)
    )


# ============================================================
# CLEAN SECTION
# ============================================================

def clean_section(
    field,
    text
):

    if not text:
        return ""

    text = clean_text(text)

    # --------------------------------------------------------
    # Contact
    # --------------------------------------------------------

    text = cut_at_words(
        text,
        CONTACT_WORDS
    )

    # --------------------------------------------------------
    # Website SEO / navigation
    # --------------------------------------------------------

    if field != "storage":

        text = cut_at_words(
            text,
            [
                "thông tin từ hoạt chất",
                "các thông tin dược lý",
                "thông tin chi tiết về"
            ]
        )

    # --------------------------------------------------------
    # Không cho section này ăn sang section khác
    # --------------------------------------------------------

    stop_map = {

        "indication": [
            "chống chỉ định",
            "liều lượng - cách dùng",
            "liều lượng và cách dùng",
            "liều lượng cách dùng",
            "liều dùng",
            "cách dùng",
            "tác dụng phụ",
            "tác dụng không mong muốn",
            "tương tác thuốc",
            "tương tác",
            "thận trọng lúc dùng",
            "thận trọng",
            "lưu ý",
            "bảo quản"
        ],

        "usage": [
            "chống chỉ định",
            "tác dụng phụ",
            "tác dụng không mong muốn",
            "tương tác thuốc",
            "tương tác",
            "thận trọng lúc dùng",
            "thận trọng",
            "lưu ý",
            "bảo quản"
        ],

        "contraindication": [
            "liều lượng - cách dùng",
            "liều lượng và cách dùng",
            "liều lượng cách dùng",
            "liều dùng",
            "cách dùng",
            "tác dụng phụ",
            "tác dụng không mong muốn",
            "tương tác thuốc",
            "tương tác",
            "thận trọng lúc dùng",
            "thận trọng",
            "lưu ý",
            "bảo quản"
        ],

        "side_effect": [
            "tương tác thuốc",
            "tương tác",
            "thận trọng lúc dùng",
            "thận trọng",
            "lưu ý",
            "bảo quản"
        ],

        "interaction": [
            "tác dụng phụ",
            "tác dụng không mong muốn",
            "thận trọng lúc dùng",
            "thận trọng",
            "lưu ý",
            "bảo quản"
        ],

        "warning": [
            "bảo quản"
        ],

        "storage": []
    }

    text = cut_at_words(
        text,
        stop_map.get(
            field,
            []
        )
    )

    # --------------------------------------------------------
    # Storage đặc biệt
    # --------------------------------------------------------

    if field == "storage":

        text = cut_at_words(
            text,
            [
                "công dụng",
                "thông tin từ hoạt chất",
                "thông tin chi tiết về"
            ]
        )

    # --------------------------------------------------------
    # Remove repeated block
    # --------------------------------------------------------

    text = remove_repeated_blocks(
        text
    )

    return clean_text(text)


# ============================================================
# QUICK INFO
# ============================================================

def is_bad_value(value):

    if not value:
        return True

    value = normalize(value)

    bad_words = [
        "chọn hình thức liên hệ",
        "chọn cách bạn muốn được tư vấn",
        "gọi điện thoại",
        "chat zalo",
        "nhắn tin qua zalo",
        "chat facebook",
        "nhắn tin qua messenger",
        "lượt xem",
        "hotline",
        "hỗ trợ 24/7",
        "hỗ trợ khách hàng",
        "danh mục"
    ]

    return any(
        word in value
        for word in bad_words
    )


def clean_quick_value(
    value,
    field=None
):

    if not value:
        return ""

    value = clean_text(value)

    if normalize(value) == "null":
        return ""

    # ========================================================
    # CONTACT
    # ========================================================

    value = cut_at_words(
        value,
        CONTACT_WORDS
    )

    # ========================================================
    # REGISTRATION
    # ========================================================

    if field == "registration_number":

        # Ví dụ:
        # 890110006100 Dạng bào chế ...
        #
        # Chỉ lấy mã đầu tiên

        match = re.search(
            r"\b(?:VD|VN|GC|QLD|SĐK)?"
            r"[- ]?[A-Z0-9]{5,}"
            r"(?:-[A-Z0-9]+)*\b",
            value,
            re.IGNORECASE
        )

        if match:

            candidate = match.group(0)

            # Không lấy các từ vô nghĩa
            if normalize(candidate) not in {
                "dang",
                "bao",
                "che",
                "quy",
                "cach"
            }:
                return clean_text(
                    candidate
                )

        # fallback: cắt tại label kế tiếp
        value = re.split(
            r"\bDạng bào chế\b",
            value,
            flags=re.IGNORECASE
        )[0]

    # ========================================================
    # DOSAGE FORM
    # ========================================================

    if field == "dosage_form":

        value = re.split(
            r"\bLượt xem\b",
            value,
            flags=re.IGNORECASE
        )[0]

        value = re.split(
            r"\bDanh mục\b",
            value,
            flags=re.IGNORECASE
        )[0]

    # ========================================================
    # PACKAGING
    # ========================================================

    if field == "packaging":

        value = re.split(
            r"\bLượt xem\b",
            value,
            flags=re.IGNORECASE
        )[0]

        value = re.split(
            r"\bDanh mục\b",
            value,
            flags=re.IGNORECASE
        )[0]

    return clean_text(value)


def extract_quick_info(soup):

    data = {
        "strength": "",
        "dosage_form": "",
        "registration_number": "",
        "packaging": ""
    }

    # ========================================================
    # TABLE
    # ========================================================

    for row in soup.find_all("tr"):

        cells = row.find_all(
            ["th", "td"],
            recursive=False
        )

        if len(cells) < 2:
            continue

        for i in range(
            len(cells) - 1
        ):

            label = normalize(
                text_of(cells[i])
            )

            for key, field in LABEL_MAP.items():

                if label != normalize(key):
                    continue

                value = clean_quick_value(
                    text_of(
                        cells[i + 1]
                    ),
                    field
                )

                if (
                    value
                    and not is_bad_value(value)
                    and not data[field]
                ):
                    data[field] = value

    # ========================================================
    # LABEL + SIBLING
    # ========================================================

    for label in soup.find_all(
        [
            "td",
            "th",
            "span",
            "strong",
            "b",
            "div"
        ]
    ):

        label_text = normalize(
            text_of(label)
        )

        field = None

        for key, mapped in LABEL_MAP.items():

            if label_text == normalize(key):

                field = mapped
                break

        if field is None:
            continue

        if data[field]:
            continue

        sibling = label.find_next_sibling()

        if sibling is None:
            continue

        value = clean_quick_value(
            text_of(sibling),
            field
        )

        if (
            value
            and not is_bad_value(value)
        ):
            data[field] = value

    # ========================================================
    # REGEX FALLBACK
    # ========================================================

    page_text = soup.get_text(
        "\n",
        strip=True
    )

    # --------------------------------------------------------
    # Registration
    # --------------------------------------------------------

    if not data["registration_number"]:

        patterns = [
            r"Số\s+đăng\s+ký\s*[:\-]?\s*"
            r"([A-Za-z0-9][A-Za-z0-9\- ]{4,})",

            r"SĐK\s*[:\-]?\s*"
            r"([A-Za-z0-9][A-Za-z0-9\- ]{4,})"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                page_text,
                re.IGNORECASE
            )

            if not match:
                continue

            value = clean_quick_value(
                match.group(1),
                "registration_number"
            )

            if value:
                data[
                    "registration_number"
                ] = value

                break

    # --------------------------------------------------------
    # Dosage form
    # --------------------------------------------------------

    if not data["dosage_form"]:

        match = re.search(
            r"Dạng\s+bào\s+chế\s*[:\-]?\s*"
            r"([^\n]+)",
            page_text,
            re.IGNORECASE
        )

        if match:

            value = clean_quick_value(
                match.group(1),
                "dosage_form"
            )

            if value:
                data[
                    "dosage_form"
                ] = value

    # --------------------------------------------------------
    # Packaging
    # --------------------------------------------------------

    if not data["packaging"]:

        patterns = [
            r"Quy\s+cách\s+đóng\s+gói\s*"
            r"[:\-]?\s*([^\n]+)",

            r"Quy\s+cách\s*"
            r"[:\-]?\s*([^\n]+)"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                page_text,
                re.IGNORECASE
            )

            if not match:
                continue

            value = clean_quick_value(
                match.group(1),
                "packaging"
            )

            if value:
                data[
                    "packaging"
                ] = value

                break

    return data


# ============================================================
# STRENGTH EXTRACTION
# ============================================================

def extract_strength_from_name(
    name
):

    if not name:
        return ""

    name = clean_text(name)

    patterns = [

        # 25mg
        r"\b\d+(?:[.,]\d+)?\s*mg\b",

        # 12,5mg/ml
        r"\b\d+(?:[.,]\d+)?\s*mg\s*/\s*ml\b",

        # 500mg/5ml
        r"\b\d+(?:[.,]\d+)?\s*mg\s*/\s*\d+(?:[.,]\d+)?\s*ml\b",

        # 20 mg
        r"\b\d+(?:[.,]\d+)?\s*mg\b"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            name,
            re.IGNORECASE
        )

        if match:
            return clean_text(
                match.group(0)
            )

    return ""


def clean_strength(
    strength
):

    if not strength:
        return ""

    strength = clean_text(
        strength
    )

    if normalize(strength) == "null":
        return ""

    return strength


# ============================================================
# INGREDIENT TABLE
# ============================================================

def find_ingredient_table(soup):

    # ========================================================
    # Theo heading
    # ========================================================

    for heading in soup.find_all(
        HEADING_TAGS
    ):

        text = heading_text(
            heading
        )

        if (
            "thành phần hoạt chất"
            in text
            or text == "thành phần"
            or "hoạt chất" in text
        ):

            table = heading.find_next(
                "table"
            )

            if table:
                return table

    # ========================================================
    # Theo header
    # ========================================================

    for table in soup.find_all(
        "table"
    ):

        text = normalize(
            table.get_text(
                " ",
                strip=True
            )
        )

        if (
            "tên hoạt chất" in text
            and "hàm lượng" in text
        ):
            return table

        if (
            "hoạt chất" in text
            and (
                "hàm lượng" in text
                or "hàm" in text
            )
        ):
            return table

    return None


def clean_ingredient_name(
    name
):

    name = clean_text(
        name
    )

    name = re.sub(
        r"\s+chính$",
        "",
        name,
        flags=re.IGNORECASE
    )

    return name


def extract_ingredients(
    soup
):

    table = find_ingredient_table(
        soup
    )

    if table is None:
        return []

    ingredients = []

    for row in table.find_all(
        "tr"
    ):

        cells = row.find_all(
            ["td", "th"],
            recursive=False
        )

        if len(cells) < 2:
            continue

        values = [
            clean_text(
                cell.get_text(
                    " ",
                    strip=True
                )
            )
            for cell in cells
        ]

        first = normalize(
            values[0]
        )

        # Header
        if (
            "tên hoạt chất" in first
            or first == "hoạt chất"
            or first == "thành phần"
        ):
            continue

        name = clean_ingredient_name(
            values[0]
        )

        strength = clean_strength(
            values[1]
        )

        if not name:
            continue

        if normalize(name) == "null":
            continue

        # Không lấy dòng không phải hoạt chất
        if normalize(name) in {
            "tổng cộng",
            "total",
            "stt",
            "số thứ tự"
        }:
            continue

        ingredients.append({

            "name": name,

            "strength": strength,

            "effect": "",

            "indication": "",

            "dosage": "",

            "contraindication": "",

            "interaction": "",

            "side_effect": "",

            "warning": ""
        })

    # ========================================================
    # Remove duplicate ingredient
    # ========================================================

    result = []
    seen = set()

    for ingredient in ingredients:

        key = normalize(
            ingredient["name"]
        )

        if key in seen:
            continue

        seen.add(key)
        result.append(
            ingredient
        )

    return result


# ============================================================
# INGREDIENT HEADING
# ============================================================

def ingredient_field_from_heading(
    heading,
    ingredient_name
):

    text = heading_text(
        heading
    )

    ingredient = normalize(
        ingredient_name
    )

    if not ingredient:
        return None

    if ingredient not in text:
        return None

    # Quan trọng:
    # chống chỉ định trước chỉ định

    if "chống chỉ định" in text:
        return "contraindication"

    if (
        "tác dụng phụ" in text
        or "tác dụng không mong muốn"
        in text
    ):
        return "side_effect"

    if "tương tác" in text:
        return "interaction"

    if (
        "liều dùng" in text
        or "liều lượng" in text
        or "cách dùng" in text
    ):
        return "dosage"

    if (
        "thận trọng" in text
        or "lưu ý" in text
    ):
        return "warning"

    if "chỉ định" in text:
        return "indication"

    return None


# ============================================================
# INGREDIENT SECTION
# ============================================================

def extract_ingredient_sections(
    soup,
    ingredient_name
):

    result = {

        "effect": "",

        "indication": "",

        "dosage": "",

        "contraindication": "",

        "interaction": "",

        "side_effect": "",

        "warning": ""
    }

    headings = soup.find_all(
        HEADING_TAGS
    )

    matched = []

    for heading in headings:

        field = ingredient_field_from_heading(
            heading,
            ingredient_name
        )

        if field:

            matched.append(
                (
                    heading,
                    field
                )
            )

    for heading, field in matched:

        value = extract_section_from_heading(
            heading
        )

        value = clean_section(
            field,
            value
        )

        if value:

            # Nếu có nhiều heading cùng field
            # thì nối lại thay vì ghi đè

            if result[field]:

                if normalize(value) not in normalize(
                    result[field]
                ):
                    result[field] += " " + value

            else:
                result[field] = value

    return result


# ============================================================
# FILL INGREDIENT
# ============================================================

def fill_ingredient_from_drug(
    ingredient,
    drug
):

    mapping = {

        "indication":
            "indication",

        "dosage":
            "usage",

        "contraindication":
            "contraindication",

        "interaction":
            "interaction",

        "side_effect":
            "side_effect",

        "warning":
            "warning"
    }

    for ingredient_field, drug_field in mapping.items():

        if ingredient.get(
            ingredient_field,
            ""
        ):
            continue

        value = drug.get(
            drug_field,
            ""
        )

        if value:

            ingredient[
                ingredient_field
            ] = clean_text(value)

    return ingredient


# ============================================================
# DRUG FIELD CLEAN
# ============================================================

def clean_drug_field(
    field,
    value
):

    if not value:
        return ""

    value = clean_text(
        value
    )

    if normalize(value) == "null":
        return ""

    value = cut_at_words(
        value,
        CONTACT_WORDS
    )

    # --------------------------------------------------------
    # QUICK INFO
    # --------------------------------------------------------

    if field == "registration_number":

        value = clean_quick_value(
            value,
            "registration_number"
        )

    elif field == "dosage_form":

        value = clean_quick_value(
            value,
            "dosage_form"
        )

    elif field == "packaging":

        value = clean_quick_value(
            value,
            "packaging"
        )

    # --------------------------------------------------------
    # STORAGE
    # --------------------------------------------------------

    if field == "storage":

        value = cut_at_words(
            value,
            [
                "công dụng",
                "thông tin từ hoạt chất",
                "thông tin chi tiết về"
            ]
        )

    return clean_text(
        value
    )


# ============================================================
# PARSE
# ============================================================

def parse_drug_page(
    html
):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    # ========================================================
    # REMOVE NON-CONTENT
    # ========================================================

    for tag in soup.find_all(
        [
            "script",
            "style",
            "noscript",
            "svg"
        ]
    ):
        tag.decompose()

    # ========================================================
    # NAME
    # ========================================================

    title = soup.find("h1")

    name = (
        text_of(title)
        if title
        else ""
    )

    if not name:

        title_tag = soup.find(
            "title"
        )

        if title_tag:

            name = text_of(
                title_tag
            )

            # Một số trang:
            # "Tên thuốc - Nhà thuốc..."

            name = re.split(
                r"\s*[-|]\s*",
                name
            )[0]

    # ========================================================
    # DRUG
    # ========================================================

    drug = {

        "name": name,

        "strength": "",

        "dosage_form": "",

        "registration_number": "",

        "packaging": "",

        "indication": "",

        "usage": "",

        "contraindication": "",

        "side_effect": "",

        "interaction": "",

        "warning": "",

        "storage": ""
    }

    # ========================================================
    # QUICK INFO
    # ========================================================

    quick_info = extract_quick_info(
        soup
    )

    for key, value in quick_info.items():

        value = clean_drug_field(
            key,
            value
        )

        if value:
            drug[key] = value

    # ========================================================
    # STRENGTH FALLBACK
    # ========================================================

    if not drug["strength"]:

        drug["strength"] = (
            extract_strength_from_name(
                drug["name"]
            )
        )

    # ========================================================
    # MAIN SECTIONS
    # ========================================================

    for field, keywords in SECTION_NAMES.items():

        heading = find_section_heading(
            soup,
            keywords
        )

        if heading is None:
            continue

        value = extract_section_from_heading(
            heading
        )

        value = clean_section(
            field,
            value
        )

        value = clean_drug_field(
            field,
            value
        )

        if value:

            drug[field] = value

    # ========================================================
    # INGREDIENTS
    # ========================================================

    ingredients = extract_ingredients(
        soup
    )

    # ========================================================
    # STRENGTH FROM INGREDIENT
    # ========================================================

    if len(ingredients) == 1:

        ingredient_strength = clean_strength(
            ingredients[0].get(
                "strength",
                ""
            )
        )

        if ingredient_strength:

            drug["strength"] = (
                ingredient_strength
            )

    # ========================================================
    # STRENGTH FROM NAME
    # ========================================================

    if not drug["strength"]:

        drug["strength"] = (
            extract_strength_from_name(
                drug["name"]
            )
        )

    # ========================================================
    # INGREDIENT SECTIONS
    # ========================================================

    for ingredient in ingredients:

        sections = extract_ingredient_sections(
            soup,
            ingredient["name"]
        )

        for key, value in sections.items():

            if value:

                ingredient[key] = value

        # Fallback:
        # ingredient dùng nội dung thuốc
        fill_ingredient_from_drug(
            ingredient,
            drug
        )

    # ========================================================
    # FINAL CLEAN
    # ========================================================

    for field in [
        "strength",
        "dosage_form",
        "registration_number",
        "packaging",
        "indication",
        "usage",
        "contraindication",
        "side_effect",
        "interaction",
        "warning",
        "storage"
    ]:

        drug[field] = clean_drug_field(
            field,
            drug[field]
        )

    # ========================================================
    # OUTPUT
    # ========================================================

    return {

        "drug": drug,

        "ingredients": ingredients
    }