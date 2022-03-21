import sqlite3
import os
import copy

from globalvar import *


def dict_factory(cursor, row):
    # 将元组类型转换为字典类型

    d = {}  
    for idx, col in enumerate(cursor.description):  
        d[col[0]] = row[idx]  
    return d  


class DataBase:

    FIELD_LIST = ["No",   "ReadOrNot",   "PublicationYear",  "Publisher",  
        "Author",   'PaperName',      "Tags",      "Notes",
        "Url",            "Path",               'LastReadDate',
        "Q0",     "Q1",     "Q2",     "Q3",     "Q4",
        "Q5",     "Q6",     "Q7",     "Q8",     "Q9"  
        ]
    
    SIMPLE_FIELD_LIST = ["ReadOrNot",   "PublicationYear", "Publisher",  
        "Author",   'PaperName',      "Tags",
        ]

    def __init__(self):
        # 初始化函数，生成并连接数据库

        # 声明全部变量的名称
        self.m_con = None    # 数据库接口        
        
        rel_path = "database.db"

        # 测试用，每次删库跑路
        try: 
            os.remove(rel_path) 
        except:
            pass

        # 检查数据库文件父目录是否存在
        # if not os.path.isdir(rel_path):
            # os.makedirs(rel_path)

        # 检查数据库文件是否存在
        if os.path.isfile(rel_path):
            self.m_con = sqlite3.connect(rel_path)
        else:
            # 若文件不存在，则初始化数据库
            # 数据库表名为paperlist
            self.m_con = sqlite3.connect(rel_path)
            self.m_con.execute('''create table paperlist(
                No INTEGER PRIMARY KEY AUTOINCREMENT,
                ReadOrNot       INT,
                PublicationYear TEXT,
                Publisher       TEXT,
                Author          TEXT,
                PaperName       TEXT,
                Tags            TEXT,
                Notes           TEXT,
                Url             TEXT,
                Path            TEXT,
                LastReadDate    TEXT,
                Q0              TEXT,
                Q1              TEXT,
                Q2              TEXT,
                Q3              TEXT,
                Q4              TEXT,
                Q5              TEXT,
                Q6              TEXT,
                Q7              TEXT,
                Q8              TEXT,
                Q9              TEXT
                );
                ''')
            self.m_con.commit()

        # 将查询结果返回为字典类型而非元组
        self.m_con.row_factory = dict_factory 

        return None



    def add_paper(self, info:dict):
        # 向数据库中插入paper条目,数据来自字典info{"字段":"值"}
        # No字段自动获取，ReadOrNot默认记为0，
        # 没有的字段默认为空字符串
        
        fields = "ReadOrNot"  # 字段
        values = "0"  # 值

        if not info.get("PaperName"):
            return MY_ERROR_NO_PAPERNAME

        # 依次从info中读取字段
        add_fields = copy.deepcopy(DataBase.FIELD_LIST)
        add_fields.remove("No")
        add_fields.remove("ReadOrNot")
        for item in add_fields:
            if info.get(item):
                fields += "," + item
                values += ",\"" + info.get(item) + "\""
            else:
                fields += "," + item
                values += ",\"\""

        self.m_con.execute(f'''
            insert into paperlist ({fields}) values ({values});     
            ''')
        self.m_con.commit()
        
        return MY_SUCCESS



    def modi_paper(self, info:dict):
        # 修改paper条目，从info中提取信息

        update = ""

        no = info.get("No")
        if not no:
            return MY_ERROR_NO_PAPERNO
        
        modi_fields = copy.deepcopy(DataBase.FIELD_LIST)
        modi_fields.remove("No")
        modi_fields.remove("ReadOrNot")

        # 依次读取待修改的属性
        if info.get("ReadOrNot"):
            update += "ReadOrNot=" + str(info.get("ReadOrNot")) + ","
        for item in modi_fields:
            if info.get(item):
                update += item + "=\"" + info.get(item) + "\","
        # 删除最后多余的 ,
        try:
            if update[-1] == ",":
                update = update[:-1]
        except:
            pass

        self.m_con.execute(f'''
            UPDATE paperlist
            SET {update}
            WHERE No = {no};
        ''')
        self.m_con.commit()

        return MY_SUCCESS



    def find_paper(self, info:dict):
        # 查找函数，按字典info信息查找特定的paper

        ret_list = []

        return ret_list



    def show_all_paper(self):
        # 返回全部内容字典
        ret_list = list(self.m_con.execute('''
            select * from paperlist;
            '''))

        return ret_list


