import tkinter as tk
from tkinter.filedialog import *
from SHA1.my_sha1 import sha1
import tkinter.messagebox
import tkinter.font as tkFont
from typing import *


def select_files():
    """
    选择多个文件
    :return: 列表形式读取的IO对象
    """
    files = askopenfiles('rb')
    return files


def get_digit_message(files, message):
    info = []
    for file in files:
        info.append(file.name + '的哈希摘要为: ' + sha1(file) + '\n')
    message.set(''.join(info))


def select_before_file():
    return askopenfile('rb')


def select_after_file():
    return askopenfile('rb')


def verify(file1, file2):
    f1_digest = sha1(file1)
    f2_digest = sha1(file2)
    result = True if f1_digest == f2_digest else False
    if result:
        tk.messagebox.showinfo("正确", "信息一致!")
    else:
        tk.messagebox.showerror("错误", "信息不一致,可能遭到了篡改!")
    return result


def on_verify_click():
    with select_after_file() as f:
        file1_content = f.read()

    with select_after_file() as f:
        file2_content = f.read()

    verify(file1=file1_content,
           file2=file2_content)


class Sha1GUI(object):
    def __init__(self, title: str):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry('1200x600')

    def setup_gui(self):
        frm_side = tk.Frame(master=self.window, width=100)
        frm_side.pack(fill=tk.Y, side=tk.LEFT)
        content = tk.StringVar()
        content.set('请选择你需要获得摘要的文件!')
        ft = tkFont.Font(family='微软雅黑', size=12, weight=tkFont.BOLD)

        btn_openFiles = tk.Button(master=frm_side, text='打开文件',
                                  command=lambda: get_digit_message(files=select_files(), message=content))
        btn_openFiles.pack(padx=5, pady=100)
        btn_verifyFile = tk.Button(master=frm_side, text='验证文件', command=on_verify_click)
        btn_verifyFile.pack(padx=5, pady=100)

        frm_header = tk.Frame(master=self.window, height=100)
        frm_header.pack(fill=tk.X)
        lbl_header = tk.Label(master=frm_header, text='基于SHA1的文件完整性校验软件',
                              font=tkFont.Font(family='微软雅黑', size=20, weight=tkFont.BOLD))
        lbl_header.pack()

        frm_content = tk.Frame(master=self.window, bg='white')
        frm_content.pack(fill=tk.BOTH, expand='yes')
        lbl_content = tk.Label(master=frm_content, textvariable=content, height=35, width=100,
                               font=ft, bg='white')
        lbl_content.pack(pady=30)
        self.window.mainloop()


if __name__ == '__main__':
    gui = Sha1GUI('SHA1-Cipher')
    gui.setup_gui()
