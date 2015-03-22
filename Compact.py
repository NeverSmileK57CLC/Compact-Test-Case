# coding=utf-8
__author__ = 'neversmile'
import os
import copy
import shutil

'''
Documentation:
- Command: là một câu lệnh ở trong một test, một test thì bao gồm nhiều command. Ví dụ: click id="name".
- Paragraph: là một đoạn gồm nhiều các command, nhưng nhỏ hơn test.
- Test: là một test case.
- Keyword: là tập các command dùng để rút ngắn test.
'''

import os


def compare_two_command(command1, command2):
    """
    CHECKED
    Trả về các phần không giống nhau giữa 2 command, ví dụ: [$EMPTY, ngoc]
    trong đó $EMPTY và ngoc tương ứng là 2 phần của command1 và command2
    :param command1: là 1 câu lệnh
    :param command2: là 1 câu lệnh
    :return: 1 list chứa các từ khác nhau giữa 1 command nếu số phần tử nhỏ hơn hoặc bằng 2, còn không trả về -1
    """
    count = 0
    w1 = command1.split("    ")
    w2 = command2.split("    ")

    temp_list_word = []
    if len(w1) != len(w2):
        count += 3
    else:
        # Để bỏ qua trường hợp là cùng câu lệnh click and clickAndWait nhưng lại khác nhau, thực tế 2 câu lệnh này có thể coi là một.
        check = w1[1] == "click" and w2[1] == "clickAndWait" or w1[1] == "clickAndWait" and w2[1] == "click"
        # Do những keyword này có 4 dấu cách ở đầu nên cả w1 và w2 đều có thêm 1 phần tử rỗng ở đầu
        if not check and w1[1] != w2[1]:
            count += 3
        for i in range(2, len(w1)):
            if w1[i] != w2[i]:
                temp_list_word.append([i, i])
                count += 1
                # print "variable_index", variable_index
    if count <= 2:
        return temp_list_word
    else:
        return -1


def length_word_in_current_command(test, command):
    """
    CHECKED
    Tính số word từ đầu test đến command hiện tại. Áp dụng cho cả trường hợp keyword và test case,
    vì nếu là keyword thì không có tên keyword nên việc trừ 1 (do mỗi dòng command thì có 4 kí tự trống),
    còn nếu là test case thì trừ 1 sẽ loại bỏ đi cái tên test case.
    :param test: list test hoặc list keyword
    :param command: list command
    :return: số word từ đầu test đến command hiện tại.
    """
    count = 0
    for l in test:
        if l != command:
            t = l.split("    ")
            count += len(t) - 1
        else:
            break
    return count


def compare_keyword_with_test(keyword, test):
    """
    CHECKED
    So sánh danh sách list1 có nằm trong danh sách 2 hay không với độ lệch value <= 2
    :param keyword: Chứa nhiều dòng lệnh, tương tự như 1 test case
    :param test: Chứa nhiều dòng lệnh, tương tự như 1 test case
    list1 luôn luôn có độ dài nhỏ hơn hoặc bằng list2
    :return: Trả về phần không giống nhau giữa keyword và test, ví dụ: [$EMPTY, ngoc] trong đó,
    $EMPTY và ngoc tương ứng là các phần trong keyword và test.
    """
    # print 'list1', list2
    # print 'list2', list1
    deviation = len(test) - len(keyword)
    # print "deviation", deviation, len(list1), len(list2)

    temp_list = []
    official_list = [1, 2, 3]
    for i in range(1, deviation + 1):
        temp_list = []
        for j in range(0, len(keyword)):
            # print "list1", list1[j]; print "list2", list2[j + i]
            # print compare_two_keyword(list1[j], list2[j+i]), list1[j], list2[i+j]
            if compare_two_command(keyword[j], test[j + i]) != -1:
                for w in compare_two_command(keyword[j], test[j + i]):
                    w[0] += length_word_in_current_command(keyword, keyword[j])
                    w[1] += length_word_in_current_command(test, test[j + i])
                    temp_list.append(w)
            else:
                # print "kieu"
                temp_list = [1, 2, 3]
        # print "temp", temp_list
        if len(official_list) > len(temp_list):
            official_list = []
            for w in temp_list:
                official_list.append(w)
                # print "official", official_list
    # print "ngoc"
    # print "offi", official_list
    if len(official_list) <= 2:
        return official_list
    return -1


def compare_two_keyword_exactly(kw1, kw2):
    """
    CHECKED
    So sánh 2 test có độ dài giống nhau, chỉ sử dụng trong việc xem
    :param test1:
    :param test2:
    :return:
    """
    if len(kw1) != len(kw2):
        return False
    dem = 0
    for i in range(0, len(kw1)):
        # print "kw1", kw1[i]
        # print kw2[i]
        # print compare_two_command(kw1[i], kw2[i])
        if compare_two_command(kw1[i], kw2[i]) != -1:
            dem += len(compare_two_command(kw1[i], kw2[i]))
        else:
            return False
    if dem <= 2:
        return True


