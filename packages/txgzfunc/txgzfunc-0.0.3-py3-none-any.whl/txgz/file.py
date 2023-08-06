# 文件夹，文件处理

import os
import docx
import json
from win32com import client as wc


def doc2docx(path):
    # 换文件格式
    word = wc.Dispatch("Word.Application")
    dirs = os.listdir(path)
    for file in dirs:
        files = file.split(".")
        file_name, file_flow = files[0], files[1]
        if file_flow == "doc":
            print(file_name, file_flow)
            doc = word.Documents.Open(path + "/{}.doc".format(file_name))

            doc.SaveAs(path + "/{}.docx".format(file_name), 12)

            doc.Close()
    word.Quit()


def read_all(path, out_file):
    # 只处理 .docx文件
    yl_list = []
    dirs = os.listdir(path)
    for file in dirs:
        doc = docx.Document(docx=path + "/" + file)
        a_ = str()
        for _ in doc.paragraphs:
            a_ += _.text + "\n"
        yl_list.append(a_)
    yl_obj = json.dumps(yl_list, ensure_ascii=False)
    with open(path + "/" + out_file, "w", encoding="utf-8") as f:
        f.write(yl_obj)
    print("end")
