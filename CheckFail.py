import xlrd
import re


file_path = '专利交易案例.xlsx'  # 专利交易案例表格文件
cmp_file_path = 'current_patent.txt' # 已下载的专利文件名
# ============将excel文件信息导出datalist=============
def from_excel(file):
    wb = xlrd.open_workbook(file)
    ws = wb.sheet_by_name('Sheet1')
    datalist = []

    for r in range(ws.nrows):
        col = []
        for c in range(ws.ncols):
            col.append(ws.cell(r, c).value)
        datalist.append(col)

    # print(datalist)
    return datalist


# =============excel表格专利号的处理=================
def change_str(s):
    re1 = r'[0-9]+\.'
    name = re.findall(re1, s)
    if name:
        name[0] = name[0].strip('.')
        length = len(name[0])
        return 'CN' + name[0][:length - 1]  # 去掉小号,即最后一位数字
    else:
        return 'CN' + s


# ============提取txt文件名=============
def from_txt(file):
    with open(file) as f:
        data = [str(x)[:14] for x in f.readlines()] # 解取前面的专利号
        return data


def write_data_to_file(filename, data):
    file = open(filename, 'a')
    file.write(str(data) + '\n')
    file.close()


def read_list_from_txt(file):
    with open(file) as f:
        return [str(x).strip() for x in f.readlines()]


if __name__ == '__main__':
    # re_data  = read_list_from_txt('redownload.txt')
    # print(len(re_data))
    # fail_index = read_list_from_txt('no_result_list.txt')
    # # new_fail_index = [str(int(x)+1) for x in fail_index]
    # # print(fail_index)
    # data = from_excel(file_path)
    # new_re_data = [change_str(str(data[int(x)][0])) for x in fail_index]
    # print(len(new_re_data))
    # ultimate_data = []
    # for key in re_data:
    #     if key not in new_re_data:
    #         ultimate_data.append(key)
    #         # write_data_to_file('new_re_down.txt', key)
    # print(len(ultimate_data))
    start_num = 1  # 开始下载的下标
    end_num = 3300  # 结束下载的下标
    data = from_excel(file_path)
    cmp_data = from_txt(cmp_file_path)
    print(len(cmp_data))
    print('===================')
    # print(cmp_data[0])
    # print(change_str(str(data[1][0])))
    count = 0
    for num in range(start_num, end_num):
        cnid = data[num][0]
        key = change_str(str(cnid))
        judge = False
        for cmp in cmp_data:
            # write_data_to_file('redownload.txt', str(key))
            if str(key) == str(cmp):
                judge = True
                break
        if not judge:
            count+=1
            print(str(num)+':  '+key)
    print('=========================')
    print(count)

