from database import SessionLocal
from sqlalchemy import text

def seed_data():
    db = SessionLocal()
    try:
        print("Đang nạp dữ liệu mẫu...")
        
        # 1. Hoạt chất mẫu
        db.execute(text("""
            INSERT OR IGNORE INTO active_ingredients (id, name, description) VALUES
            (1, 'Paracetamol', 'Giảm đau, hạ sốt nhẹ đến vừa'),
            (2, 'Ibuprofen', 'Kháng viêm không steroid (NSAID)'),
            (3, 'Amoxicillin', 'Kháng sinh nhóm Penicillin'),
            (4, 'Cetirizine', 'Thuốc kháng Histamine chống dị ứng'),
            (5, 'Omeprazole', 'Thuốc ức chế bơm Proton giảm tiết axit dạ dày'),
            (6, 'Loperamide', 'Thuốc cầm tiêu chảy'),
            (7, 'Salbutamol', 'Thuốc giãn phế quản trị hen suyễn'),
            (8, 'Loratadine', 'Kháng dị ứng không gây buồn ngủ');
        """))

        # 2. Thuốc mẫu
        db.execute(text("""
            INSERT OR IGNORE INTO medicines (id, name, sdk_code, active_ingredient_id, strength, dosage_form, manufacturer, indication, contraindication, side_effect, warning) VALUES
            (1, 'Panadol Extra', 'VD-12345-20', 1, '500mg/65mg', 'Viên nén', 'GSK', 'Giảm đau đầu, đau răng, hạ sốt', 'Mẫn cảm với Paracetamol', 'Nhẹ: Phát ban, buồn nôn', 'Không dùng quá 4g/ngày'),
            (2, 'Efferalgan 500mg', 'VD-12346-20', 1, '500mg', 'Viên sủi', 'Upsa', 'Hạ sốt, giảm đau nhẹ', 'Suy gan nặng', 'Hiếm gặp dị ứng da', 'Hòa tan hoàn toàn trước khi uống'),
            (3, 'Decolgen Forte', 'VD-12347-20', 1, '500mg', 'Viên nén', 'United Pharma', 'Điều trị cảm cúm, nhức đầu, sổ mũi', 'Mẫn cảm với thành phần thuốc', 'Buồn ngủ, khô miệng', 'Không lái xe khi dùng thuốc'),
            (4, 'Hapacol 250', 'VD-12348-20', 1, '250mg', 'Gói bột', 'Dược Hậu Giang', 'Hạ sốt cho trẻ em', 'Suy gan', 'Dị ứng nhẹ', 'Chờ 4-6 tiếng giữa các lần uống'),
            (5, 'Gualip', 'VD-12349-20', 2, '400mg', 'Viên bao phim', 'Stada', 'Giảm đau xương khớp, đau kinh nguyệt', 'Loét dạ dày tiến triển', 'Đau dạ dày, ợ chua', 'Uống sau khi ăn no'),
            (6, 'Ibuprofen Stada 400', 'VD-12350-20', 2, '400mg', 'Viên nén', 'Stada', 'Kháng viêm, giảm đau nhức', 'Thủng dạ dày, suy thận', 'Buồn nôn, chóng mặt', 'Thận trọng cho người lớn tuổi'),
            (7, 'Clamoxyl 500mg', 'VD-12351-20', 3, '500mg', 'Viên nang', 'GSK', 'Nhiễm khuẩn đường hô hấp, tai mũi họng', 'Dị ứng Penicillin', 'Tiêu chảy, nổi mề đay', 'Phải uống đủ liều theo đơn'),
            (8, 'Augmentin 625mg', 'VD-12352-20', 3, '500mg/125mg', 'Viên nén', 'GSK', 'Nhiễm khuẩn phế quản, tiết niệu', 'Tiền sử vàng da do thuốc', 'Rối loạn tiêu hóa', 'Uống vào đầu bữa ăn'),
            (9, 'Zyrtec 10mg', 'VD-12353-20', 4, '10mg', 'Viên nén', 'UCB', 'Trị viêm mũi dị ứng, nổi mề đay', 'Mẫn cảm với Cetirizine', 'Buồn ngủ nhẹ, khô miệng', 'Tránh dùng chung với cồn'),
            (10, 'Cetirizin Stada 10mg', 'VD-12354-20', 4, '10mg', 'Viên nén', 'Stada', 'Giảm ngứa, hắt hơi, chảy nước mũi', 'Suy thận nặng', 'Mệt mỏi, nhức đầu', 'Thận trọng khi lái xe'),
            (11, 'Omez 20mg', 'VD-12355-20', 5, '20mg', 'Viên nang', 'Dr. Reddys', 'Trào ngược dạ dày thực quản, loét dạ dày', 'Mẫn cảm với Omeprazole', 'Đau đầu, tiêu chảy', 'Uống trước bữa ăn 30 phút'),
            (12, 'Losec Mups 20mg', 'VD-12356-20', 5, '20mg', 'Viên nén', 'AstraZeneca', 'Điều trị viêm loét dạ dày tá tràng', 'Dùng chung với Nelfinavir', 'Táo bón, đầy hơi', 'Uống nguyên viên với nước'),
            (13, 'Imodium 2mg', 'VD-12357-20', 6, '2mg', 'Viên nang', 'Janssen', 'Điều trị tiêu chảy cấp và mãn tính', 'Viêm đại lượng cấp', 'Táo bón, khô miệng', 'Không dùng cho trẻ dưới 6 tuổi'),
            (14, 'Ventolin Evohaler', 'VD-12358-20', 7, '100mcg/liều', 'Bình xịt', 'GSK', 'Cắt cơn hen phế quản, co thắt phế quản', 'Mẫn cảm với Salbutamol', 'Run tay, nhịp tim nhanh', 'Xịt đúng kỹ thuật theo chỉ dẫn'),
            (15, 'Claritine 10mg', 'VD-12359-20', 8, '10mg', 'Viên nén', 'Bayer', 'Giảm triệu chứng viêm mũi dị ứng', 'Mẫn cảm với Loratadine', 'Đau đầu, khô miệng', 'An toàn không gây buồn ngủ');
        """))

        # 3. Triệu chứng mẫu
        db.execute(text("""
            INSERT OR IGNORE INTO symptoms (id, name, description) VALUES
            (1, 'Sốt', 'Thân nhiệt cao trên 37.5 độ C'),
            (2, 'Đau đầu', 'Đau nhức vùng đầu, thái dương'),
            (3, 'Ho', 'Ho khô hoặc ho có đờm'),
            (4, 'Sổ mũi', 'Chảy nước mũi, nghẹt mũi'),
            (5, 'Đau dạ dày', 'Đau thượng vị, ợ chua, trào ngược'),
            (6, 'Tiêu chảy', 'Đi ngoài phân lỏng nhiều lần');
        """))

        # 4. Liên kết Thuốc <-> Triệu chứng
        db.execute(text("""
            INSERT OR IGNORE INTO medicine_symptoms (medicine_id, symptom_id) VALUES
            (1, 1), (1, 2),
            (2, 1), (2, 2),
            (3, 1), (3, 2), (3, 4),
            (11, 5), (12, 5),
            (13, 6);
        """))

        db.commit()
        print(" Nạp dữ liệu thuốc mẫu thành công!")
    except Exception as e:
        db.rollback()
        print(f" Lỗi khi nạp dữ liệu: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()