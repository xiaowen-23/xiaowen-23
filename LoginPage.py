from tkinter import *
from tkinter import messagebox
import mysql_student
from MianPgae import MianPage

class LoginPage:
    def __init__(self, master):
        self.root = master

        # 定义窗口面
        self.root.geometry('300x150')
        self.root.title('登录页')
        # 使用Frame框架定义子组件page
        self.page = Frame(self.root)
        self.page.pack()

        # 通过键盘键入账号，密码的容器l
        self.username = StringVar()
        self.password = StringVar()
        # 账号框
        Label(self.page, text='账号: ').grid(row=1, column=1,pady = 5)
        Entry(self.page, textvariable=self.username).grid(row=1, column=2)
        # 密码框
        Label(self.page, text='密码: ', ).grid(row=2, column=1, pady=18)
        Entry(self.page, show='*', textvariable=self.password).grid(row=2, column=2)
        # 注册登录退出三个选项
        Button(self.page, text='注册', command=self.register).grid(row=3, column=1, pady=4)
        Button(self.page, text='登录', command=self.login).grid(row=3, column=2)
        Button(self.page, text='退出', command=self.page.quit).grid(row=3, column=3)


    # 注册部分调用add_login类来实现注册新账号
    def register(self):
        self.page.destroy()
        add_login(self.root)

    # 点击登录按键后去查找账号密码是否正确，不正确发出警告，正确则进入信息页面
    def login(self):
        uname = self.username.get()
        pwd = self.password.get()
        flag, message = mysql_student.check_login(uname, pwd) # 通过文件mysql_student的函数判断账号密码是否正确
        if flag:
            self.page.pack_forget()
            MianPage(self.root)
        else: messagebox.showwarning(title = '警告', message = message) # 登录失败的警告


# 主要负责注册页面的实现
class add_login:
    def __init__(self, master):

        self.page = master

        self.username = StringVar()             # 账号容器
        self.password = StringVar()             # 密码容器
        self.password_examine = StringVar()     # 二次键入密码容器
        self.password_root = StringVar()        # 管理员密码容器
        # 管理员密码用于查验管理员身份，若一致才能注册账号并登录

        self.page.title('注册账号')
        self.page.geometry('300x250')

        self.root = Frame(self.page)
        self.root.pack()

        Label(self.root, text='账   号: ').grid(row=1, column=1)
        Entry(self.root, textvariable=self.username).grid(row=1, column=2)

        # 密码
        Label(self.root, text='密   码: ').grid(row=2, column=1, pady=18)
        Entry(self.root,  show = '*', textvariable=self.password).grid(row=2, column=2)

        Label(self.root, text='确 认 密 码: ').grid(row=3, column=1)
        Entry(self.root,  show = '*', textvariable=self.password_examine).grid(row=3, column=2)

        Label(self.root, text= '管理员密码: ').grid(row=4, column=1, pady=18)
        Entry(self.root, show='*', textvariable=self.password_root).grid(row=4, column=2)

        Button(self.root, text='返  回', command=self.login_page).grid(row=5, column=1)
        Button(self.root, text='注  册', command=self.examine).grid(row=5, column=2)

    # 用户取消账号注册，选择取消，进入登录界面
    def login_page(self):
        self.root.pack_forget()
        LoginPage(self.page)

    # 英文意思检查，检验，用户检验账号密码是否合规，例如长度，账号是否已经被注册，管理员密码是否正确
    def examine(self):
        self.uname = self.username.get()
        self.pwd = self.password.get()
        self.pwd_exm = self.password_examine.get()
        self.pwd_root = self.password_root.get()
        if len(self.uname) < 5:
            messagebox.showwarning(title='警告', message='账号不符合要求，请输入最少5位字符')
        elif mysql_student.check_usname(self.uname) == True:
            messagebox.showwarning(title='警告', message='账号已存在，请更改你的账号')
        elif len(self.pwd) < 8:
            messagebox.showwarning(title='警告', message='密码不符合要求，请输入最少8位字符')
        elif self.pwd != self.pwd_exm:
            messagebox.showwarning(title='警告', message='两次密码不相同，请重新输入')
        elif self.pwd_root != 'root':
            messagebox.showwarning(title='警告', message='管理员密码错误，无法注册账号')
        else: self.login()

    # 同登录页面的login, 实现账号密码的新添加以及进入主页面，即信息页面
    def login(self):
        mysql_student.add_admin_name_pwd(self.uname, self.pwd)
        self.root.pack_forget()
        MianPage(self.page)

if __name__ == '__main__':
    page = Tk()
    LoginPage(page)
    page.mainloop()
