# 文件夹，文件处理
import re
import os
import docx
import json
from win32com import client as wc
from zhon.hanzi import punctuation
from io import StringIO
from io import open
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf


class ReadFile:

    @staticmethod
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
                os.remove(path + "/{}.doc".format(file_name))
        word.Quit()

    @staticmethod
    def read_pdf(path):
        try:
            with open(path, "rb") as my_pdf:
                # resource manager
                rsrcmgr = PDFResourceManager()
                retstr = StringIO()
                laparams = LAParams()
                # device
                device = TextConverter(rsrcmgr, retstr, laparams=laparams)
                process_pdf(rsrcmgr, device, my_pdf)
                device.close()
                content = retstr.getvalue()
                retstr.close()
                # 获取所有行
                lines = str(content)
                return lines
        except Exception as e:
            print(path, "文件错误")
        finally:
            return ""

    @staticmethod
    def read_docx(file):
        # 读取docx
        doc = docx.Document(docx=file)
        a_ = str()
        for _ in doc.paragraphs:
            a_ += _.text + "\n"
        return a_

    @staticmethod
    def filter_str(str):
        # 去空格
        lines = str.replace(" ", "")
        # 去标点
        line = re.sub(u"[%s]+" % punctuation, "", lines)
        # 把多个换行变成1个
        data = re.sub(r"\n+", r"\n", line)
        return data

    def read_ppt(self, ppt_file):
        ppt = wc.Dispatch('PowerPoint.Application')
        ppt.Visible = 1
        a_ = str()
        try:
            pptSel = ppt.Presentations.Open(ppt_file)
            slide_count = pptSel.Slides.Count

            for i in range(1, slide_count + 1):
                shape_count = pptSel.Slides(i).Shapes.Count
                for j in range(1, shape_count + 1):
                    if pptSel.Slides(i).Shapes(j).HasTextFrame:
                        s = pptSel.Slides(i).Shapes(j).TextFrame.TextRange.Text
                        a_ += s + "\n"
        except Exception as e:
            print(ppt_file, "文件错误")
        finally:
            ppt.Quit()
        return a_

    def read_all(self, path, out_file):
        yl_list = []
        dirs = os.listdir(path)
        for file in dirs:
            _s = ''
            files = file.split(".")
            file_name, file_flow = files[0], files[1]
            if file_flow == "docx":
                # pass
                print(file)
                _s = self.read_docx(path + "/" + file)
            if file_flow == "pdf":
                # pass
                print(file)
                _s = self.read_pdf(path + "/" + file)
            if file_flow == "ppt" or file_flow == "pptx":
                # pass
                print(file)
                _s = self.read_ppt(path + "/" + file)
            item_list = self.filter_str(_s)
            if item_list:
                yl_list.append(item_list)
        yl_obj = json.dumps(yl_list, ensure_ascii=False)
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(yl_obj)
        print("end")


path = r"F:\AI\data\src_data\fdch"
out_file = r"F:\AI\data\fdc.json"

if __name__ == "__main__":
    ReadFile().read_all(path, out_file)
