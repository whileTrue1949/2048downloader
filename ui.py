import tkinter
from tkinter import ttk
from tkinter import messagebox
import spider


def combobox_username_index(username):
    if username == '用户名: ':
        return 0
    elif username == 'UID: ':
        return 1
    elif username == 'Email: ':
        return 2


def combobox_question_index(question):
    question_num = -1
    if question == '无安全问题':
        question_num = 0
    elif question == '我爸爸的出生地':
        question_num = 1
    elif question == '我妈妈的出生地':
        question_num = 2
    elif question == '我的小学校名':
        question_num = 3
    elif question == '我的中学校名':
        question_num = 4
    elif question == '我最喜欢的运动':
        question_num = 5
    elif question == '我最喜欢的歌曲':
        question_num = 6
    elif question == '我最喜欢的电影':
        question_num = 7
    elif question == '我最喜欢的颜色':
        question_num = 8
    return question_num


class loginUI():

    def __init__(self):
        self.tk_login = tkinter.Tk()
        self.combobox_username = ttk.Combobox(self.tk_login, state="readonly", width=7, font=('', 20),
                                              values=("用户名: ", "UID: ", "Email: "))
        self.entry_username = ttk.Entry(self.tk_login, font=('', 20), width=10)
        self.label_passwd = ttk.Label(self.tk_login, font=('', 20), text="密码: ")
        self.label_question = ttk.Label(self.tk_login, font=('', 20), text="安全问题: ")
        self.combobox_question = ttk.Combobox(self.tk_login, state="readonly", font=('', 14), width=12,
                                              values=("无安全问题", "我爸爸的出生地", "我妈妈的出生地", "我的小学校名",
                                                      "我的中学校名", "我最喜欢的运动", "我最喜欢的歌曲", "我最喜欢的电影",
                                                      "我最喜欢的颜色", "自定义问题"))
        self.entry_customquest = ttk.Entry(self.tk_login, font=('', 20), width=10)
        self.label_answer = ttk.Label(self.tk_login, font=('', 20), text="您的答案: ")
        self.entry_answer = ttk.Entry(self.tk_login, font=('', 20), width=10)
        self.button_login = ttk.Button(self.tk_login, text="登陆", command=self.login)
        self.entry_passwd = ttk.Entry(self.tk_login, width=10, font=('', 20), show="*")
        self.combobox_question.bind('<<ComboboxSelected>>', self.combobox_question_selected)
        self.show()

    def show(self):
        self.tk_login.title("2048附件下载器")
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
        res = spider.sp.login(username, passwd, combobox_question_index(question), answer,
                              combobox_username_index(lgt), customquest)
        messagebox.showinfo("提示: ", res)
        if res == "您已经顺利登录":
            self.tk_login.destroy()

    def combobox_question_selected(self, *args):
        if self.combobox_question.get() == '自定义问题':
            self.entry_customquest.place(x=150, y=120)
        else:
            self.entry_customquest.delete(0, len(self.entry_customquest.get()))
            self.entry_customquest.place_forget()
