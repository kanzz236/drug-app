# Yêu Cầu Chức Năng (Functional Requirements - FR)

### Tổng Quan Nhóm Yêu Cầu Chức Năng

| Nhóm | Số lượng FR | Nội dung chính |
| :--- | :---: | :--- |
| **A – Tra cứu thuốc** | 4 | Tìm kiếm thuốc, xem thông tin chi tiết, tìm bằng hình ảnh, hiển thị thuốc cùng hoạt chất |
| **B – Phân tích đơn thuốc** | 3 | Tải ảnh đơn thuốc, nhận diện và trích xuất thông tin, đối chiếu CSDL |
| **C – Lịch sử tra cứu** | 2 | Lưu và xem lại lịch sử tra cứu, xóa lịch sử |
| **D – Xử lý lỗi** | 2 | Kiểm tra dữ liệu/hình ảnh, thông báo lỗi và không tìm thấy thuốc |

---

### Chi Tiết Yêu Cầu Chức Năng

#### A – Tra cứu thuốc

| Mã | Yêu cầu chức năng |
| :---: | :--- |
| **FR-01** | Người dùng có thể tìm kiếm thuốc theo tên. |
| **FR-02** | Hệ thống hiển thị thông tin chi tiết của thuốc. |
| **FR-03** | Hệ thống hiển thị các thuốc có cùng hoạt chất. |
| **FR-04** | Người dùng có thể tìm kiếm thuốc bằng hình ảnh thông qua OCR. |

#### B – Phân tích đơn thuốc

| Mã | Yêu cầu chức năng |
| :---: | :--- |
| **FR-05** | Người dùng có thể tải hình ảnh đơn thuốc lên hệ thống. |
| **FR-06** | Hệ thống nhận diện và trích xuất thông tin thuốc từ đơn thuốc. |
| **FR-07** | Hệ thống đối chiếu thông tin thuốc với cơ sở dữ liệu và hiển thị kết quả. |

#### C – Lịch sử tra cứu

| Mã | Yêu cầu chức năng |
| :---: | :--- |
| **FR-08** | Hệ thống lưu lịch sử tra cứu thuốc của người dùng. |
| **FR-09** | Người dùng có thể xem lại và xóa lịch sử tra cứu. |

#### D – Xử lý lỗi

| Mã | Yêu cầu chức năng |
| :---: | :--- |
| **FR-10** | Hệ thống thông báo khi dữ liệu hoặc hình ảnh đầu vào không hợp lệ. |
| **FR-11** | Hệ thống thông báo khi không tìm thấy thuốc trong cơ sở dữ liệu. |

---

# Yêu Cầu Phi Chức Năng (Non-Functional Requirements - NFR)

### Tổng Quan Nhóm Yêu Cầu Phi Chức Năng

| Nhóm | Số lượng NFR | Nội dung chính |
| :--- | :---: | :--- |
| **A – Hiệu năng** | 3 | Phản hồi tra cứu ≤ 2 giây, xử lý ảnh ≤ 10 giây, hỗ trợ tối thiểu 10 yêu cầu đồng thời |
| **B – Khả năng sử dụng** | 3 | Giao diện đơn giản, chức năng rõ ràng, thông báo dễ hiểu |
| **C – Độ tin cậy** | 2 | Xử lý lỗi ảnh và đảm bảo tính toàn vẹn dữ liệu thuốc |
| **D – Khả năng bảo trì** | 3 | Phân tách chức năng, quản lý mã nguồn bằng Git, dễ mở rộng |

---

### Chi Tiết Yêu Cầu Phi Chức Năng

#### A – Hiệu năng

| Mã | Yêu cầu |
| :---: | :--- |
| **NFR-01** | Thời gian phản hồi tìm kiếm thuốc không vượt quá 2 giây trong điều kiện tải thông thường. |
| **NFR-02** | Thời gian xử lý hình ảnh không vượt quá 10 giây trong điều kiện thử nghiệm. |
| **NFR-03** | Hệ thống hỗ trợ tối thiểu 10 yêu cầu tra cứu đồng thời trong môi trường thử nghiệm. |

#### B – Khả năng sử dụng

| Mã | Yêu cầu |
| :---: | :--- |
| **NFR-04** | Giao diện đơn giản, dễ sử dụng đối với người dùng phổ thông. |
| **NFR-05** | Các chức năng chính được hiển thị rõ ràng và dễ thao tác. |
| **NFR-06** | Thông báo lỗi được trình bày bằng ngôn ngữ dễ hiểu. |

#### C – Độ tin cậy

| Mã | Yêu cầu |
| :---: | :--- |
| **NFR-07** | Khi xử lý ảnh thất bại, hệ thống thông báo lỗi và cho phép thực hiện lại. |
| **NFR-08** | Dữ liệu thuốc trong cơ sở dữ liệu không bị thay đổi ngoài các thao tác được thiết kế. |

#### D – Khả năng bảo trì

| Mã | Yêu cầu |
| :---: | :--- |
| **NFR-09** | Hệ thống được tổ chức thành các thành phần riêng biệt để thuận tiện bảo trì. |
| **NFR-10** | Mã nguồn được quản lý bằng hệ thống kiểm soát phiên bản Git. |
| **NFR-11** | Có thể bổ sung chức năng mới mà không ảnh hưởng đến các chức năng hiện có nếu không có phụ thuộc trực tiếp. |
