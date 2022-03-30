import yaml
import threading
import webbrowser
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from sys import argv as sys_argv
from sys import exit as sys_exit
from PyQt5 import QtCore, QtGui, QtWidgets
from os import path
import re
import html
from urllib import parse
import requests

GOOGLE_TRANSLATE_URL = 'http://translate.google.cn/m?q=%s&tl=%s&sl=%s'

def translate(text, to_language="auto", text_language="auto"):

    text = parse.quote(text)
    url = GOOGLE_TRANSLATE_URL % (text,to_language,text_language)
    response = requests.get(url)
    data = response.text
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    result = re.findall(expr, data)
    if (len(result) == 0):
        return ""
    return html.unescape(result[0])

def translating(ymlKey:int,yml:dict):
    yml[ymlKey] = translate(yml[ymlKey],"zh-TW")
    value = ui.getBarValue()
    ui.setBarValue(value + 100/len(yml))

def selectFile():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    if not file_path.endswith(".yml"):
        messagebox.showinfo("錯誤", "未知的檔案格式")
        selectFile()
    
    return file_path

def openYmlFile():
    file_path = selectFile()

    with open(file_path,"r",encoding="UTF8") as f:
        yml = yaml.safe_load(f.read())

    threads = []

    for i in yml:
        threads.append(threading.Thread(target=translating, args=(i,yml)))
        threads[len(threads)-1].start()

    for i in threads:
        threads[len(threads)-1].join()

    ymlText = yaml.dump(yml,allow_unicode=True)
    
    with open(path.basename(file_path)[:-4]+"(translate).yml","w",encoding="UTF8") as f:
        f.write(ymlText)

class GUI(object):
    def setupUi(self, Form):
        Form.setObjectName("快速Yml翻譯工具")
        Form.setFixedSize(312, 172)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(60, 20, 201, 71))
        font = QtGui.QFont()
        font.setPointSize(23)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 140, 141, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(160, 140, 141, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(40, 110, 251, 21))
        font = QtGui.QFont()
        font.setKerning(True)
        self.progressBar.setFont(font)
        self.progressBar.setStatusTip("")
        self.progressBar.setWhatsThis("")
        self.progressBar.setAccessibleName("")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    
    def setBarValue(self,value):
        self.progressBar.setProperty("value", value)

    def getBarValue(self):
        return self.progressBar.value()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "快速Yml翻譯工具"))
        self.pushButton.setText(_translate("Form", "開啟yml檔案"))
        self.pushButton.clicked.connect(lambda:openYmlFile())
        self.pushButton_2.setText(_translate("Form", "查看Github原始碼"))
        self.pushButton_2.clicked.connect(lambda:webbrowser.open("http://www.baidu.com"))
        self.pushButton_3.setText(_translate("Form", "支持作者Youtube頻道"))
        self.pushButton_3.clicked.connect(lambda:webbrowser.open("https://www.youtube.com/channel/UCoIyvDVUbE-9g6A7AtL7aBQ"))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys_argv)
    Form = QtWidgets.QWidget()
    ui = GUI()
    ui.setupUi(Form)
    Form.show()
    sys_exit(app.exec_())
