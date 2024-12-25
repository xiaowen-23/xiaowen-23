from tkinter import *
from tkinter import ttk
import mysql_student
from tkinter import messagebox


# 实现录入页面的类
class InsertFrame(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.id = StringVar()
        self.name = StringVar()
        self.kulas = StringVar()
        self.math = StringVar()
        self.english = StringVar()
        self.computer = StringVar()
        self.chinese = StringVar()

        # 打印录入是否成功信息
        self.status_insert = StringVar()

        self.insert_page()


    # 打印修输入的项目以及输入框
    def insert_page(self):
        Label(self, text='学   号 : ').grid(row=1, column=1, pady=5)
        self.entry_id = Entry(self, textvariable=self.id)
        self.entry_id.grid(row=1, column=2, pady=5)

        Label(self, text = '姓   名 : ').grid(row=2, column = 1, pady=5)
        self.entry_name = Entry(self, textvariable=self.name)
        self.entry_name.grid(row = 2, column = 2, pady = 5)

        Label(self, text='班   级 : ').grid(row=3, column=1, pady=5)
        self.entry_kulas = Entry(self, textvariable=self.kulas)
        self.entry_kulas.grid(row=3, column=2, pady=5)

        Label(self, text='数   学 : ').grid(row=4, column=1, pady=5)
        self.entry_math = Entry(self, textvariable=self.math)
        self.entry_math.grid(row=4, column=2, pady=5)

        Label(self, text='英   语 : ').grid(row=5, column=1, pady=5)
        self.entry_english = Entry(self, textvariable=self.english)
        self.entry_english.grid(row=5, column=2, pady=5)

        Label(self, text='计算机 : ').grid(row=6, column=1, pady=5)
        self.entry_computer = Entry(self, textvariable=self.computer)
        self.entry_computer.grid(row=6, column=2, pady=5)

        Label(self, text='语文 : ').grid(row=7, column=1, pady=5)
        self.entry_chinese = Entry(self, textvariable=self.chinese)
        self.entry_chinese.grid(row=7, column=2, pady=5)

        Button(self, text = '清空', command = self.insert_deleteValue).grid(row=8, column=1, pady=10)
        Button(self, text = '录入', command = self.insert_data).grid(row = 8, column = 3, pady = 10)

        Label(self, textvariable=self.status_insert).grid(row=9, column=2, padx=10)
    # 输出所有学生信息
    def insert_data(self):
        if not self.id.get():
            self.insert_id = int(0)
        else: self.insert_id = int(self.id.get())

        if not self.name.get():
            self.insert_name = 'NULL'
        else: self.insert_name = self.name.get()

        if not self.kulas.get():
            self.insert_kulas = 'NULL'
        else: self.insert_kulas = self.kulas.get()

        if not self.math.get():
            self.insert_math = int(0)
        else: self.insert_math = int(self.math.get())

        if not self.english.get():
            self.insert_english = int(0)
        else: self.insert_english = int(self.english.get())

        if not self.computer.get():
            self.insert_computer = int(0)
        else: self.insert_computer = int(self.computer.get())

        if not self.chinese.get():
            self.insert_chinese = int(0)
        else: self.insert_chinese = int(self.computer.get())


        flag, s = mysql_student.check_student_id(self.insert_id) # 查询id
        self.status_insert.set(s)
        if flag == False: # 若已经存在的情况，不能录入
            return
        self.insert_total = self.insert_math + self.insert_computer + self.insert_english + self.insert_chinese
        stu = (self.insert_id, self.insert_name, self.insert_kulas, self.insert_math,
               self.insert_english, self.insert_computer, self.insert_total, self.insert_chinese)
        mysql_student.insert(stu) # 这一部分为存在并导入信息


    # 删除输入框中的内容
    def insert_deleteValue(self):
        self.entry_id.delete(0, END)
        self.entry_name.delete(0, END)
        self.entry_kulas.delete(0, END)
        self.entry_math.delete(0, END)
        self.entry_english.delete(0, END)
        self.entry_computer.delete(0, END)
        self.entry_chinese.delete(0, END)


# 实现查找功能的类
class SearchFrame(Frame):
    def __init__(self, root):
        super().__init__(root)

        self.table_search_view = Frame()

        self.show_table_search()

    # 实现显示查询页面的整个大框架分布
    def show_table_search(self):
        columns = ("id", "name", "kulas", "math", "english", "computer", "total", "chinese")
        columns_values = ("学号", "姓名", "班级", "数学", "英语", "计算机", "总分", "语文")
        self.tree_view = ttk.Treeview(self, show = 'headings', columns = columns)

        for col in columns:
            self.tree_view.column(col, width = 80, anchor = 'center')

        for col, colvalue in zip(columns, columns_values):
            self.tree_view.heading(col, text = colvalue)

        self.tree_view.pack(fill = BOTH, expand = True)
        self.show_search_data()

        self.kulas_kulas = StringVar()
        Entry(self, textvariable=self.kulas_kulas).pack(side = LEFT)
        Button(self, text='按班查询', command=self.search_kulas).pack(side=LEFT) # , command = self.treeviewClick
        Button(self, text = '删   除', command=self.treeviewClick).pack(side = RIGHT)

        # 下面循环加函数是实现点击标题实现排序
        def treeview_sort_column1(tv, col, reverse):  # Treeview、列名、排列方式
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            l.sort(key=lambda t: int(t[0]), reverse=reverse)  # 排序方式
            for index, (val, k) in enumerate(l):  # 根据排序后索引移动
                tv.move(k, '', index)
            tv.heading(col, command=lambda: treeview_sort_column1(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题
            self.tree_color()  # 启动程序，根据奇偶行设为不同的背景颜色

        def treeview_sort_column2(tv, col, reverse):  # Treeview、列名、排列方式
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            l.sort(reverse=reverse)  # 排序方式
            for index, (val, k) in enumerate(l):  # 根据排序后索引移动
                tv.move(k, '', index)
            tv.heading(col, command=lambda: treeview_sort_column2(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题
            self.tree_color()  # 启动程序，根据奇偶行设为不同的背景颜色

        for i in range(7):  # 给所有标题加（循环上边的“手工”）
            if i >= 1 and i <=2:
                self.tree_view.heading(columns[i], text=columns_values[i], command=lambda _col=columns[i]: treeview_sort_column2(self.tree_view, _col, False))
            else: self.tree_view.heading(columns[i], text = columns_values[i], command=lambda _col = columns[i]: treeview_sort_column1(self.tree_view, _col, False))
        # 定义背景色风格
        self.tree_view.tag_configure('even', background='lightblue')  # even标签设定为浅蓝色背景颜色

    def search_kulas(self):
        for _ in map(self.tree_view.delete, self.tree_view.get_children('')):
            pass
        if not self.kulas_kulas.get():
            self.show_search_data()
            return
        else:
            self.kulas_value = self.kulas_kulas.get()
            students = mysql_student.search_kulas(self.kulas_value)

        index = -1
        for stu in students:
            self.tree_view.insert('', index + 1, values = (
                stu['id'], stu['name'], stu['kulas'], stu['math'],
                stu['english'], stu['computer'], stu['total'],stu["chinese"]
            ))
        self.tree_color()  # 启动程序，根据奇偶行设为不同的背景颜色

    def treeviewClick(self):  # 单击
        for item in self.tree_view.selection():
            item_text = self.tree_view.item(item, "values")
            mysql_student.delete_id(item_text[0])  # 删除所选行的第一列的值
            self.show_search_data()

    # 显示数据库中学生信息表上的信息
    def show_search_data(self):

        for _ in map(self.tree_view.delete, self.tree_view.get_children('')): # 删除原本显示的数据
            pass
        students = mysql_student.all() # 获取数据库中的信息并以字典形式返回
        index = -1
        for stu in students:
            self.tree_view.insert('', index + 1, values=(
                stu['id'], stu['name'], stu['kulas'], stu['math'],
                stu['english'], stu['computer'], stu['total'],stu["chinese"]
            ))
        self.tree_color()  # 启动程序，根据奇偶行设为不同的背景颜色

    def tree_color(self):  # 表格栏隔行显示不同颜色函数
        items = self.tree_view.get_children()  # 得到根目录所有行的iid
        i = 0  # 初值
        for hiid in items:
            if i / 2 != int(i / 2):  # 判断奇偶
                tag1 = ''  # 奇数行
            else:
                tag1 = 'even'  # 偶数行
            self.tree_view.item(hiid, tag=tag1)  # 偶数行设为浅蓝色的tag='even'
            i += 1  # 累加1

# 实现删除页面的类
class DeleteFrame(Frame):
    def __init__(self, root):
        super().__init__(root, width = 570, height = 290)

        self.delete_student = StringVar()
        self.status_student = StringVar()

        Label(self, text='请输入需要删除学生的').place(x = 40, y = 60)
        Label(self, text='姓名或者学号').place(x=64, y=80)
        Entry(self, textvariable=self.delete_student).place(x = 30, y = 100)
        Button(self, text='按学号查询', command=self.id_delete).place(x = 30, y = 130)
        Button(self, text='按姓名查询', command=self.name_delete).place(x=110, y=130)
        Label(self, textvariable=self.status_student).place(x = 45, y = 160)

        self.id = StringVar()
        self.name = StringVar()
        self.kulas = StringVar()
        self.math = StringVar()
        self.english = StringVar()
        self.computer = StringVar()
        self.chinese = StringVar()

        Label(self, text = '学   号 :').place(x=300, y=20)
        Label(self, textvariable=self.id).place(x=360, y=20)
        Label(self, text='姓   名 :').place(x=300, y=50)
        Label(self, text = '姓   名 :', textvariable=self.name).place(x=360, y=50)
        Label(self, text='班   级 :').place(x=300, y=80)
        Label(self, text = '班   级 :', textvariable=self.kulas).place(x=360, y=80)
        Label(self, text='数   学 :').place(x=300, y=110)
        Label(self, textvariable=self.math).place(x=360, y=110)
        Label(self, text='英   语 :').place(x=300, y=140)
        Label(self, textvariable=self.english).place(x=360, y=140)
        Label(self, text='计算机 :').place(x=300, y=170)
        Label(self, textvariable=self.computer).place(x=360, y=170)

        Label(self, text='语文 :').place(x=300, y=190)
        Label(self, textvariable=self.chinese).place(x=360, y=190)

        self.status_delete = StringVar()
        Button(self, text='删    除', command=self.delete_stu).place(x=340, y=230)
        Label(self, textvariable=self.status_delete).place(x=300, y=230)

    # 通过学号来删除对应学生的信息
    def id_delete(self):
        if self.delete_student.get():
            self.search_user_id = self.delete_student.get()
            flag, stu = mysql_student.search_id(self.search_user_id)
            if flag:
                self.id.set(stu[0][0]),self.name.set(stu[0][1])
                self.kulas.set(stu[0][2]),self.math.set(stu[0][3])
                self.english.set(stu[0][4]),self.computer.set(stu[0][5])
                self.chinese.set(stu[0][7])
                self.status_student.set('数据查询成功')
            else:
                self.status_student.set(stu)
        else:
            self.status_student.set('请输入需要查询的信息')
    def name_delete(self):
        if self.delete_student.get():
            self.search_user_name = self.delete_student.get()
            flag, stu = mysql_student.search_name(self.search_user_name)
            if flag:
                self.id.set(stu[0][0])
                self.name.set(stu[0][1])
                self.kulas.set(stu[0][2])
                self.math.set(stu[0][3])
                self.english.set(stu[0][4])
                self.computer.set(stu[0][5])
                self.chinese.set(stu[0][7])
                self.status_student.set('数据查询成功')
            else:
                self.status_student.set(stu)
        else:
            self.status_student.set('请输入需要查询的信息')

    def delete_stu(self):
        flag, str = mysql_student.delete_id(self.id.get())
        if not self.id.get():
            str = '需要删除信息不能NULL'
        self.status_delete.set(str)


# 实现修改页面的类
class ChangeFrame(Frame):
    def __init__(self, root):
        super().__init__(root, width = 570, height = 290)
        # Label(self, text = '修改页面').pack()
        # 查询的修改信息，以及查询、修改成功的提示
        self.change_student = StringVar()
        self.status_student = StringVar()
        self.status_name = StringVar()


        # 存储学生信息已经更改的变量
        self.id = StringVar()
        self.name = StringVar()
        self.kulas = StringVar()
        self.math = StringVar()
        self.english = StringVar()
        self.computer = StringVar()
        self.chinese = StringVar()

        # 用于存储修改之前的信息
        self.id_change_before = StringVar()
        self.name_change_before = StringVar()
        self.kulas_change_before = StringVar()
        self.math_change_before = StringVar()
        self.english_change_before = StringVar()
        self.computer_change_before = StringVar()
        self.chinese_change_before = StringVar()

        self.insert_page()



    # 打印修输入的项目以及输入框
    def insert_page(self):

        Label(self, text='请输入需要查询学生的').place(x=40, y=60)
        Label(self, text='姓名或者学号').place(x=64, y=80)
        Entry(self, textvariable=self.change_student).place(x=30, y=100)
        Button(self, text='按学号查询', command=self.id_change).place(x=30, y=130)
        Button(self, text='按姓名查询', command=self.name_change).place(x=110, y=130)
        Label(self, textvariable=self.status_student).place(x=45, y=160)

        Label(self, text='学   号 : ').place(x=240, y=20)
        Label(self, textvariable=self.id_change_before).place(x=320, y=20)
        self.entry_id = Entry(self, textvariable=self.id)
        self.entry_id.place(x=380, y=20)

        Label(self, text='姓   名 : ').place(x=240, y=50)
        Label(self, textvariable=self.name_change_before).place(x=315, y=50)
        self.entry_name = Entry(self, textvariable=self.name)
        self.entry_name.place(x=380, y=50)

        Label(self, text='班   级 : ').place(x=240, y=80)
        Label(self, textvariable=self.kulas_change_before).place(x=300, y=80)
        self.entry_kulas = Entry(self, textvariable=self.kulas)
        self.entry_kulas.place(x=380, y=80)

        Label(self, text='数   学 : ').place(x=240, y=110)
        Label(self, textvariable=self.math_change_before).place(x=318, y=110)
        self.entry_math = Entry(self, textvariable=self.math)
        self.entry_math.place(x=380, y=110)

        Label(self, text='英   语 : ').place(x=240, y=140)
        Label(self, textvariable=self.english_change_before).place(x=318, y=140)
        self.entry_english = Entry(self, textvariable=self.english)
        self.entry_english.place(x=380, y=140)

        Label(self, text='计算机 : ').place(x=240, y=170)
        Label(self, textvariable=self.computer_change_before).place(x=318, y=170)
        self.entry_computer = Entry(self, textvariable=self.computer)
        self.entry_computer.place(x=380, y=170)


        Label(self, text='语文 : ').place(x=240, y=190)
        Label(self, textvariable=self.chinese_change_before).place(x=318, y=190)
        self.entry_chinese = Entry(self, textvariable=self.chinese)
        self.entry_chinese.place(x=380, y=190)


        Button(self, text='修    改', command = self.create_user).place(x=320, y=240)

        Label(self, textvariable=self.status_name).place(x=305, y=240)

    # 通过学号或者姓名来查询学生信息，优先通过学号，若未输入学号，则通过姓名来查询
    def id_change(self):
        if self.change_student.get():
            self.search_user_id = self.change_student.get()
            flag, stu = mysql_student.search_id(self.search_user_id)
            if flag:
                self.change_Information(stu)
                self.status_student.set('数据查询成功')
            else:
                self.status_student.set(stu)
        else:
            self.status_student.set('请输入需要查询的信息')

    def name_change(self):
        if self.change_student.get():
            self.search_user_name = self.change_student.get()
            flag, stu = mysql_student.search_name(self.search_user_name)
            if flag:
                self.change_Information(stu)
                self.status_student.set('数据查询成功')
            else:
                self.status_student.set(stu)
        else:
            self.status_student.set('请输入需要查询的信息')
    def change_Information(self, stu):
        self.id.set(stu[0][0])
        self.name.set(stu[0][1])
        self.kulas.set(stu[0][2])
        self.math.set(stu[0][3])
        self.english.set(stu[0][4])
        self.computer.set(stu[0][5])
        self.chinese.set(stu[0][7])
        self.id_change_before.set(stu[0][0])
        self.name_change_before.set(stu[0][1])
        self.kulas_change_before.set(stu[0][2])
        self.math_change_before.set(stu[0][3])
        self.english_change_before.set(stu[0][4])
        self.computer_change_before.set(stu[0][5])
        self.chinese_change_before.set(stu[0][7])
    # 通过获取输入框的信息来修改数据库中学生的信息
    def create_user(self):
        if not self.id.get():
            self.insert_id = int(0)
            self.status_name.set('请输入修改的学号')
            return
        else:
            self.insert_id = int(self.id.get())

        if not self.name.get():
            self.insert_name = 'NULL'
        else:
            self.insert_name = self.name.get()

        if not self.kulas.get():
            self.insert_kulas = 'NULL'
        else:
            self.insert_kulas = self.kulas.get()

        if not self.math.get():
            self.insert_math = int(0)
        else:
            self.insert_math = int(self.math.get())

        if not self.english.get():
            self.insert_english = int(0)
        else:
            self.insert_english = int(self.english.get())

        if not self.computer.get():
            self.insert_computer = int(0)
        else:
            self.insert_computer = int(self.computer.get())

        if not self.chinese.get():
            self.insert_chinese = int(0)
        else:
            self.insert_chinese = int(self.chinese.get())
        mysql_student.delete_id(self.id_change_before.get())
        self.insert_total = self.insert_math + self.insert_computer + self.insert_english + self.insert_chinese
        stu = (self.insert_id, self.insert_name, self.insert_kulas, self.insert_math,
               self.insert_english, self.insert_computer, self.insert_total, self.insert_chinese)
        mysql_student.insert(stu)

        self.status_name.set('数据修改成功')

# 实现帮助页面的类，主要打印一些程序运行的帮助以及规则
class HelpFrame(Frame):
    def __init__(self, root):
        super().__init__(root)

        Label(self, text = '关于录入界面').pack()
        Label(self, text = '可以录入所有信息为空的信息，但不建议，且学号具有唯一性').pack()
        Label(self, text = ' ').pack()
        Label(self, text = '关于查询界面').pack()
        Label(self, text = '默认为升序排列，可以根据学生的各类信息进行排列，并能通过快捷键以及鼠标右键实现一定的功能').pack()
        Label(self, text = '可以查看班级信息以及可以选择信息进行删除').pack()
        Label(self, text = ' ').pack()
        Label(self, text = '关于删除界面').pack()
        Label(self, text = '可以根据学号或者姓名对学生信息进行删除，学号是唯一的').pack()
        Label(self, text = ' ').pack()
        Label(self, text = '关于修改界面').pack()
        Label(self, text = '可以通过学号或者姓名来查询学学生信息，但查询名字只会出现第一位学生，按下修改键出现提示即成功').pack()