def command_contain_string(keyword, string):
    """
    CHECHED
    Tính xem keyword có chứa xâu string hay không?
    :param keyword:
    :param string:
    :return: true: nếu có chứa, false: nếu không chứa xâu string
    """
    kw = keyword.split("    ")
    try:
        kw.index(string)
    except ValueError:
        return False
    else:
        return True


def list_test_contain_test(list_test, test):
    """
    CHECKED
    Kiểm tra xem test có nằm trong danh sách list_test hay không
    :param list:
    :param test:
    :return: -1: nếu test không nằm trong list_test, ngược lại trả về vị trí xuất hiện
    """
    for i in range(0, len(list_test)):
        if compare_two_keyword_exactly(list_test[i], test):
            return i
    return -1


def add_to_list_keyword(list_temp):
    """
    CHECKED
    Thêm list temp vào danh sách các định nghĩa cho keyword
    :param list_temp: là tập các câu lệnh định nghĩa cho 1 keyword
    :return: no return
    """
    global list_define_keyword
    temp = list_test_contain_test(list_define_keyword, list_temp)
    if temp != -1:
        pass
    else:
        list_define_keyword.append(list_temp)


def create_list_define_keyword():
    global list_test
    for test in list_test:
            start = 1
            end = 1
            for i in range(1, len(test)):
                if i == len(test) - 1 or command_contain_string(test[i], "clickAndWait"):
                    end = i
                    if end - start >= 3:
                        for j in range(0, end - start - 2):
                            length = 4 + j
                            for k in range(0, end - start - length + 2):
                                new_start = start + k
                                # print new_start, length
                                list_temp = test[new_start:new_start + length]
                                # print list_temp
                                add_to_list_keyword(list_temp)
                    start = end + 1


def check_variable_in_list_variable(list_variable1, list_variable2):
    '''
    CHECKED
    Kiểm tra xem tất cả a1 ở trong list_variable1 có nằm trong a ở trong list_variable2 hay không
    :param list_variable1: là một list có dạng [a1, b1]
    :param list_variable2: là một list có dạng [[a0, b0], [a1, b1]]
    :return: True: nếu có nằm ở trong, False: ngược lại
    '''
    for i in list_variable1:
        ktra = False
        for j in list_variable2:
            if i[0] == j[0]:
                ktra = True
        if not ktra:
            return False
    return True


def variable_in_a_keyword(keyword, list_test):
    '''
    Tính toán số lần xuất hiện của keyword ở trong list_test.
    :param keyword: list keyword
    :param list_test: list list_test
    :return: trả về cặp các vị trí của nhũng word khác nhau và số lần xuất hiện của chúng.
    '''
    variable_in_a_keyword_temp = []
    number_of_similar = 0
    for test in list_test:
        # Tức là keyword có nằm trong test, và trả về các phần khác nhau.
        if compare_keyword_with_test(keyword, test) != -1:
            temp = [compare_keyword_with_test(keyword, test), 1]
            # print ("temp", temp, "\n")
            if len(temp[0]) == 0:  # Nếu keyword và test giống nhau hoàn toàn
                # print ("final0", test)
                for variable in variable_in_a_keyword_temp:
                    variable[1] += 1
                number_of_similar += 1
                # print (False)
            else:  # keyword và test không giống nhau hoàn toàn
                if len(variable_in_a_keyword_temp) == 0:
                    temp[1] += number_of_similar
                    variable_in_a_keyword_temp.append(temp)
                else:
                    # print (len(variable_in_a_keyword))
                    check_exist = False
                    for variable in variable_in_a_keyword_temp:
                        if check_variable_in_list_variable(temp[0], variable[0]):
                            variable[1] += 1
                            check_exist = True
                    if not check_exist:
                        temp[1] += number_of_similar
                        # Kiểm tra 1 lượt nữa những variable trong danh sách nếu trùng với keyword chuần bị
                        # thêm vào thì cộng vào.
                        for v in variable_in_a_keyword_temp:
                            if check_variable_in_list_variable(v[0], temp[0]):
                                temp[1] += 1
                        variable_in_a_keyword_temp.append(temp)
    # print len(list_test)
    max_length = 0
    max_pos = -1
    for i in range(0, len(variable_in_a_keyword_temp)):
        if variable_in_a_keyword_temp[i][1] > max_length:
            max_length = variable_in_a_keyword_temp[i][1]
            max_pos = i
    if max_pos == -1:
        return []
    else:
        return variable_in_a_keyword_temp[max_pos]


