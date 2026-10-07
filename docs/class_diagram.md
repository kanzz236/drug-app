# Biểu Đồ Lớp (Class Diagram)

Tài liệu mô tả chi tiết danh sách các Lớp (Classes), thuộc tính (Attributes), phương thức (Methods) và vai trò của từng thành phần trong hệ thống.

---

## Danh Sách Các Lớp Chi Tiết

### User (Người dùng)
* **Thuộc tính (Attributes):**
  * `- user_id: INT`
  * `- username: VARCHAR`
  * `- email: VARCHAR`
  * `- password_hash: VARCHAR`
  * `- created_at: DATETIME`
* **Phương thức (Methods):**
  * `+ register(): Boolean`
  * `+ login(): String`
  * `+ updateProfile(): Boolean`
* **Vai trò:** Quản lý thông tin tài khoản người dùng, xử lý các thao tác đăng ký, đăng nhập và cập nhật thông tin cá nhân.

---

### Drug (Thuốc)
* **Thuộc tính (Attributes):**
  * `- drug_id: INT`
  * `- drug_name: VARCHAR`
  * `- brand_name: VARCHAR`
  * `- manufacturer: VARCHAR`
  * `- dosage_form: VARCHAR`
  * `- usage_instructions: TEXT`
  * `- contraindications: TEXT`
* **Phương thức (Methods):**
  * `+ getDrugDetails(): Drug`
  * `+ searchByName(name: String): List<Drug>`
* **Vai trò:** Đại diện cho danh mục các loại thuốc trong hệ thống; cung cấp thông tin chi tiết về tên, nhà sản xuất, dạng bào chế, hướng dẫn sử dụng và chống chỉ định.

---

### ActiveIngredient (Hoạt chất)
* **Thuộc tính (Attributes):**
  * `- ingredient_id: INT`
  * `- ingredient_name: VARCHAR`
  * `- description: TEXT`
  * `- side_effects: TEXT`
* **Phương thức (Methods):**
  * `+ getIngredientInfo(): ActiveIngredient`
* **Vai trò:** Quản lý thông tin các hoạt chất hóa học cấu thành nên thuốc, bao gồm mô tả chi tiết và các tác dụng phụ đi kèm.

---

### Prescription (Đơn thuốc)
* **Thuộc tính (Attributes):**
  * `- prescription_id: INT`
  * `- user_id: INT`
  * `- image_url: VARCHAR`
  * `- status: VARCHAR`
  * `- created_at: DATETIME`
* **Phương thức (Methods):**
  * `+ uploadImage(): String`
  * `+ processOCR(): String`
  * `+ parsePrescription(): List<Drug>`
* **Vai trò:** Đại diện cho lượt tải lên và xử lý hình ảnh đơn thuốc của người dùng để phân tích OCR trích xuất thông tin.

---

### SearchHistory (Lịch sử tìm kiếm - Bảng trung gian)
* **Thuộc tính (Attributes):**
  * `- history_id: INT`
  * `- user_id: INT`
  * `- drug_id: INT`
  * `- search_query: VARCHAR`
  * `- searched_at: DATETIME`
* **Phương thức (Methods):**
  * `+ saveHistory(): Boolean`
  * `+ getHistoryByUser(user_id: INT): List<SearchHistory>`
* **Vai trò:** Lưu vết thông tin tra cứu của người dùng (từ khóa tìm kiếm, loại thuốc được truy cập, thời gian truy cập).

---

### DrugActiveIngredient (Liên kết Thuốc - Hoạt chất)
* **Thuộc tính (Attributes):**
  * `- drug_id: INT`
  * `- ingredient_id: INT`
  * `- concentration: VARCHAR`
* **Phương thức (Methods):**
  * `+ getConcentration(): String`
* **Vai trò:** Giải quyết quan hệ N-N (nhiều - nhiều) giữa **Thuốc** và **Hoạt chất**, lưu trữ nồng độ/hàm lượng (`concentration`) cụ thể của từng hoạt chất trong loại thuốc đó.

