# Compact-Test-Case
Tìm những điểm chung của các test case từ đó sinh ra các keyword làm cho độ dài của test case ngắn lại.

<h2>Các khái niệm:</h2>
- **Command**: là một câu lệnh ở trong một test, một test thì bao gồm nhiều command. Ví dụ: click id="name".
- **Paragraph**: là một đoạn gồm nhiều các command, nhưng nhỏ hơn test.
- **Test**: là một test case.
- **Keyword**: là tập các command dùng để rút ngắn test.

<h2>Ý tưởng chính</h2>: Từ các test case sinh ra bộ các keyword theo một số tiêu chí nhất định, từ những keyword đó so sánh với tất cả test case, nếu "giống nhau" thì tăng biến đếm cho keyword đó. Sau khi thực hiện việc đó thì lấy ra keyword cần thay thế theo tiêu chí như độ phổ biến, số command của keyword và thực hiện việc thay thế.

<h2>Đọc dữ liệu:</h2>
- Đọc tất cả các file dữ liệu đầu vào cho vào một list gọi là list_test.
- Trong list_test bao gồm nhiều phần tử mỗi phần tử là một test_case. Ví dụ: list_test = [test1, test2]
- Trong mỗi test_case bao gồm nhiều command. Ví dụ: test1 = [command1, command2, command3]
- Mỗi command là một dòng lệnh bao gồm phần lệnh và phần value cách nhau bởi 4 dấu cách. command1 = "    type=id_name    BachNgoc"

<h2>Sinh keyword:</h2>
- Duyệt hết tất cả các test case, mỗi test case sẽ thực hiện việc tạo ra bộ các keyword với n dòng (n <= số dòng của test case).
	Ví du: Với keyword có 7 dòng lệnh và mặc định mỗi keyword tối thiểu 4 dòng:
	# Ví dụ
- Việc sinh ra keyword có thể có nhiều trường hợp để chọn, như trong bài thì thực hiện khi nào có câu lệnh clickAndWait hoặc cuối test case (cái này có thể cải tiến sau để phù hợp với nghiệp vụ).
- Các keyword được đưa vào một danh sách gọi là list_define_keyword với mỗi phần từ là một keyword, mỗi keyword là chứa một danh sách các command. Ví dụ: keyword = [[['    click    id=name', '    click    id=birthday']], []]

<h2>Tính độ phổ biến cho mỗi keyword:</h2> Với mỗi keyword ta so sánh với tất cả các test case, nếu "giống nhau" thì tăng biến đếm cho keyword đó. Việc kiểm tra sự giống nhau của keyword với test case phụ thuộc vào một số tiêu chí:
- Định nghĩa một mức khác nhau tối đa MAX_ARGUMENT
- Hai command nếu khác nhau về phần lệnh thì coi như là khác nhau, còn khác nhau về phần value thì đếm số lần khác nhau về value đó.
- Giá trị được lưu trong mảng variable_in_a_keyword là tập hợp tất cả các argument khác nhau của keyword so với test case. Ví dụ: variable_in_a_keyword[0] = [[[5, 7], [9, 11], 6], []] tức là có 1 list argument có 6 lần trùng và có 2 argument là word ở vị trí thứ 5 và vị trí số 9 trong keyword, con 7 và 11 lần lượt là vị trí của argument đó trong test case (cái này giúp ích cho việc thay thế sau này).
- Nếu tổng số lần khác nhau của các command tương ứng giữa keyword và test case nhỏ hơn MAX_ARGUMENT thì coi như keyword đó "giống nhau" với test case và tăng biến đếm cho keyword đó.

<h2>Chọn keyword phổ biến nhất và thực hiện việc thay thế:</h2>
