# Tiêu Chí Nghiệm Thu (Gherkin BDD)

### US-01: Tra cứu thuốc theo tên
```gherkin
Feature: Tra cứu thuốc theo tên
  As a: người dùng
  I want to: tìm kiếm thuốc theo tên
  So that: tôi có thể nhanh chóng tra cứu thông tin của thuốc

  Scenario: Tra cứu thuốc thành công
    Given tôi đang ở chức năng tra cứu thuốc
    When tôi nhập tên thuốc "Panadol"
    And tôi nhấn nút "Tìm kiếm"
    Then hệ thống hiển thị danh sách các thuốc phù hợp
    And tôi có thể chọn thuốc để xem thông tin chi tiết

  Scenario: Không tìm thấy thuốc
    Given tôi đang ở chức năng tra cứu thuốc
    When tôi nhập tên thuốc "ThuocKhongTonTai"
    And tôi nhấn nút "Tìm kiếm"
    Then hệ thống hiển thị thông báo "Không tìm thấy thuốc trong cơ sở dữ liệu"
    And không có kết quả thuốc được hiển thị
```
### US-02: Xem thông tin chi tiết thuốc
``` gherkin
Feature: Xem thông tin chi tiết thuốc
  As a: người dùng
  I want to: xem thông tin chi tiết của thuốc
  So that: tôi có thể biết các thông tin liên quan đến thuốc

  Scenario: Hiển thị thông tin thuốc thành công
    Given tôi đã tìm thấy thuốc "Panadol"
    When tôi chọn thuốc cần xem
    Then hệ thống hiển thị thông tin chi tiết của thuốc
    And thông tin gồm tên thuốc, hoạt chất, hàm lượng, dạng bào chế và nhà sản xuất

  Scenario: Không có thông tin thuốc
    Given thuốc không có đầy đủ dữ liệu trong cơ sở dữ liệu
    When tôi chọn thuốc cần xem
    Then hệ thống hiển thị các thông tin hiện có
    And thông báo những thông tin chưa được cung cấp
```
### US-03: Tra cứu thuốc bằng hình ảnh
``` gherkin
Feature: Tra cứu thuốc bằng hình ảnh
  As a: người dùng
  I want to: tải hình ảnh thuốc lên hệ thống
  So that: tôi có thể tra cứu thuốc mà không cần nhập tên thủ công

  Scenario: Tra cứu bằng hình ảnh thành công
    Given tôi đang ở chức năng tra cứu thuốc bằng hình ảnh
    When tôi tải lên một hình ảnh thuốc hợp lệ
    And tôi nhấn nút "Tra cứu"
    Then hệ thống thực hiện nhận diện thông tin từ hình ảnh
    And hệ thống hiển thị thuốc phù hợp với thông tin nhận diện được

  Scenario: Hình ảnh không hợp lệ
    Given tôi đang ở chức năng tra cứu thuốc bằng hình ảnh
    When tôi tải lên một tệp không phải hình ảnh
    And tôi nhấn nút "Tra cứu"
    Then hệ thống hiển thị thông báo "Dữ liệu hình ảnh không hợp lệ"
    And hệ thống không thực hiện tra cứu
```
### US-04: Xem các thuốc cùng hoạt chất
``` gherkin
Feature: Xem các thuốc cùng hoạt chất
  As a: người dùng
  I want to: xem các thuốc có cùng hoạt chất
  So that: tôi có thêm thông tin tham khảo về các thuốc có cùng hoạt chất

  Scenario: Hiển thị thuốc cùng hoạt chất
    Given tôi đang xem thông tin chi tiết của một thuốc
    When thuốc có thông tin về hoạt chất
    Then hệ thống hiển thị danh sách các thuốc có cùng hoạt chất
    And danh sách không bao gồm các thuốc không cùng hoạt chất

  Scenario: Không có thuốc cùng hoạt chất
    Given tôi đang xem thông tin chi tiết của một thuốc
    When không có thuốc nào khác có cùng hoạt chất
    Then hệ thống hiển thị thông báo "Không tìm thấy thuốc cùng hoạt chất"
```
### US-05: Phân tích đơn thuốc
``` gherkin
Feature: Phân tích đơn thuốc
  As a: người dùng
  I want to: tải hình ảnh đơn thuốc lên hệ thống
  So that: tôi có thể nhận diện các thuốc trong đơn

  Scenario: Phân tích đơn thuốc thành công
    Given tôi đang ở chức năng phân tích đơn thuốc
    When tôi tải lên hình ảnh đơn thuốc hợp lệ
    And tôi nhấn nút "Phân tích"
    Then hệ thống thực hiện nhận diện nội dung đơn thuốc
    And hệ thống hiển thị danh sách các thuốc được nhận diện

  Scenario: Hình ảnh đơn thuốc không hợp lệ
    Given tôi đang ở chức năng phân tích đơn thuốc
    When tôi tải lên hình ảnh không hợp lệ
    And tôi nhấn nút "Phân tích"
    Then hệ thống hiển thị thông báo "Hình ảnh không hợp lệ"
    And hệ thống không thực hiện phân tích
```
### US-06: Đối chiếu thuốc trong đơn với cơ sở dữ liệu
``` gherkin
Feature: Đối chiếu thuốc với cơ sở dữ liệu
  As a: người dùng
  I want to: đối chiếu các thuốc trong đơn với cơ sở dữ liệu
  So that: tôi có thể xem thông tin tương ứng của từng thuốc

  Scenario: Đối chiếu thành công
    Given hệ thống đã nhận diện được thuốc từ đơn
    When hệ thống thực hiện đối chiếu với cơ sở dữ liệu
    Then hệ thống hiển thị thông tin của các thuốc tìm thấy
    And thông tin được đối chiếu tương ứng với từng thuốc

  Scenario: Không tìm thấy thuốc trong cơ sở dữ liệu
    Given hệ thống đã nhận diện được tên thuốc từ đơn
    When thuốc không tồn tại trong cơ sở dữ liệu
    Then hệ thống hiển thị thông báo "Không tìm thấy thuốc trong cơ sở dữ liệu"
    And hệ thống đánh dấu thuốc đó chưa được đối chiếu
```
### US-07: Xem lịch sử tra cứu
``` gherkin
Feature: Xem lịch sử tra cứu
  As a: người dùng
  I want to: xem lại lịch sử tra cứu thuốc
  So that: tôi có thể truy cập lại các thông tin đã tìm kiếm

  Scenario: Xem lịch sử tra cứu thành công
    Given tôi đã thực hiện một hoặc nhiều lần tra cứu thuốc
    When tôi mở chức năng "Lịch sử tra cứu"
    Then hệ thống hiển thị danh sách các lần tra cứu
    And mỗi bản ghi hiển thị thông tin cần thiết của lần tra cứu

  Scenario: Không có lịch sử tra cứu
    Given tôi chưa thực hiện lần tra cứu nào
    When tôi mở chức năng "Lịch sử tra cứu"
    Then hệ thống hiển thị thông báo "Chưa có lịch sử tra cứu"
```
### US-08: Xóa lịch sử tra cứu
``` gherkin
Feature: Xóa lịch sử tra cứu
  As a: người dùng
  I want to: xóa một bản ghi trong lịch sử tra cứu
  So that: tôi có thể quản lý lịch sử của mình

  Scenario: Xóa lịch sử thành công
    Given tôi đang xem danh sách lịch sử tra cứu
    And danh sách có ít nhất một bản ghi
    When tôi chọn một bản ghi và nhấn nút "Xóa"
    Then hệ thống xóa bản ghi được chọn
    And bản ghi không còn xuất hiện trong danh sách lịch sử

  Scenario: Hủy thao tác xóa
    Given tôi đang xem danh sách lịch sử tra cứu
    When tôi chọn một bản ghi và nhấn nút "Xóa"
    And tôi chọn "Hủy"
    Then hệ thống không xóa bản ghi
    And bản ghi vẫn được hiển thị trong lịch sử
```
### US-09: Thông báo lỗi khi dữ liệu không hợp lệ
``` gherkin
Feature: Xử lý dữ liệu đầu vào không hợp lệ
  As a: người dùng
  I want to: nhận được thông báo khi dữ liệu không hợp lệ
  So that: tôi biết cách xử lý và thực hiện lại thao tác

  Scenario: Dữ liệu đầu vào không hợp lệ
    Given tôi đang thực hiện một chức năng yêu cầu nhập dữ liệu
    When tôi nhập hoặc tải lên dữ liệu không hợp lệ
    Then hệ thống hiển thị thông báo lỗi phù hợp
    And hệ thống không thực hiện thao tác với dữ liệu không hợp lệ
```
### US-10: Thông báo khi không tìm thấy thuốc
``` gherkin
Feature: Thông báo thuốc không tồn tại
  As a: người dùng
  I want to: nhận được thông báo khi thuốc không có trong cơ sở dữ liệu
  So that: tôi biết kết quả tra cứu không tồn tại

  Scenario: Không tìm thấy thuốc
    Given tôi thực hiện tra cứu một thuốc
    When hệ thống không tìm thấy thuốc trong cơ sở dữ liệu
    Then hệ thống hiển thị thông báo "Không tìm thấy thuốc trong cơ sở dữ liệu"
    And hệ thống cho phép tôi thực hiện tra cứu lại
```