def write_keyword_file(name_keyword, define_keyword):
    """
    Hàm ghi các định nghĩa của các keyword với tên name_keyword vào file resource.txt
    :param name_keyword:
    :param define_keyword: định nghĩa cho keyword
    :return:
    """
    out = open(path_keyword_file, "a")
    out.write(name_keyword + "\n")
    for i in define_keyword:
        out.write(i)
    out.close()


def print_list(list):
    for li in list:
        print li,
    print ""


def pos_word_in_list(pos, list):
    '''
    Kiểm tra xem vị trí pos có nằm trong phần tử đầu của list hay không? Ví dụ: 9 nằm trong [[9,7], [3,4]]
    :param pos: vị trí
    :param list: list chứa các cặp số, và mục đích của mình là so sanh pos với số thứ nhất của cặp số
    :return: True or False
    '''
    for pair in list:
        if pos == pair[0]:
            return True
    return False


def value_of_pos_in_test(pos, test):
    '''
    Xác định word thứ pos ở trong test.
    :param pos: vị trí
    :param test: là test case hoặc là keyword
    :return: word ở vị trí thứ pos
    '''
    co = 0
    for cm in test:
        wos = cm.split("    ")
        wos.remove(wos[0])
        for wo in wos:
            co += 1
            if co == pos:
                if '\n' in wo:
                    wo = wo[0: len(wo) - 1]
                    return wo


def check_and_replace_keyword(keyw, kw_name, variable_element):
    '''
    Kiểm tra xem keyword có nằm trong list test hay không, nếu có thì thay thế bởi keyword_and_argument
    :param keyword:
    :param list_test:
    :param kw_name:
    :return: trả về list_test
    '''
    print "variable_element", variable_element
    global list_test
    for test in list_test:
        kw_name_and_arg = "    " + kw_name
        tmp = compare_keyword_with_test(keyw, test)
        if tmp != -1 and tmp != []:
            print "thaythe"
            # Tìm vị trí trong test case để thay thế
            len_word = tmp[0][1] - tmp[0][0]
            # po_temp là vị trí dòng mà keyword nằm trong test case, để dùng cho việc thay thế
            po_temp = 0
            for po in range(1, len(test)):
                if len_word != 0:
                    len_word = len_word - len(test[po].split("    ")) + 1
                else:
                    po_temp = po
                    break

            if len(tmp) == len(variable_element):
                ch = True
                for i in range(0, len(tmp)):
                    if tmp[i][0] != variable_element[i][0]:
                        ch = False
                # Nếu ch mà đúng thì keyword nằm trong test và tiến hành thay thế
                if ch:
                    for pair in tmp:
                        kw_name_and_arg = kw_name_and_arg + "    " + value_of_pos_in_test(pair[1], test)
                    kw_name_and_arg += "\n"
                    for k in range(0, len(keyw)):
                        test.remove(test[po_temp])
                    test.insert(po_temp, kw_name_and_arg)
            elif len(variable_element) > len(tmp):
                print "lon hon"
                j = 0
                k = 0
                while j < len(variable_element) and k < len(tmp):
                    # Xử lý trường hợp sô argument của test case ít hơn của keyword, phải thêm argument của
                    # keyword vào trong test case
                    if variable_element[j][0] < tmp[k][0]:
                        kw_name_and_arg += "    " + value_of_pos_in_test(variable_element[j][0], keyw)
                        j += 1
                    elif variable_element[j][0] == tmp[k][0]:
                        kw_name_and_arg += "    " + value_of_pos_in_test(tmp[k][1], test)
                        k += 1
                        j += 1
                # Xử lí trường hợp số argument của test nhỏ hơn của keyword, tức là ta phải thêm argument
                # của keyword vào trong test case
                while k >= len(tmp) and j < len(variable_element):
                    kw_name_and_arg += "    " + value_of_pos_in_test(variable_element[j][0], keyw)
                    k += 1
                    j += 1
                kw_name_and_arg += '\n'
                for k in range(0, len(keyw)):
                    test.remove(test[po_temp])
                test.insert(po_temp, kw_name_and_arg)

        elif tmp != -1 and tmp == []:
            po_temp = 0
            for li in range(0, len(test)):
                check = True
                for lm in range(0, len(keyw)):
                    if keyw[lm] != test[lm + li]:
                        check = False
                if check:
                    po_temp = li
                    break
            for k in range(0, len(keyw)):
                test.remove(test[po_temp])
            for pair in variable_element:
                kw_name_and_arg += "    " + value_of_pos_in_test(pair[0], keyw)
            kw_name_and_arg += "\n"
            test.insert(po_temp, kw_name_and_arg)


# ---------------------------MAIN-------------------------------------------


list_define_keyword = []  # Lưu các định nghĩa các keyword
header = """
*** Settings ***
Resource    seleniumLibrary.txt

*** Keywords ***
"""
path = "/home/nevesmile/Documents/tests/Solution/"
path_solution2 = "/home/nevesmile/Documents/tests/Solution2/"

