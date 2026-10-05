# Thiết Kế & Đặc Tả REST API Backend
 
## Đặc Tả REST API
Hệ thống API được thiết kế theo kiến trúc chuẩn **RESTful** và có thể mô tả chi tiết bằng quy chuẩn **OpenAPI 3.0 / Swagger**.

### Danh sách các Endpoints chính:

| HTTP Method | Endpoint | Chức năng |
| :---: | :--- | :--- |
| `GET` | `/api/v1/drugs/search` | Tìm kiếm thuốc theo tên |
| `GET` | `/api/v1/drugs/{id}` | Xem thông tin chi tiết thuốc |
| `GET` | `/api/v1/drugs/{id}/similar` | Xem các thuốc có cùng hoạt chất |
| `POST` | `/api/v1/drugs/search-image` | Tra cứu thuốc bằng hình ảnh |
| `POST` | `/api/v1/prescriptions/analyze` | Phân tích hình ảnh đơn thuốc |
| `GET` | `/api/v1/history` | Xem lịch sử tra cứu của người dùng |
| `DELETE` | `/api/v1/history/{id}` | Xóa một bản ghi lịch sử tra cứu |

---

## Khởi Tạo Backend API
Backend của ứng dụng được xây dựng trên nền tảng **FastAPI (Python)** nhằm tối ưu hóa hiệu năng và tốc độ xử lý bất đồng bộ (Asynchronous).

### Cấu trúc thư mục dự án (`backend/`):

```text
backend/
├── main.py                     # Entry point chính của ứng dụng FastAPI
├── database.py                 # Cấu hình kết nối cơ sở dữ liệu (SQLAlchemy / Async Engine)
├── models/                     # Database Models (ORMs)
│   ├── drug.py                 # Lớp đại diện bảng Thuốc
│   ├── ingredient.py           # Lớp đại diện bảng Hoạt chất
│   ├── history.py              # Lớp đại diện bảng Lịch sử tra cứu
│   └── prescription.py         # Lớp đại diện bảng Đơn thuốc
├── schemas/                    # Pydantic Schemas (Data Validation & Serialization)
│   ├── drug_schema.py
│   ├── history_schema.py
│   └── prescription_schema.py
├── routers/                    # REST API Controllers / Endpoints Definition
│   ├── drugs.py                # Endpoints liên quan đến tra cứu thuốc
│   ├── prescriptions.py        # Endpoints liên quan đến xử lý đơn thuốc
│   └── history.py              # Endpoints quản lý lịch sử người dùng
└── services/                   # Business Logic & Third-party Integrations
    ├── drug_service.py         # Logic tìm kiếm, truy vấn dữ liệu thuốc
    ├── ocr_service.py          # Tích hợp mô hình AI/OCR bóc tách chữ từ ảnh
    └── prescription_service.py # Logic đối chiếu dữ liệu đơn thuốc với CSDL
