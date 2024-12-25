from tkinter import *
from views import ChangeFrame, DeleteFrame, InsertFrame, SearchFrame, HelpFrame
import mysql_student
import keyboard


# 主页面的实现
class MianPage:
    def __init__(self, master):
        self.root = master
        self.root.title('学生信息管理系统')
        self.root.geometry('570x290')
        self.create_page()

    # 创建页面，通过menu组件创建菜单
    def create_page(self):
        self.insert_frame = InsertFrame(self.root)
        self.search_frame = SearchFrame(self.root)
        self.delete_frame = DeleteFrame(self.root)
        self.change_frame = ChangeFrame(self.root)
        self.help_frame = HelpFrame(self.root)

        menubar = Menu(self.root, tearoff=False)

        # 对于菜单按钮的一个实现
        # 第一个大按钮录入
        menubar.add_command(label=' 录 入 ', command=self.show_insert)

        # 第二部分查询按钮，实现最复杂的一部分
        submenu_search = Menu(menubar)
        # 实现降序， 快捷键为ctrl + j
        submenu_search.add_command(label = '降   序', command=self.show_search_sort_down,accelerator="Ctrl + J")
        # 分割降序和其他部分，降序是是否选，下面的是多选一，默认为选择学号
        submenu_search.add_separator()
        submenu_search.add_command(label='学   号',  command=self.show_search_id,  accelerator="Ctrl + D")
        submenu_search.add_command(label='总   分', command=self.show_search_total, accelerator="Ctrl + T")
        submenu_search.add_command(label='数   学', command=self.show_search_math,accelerator="Ctrl + M")
        submenu_search.add_command(label='英   语', command=self.show_search_english, accelerator="Ctrl + E")
        submenu_search.add_command(label='计算机', command=self.show_search_computer, accelerator="Ctrl + S")

        # 实现快捷键
        keyboard.add_hotkey('ctrl+j', self.show_search_sort_down)    # 降序快捷键ctrl+j
        keyboard.add_hotkey('ctrl+d', self.show_search_id)           # 学号快捷键ctrl+d
        keyboard.add_hotkey('ctrl+t', self.show_search_total)        # 总分快捷键ctrl+t
        keyboard.add_hotkey('ctrl+m', self.show_search_math)         # 数学快捷键ctrl+m
        keyboard.add_hotkey('ctrl+e', self.show_search_english)      # 英语快捷键ctrl+e
        keyboard.add_hotkey('ctrl+s', self.show_search_computer)     # 计算机快捷键ctrl+s

        #实现剩下的主菜单栏
        menubar.add_cascade(label=' 查 询 ', menu = submenu_search)
        menubar.add_command(label=' 删 除 ', command=self.show_delete)
        menubar.add_command(label=' 修 改 ', command=self.show_change)
        menubar.add_command(label=' 帮 助 ', command=self.show_help)
        self.root.config(menu = menubar)

        def xShowMenu(event):
            menubar.post(event.x_root, event.y_root)  # #将菜单条绑定上事件，坐标为x和y的root位置

        self.root.bind("<Button-3>", xShowMenu)   # #设定鼠标右键触发事件，调用xShowMenu方法

        self.show_insert()


    # 升或降序排列的值由mysql.student.sort_student 的值来决定，每点击一次就异或上一改变其值
    def show_search_sort_down(self):
        mysql_student.sort_student ^= 1
        self.show_search()

    # 下面都是剩下几种排序的实现
    def show_search_id(self):
        mysql_student.sort_data = 0
        self.show_search()
    def show_search_total(self):
        mysql_student.sort_data = 1
        self.show_search()
    def show_search_math(self):
        mysql_student.sort_data = 2
        self.show_search()
    def show_search_english(self):
        mysql_student.sort_data = 3
        self.show_search()
    def show_search_computer(self):
        mysql_student.sort_data = 4
        self.show_search()

    # 创建某一个页面需要把前面页面留下的东西给pack_forget()来清空一下，然后在实现功能
    def show_insert(self):
        self.insert_frame.pack()
        self.search_frame.pack_forget()
        self.delete_frame.pack_forget()
        self.change_frame.pack_forget()
        self.help_frame.pack_forget()

    def show_search(self):
        self.insert_frame.pack_forget()
        self.delete_frame.pack_forget()
        self.change_frame.pack_forget()
        self.help_frame.pack_forget()
        self.search_frame.pack()
        self.search_frame.show_search_data()

    def show_delete(self):
        self.delete_frame.pack()
        self.insert_frame.pack_forget()
        self.search_frame.pack_forget()
        self.change_frame.pack_forget()
        self.help_frame.pack_forget()

    def show_change(self):
        self.change_frame.pack()
        self.insert_frame.pack_forget()
        self.search_frame.pack_forget()
        self.delete_frame.pack_forget()
        self.help_frame.pack_forget()
    def show_help(self):
        self.change_frame.pack_forget()
        self.insert_frame.pack_forget()
        self.search_frame.pack_forget()
        self.delete_frame.pack_forget()
        self.help_frame.pack()

