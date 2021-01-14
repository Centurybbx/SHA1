import tkinter as tk
from tkinter.filedialog import *
from SHA1.my_sha1 import sha1
import tkinter.messagebox
import tkinter.font as tkFont
import os
from typing import *


def open_files():
    files = askopenfiles('rb')
    return files


def open_folders():
    folders = askdirectory()
    return folders


def get_digit_message(files, message):
    info = []
    for file in files:
        info.append(file.name + '的哈希摘要为: ' + sha1(file) + '\n')
    message.set(''.join(info))


def select_before_file():
    return askopenfile('rb')


def select_after_file():
    return askopenfile('rb')


def verify(file1, file2, name_list):
    f1_digest = sha1(file1)
    f2_digest = sha1(file2)
    result = True if f1_digest == f2_digest else False
    if name_list[0] != name_list[-1]:
        tk.messagebox.showwarning("警告", "请比较相同的文件!")
    elif result and name_list[0] == name_list[-1]:
        tk.messagebox.showinfo("正确", "信息一致!")
    else:
        tk.messagebox.showerror("错误", "信息不一致,可能遭到了篡改!")
    return result


def on_verify_click():
    fileName_list = []
    with select_after_file() as f:
        file1_content = f.read()
        fileName_list.append(f.name)

    with select_after_file() as f:
        file2_content = f.read()
        fileName_list.append(f.name)

    verify(file1=file1_content, file2=file2_content, name_list=fileName_list)


class Sha1GUI(object):
    def __init__(self, title: str):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry('1200x600')
        ft = tkFont.Font(family='微软雅黑', size=12, weight=tkFont.BOLD)
        btn_ft = tkFont.Font(family='微软雅黑', size=10, weight=tkFont.BOLD)
        content = tk.StringVar()
        content.set('请选择你需要获得摘要的文件!')
        self.frm_side = tk.Frame(master=self.window, width=100)
        self.frm_header = tk.Frame(master=self.window, height=100)
        self.frm_content = tk.Frame(master=self.window, bg='white')

        self.btn_openFiles = tk.Button(master=self.frm_side, text='打开文件', width=10, font=btn_ft,
                                       command=lambda: get_digit_message(files=open_files(), message=content))
        self.btn_verifyFile = tk.Button(master=self.frm_side, text='验证文件', width=10, font=btn_ft,
                                        command=on_verify_click)
        self.btn_openDir = tk.Button(master=self.frm_side, text='打开文件夹', width=10, font=btn_ft,
                                     command=lambda: self.show_content(message=content))
        self.btn_verifyFiles = tk.Button(master=self.frm_side, text='验证文件夹下\n文件完整性', width=10, font=btn_ft,
                                         command=self.monitor_integrity)
        self.btn_intro = tk.Button(master=self.frm_side, text='使用说明', width=10, font=btn_ft,
                                   command=self.show_intro)

        self.lbl_header = tk.Label(master=self.frm_header, text='基于SHA1的文件完整性校验工具',
                                   font=tkFont.Font(family='微软雅黑', size=20, weight=tkFont.BOLD))
        self.lbl_content = tk.Label(master=self.frm_content, textvariable=content, height=35, width=100,
                                    font=ft, bg='white')

    def setup_gui(self):
        self.frm_side.pack(fill=tk.Y, side=tk.LEFT)
        self.frm_header.pack(fill=tk.X)
        self.frm_content.pack(fill=tk.BOTH, expand='yes')

        self.btn_openFiles.pack(padx=5, pady=20)
        self.btn_verifyFile.pack(padx=5, pady=20)
        self.btn_openDir.pack(padx=5, pady=20)
        self.btn_verifyFiles.pack(padx=5, pady=20)
        self.btn_intro.pack(padx=5, pady=20)

        self.lbl_header.pack()

        self.lbl_content.pack(pady=30)

        self.window.mainloop()

    @staticmethod
    def open_specDir_files():
        dir_path = open_folders() + '/'
        files = os.listdir(dir_path)
        file_dict = {}
        for file in files:
            # 对不选择文件进行防错处理
            if file.find('.') != -1 and dir_path != '/':
                with open(dir_path + file, mode='rb') as f:
                    file_dict[f.name] = sha1(f)
        return file_dict

    def show_content(self, message):
        file_dict = self.open_specDir_files()
        content = []
        for file_name in file_dict:
            content.append(file_name + "的哈希摘要值为: " + file_dict[file_name] + '\n')
        message.set(''.join(content))

    def monitor_integrity(self):
        before_dict = self.open_specDir_files()
        after_dict = self.open_specDir_files()
        if before_dict == after_dict:
            tk.messagebox.showinfo("正确", "信息一致!")
        else:
            tk.messagebox.showerror("错误", "信息完整性遭到了破坏!")

    @staticmethod
    def show_intro():
        intro = "使用说明：\n1.打开文件：打开单个/多个文件, 得到所选择文件的摘要值显示在屏幕上\n2.验证文件：分别打开两个文件" \
                "对其进行完整性校验\n3.打开文件夹：打开指定文件夹, 计算文件夹下所有文件的摘要值显示在屏幕上\n" \
                "4.验证文件夹下文件完整性：监控文件夹下所有文件的完整性"
        tk.messagebox.showinfo("使用说明", intro)


if __name__ == '__main__':
    gui = Sha1GUI('SHA1-Cipher')
    gui.setup_gui()
