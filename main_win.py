# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from eric6.eric6 import mainWindow

from Ui_main_win import Ui_MainWindow
import find

class MainWindow(QMainWindow, Ui_MainWindow,find.hetong):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setAcceptDrops(True)
    # 鼠标进入
    def dragEnterEvent(self, evn):
        # 鼠标放开函数事件
        evn.accept()

    # 鼠标放开
    def dropEvent(self, evn):

        self.file_path = evn.mimeData().text().split("///")[1]
        if "pdf" in self.file_path:
            self.lineEdit_file_path.setText(self.file_path)
            self.textBrowser_log.setText(self.file_path + "已被选择")
        else:
            reply=QMessageBox.warning(self,"文件类型错误","请选择pdf后缀文件",QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
            print(type(reply))

    # 鼠标拖动
    def dragMoveEvent(self, evn):
        #print("3333333333333333333")
        pass
    #选择文件
    def select_file(self):
        """选择文件对话框"""
        # QFileDialog组件定义
        fileDialog = QFileDialog(self)
        # QFileDialog组件设置
        fileDialog.setWindowTitle("标题")             # 设置对话框标题
        fileDialog.setFileMode(QFileDialog.AnyFile)  # 设置能打开文件的格式
        fileDialog.setDirectory(r'D:\01MyCode\01DemoCode\pyqt5_widgets\img')  # 设置默认打开路径
        fileDialog.setNameFilter("Images (*.pdf)")  # 按文件名过滤
        file_path = fileDialog.exec()                # 窗口显示，返回文件路径
        name = fileDialog.selectedFiles()[0]

        if file_path and fileDialog.selectedFiles():
            print("选择文件成功：{}".format(fileDialog.selectedFiles()[0]))
        return name




    

    @pyqtSlot()
    def on_pushButton_filechoose_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.file_path=self.select_file()
        self.lineEdit_file_path.setText(self.file_path)
        self.textBrowser_log.setText(self.file_path+"已被选择")
    
    @pyqtSlot()
    def on_pushButton_Recognize_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        print(self.file_path)
        self.contact=find.hetong(self.file_path)
        if self.file_path =="":
            reply = QMessageBox.warning(self, "文件类型错误", "没有文件", QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.Yes)
        else:
            self.textBrowser_log.append("识别到pdf为{}".format(self.contact.form))
            self.contact.get_text()
            self.textBrowser_log.append(self.contact.texts)

        
    





if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