---

### PrescriptionDrug (Liên kết Đơn thuốc - Thuốc)
* **Thuộc tính (Attributes):**
  * `- prescription_id: INT`
  * `- drug_id: INT`
  * `- quantity: INT`
  * `- dosage: VARCHAR`
  * `- confidence_score: FLOAT`
* **Phương thức (Methods):**
  * `+ verifyDrug(): Boolean`
* **Vai trò:** Giải quyết quan hệ N-N (nhiều - nhiều) giữa **Đơn thuốc** và **Thuốc**, lưu thông tin số lượng (`quantity`), liều dùng (`dosage`) và độ tin cậy kết quả nhận diện OCR (`confidence_score`).

---

## Bảng Tóm Tắt Mối Quan Hệ Giữa Các Lớp

| Lớp Nguồn | Lớp Đích | Tỷ lệ (Multiplicity) | Lớp Trung Gian / Giải Thích |
| :--- | :--- | :---: | :--- |
| **User** | **Prescription** | `1 - N` | Một người dùng có thể tải lên nhiều đơn thuốc. |
| **User** | **Drug** | `N - N` | Liên kết qua `SearchHistory` để lưu lịch sử tra cứu. |
| **Drug** | **ActiveIngredient** | `N - N` | Liên kết qua `DrugActiveIngredient` (chứa thuộc tính `concentration`). |
| **Prescription** | **Drug** | `N - N` | Liên kết qua `PrescriptionDrug` (chứa `quantity`, `dosage`, `confidence_score`). |

---

## Sơ Đồ Lớp (Mermaid Diagram)

```mermaid
classDiagram
    class User {
        -user_id: INT
        -username: VARCHAR
        -email: VARCHAR
        -password_hash: VARCHAR
        -created_at: DATETIME
        +register() Boolean
        +login() String
        +updateProfile() Boolean
    }

    class Drug {
        -drug_id: INT
        -drug_name: VARCHAR
        -brand_name: VARCHAR
        -manufacturer: VARCHAR
        -dosage_form: VARCHAR
        -usage_instructions: TEXT
        -contraindications: TEXT
        +getDrugDetails() Drug
        +searchByName(name: String) List~Drug~
    }

    class ActiveIngredient {
        -ingredient_id: INT
        -ingredient_name: VARCHAR
        -description: TEXT
        -side_effects: TEXT
        +getIngredientInfo() ActiveIngredient
    }

    class Prescription {
        -prescription_id: INT
        -user_id: INT
        -image_url: VARCHAR
        -status: VARCHAR
        -created_at: DATETIME
        +uploadImage() String
        +processOCR() String
        +parsePrescription() List~Drug~
    }

    class SearchHistory {
        -history_id: INT
        -user_id: INT
        -drug_id: INT
        -search_query: VARCHAR
        -searched_at: DATETIME
        +saveHistory() Boolean
        +getHistoryByUser(user_id: INT) List~SearchHistory~
    }

    class DrugActiveIngredient {
        -drug_id: INT
        -ingredient_id: INT
        -concentration: VARCHAR
        +getConcentration() String
    }

    class PrescriptionDrug {
        -prescription_id: INT
        -drug_id: INT
        -quantity: INT
        -dosage: VARCHAR
        -confidence_score: FLOAT
        +verifyDrug() Boolean
    }

    User "1" -- "*" Prescription : Uploads
    User "1" -- "*" SearchHistory : Generates
    Drug "1" -- "*" SearchHistory : Recorded_In
    Drug "1" -- "*" DrugActiveIngredient : Has
    ActiveIngredient "1" -- "*" DrugActiveIngredient : Belongs_To
    Prescription "1" -- "*" PrescriptionDrug : Contains
    Drug "1" -- "*" PrescriptionDrug : Mapped_In
