import os
import zipfile
import re
import shutil

# ---------------------------------------------请修改自己电脑上的路径参数--------------------------#
patent_range = '(2950-3000)'
filename = r'e:\data\patent_pool' + patent_range  # 要解压的文件位置
filedir = r'e:\testData\info_txt' + patent_range  # 解压后放入的目录
savetxt_path = r'e:\testData\info_txt' + patent_range  # 生成的txt保存的根位置


# ------------------------------------------------------------------------------------------------#


def save(txt_path, contents):
    fh = open(txt_path, 'w', encoding='utf-8')
    fh.write(contents)
    fh.close()


def release(fromfile, tofile):
    file = os.listdir(filename)
    listfile = []
    length = len(file)
    for i in range(1, length):
        listfile.append(file[i])

    for i in range(0, length - 1):
        file_name = fromfile + '\\' + listfile[i]
        # print(file_name)
        r = zipfile.is_zipfile(file_name)
        if r:
            # --------------------------解压-----------------------------------#
            fz = zipfile.ZipFile(file_name, 'r')
            # print(fz.namelist())
            file = fz.namelist()[3]
            fz.extract(file, tofile)

            # --------------------------打开html转换成TXT----------------------#
            re_folder = r'[A-Z0-9_]+'
            folder_name = re.findall(re_folder, fz.namelist()[1])
            # print(folder_name[0])
            html_path = filedir + '\\' + folder_name[0] + '\\' + 'Full text.html'
            # print(html_path)
            try:
                get_txt(html_path, folder_name[0])
                print('this file ' + file_name + ' has been released')
            except FileNotFoundError:
                print(folder_name[0])
                write_data_to_file('release_fail.txt', folder_name[0])
            finally:
                # --------------------------生成txt之后自动删除无用的文件夹-------------------------#
                folder_path = filedir + '\\' + folder_name[0]
                shutil.rmtree(folder_path)
        else:
            print('This file is not zip file')


def get_txt(html_path, save_name):
    html = open(html_path, 'r', encoding="utf-8")
    htmlcont = html.read()
    html_text = re.sub("[A-Za-z0-9\!\%\[\]\,\。\< \> \/ \"=\" \_ \= \: \{.*} \; \---'宋体'--#---'宋体'--#?-?]", "", htmlcont)
    # print(html_text)
    save_path = savetxt_path + '\\' + save_name + '.txt'
    save(save_path, html_text)


def write_data_to_file(filename, data):
    file = open(filename, 'a')
    file.write(str(data) + '\n')
    file.close()


if __name__ == '__main__':
    release(filename, filedir)
    # get_txt(base_html)