if not os.path.exists(path_solution2):
    os.makedirs(path_solution2)

path_keyword_file = path_solution2 + "resource.txt"
define_file = open(path_keyword_file, "w")
define_file.write(header)
define_file.close()
header_filename_numtest = []

if os.path.exists(path):
    if os.path.isdir(path):
        dirs = os.listdir(path)
        list_test = []
        for f in sorted(dirs):
            count_file = 0
            path_suite = path + "/" + f
            suite = open(path_suite)
            # Đọc phần header rồi cho vào biến, để sau này ghi vào file mới chứa các keyword đã được thay thế
            header_temp = ""
            for line in suite:
                if line.find("*** Variables ***") != -1:
                    header_temp += "Resource    resource.txt\n"
                if line.find("*** Test Cases ***") == -1:
                    header_temp += line
                else:
                    header_temp += line
                    break
            suite.close()

            suite = open(path_suite)
            previous_line = ""
            one_test = []
            for line in suite:
                if line == '\n' and len(one_test) > 1:
                    list_test.append(one_test)
                    count_file += 1
                    one_test = []
                else:
                    if previous_line.find("*** Test Cases ***") != 0:
                        previous_line = line
                    else:
                        if line[0:4] != "    ":
                            if len(one_test) > 1:  # Để loại bỏ những test chỉ có tên test case.
                                list_test.append(one_test)
                                count_file += 1
                            one_test = [line]
                        else:
                            one_test.append(line)
            # Trường hợp đọc đến hết file.
            else:
                list_test.append(one_test)
                count_file += 1
            suite.close()
            header_filename_numtest.append([header_temp, path_solution2 + "Ver2_" + f, count_file])

        while True:
            list_define_keyword = []
            # Thêm các định nghĩa cho keyword vào list list_define_word
            create_list_define_keyword()

            list_word_variable = []  # Danh sách chứa các từ khác nhau giữa keyword và test case.
            for keyword in list_define_keyword:
                list_word_variable.append(variable_in_a_keyword(keyword, list_test))

            print list_word_variable
            # Tiến hành tìm kiếm các keyword phổ biến nhất và ghi vào file
            # while True:
            max_count = 0
            max_element = -1
            for i in range(0, len(list_word_variable)):
                if list_word_variable[i] != [] and list_word_variable[i][1] > max_count:
                    max_count = list_word_variable[i][1]
                    max_element = i

            print "Do you want to define this keyword (Y/N):"
            print_list(list_define_keyword[max_element])
            print "With arguments: ",
            for i in list_word_variable[max_element][0]:
                print value_of_pos_in_test(i[0], list_define_keyword[max_element]),
            print "With number of similarity is: ", max_count
            answer = raw_input("")
            if answer == "y" or answer == "Y":
                keyword_name = raw_input("Please input keyword name: ")

                # Ghi phần tên keyword và argument
                out = open(path_keyword_file, "a")
                out.write(keyword_name + "\n")
                out.write("    [Arguments]")
                list_argument = ""
                for i in range(0, len(list_word_variable[max_element][0])):
                    list_argument += "    ${value"
                    list_argument += str(i + 1)
                    list_argument += "}"
                list_argument += "\n"
                out.write(list_argument)
                out.write("\n")
                # Ghi phần các lệnh của keyword
                count_word = 0
                num_of_vari = 0
                for command in list_define_keyword[max_element]:
                    words = command.split("    ")  # Lưu ý phần tử ở đầu là rỗng
                    for i in range(1, len(words)):
                        count_word += 1
                        if pos_word_in_list(count_word, list_word_variable[max_element][0]):
                            num_of_vari += 1
                            out.write("    ${value")
                            out.write(str(num_of_vari))
                            out.write("}")
                        else:
                            out.write("    ")
                            out.write(words[i])
                    out.write("\n")
                out.write("\n")
                out.close()  # Xong phần ghi file, thêm keyword vào file resource.txt

                # Bắt đầu phần thay thế keyword vào list_test va file test case.
                keyword_and_argument = "    " + keyword_name + list_argument
                check_and_replace_keyword(list_define_keyword[max_element], keyword_name, list_word_variable[max_element][0])
                for test in list_test:
                    print_list(test)
            else:
                break

        # Tiến hành ghi vào file với form Ver2_tenfile.txt
        shutil.copy(path + "seleniumLibrary.txt", path_solution2)

        pos_file = -1
        for triple in header_filename_numtest:
            suite = open(triple[1], "w")
            suite.write(triple[0])
            for i in range(0, triple[2]):
                pos_file += 1
                for line in list_test[pos_file]:
                    suite.write(line)

    elif os.path.isfile(path):
        print path
