# User Stories (Chuẩn INVEST)

Dựa trên các yêu cầu chức năng, hệ thống xây dựng các User Story theo chuẩn INVEST cho người sử dụng trực tiếp.

---

### US-01: Tra cứu thuốc theo tên
> **Là người dùng,** tôi muốn tìm kiếm thuốc theo tên để nhanh chóng tra cứu thông tin của thuốc.

* **Tiêu chí INVEST:**
  * **Independent:** Có thể thực hiện độc lập với các chức năng khác.
  * **Negotiable:** Có thể thảo luận về cách tìm kiếm và cách hiển thị kết quả.
  * **Valuable:** Giúp người dùng nhanh chóng tìm được thông tin thuốc cần tra cứu.
  * **Estimable:** Ước lượng 2 ngày công.
  * **Small:** Phạm vi chức năng nhỏ, có thể hoàn thành trong một Sprint.
  * **Testable:** Có thể kiểm tra bằng cách nhập tên thuốc và xác nhận kết quả trả về.

---

### US-02: Xem thông tin chi tiết thuốc
> **Là người dùng,** tôi muốn xem thông tin chi tiết của thuốc để hiểu rõ các thông tin liên quan đến thuốc.

* **Tiêu chí INVEST:**
  * **Independent:** Có thể phát triển dựa trên dữ liệu thuốc đã có.
  * **Negotiable:** Có thể thảo luận về các trường thông tin được hiển thị.
  * **Valuable:** Cung cấp thông tin cần thiết cho người dùng khi tra cứu thuốc.
  * **Estimable:** Ước lượng 2 ngày công.
  * **Small:** Chỉ tập trung vào việc hiển thị thông tin chi tiết.
  * **Testable:** Có thể kiểm tra bằng cách chọn một thuốc và xác nhận các thông tin được hiển thị.

---

### US-03: Tra cứu thuốc bằng hình ảnh
> **Là người dùng,** tôi muốn tải hình ảnh thuốc lên hệ thống để tìm kiếm thuốc mà không cần nhập tên thuốc thủ công.

* **Tiêu chí INVEST:**
  * **Independent:** Có thể phát triển độc lập với chức năng tìm kiếm bằng tên.
  * **Negotiable:** Có thể thảo luận về định dạng và chất lượng hình ảnh đầu vào.
  * **Valuable:** Giúp người dùng tra cứu thuốc thuận tiện hơn.
  * **Estimable:** Ước lượng 3 ngày công.
  * **Small:** Tập trung vào việc nhận diện thông tin từ hình ảnh và thực hiện tra cứu.
  * **Testable:** Có thể kiểm tra bằng cách tải hình ảnh thuốc và xác nhận hệ thống trả về kết quả phù hợp.

---

### US-04: Xem các thuốc cùng hoạt chất
> **Là người dùng,** tôi muốn xem các thuốc có cùng hoạt chất với thuốc đang tra cứu để có thêm thông tin tham khảo.

* **Tiêu chí INVEST:**
  * **Independent:** Có thể thực hiện sau khi có thông tin hoạt chất của thuốc.
  * **Negotiable:** Có thể thảo luận về số lượng và cách hiển thị các thuốc cùng hoạt chất.
  * **Valuable:** Giúp người dùng dễ dàng tham khảo các thuốc có cùng hoạt chất.
  * **Estimable:** Ước lượng 2 ngày công.
  * **Small:** Phạm vi giới hạn ở việc tìm và hiển thị các thuốc cùng hoạt chất.
  * **Testable:** Có thể kiểm tra bằng cách chọn một thuốc và xác nhận danh sách thuốc cùng hoạt chất.

---

### US-05: Phân tích đơn thuốc
> **Là người dùng,** tôi muốn tải hình ảnh đơn thuốc lên hệ thống để hệ thống nhận diện và trích xuất thông tin các thuốc trong đơn.

* **Tiêu chí INVEST:**
  * **Independent:** Là chức năng riêng, không phụ thuộc trực tiếp vào lịch sử tra cứu.
  * **Negotiable:** Có thể thảo luận về định dạng ảnh và thông tin cần trích xuất.
  * **Valuable:** Giúp người dùng nhanh chóng tra cứu thông tin từ đơn thuốc.
  * **Estimable:** Ước lượng 4 ngày công.
  * **Small:** Tập trung vào việc nhận diện và trích xuất thông tin thuốc từ đơn.
  * **Testable:** Có thể kiểm tra bằng cách tải ảnh đơn thuốc và xác nhận thông tin thuốc được nhận diện.

