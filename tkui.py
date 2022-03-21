import tkinter as tk
from tkinter import DISABLED, HORIZONTAL, VERTICAL, ttk
import copy
from tkinter.scrolledtext import ScrolledText


from database import DataBase
from globalvar import *


class TkUI:

    def __init__(self, db:DataBase=None):
        #  内部变量赋值
        self.m_db = db      # 数据库

        self.all_tag_list = ['123', "1234"]
        self.all_puber_list = ['abc', "abcd"]
        self.paper_list = []

        self.root = tk.Tk()     # 主窗口
        self.menu = tk.Menu(self.root)  # 菜单栏

        # 设置root的分割 允许填充
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.info_frame = tk.Frame(self.root)   # 底端显示信息的框
        self.info_frame.grid(row=1, column=0, sticky=tk.NSEW)
        self.body_frame = tk.Frame(self.root, bg='blue')   # 主体frame
        self.body_frame.grid(row=0, column=0, sticky=tk.NSEW)

        # 设置body_frame的分割 允许show_frame填充
        self.body_frame.grid_rowconfigure(0, weight=1)
        self.body_frame.grid_columnconfigure(1, weight=1)
        self.search_frame = tk.Frame(self.body_frame, )   # 搜索frame
        self.search_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.show_frame = tk.Frame(self.body_frame, bg = 'red')     # 显示frame
        self.show_frame.grid(row=0, column=1, sticky=tk.NSEW)


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
        self.search_frame.grid_columnconfigure(1, weight=1)
        # 按发表年份搜索
        self.pubyear_frame = tk.Frame(self.search_frame)
        self.pubyear_frame.grid(row=1, column=0, sticky='we')
        tk.Label(self.pubyear_frame,text="发表时间").pack(side='left')
        tk.Label(self.pubyear_frame,text="从：").pack(side='left')
        self.pubyear_begin_entry = tk.Entry(self.pubyear_frame, width=5)
        self.pubyear_begin_entry.pack(side='left')
        tk.Label(self.pubyear_frame,text="到：").pack(side='left')
        self.pubyear_end_entry = tk.Entry(self.pubyear_frame, width=5)
        self.pubyear_end_entry.pack(side='left')

        # 按照标签搜索
        self.tag_frame = tk.Frame(self.search_frame)
        self.tag_frame.grid(row=2, column=0, sticky='we')
        tk.Label(self.tag_frame, text="包含标签").grid(row=0, column=0, columnspan=2)
        tk.Button(self.tag_frame, text="+", command=self.search_add_tag).grid(row=1,column=0)
        tk.Button(self.tag_frame, text='-', command=self.search_remove_tag).grid(row=1, column=1)
        # 标签输入
        self.search_tag_input_list = []
        self.search_tag_input_list.append( ttk.Combobox(self.tag_frame, values=self.all_tag_list) )
        self.search_tag_input_list[0].grid(row=0, column=2)

        # 按照期刊搜索
        self.puber_frame = tk.Frame(self.search_frame)
        self.puber_frame.grid(row=3, column=0, sticky='we')
        tk.Label(self.puber_frame, text="含出版商").grid(row=0, column=0, columnspan=2)
        tk.Button(self.puber_frame, text="+", command=self.search_add_puber).grid(row=1,column=0)
        tk.Button(self.puber_frame, text='-', command=self.search_remove_puber).grid(row=1, column=1)
        # 期刊输入
        self.search_puber_input_list = []
        self.search_puber_input_list.append( ttk.Combobox(self.puber_frame, values=self.all_puber_list) )
        self.search_puber_input_list[0].grid(row=0, column=2)

        # 按关键词搜索
        self.keyword_frame = tk.Frame(self.search_frame)
        self.keyword_frame.grid(row=4,column=0, sticky='we')
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
        tk.Button(self.search_frame, text="筛选", width=20, height=4, command=DISABLED).grid(row=5, column=0, sticky='we')


        # 显示主体
        self.show_frame.config(bd='1p')
        self.show_frame.grid_rowconfigure(0, weight=1)
        self.show_frame.grid_columnconfigure(0, weight=1)
        # 显示表
        self.show_table = ttk.Treeview(self.show_frame, columns=DataBase.SIMPLE_FIELD_LIST, selectmode='extended', show='headings')
        for item in DataBase.SIMPLE_FIELD_LIST:
            self.show_table.column(item,anchor='w', stretch=0)
            self.show_table.heading(item,text=item)
        self.paper_list = search(self)
        i = 0
        for item in self.paper_list:
            val = []
            for tem in DataBase.SIMPLE_FIELD_LIST:
                val.append(item.get(tem))
            self.show_table.insert('', i, values=val, iid=str(item.get("No")) )
        self.show_table.bind("<Double-1>", lambda event:open_edit_ui(event, self, self.show_table.selection()[0]))
        self.show_table.grid(row=0, column=0, sticky='eswn')
        # 垂直滚动条
        self.show_table_ybar = ttk.Scrollbar(self.show_frame, orient=VERTICAL,command=self.show_table.yview)
        self.show_table.configure(yscrollcommand=self.show_table_ybar.set)
        self.show_table_ybar.grid(row=0, column=1, sticky='ns')
        # 水平滚动条
        self.show_table_xbar = ttk.Scrollbar(self.show_frame, orient=HORIZONTAL,command=self.show_table.xview)
        self.show_table.configure(xscrollcommand=self.show_table_xbar.set)
        self.show_table_xbar.grid(row=1, column=0, columnspan=2, sticky='ew')


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

