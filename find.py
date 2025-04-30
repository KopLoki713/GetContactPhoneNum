import keyboard
import pymupdf
import fitz # 导入 PyMuPDF 库
import os
import unicodedata
import shutil
from io import BytesIO
import pytesseract
import re

#from pymupdf.utils import get_text


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
try:
    from PIL import Image, ImageEnhance, ImageFilter
except ImportError:
    import Image


def pixmap_to_pil(pixmap):
    # 获取像素格式
    mode = "RGB" if pixmap.n == 3 else "RGBA"

    # 直接转换为 PIL Image
    pil_image = Image.frombytes(
        mode,  # "RGB" 或 "RGBA"
        (pixmap.width, pixmap.height),  # 图像尺寸
        pixmap.samples,  # 原始像素数据
        "raw",  # 原始数据模式
        mode,  # 数据格式（与 mode 一致）
        0,  # 行对齐（通常为 0）
        1  # 反转行序（1 表示不反转）
    )
    return pil_image

class hetong:
    def __init__(self,file_path):
        self.company_name=""
        self.phone_number=""
        self.file_path = file_path
        self.doc=fitz.open(file_path)
        text = self.doc[0].get_text()
        print(text)
        if text == '' or text =="扫描全能王 创建\n":
            self.form="图片"
        else:
            self.form="文字"
        print(self.form)



    def get_text(self,page_numb=3):
        #os.system("cls")
        if self.form=="文字":

            self.texts = self.doc[page_numb].get_text()
            print(self.texts)

        else:
            page = self.doc[page_numb]
            rotate = int(0)
            # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
            # 此处若是不做设置，默认图片大小为：792X612, dpi=72
            # zoom_x = 1.33333333  # (1.33333333-->1056x816)   (2-->1584x1224)
            # zoom_y = 1.33333333
            zoom_x = 1.33333333  # (1.33333333-->1056x816)   (2-->1584x1224)
            zoom_y = 1.33333333

            mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            #print(pix)

            img = pixmap_to_pil(pix)
            #img = img.convert('L')  # 转换为灰度图
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2)  # 提高对比度
            #img = img.filter(ImageFilter.MedianFilter())  # 应用中值滤波去噪
            #img = img.point(lambda x: 0 if x < 140 else 255)  # 二值化


            #img.show()
            self.texts = pytesseract.image_to_string(img, lang='chi_sim')
            if self.texts == '':
                images = page.get_images()

                # 遍历图片
                for image in images:
                    # 返回图片引用
                    xref = image[0]

                    # 根据引用从pdf中释放出图片
                    base_image = self.doc.extract_image(xref)
                    #print(base_image)
                    # 获得图片数据
                    image_data = base_image["image"]
                    image = Image.open(BytesIO(image_data))
                    self.texts = pytesseract.image_to_string(image, lang='chi_sim')
                    if self.texts != '':
                        break



    def get_info(self):



        format_text = unicodedata.normalize('NFKC', self.texts).replace(" ", "")
        print(format_text)
        print("*" * 30 + self.file_path + "*" * 30)

        #text = re.search("甲方.*?电话.*?乙方|[^\x00-\xff]方.*?电话.*?乙方|甲方.*?电话.*?\n", format_text, re.DOTALL).group()
        match = re.search(r"甲方.*?电话.*?(?:乙方|\n)", format_text, re.DOTALL)
        if not match:
            # 如果失败，再尝试泛化的规则
            match = re.search(r"[^\x00-\xff]方.*?电话.*?乙方", format_text, re.DOTALL)
        text=match.group()
        tmp_re = re.search("方.*?\n", text).group()
        self.company_name = re.sub("甲|方|:|【|】|“|,|”", "", tmp_re)
        print("公司名----" + self.company_name)

        tmp_re = re.search("电话.*?\n", text).group()
        self.phone_number = re.sub("电话|:|【|】|,|“", "", tmp_re)
        print("电话----" + self.phone_number)
        #





    def finding(self):

        page_range = min(self.doc.page_count,5)
        #os.system("cls")
        for i in range(0,page_range):
            try:

                self.get_text(page_numb=i)
                self.get_info()
                self.info = [self.file_path, self.company_name, self.phone_number]
                ws.append(self.info)
                break
            except:
                pass
            if i ==2:
                print("这个pdf没有或者是没事别到")



    def close(self):
        self.doc.close()
        if self.company_name =="" and self.phone_number =="" :

            shutil.move(self.file_path,"./debug_pdf/")
        else:
            print("找到的公司名称为:"+self.company_name)
            print("找到的电话号码为:" + self.phone_number)








def chazhao(file_path,model):
    contact = hetong(file_path)
    contact.finding()
    if model =="1":

        contact.close()
    if model =="2":
        print("找到的公司名称为:" + contact.company_name)
        print("找到的电话号码为:" + contact.phone_number)



    #os.system('cls')






if __name__ == '__main__':
    import openpyxl

    wb = openpyxl.Workbook()
    ws = wb.active
    def test1():
        print("Is 1")

        ws.append(["公司", "电话"])
        success_file = 0
        false_file = 0
        for root, folders, files in os.walk("./ycx合同/"):
            for file in files:
                print(os.path.join(root, file))
                chazhao(os.path.join(root, file), "1")

        wb.save("电话0430.xlsx")
        print("运行结束")

    def test2():
        contact_file = chazhao("./debug_pdf/CgAA42cPXeWANvSsACHyCGniI0M933.pdf","2")


    keyboard.add_hotkey('1', test1)
    keyboard.add_hotkey('2', test2)
    keyboard.wait()



    #



    #         file_path = root + file
    #         print(file_path+"---------------------------------------------------------------------")
    #         myhetong = hetong(file_path)
    #
    #         myhetong.get_text()
    #         try:
    #             myhetong.find_phone(myhetong.texts)
    #             print("执行成功")
    #             success_file +=1
    #         except:
    #             false_file +=1
    #             print(file_path + "运行失败，已扔到debug文件夹")
    #             shutil.copy(file_path, "./debug_pdf/")
    # print(success_file)
    # print(false_file)