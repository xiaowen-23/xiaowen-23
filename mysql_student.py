
from tkinter import *
import pymysql
# 创建连接数据库student的对象conn
conn = pymysql.connect(
    host='localhost',  # 数据库主机名
    port=3306,  # 数据库端口号，默认为3306
    user='root',  # 数据库用户名
    password='2021czp',  # 数据库密码
    autocommit=True  # 设置修改数据无需确认
)
# 获取游标对象
sort_student = int(0)
sort_data = int(0)

cursor = conn.cursor()

# 创建数据库，若有则不创建
cursor.execute("create database if not exists student;")
conn.select_db("student") # 建立与数据库的连接

# 创建学生信息表， 若有则不创建
cursor.execute("CREATE TABLE IF NOT EXISTS students(id int,name varchar(10),kulas varchar(10),math int,english int,computer int,total int, chinese int);")


# 创建账号密码表，若有则不创建
cursor.execute("CREATE TABLE IF NOT EXISTS admin_name_pwd(name varchar(10),pwd varchar(10));")


# 判断登录的账号密码是否都正确
def check_login(uname, pwd):
    cursor.execute("select * from admin_name_pwd")
    results = cursor.fetchall()
    # print(results)
    for na, pd in results:
        if na == uname and pd == pwd:
            return True, '登录成功'
    return False, '登录失败,账号或密码错误'

# 添加正确注册的账号以及密码
def add_admin_name_pwd(uname, pwd):
    cursor.execute("insert into admin_name_pwd values('{0}', '{1}');".format(uname, pwd))
add_admin_name_pwd("123", "123")

# 检验注册的账号名称是否已经存在
def check_usname(uname):
    cursor.execute("select count(*) from admin_name_pwd anp where name = '{0}';".format(uname))
    res = cursor.fetchall()
    if res[0][0]:
        return True
    return False


# 获取数据库中学生所有信息，按给定的信息给出
# 通过全局变量sort_data以及sort_student
# sort_student 为0代表升序，为一代表降序
def all():
    if sort_student == 1:
        if sort_data == 0:
            cursor.execute("select * from students order by id;")
        elif sort_data == 1:
            cursor.execute("select * from students order by total;")
        elif sort_data == 2:
            cursor.execute("select * from students order by math;")
        elif sort_data == 3:
            cursor.execute("select * from students order by english;")
        elif sort_data == 4:
            cursor.execute("select * from students order by computer;")
        elif sort_data == 5:
            cursor.execute("select * from students order by chinese;")
    else:
        if sort_data == 0:
            cursor.execute("select * from students order by id desc;")
        elif sort_data == 1:
            cursor.execute("select * from students order by total desc;")
        elif sort_data == 2:
            cursor.execute("select * from students order by math desc;")
        elif sort_data == 3:
            cursor.execute("select * from students order by english desc;")
        elif sort_data == 4:
            cursor.execute("select * from students order by computer desc;")
        elif sort_data == 5:
            cursor.execute("select * from students order by chinese desc;")
    data = cursor.fetchall()
    key = ('id', 'name', 'kulas', 'math', 'english', 'computer', 'total', 'chinese')
    jsonList = []
    # 通过数据得到的数据是元组类型，需要压缩成字典类型便于输出
    for i in data:
        jsonList.append(dict(zip(key, i)))
    return jsonList

# 查询录入的学号是否存在

def check_student_id(id):
    cursor.execute("select count(*) from students where id = '{0}';".format(id))
    res = cursor.fetchall()
    if res[0][0]:
        return False, "该学号已存在请重新输入"
    return True, '录入成功'


# 单独查询某个班级的成绩
def search_kulas(kulas_value):
    cursor.execute("select * from students where kulas = '{0}';".format(kulas_value))
    data = cursor.fetchall()
    key = ('id', 'name', 'kulas', 'math', 'english', 'computer', 'total', 'chinese')
    jsonList = []
    # 通过数据得到的数据是元组类型，需要压缩成字典类型便于输出
    for i in data:
        jsonList.append(dict(zip(key, i)))
    return jsonList