def search(ui:TkUI, info:dict=None):
    # 使用db搜索条目
    if (info == None):
        # 返回全部paper
        return ui.m_db.show_all_paper()

    return None
    

def open_edit_ui(event, ui:TkUI, paper_no:str):

    # 函数定义：
    def begin_edit_paper():
        edit_button.config(state='disable')
        save_button.config(state='normal')

        read_or_not_text.config(state='normal', bg='#e8f0fe')
        publication_year_text.config(state='normal', bg='#e8f0fe')
        publisher_text.config(state='normal', bg='#e8f0fe')
        author_text.config(state='normal', bg='#e8f0fe')
        paper_name_text.config(state='normal', bg='#e8f0fe')
        tags_text.config(state='normal', bg='#e8f0fe')
        notes_text.config(state='normal', bg='#e8f0fe')
        url_text.config(state='normal', bg='#e8f0fe')
        path_text.config(state='normal', bg='#e8f0fe')
        last_read_date_text.config(state='normal', bg='#e8f0fe')
        for i in range(10):
            q_text_list[i].config(state='normal', bg='#e8f0fe')

    def edit_paper():
        edit_button.config(state='normal', bg='#e8f0fe')
        save_button.config(state='disable', bg='#ffffff')

        read_or_not_text.config(state='disable', bg='#ffffff')
        publication_year_text.config(state='disable', bg='#ffffff')
        publisher_text.config(state='disable', bg='#ffffff')
        author_text.config(state='disable', bg='#ffffff')
        paper_name_text.config(state='disable', bg='#ffffff')
        tags_text.config(state='disable', bg='#ffffff')
        notes_text.config(state='disable', bg='#ffffff')
        url_text.config(state='disable', bg='#ffffff')
        path_text.config(state='disable', bg='#ffffff')
        last_read_date_text.config(state='disable', bg='#ffffff')
        for i in range(10):
            q_text_list[i].config(state='disable', bg='#ffffff')

        paper_dict['ReadOrNot'] = int(read_or_not_text.get(1.0,'end'))
        paper_dict['PublicationYear'] = publication_year_text.get(1.0,'end')
        paper_dict['Publisher'] = publisher_text.get(1.0,'end')
        paper_dict['Author'] = author_text.get(1.0,'end')
        paper_dict['PaperName'] = paper_name_text.get(1.0,'end')
        paper_dict['Tags'] = tags_text.get(1.0,'end')
        paper_dict['Notes'] = notes_text.get(1.0,'end')
        paper_dict['Url'] = url_text.get(1.0,'end')
        paper_dict['Path'] = path_text.get(1.0,'end')
        for i in range(10):
            paper_dict['Q'+str(i)] = q_text_list[i].get(1.0,'end')
        
        i = 0
        for item in ui.paper_list:
            val = []
            for tem in DataBase.SIMPLE_FIELD_LIST:
                val.append(item.get(tem))
            ui.show_table.item(str(item.get("No")), values=val )
        print(paper_dict)

        ui.m_db.modi_paper(paper_dict)

        print(ui.m_db.show_all_paper())



    # 正式开始
    paper_dict = {}
    for item in ui.paper_list:
        if (str(item.get("No"))==paper_no):
            # paper_dict = copy.deepcopy(item)
            paper_dict = item
            break

    edit_root = tk.Toplevel(ui.root)
    edit_root.geometry('770x800')
    edit_root.resizable(False, True)
    edit_root.title("Paper: "+str(paper_dict.get("PaperName")))
    edit_root.protocol("WM_DELETE_WINDOW",edit_root.destroy)

    edit_root.grid_rowconfigure(1, weight=1)
    edit_root.grid_columnconfigure(0, weight=1)
    button_frame = tk.Frame(edit_root) # 按钮区
    button_frame.grid(row=0, column=0, columnspan=2 ,sticky='new')

    # 修改区
    edit_canvas = tk.Canvas(edit_root,bg='yellow')
    edit_canvas.bind('<Configure>', lambda event: edit_canvas.config(scrollregion=edit_canvas.bbox('all')))
    edit_canvas.grid(row=1, column=0, sticky='ewns')
    # 修改区主体
    edit_frame = tk.Frame(edit_canvas) 
    edit_canvas.create_window((0,0), window=edit_frame, anchor='n')
    # 修改区滚动条
    ybar = ttk.Scrollbar(edit_root,orient=VERTICAL,command=edit_canvas.yview)
    ybar.configure(command=edit_canvas.yview)
    edit_canvas.configure(yscrollcommand=ybar.set)
    ybar.grid(row=1, column = 1, sticky='ns')

    # 在按钮区添加按钮
    edit_button = tk.Button(button_frame)
    edit_button.config(text='edit', command=begin_edit_paper, state='normal')
    edit_button.grid(row=0, column=0)
    save_button = tk.Button(button_frame)
    save_button.config(text='save', command=edit_paper, state = 'disable')
    save_button.grid(row=0, column=1)

    # 在修改区添加
    # No 序号
    no_label = tk.Label(edit_frame, text="Paper Local No: "+paper_no)
    no_label.grid(row=0,column=0)
    # ReadOrNot 标识
    read_or_not_label = tk.Label(edit_frame, text="阅读标记：")
    read_or_not_label.grid(row=1,column=0)
    read_or_not_text = tk.Text(edit_frame, height=1)
    read_or_not_text.insert('end',str(paper_dict.get("ReadOrNot")))
    read_or_not_text.config(state='disable', bg='#ffffff')
    read_or_not_text.grid(row=2,column=0)
    # PublicationYear
    publication_year_label = tk.Label(edit_frame, text="发表年份：")
    publication_year_label.grid(row=3,column=0)
    publication_year_text = tk.Text(edit_frame, height=1)
    publication_year_text.insert('end',str(paper_dict.get("PublicationYear")))
    publication_year_text.config(state='disable', bg='#ffffff')
    publication_year_text.grid(row=4,column=0)
    # Publisher
    publisher_label = tk.Label(edit_frame, text="出版商：")
    publisher_label.grid(row=5,column=0)
    publisher_text = tk.Text(edit_frame, height=1)
    publisher_text.insert('end',str(paper_dict.get("Publisher")))
    publisher_text.config(state='disable', bg='#ffffff')
    publisher_text.grid(row=6,column=0)
    # Author
    author_label = tk.Label(edit_frame, text="作者：")
    author_label.grid(row=7,column=0)
    author_text = tk.Text(edit_frame, height=1)
    author_text.insert('end',str(paper_dict.get("Author")))
    author_text.config( state='disable', bg='#ffffff')
    author_text.grid(row=8,column=0)
    # PaperName
    paper_name_label = tk.Label(edit_frame, text="论文名：")
    paper_name_label.grid(row=9,column=0)
    paper_name_text = tk.Text(edit_frame, height=3)
    paper_name_text.insert('end',str(paper_dict.get("PaperName")))
    paper_name_text.config( state='disable', bg='#ffffff')
    paper_name_text.grid(row=10,column=0)
    # Tages
    tags_label = tk.Label(edit_frame, text="标签：")
    tags_label.grid(row=11,column=0)
    tags_text = tk.Text(edit_frame, height=1)
    tags_text.insert('end',str(paper_dict.get("Tags")))
    tags_text.config(state='disable', bg='#ffffff')
    tags_text.grid(row=12,column=0)
    # Notes
    notes_label = tk.Label(edit_frame, text="备注：")
    notes_label.grid(row=13,column=0)
    notes_text = tk.Text(edit_frame, height=1)
    notes_text.insert('end',str(paper_dict.get("Notes")))
    notes_text.config(state='disable', bg='#ffffff')
    notes_text.grid(row=14,column=0)
    # Url
    url_label = tk.Label(edit_frame, text="网页链接：")
    url_label.grid(row=15,column=0)
    url_text = tk.Text(edit_frame, height=1)
    url_text.insert('end',str(paper_dict.get("Url")))
    url_text.config(state='disable', bg='#ffffff')
    url_text.grid(row=16,column=0)
    # Path
    path_label = tk.Label(edit_frame, text="本地目录：")
    path_label.grid(row=17,column=0)
    path_text = tk.Text(edit_frame, height=1)
    path_text.insert('end',str(paper_dict.get("Path")))
    path_text.config(state='disable', bg='#ffffff')
    path_text.grid(row=18,column=0)
    # LastReadDate
    last_read_date_label = tk.Label(edit_frame, text="上次阅读的时间：")
    last_read_date_label.grid(row=19,column=0)
    last_read_date_text = tk.Text(edit_frame, height=1)
    last_read_date_text.insert('end',str(paper_dict.get("LastReadDate")))
    last_read_date_text.config(state='disable', bg='#ffffff')
    last_read_date_text.grid(row=20,column=0)

    # 10Q
    q_label_list = []
    q_text_list = []
    for i in range(10):
        q_label_list.append(tk.Label(edit_frame, text='Q'+str(i)))
        q_label_list[-1].grid(row=21+2*i, column=0)
        q_text_list.append(ScrolledText(edit_frame, height=10))
        q_text_list[-1].insert('end',str(paper_dict.get("Q"+str(i))))
        q_text_list[-1].configure(state='disable', bg='#ffffff')
        q_text_list[-1].grid(row=21+2*i+1, column=0)
    

    edit_root.mainloop()

    
    


