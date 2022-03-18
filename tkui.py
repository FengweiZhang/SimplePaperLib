import tkinter as tk
from tkinter import ttk

from database import DataBase
from globalvar import *


class TkUI:

    def __init__(self, db:DataBase=None):
        #  内部变量赋值
        self.m_db = db      # 数据库

        self.all_tag_list = ['123', "1234"]
        self.all_puber_list = ['abc', "abcd"]


        self.root = tk.Tk()     # 主窗口
        self.menu = tk.Menu(self.root)  # 菜单栏

        self.info_frame = tk.Frame(self.root)   # 底端显示信息的框
        self.info_frame.pack(side='bottom', fill='x')
        self.body_frame = tk.Frame(self.root, bg='blue')   # 主体frame
        self.body_frame.pack(side="top", fill='both', expand=True)

        self.search_frame = tk.Frame(self.body_frame)   # 搜索frame
        self.search_frame.pack(side='left', fill='y')
        self.show_frame = tk.Frame(self.body_frame)     # 显示frame
        self.show_frame.pack(side='right', fill='y')


        # 窗口基本设置
        self.root.geometry("1500x800+100+100")
        self.root.title("Simple Paper Lib")
        self.root.protocol("WM_DELETE_WINDOW",self.root.quit)

        # 设置菜单栏
        self.menu.add_command(label="Add", command=tk.DISABLED)
        self.menu.add_command(label="Setting", command=tk.DISABLED)
        self.menu.add_command(label="Exit", command=tk.DISABLED)
        # 放置菜单栏
        self.root.config(menu=self.menu)

        # 底端信息框
        self.info_frame.config(bg="#ffffdd", bd='1p')
        self.info_var = tk.StringVar()
        self.info_var.set("Info: No Info!")
        self.info = tk.Label(self.info_frame, bg='#ffffdd', textvariable=self.info_var)
        self.info.pack(side='left')

        
        # 搜索栏
        self.search_frame.config(bg='#1e1e1e', bd='1p')
        tk.Canvas(self.search_frame, width=300, height=5).grid(row=0,column=0)

        # 按发表年份搜索
        self.pubyear_frame = tk.Frame(self.search_frame)
        self.pubyear_frame.grid(row=1, column=0)
        tk.Label(self.pubyear_frame,text="发表时间").pack(side='left')
        tk.Label(self.pubyear_frame,text="从：").pack(side='left')
        self.pubyear_begin_entry = tk.Entry(self.pubyear_frame, width=5)
        self.pubyear_begin_entry.pack(side='left')
        tk.Label(self.pubyear_frame,text="到：").pack(side='left')
        self.pubyear_end_entry = tk.Entry(self.pubyear_frame, width=5)
        self.pubyear_end_entry.pack(side='left')

        # 按照标签搜索
        self.tag_frame = tk.Frame(self.search_frame)
        self.tag_frame.grid(row=2, column=0)
        tk.Label(self.tag_frame, text="包含标签").grid(row=0, column=0, columnspan=2)
        tk.Button(self.tag_frame, text="+", command=self.search_add_tag).grid(row=1,column=0)
        tk.Button(self.tag_frame, text='-', command=self.search_remove_tag).grid(row=1, column=1)
        # 标签输入
        self.search_tag_input_list = []
        self.search_tag_input_list.append( ttk.Combobox(self.tag_frame, values=self.all_tag_list) )
        self.search_tag_input_list[0].grid(row=0, column=2)

        # 按照期刊搜索
        self.puber_frame = tk.Frame(self.search_frame)
        self.puber_frame.grid(row=3, column=0)
        tk.Label(self.puber_frame, text="含出版商").grid(row=0, column=0, columnspan=2)
        tk.Button(self.puber_frame, text="+", command=self.search_add_puber).grid(row=1,column=0)
        tk.Button(self.puber_frame, text='-', command=self.search_remove_puber).grid(row=1, column=1)
        # 期刊输入
        self.search_puber_input_list = []
        self.search_puber_input_list.append( ttk.Combobox(self.puber_frame, values=self.all_puber_list) )
        self.search_puber_input_list[0].grid(row=0, column=2)

        # 按关键词搜索
        self.keyword_frame = tk.Frame(self.search_frame)
        self.keyword_frame.grid(row=4,column=0)
        tk.Label(self.keyword_frame, text='含关键词').grid(row=0, column=0)
        # 搜索模式
        self.search_papername_flag = tk.IntVar()    # 标记从论文标题中搜索
        self.search_notes_flag = tk.IntVar()        # 标记从备注中搜索
        tk.Checkbutton(self.keyword_frame, text='标题',variable=self.search_papername_flag, onvalue=1, offvalue=0).grid(row=1, column=0)
        tk.Checkbutton(self.keyword_frame, text='备注',variable=self.search_notes_flag, onvalue=1, offvalue=0).grid(row=2, column=0)
        # 搜索内容
        self.search_keyword_input_entry = tk.Entry(self.keyword_frame)
        self.search_keyword_input_entry.grid(row=0, column=1)

        # 搜索按钮
        tk.Button(self.search_frame, text="筛选", width=20, height=4).grid(row=5, column=0)









        # 主循环
        self.root.mainloop()

        return None


    def search_add_tag(self):
        # 在搜索面板添加tag搜索条件输入框
        self.search_tag_input_list.append(ttk.Combobox(self.tag_frame, values=self.all_tag_list))
        self.search_tag_input_list[-1].grid(row=len(self.search_tag_input_list)-1, column=2)

        return None

    def search_remove_tag(self):
        # 在搜索面板去除tag搜索条件输入框
        if(len(self.search_tag_input_list) <= 0):
            return None
        else:
            self.search_tag_input_list[-1].grid_forget()
            self.search_tag_input_list.pop()
        
        return None

    def search_add_puber(self):
        # 在搜索面板添加puber搜索条件输入框
        self.search_puber_input_list.append(ttk.Combobox(self.puber_frame, values=self.all_puber_list))
        self.search_puber_input_list[-1].grid(row=len(self.search_puber_input_list)-1, column=2)

        return None

    def search_remove_puber(self):
        # 在搜索面板去除tag搜索条件输入框
        if(len(self.search_puber_input_list) <= 0):
            return None
        else:
            self.search_puber_input_list[-1].grid_forget()
            self.search_puber_input_list.pop()
        
        return None

a = TkUI()

