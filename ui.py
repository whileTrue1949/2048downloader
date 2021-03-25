import tkinter
from tkinter import ttk
from tkinter import messagebox, filedialog
import spider
import config
import os

logintype_lgt_map = {
    '用户名': 0,
    'UID': 1,
    'Email': 2
}

question_num_map = {
    '无安全问题': 0,
    '我爸爸的出生地': 1,
    '我妈妈的出生地': 2,
    '我的小学校名': 3,
    '我的中学校名': 4,
    '我最喜欢的运动': 5,
    '我最喜欢的歌曲': 6,
    '我最喜欢的电影': 7,
    '我最喜欢的颜色': 8,
    '自定义问题': -1
}


class loginUI():

    def __init__(self):
        self.tk_login = tkinter.Tk()
        self.combobox_username = ttk.Combobox(self.tk_login, state="readonly", width=7, font=('', 20),
                                              values=[s for s in logintype_lgt_map.keys()])
        self.entry_username = ttk.Entry(self.tk_login, font=('', 20), width=10)
        self.label_passwd = ttk.Label(self.tk_login, font=('', 20), text="密码: ")
        self.label_question = ttk.Label(self.tk_login, font=('', 20), text="安全问题: ")
        self.combobox_question = ttk.Combobox(self.tk_login, state="readonly", font=('', 14), width=12,
                                              values=[s for s in question_num_map.keys()])
        self.entry_customquest = ttk.Entry(self.tk_login, font=('', 20), width=10)
        self.label_answer = ttk.Label(self.tk_login, font=('', 20), text="您的答案: ")
        self.entry_answer = ttk.Entry(self.tk_login, font=('', 20), width=10)
        self.button_login = ttk.Button(self.tk_login, text="登陆", command=self.login)
        self.entry_passwd = ttk.Entry(self.tk_login, width=10, font=('', 20), show="*")
        self.combobox_question.bind('<<ComboboxSelected>>', self.combobox_question_selected)
        self.show()

    def show(self):
        self.tk_login.title("2048账号登陆")
        width = 320
        height = 260
        self.tk_login.geometry("%dx%d+%d+%d" % (width, height,
                                                (self.tk_login.winfo_screenwidth() - width) / 2,
                                                (self.tk_login.winfo_screenheight() - height) / 2))
        self.combobox_username.current(0)
        self.combobox_username.place(x=20, y=10)
        self.entry_username.place(x=150, y=10)
        self.label_passwd.place(x=20, y=50)
        self.entry_passwd.place(x=150, y=50)
        self.label_question.place(x=20, y=90)
        self.combobox_question.current(0)
        self.combobox_question.place(x=150, y=90)
        self.label_answer.place(x=20, y=160)
        self.entry_answer.place(x=150, y=160)
        self.button_login.place(x=120, y=210)
        self.tk_login.mainloop()

    def login(self):
        lgt = self.combobox_username.get()
        username = self.entry_username.get()
        passwd = self.entry_passwd.get()
        question = self.combobox_question.get()
        customquest = self.entry_customquest.get()
        answer = self.entry_answer.get()
        res = spider.sp.login(username, passwd, question_num_map.get(question), answer,
                              logintype_lgt_map.get(lgt), customquest)
        messagebox.showinfo("提示: ", res)
        if res == "您已经顺利登录":
            self.tk_login.destroy()
            mainUI()

    def combobox_question_selected(self, *args):
        if self.combobox_question.get() == '自定义问题':
            self.entry_customquest.place(x=150, y=120)
        else:
            self.entry_customquest.delete(0, len(self.entry_customquest.get()))
            self.entry_customquest.place_forget()


str_fid_list = {
    '最新合集': 3,
    '亞洲無碼': 4,
    '日本騎兵': 5,
    '歐美新片': 13,
    '國內原創': 15,
    '中字原創': 16,
    '動漫原創': 17,
    '三級寫真': 18,
    '轉帖交流區': 19
}


class mainUI():

    def __init__(self):
        self.tk_main = tkinter.Tk()
        self.combobox_fid = ttk.Combobox(self.tk_main, state="readonly", font=('', 14), width=12,
                                         values=[s for s in str_fid_list.keys()])
        self.label_download_dir = ttk.Label(self.tk_main, font=('', 20), text="保存路径: ")
        self.entry_download_dir = ttk.Entry(self.tk_main, font=('', 20), width=10,
                                            text=os.path.join(os.getcwd(), config.DOWNLOAD_DIR))
        self.button_choose_dir = ttk.Button(self.tk_main, text="选择文件夹", command=self.choose_dir)
        self.button_download = ttk.Button(self.tk_main, text="开始下载", command=self.download)
        self.show()

    def show(self):
        self.tk_main.title("2048附件下载器")
        width = 300
        height = 500
        self.tk_main.geometry("%dx%d+%d+%d" % (width, height,
                                               (self.tk_main.winfo_screenwidth() - width) / 2,
                                               (self.tk_main.winfo_screenheight() - height) / 2))
        self.combobox_fid.current(0)
        self.combobox_fid.place(x=0, y=0)
        self.tk_main.mainloop()

    def choose_dir(self):  # 选择文件
        download_dir = filedialog.askdirectory(title='选择文件')
        # self.entry_download_dir.config('text', download_dir)

    def download(self):
        pass