# 插入一条学生信息
def insert(stu):
    cursor.execute("insert into students values('{0}', '{1}', '{2}','{3}', '{4}', '{5}', '{6}', '{7}');".
                   format(stu[0], stu[1], stu[2], stu[3], stu[4], stu[5], stu[6], stu[7]))

# 通过id来删除学生信息
def delete_id(user_id):
    cursor.execute("select count(*) from students where id = '{0}';".format(user_id))
    res = cursor.fetchall()
    if res[0][0]:
        cursor.execute("delete from students where id = '{0}';".format(user_id))
        return True, '删除成功'
    else: return False, '学号为' + str(user_id) + '的学生不存在'

# 通过名字来删除学生信息
def delete_name(user_name):
    cursor.execute("select count(*) from students where name = '{0}';".format(user_name))
    res = cursor.fetchall()
    # print(res)
    if res[0][0]:
        cursor.execute("delete from students where name = '{0}';".format(user_name))
        return True, '删除成功'
    else: return False, '姓名为' + str(user_name) + '的学生不存在'


# 通过id来查询学生的信息
def search_id(user_id):
    cursor.execute("select count(*) from students where id = '{0}';".format(user_id))
    res = cursor.fetchall()
    if res[0][0]:
        cursor.execute("select * from students where id = '{0}';".format(user_id))
        stu = cursor.fetchall()
        return True, stu
    else:
        return False, '学号为' + str(user_id) + '的学生不存在'

# 通过学生姓名来查询剩余的信息
def search_name(user_name):
    cursor.execute("select count(*) from students where name = '{0}';".format(user_name))
    res = cursor.fetchall()
    if res[0][0]:
        cursor.execute("select * from students where name = '{0}';".format(user_name))
        stu = cursor.fetchall()
        return True, stu
    else:
        return False, '名字为' + str(user_name) + '的学生不存在'

# 下面内容是初始化数据库，不过需要手动解开注释
tuple = (
         (20, '王伟', '软件开发4班', 75, 62, 80, 302, 85),
         (19, '李娜', '软件开发4班', 63, 90, 55, 286, 78),
         (18, '张杰', '软件开发4班', 82, 79, 91, 344, 92),
         (17, '赵丽', '软件开发4班', 74, 96, 71, 328, 87),
         (16, '刘翔', '软件开发4班', 85, 70, 88, 332, 89),
         (15, '周华', '软件开发4班', 70, 55, 85, 282, 72),
         (14, '陈刚', '软件开发4班', 81, 82, 60, 311, 88),
         (13, '吴静', '软件开发4班', 72, 76, 84, 312, 80),
         (12, '孙强', '软件开发4班', 77, 49, 91, 291, 74),
         (11, '李佳', '物联网3班', 86, 69, 90, 326, 81),
         (10, '王东', '物联网2班', 83, 78, 86, 331, 84),
         (9, '陈华', '大数据1班', 90, 85, 66, 341, 100),
         (8, '杨洋', '软件土木3班', 88, 72, 93, 253, 80),
         (7, '赵磊', '计算机1班', 67, 74, 82, 223, 68),
         (6, '邓丽', '金融2班', 80, 91, 65, 236, 85),
         (5, '黄明', '大数据3班', 78, 81, 75, 234, 86),
         (4, '钱玉', '软件会计2班', 82, 84, 47, 213, 80),
         (3, '张慧', '软件土木5班', 63, 70, 80, 213, 75),
         (2, '陈宇', '计算机5班', 83, 66, 74, 223, 80),
         (1, '刘洋', '软件开发4班', 62, 88, 68, 218, 82))


for stu in tuple:
    if check_student_id(stu[0])[0] == True:
        insert(stu)

# 加入初始账号，若有则不加入
if check_usname("root") == False:
    add_admin_name_pwd('root', 'root')