---

### US-06: Đối chiếu thuốc trong đơn với cơ sở dữ liệu
> **Là người dùng,** tôi muốn hệ thống đối chiếu các thuốc được nhận diện trong đơn với cơ sở dữ liệu để xem thông tin tương ứng của từng thuốc.

* **Tiêu chí INVEST:**
  * **Independent:** Có thể phát triển dựa trên dữ liệu thuốc và kết quả nhận diện từ đơn.
  * **Negotiable:** Có thể thảo luận về cách đối chiếu và hiển thị kết quả.
  * **Valuable:** Giúp người dùng xác định thông tin của các thuốc trong đơn.
  * **Estimable:** Ước lượng 3 ngày công.
  * **Small:** Tập trung vào việc đối chiếu thông tin thuốc.
  * **Testable:** Có thể kiểm tra bằng cách cung cấp tên thuốc đã nhận diện và xác nhận kết quả đối chiếu.

---

### US-07: Xem lịch sử tra cứu
> **Là người dùng,** tôi muốn xem lại lịch sử các lần tra cứu thuốc để dễ dàng truy cập lại những thông tin đã tìm kiếm.

* **Tiêu chí INVEST:**
  * **Independent:** Có thể phát triển độc lập với chức năng phân tích đơn thuốc.
  * **Negotiable:** Có thể thảo luận về số lượng và cách sắp xếp lịch sử.
  * **Valuable:** Giúp người dùng thuận tiện khi tra cứu lại thông tin.
  * **Estimable:** Ước lượng 2 ngày công.
  * **Small:** Phạm vi chức năng nhỏ và rõ ràng.
  * **Testable:** Có thể kiểm tra bằng cách thực hiện tra cứu và xác nhận kết quả xuất hiện trong lịch sử.

---

### US-08: Xóa lịch sử tra cứu
> **Là người dùng,** tôi muốn xóa các bản ghi trong lịch sử tra cứu để quản lý thông tin lịch sử của mình.

* **Tiêu chí INVEST:**
  * **Independent:** Có thể thực hiện độc lập sau khi dữ liệu lịch sử đã được lưu.
  * **Negotiable:** Có thể thảo luận về việc xóa từng bản ghi hoặc xóa nhiều bản ghi.
  * **Valuable:** Giúp người dùng quản lý lịch sử tra cứu.
  * **Estimable:** Ước lượng 1 ngày công.
  * **Small:** Phạm vi chức năng nhỏ.
  * **Testable:** Có thể kiểm tra bằng cách chọn một bản ghi và xác nhận bản ghi được xóa.

---

### US-09: Thông báo lỗi khi dữ liệu không hợp lệ
> **Là người dùng,** tôi muốn hệ thống thông báo khi dữ liệu hoặc hình ảnh đầu vào không hợp lệ để biết cách xử lý và thực hiện lại thao tác.

* **Tiêu chí INVEST:**
  * **Independent:** Có thể áp dụng cho các chức năng có dữ liệu đầu vào.
  * **Negotiable:** Có thể thảo luận về nội dung và cách hiển thị thông báo lỗi.
  * **Valuable:** Giúp người dùng nhận biết và xử lý lỗi dễ dàng.
  * **Estimable:** Ước lượng 1 ngày công.
  * **Small:** Phạm vi chức năng nhỏ.
  * **Testable:** Có thể kiểm tra bằng cách nhập dữ liệu không hợp lệ và xác nhận thông báo lỗi được hiển thị.

---

### US-10: Thông báo khi không tìm thấy thuốc
> **Là người dùng,** tôi muốn hệ thống thông báo khi không tìm thấy thuốc trong cơ sở dữ liệu để biết rằng kết quả tra cứu không tồn tại.

* **Tiêu chí INVEST:**
  * **Independent:** Có thể áp dụng cho các chức năng tra cứu thuốc.
  * **Negotiable:** Có thể thảo luận về nội dung và cách hiển thị thông báo.
  * **Valuable:** Giúp người dùng hiểu rõ nguyên nhân không có kết quả.
  * **Estimable:** Ước lượng 1 ngày công.
  * **Small:** Phạm vi chức năng nhỏ.
  * **Testable:** Có thể kiểm tra bằng cách nhập tên thuốc không tồn tại và xác nhận thông báo được hiển thị.

---

